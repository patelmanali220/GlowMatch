"""
Core ML Service Module - Skin Tone Analysis Engine

This module contains the main machine learning logic for:
1. Face detection from images using MediaPipe
2. Skin region extraction using OpenCV and HSV color space
3. Skin tone analysis (depth: Fair/Medium/Dark)
4. Undertone detection (Warm/Cool/Neutral)
5. Personalized color recommendation generation

The algorithm uses HSV (Hue, Saturation, Value) color space analysis
which is more intuitive for skin tone analysis than RGB.

Author: GlowMatch Development Team
Version: 1.0.0
"""

import cv2
import numpy as np
import logging
from typing import Dict, List, Tuple, Any

# Try importing mediapipe solutions
try:
    from mediapipe.python.solutions import face_detection
    from mediapipe.framework.formats import landmark_pb2
except ImportError:
    try:
        import mediapipe as mp
        face_detection = mp.solutions.face_detection
    except (ImportError, AttributeError):
        face_detection = None
        
# Configure logging for this module
logger = logging.getLogger(__name__)


class SkinToneAnalyzer:
    """
    Analyzes skin tone from face images and generates personalized color recommendations.
    
    This class handles the complete ML pipeline:
    - Face detection using MediaPipe FaceMesh
    - Skin region extraction from detected faces
    - Color analysis in HSV color space
    - Classification of skin depth and undertone
    - Generation of personalized color palettes
    
    The classification uses rule-based algorithms optimized for accuracy:
    - Depth is determined by brightness (Value in HSV)
    - Undertone is determined by hue distribution
    
    Color recommendations are based on color theory and makeup industry standards.
    """
    
    # ==================== HSV Color Space Ranges ====================
    # These ranges define what we consider "skin-like" colors
    # OpenCV uses H: 0-180, S: 0-255, V: 0-255 (not 0-360, 0-100, 0-100)
    
    SKIN_HSV_MIN = np.array([0, 5, 25])      # Lower bound (Hue, Saturation, Value)
    SKIN_HSV_MAX = np.array([50, 65, 95])    # Upper bound
    
    # ==================== Undertone Hue Ranges ====================
    # Hue ranges in degrees (0-360), converted to OpenCV scale (0-180)
    
    WARM_HUE_RANGE = (0, 35)       # Red-Yellow spectrum (warm tones)
    NEUTRAL_HUE_RANGE = (35, 60)   # Yellow-Green spectrum (balanced)
    COOL_HUE_RANGE = (340, 360)    # Purple-Red spectrum (cool tones)
    
    def __init__(self):
        """
        Initialize the SkinToneAnalyzer with pre-trained models.
        
        Sets up:
        - MediaPipe Face Detection model for face detection
        - Color palettes for 6 skin tone combinations (3 depths × 3 undertones)
        
        The MediaPipe model is loaded from cache on subsequent uses,
        so initialization is fast after the first run.
        """
        logger.info("Initializing SkinToneAnalyzer...")
        
        # Initialize MediaPipe Face Detection
        # model_selection: 0 = short-range (0-2m), 1 = full-range (0-5m)
        # We use model_selection=1 for robustness
        if face_detection is None:
            logger.warning("MediaPipe not available, using fallback face detection")
            self.face_detector = None
        else:
            try:
                self.face_detector = face_detection.FaceDetection(
                    model_selection=1,
                    min_detection_confidence=0.5  # 50% confidence threshold
                )
                logger.info("MediaPipe Face Detector loaded successfully")
            except Exception as e:
                logger.error(f"Failed to initialize MediaPipe: {e}")
                self.face_detector = None
        
        # Initialize color recommendation palettes
        self._initialize_color_palettes()
        logger.info("Color palettes initialized")
    
    def _initialize_color_palettes(self) -> None:
        """
        Initialize predefined color palettes for all 6 skin tone combinations.
        
        Creates a dictionary with palettes for:
        - 3 Depths: Fair (light), Medium (mid), Dark (deep)
        - 3 Undertones: Warm (golden), Cool (pink), Neutral (balanced)
        - Total combinations: 3 × 3 = 6 palettes
        
        Each palette includes:
        - Clothing colors (hex codes)
        - Makeup recommendations (foundation, lipstick, eyeshadow)
        - Jewelry recommendations (metals and stones)
        
        Format: {
            (depth, undertone): {
                'clothing': [hex colors],
                'makeup': {
                    'foundation': [hex colors],
                    'lipstick': [hex colors],
                    'eyeshadow': [hex colors]
                },
                'jewelry': {
                    'metals': [hex colors],
                    'stones': [hex colors]
                }
            }
        }
        """
        self.palettes = {
            # ========== FAIR SKIN (Light) ==========
            
            # Fair + Warm: Golden undertones look best
            ('Fair', 'Warm'): {
                'clothing': ['#FFB347', '#FF8C00', '#CD853F', '#DEB887', '#F4A460', '#DAA520'],
                'makeup': {
                    'foundation': ['#F5DEB3', '#FFE4B5', '#FFDAB9'],
                    'lipstick': ['#FF6347', '#FF7F50', '#E75480'],
                    'eyeshadow': ['#FFD700', '#FFA500', '#FF8C00']
                },
                'jewelry': {
                    'metals': ['#FFD700', '#B76E79'],  # Gold, Rose Gold
                    'stones': ['#FF8C00', '#DAA520']   # Amber, Topaz
                }
            },
            
            # Fair + Cool: Silver and cool tones look best
            ('Fair', 'Cool'): {
                'clothing': ['#4B0082', '#00CED1', '#E0FFFF', '#B0E0E6', '#ADD8E6', '#87CEEB'],
                'makeup': {
                    'foundation': ['#E8E8E8', '#F5F5DC', '#FFFAFA'],
                    'lipstick': ['#FF1493', '#FF69B4', '#8B0000'],
                    'eyeshadow': ['#4B0082', '#8A2BE2', '#00CED1']
                },
                'jewelry': {
                    'metals': ['#C0C0C0', '#E8E8E8'],  # Silver, Platinum
                    'stones': ['#00CED1', '#FF69B4']   # Turquoise, Pink
                }
            },
            
            # Fair + Neutral: Both warm and cool colors work
            ('Fair', 'Neutral'): {
                'clothing': ['#DC143C', '#FF0000', '#FFFFFF', '#000000', '#808080', '#A9A9A9'],
                'makeup': {
                    'foundation': ['#F5DEB3', '#FAEBD7', '#F0F8FF'],
                    'lipstick': ['#DC143C', '#C71585', '#FF6347'],
                    'eyeshadow': ['#8B008B', '#FF0000', '#006666']
                },
                'jewelry': {
                    'metals': ['#FFD700', '#C0C0C0'],  # Gold, Silver - both work
                    'stones': ['#FF0000', '#006666']   # Ruby, Emerald
                }
            },
            
            # ========== MEDIUM SKIN (Mid-tone) ==========
            
            # Medium + Warm: Warm, earthy tones
            ('Medium', 'Warm'): {
                'clothing': ['#8B4513', '#D2691E', '#CD853F', '#FF8C00', '#FFB347', '#DAA520'],
                'makeup': {
                    'foundation': ['#C9A877', '#D4A574', '#DEB887'],
                    'lipstick': ['#E75480', '#FF6347', '#FF8C00'],
                    'eyeshadow': ['#8B4513', '#CD853F', '#FFD700']
                },
                'jewelry': {
                    'metals': ['#FFD700', '#B76E79'],  # Gold, Rose Gold
                    'stones': ['#8B4513', '#FFD700']   # Bronze, Gold
                }
            },
            
            # Medium + Cool: Cool, jewel tones
            ('Medium', 'Cool'): {
                'clothing': ['#4B0082', '#008080', '#20B2AA', '#3CB371', '#66CDAA', '#00FA9A'],
                'makeup': {
                    'foundation': ['#C9A877', '#BC8F8F', '#A0826D'],
                    'lipstick': ['#8B008B', '#FF1493', '#00CED1'],
                    'eyeshadow': ['#483D8B', '#4169E1', '#00CED1']
                },
                'jewelry': {
                    'metals': ['#C0C0C0', '#E8E8E8'],  # Silver, Platinum
                    'stones': ['#00CED1', '#50C878']   # Turquoise, Emerald
                }
            },
            
            # Medium + Neutral: Versatile, works with both warm and cool
            ('Medium', 'Neutral'): {
                'clothing': ['#50C878', '#DC143C', '#FF4500', '#228B22', '#FFD700', '#FF6347'],
                'makeup': {
                    'foundation': ['#C9A877', '#D4A574', '#BC8F8F'],
                    'lipstick': ['#DC143C', '#FF4500', '#C71585'],
                    'eyeshadow': ['#50C878', '#FFD700', '#FF4500']
                },
                'jewelry': {
                    'metals': ['#FFD700', '#B76E79'],  # Gold, Rose Gold - both versatile
                    'stones': ['#50C878', '#FF4500']   # Emerald, Orange
                }
            },
            
            # ========== DARK SKIN (Deep) ==========
            
            # Dark + Warm: Vibrant warm colors pop
            ('Dark', 'Warm'): {
                'clothing': ['#FFD700', '#FFA500', '#FF8C00', '#FF6347', '#DC143C', '#8B4513'],
                'makeup': {
                    'foundation': ['#8B4513', '#A0522D', '#8B6914'],
                    'lipstick': ['#FF4500', '#FF6347', '#DC143C'],
                    'eyeshadow': ['#FFD700', '#FFA500', '#FF8C00']
                },
                'jewelry': {
                    'metals': ['#FFD700', '#B76E79'],  # Gold, Rose Gold
                    'stones': ['#FFD700', '#FF4500']   # Gold, Deep Orange
                }
            },
            
            # Dark + Cool: Cool, bright colors stand out
            ('Dark', 'Cool'): {
                'clothing': ['#00CED1', '#87CEEB', '#00FA9A', '#20B2AA', '#FF1493', '#FF69B4'],
                'makeup': {
                    'foundation': ['#3D3D3D', '#545454', '#696969'],
                    'lipstick': ['#FF1493', '#FF69B4', '#00CED1'],
                    'eyeshadow': ['#00CED1', '#87CEEB', '#FF1493']
                },
                'jewelry': {
                    'metals': ['#C0C0C0', '#E8E8E8'],  # Silver, Platinum
                    'stones': ['#00CED1', '#FF1493']   # Turquoise, Hot Pink
                }
            },
            
            # Dark + Neutral: Both warm and cool colors work beautifully
            ('Dark', 'Neutral'): {
                'clothing': ['#50C878', '#FFD700', '#FF4500', '#00CED1', '#FF1493', '#DC143C'],
                'makeup': {
                    'foundation': ['#704214', '#8B6914', '#A0522D'],
                    'lipstick': ['#FF4500', '#DC143C', '#FF1493'],
                    'eyeshadow': ['#50C878', '#FFD700', '#FF4500']
                },
                'jewelry': {
                    'metals': ['#FFD700', '#C0C0C0'],  # Gold and Silver both work
                    'stones': ['#50C878', '#FFD700']   # Emerald, Gold
                }
            }
        }
    
    def analyze_skin_tone(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Complete skin tone analysis pipeline.
        
        This is the main method that orchestrates the entire analysis process:
        1. Face detection - find face in image
        2. Skin extraction - isolate skin pixels
        3. Color analysis - analyze HSV values
        4. Classification - determine depth and undertone
        5. Recommendation - generate color palette
        
        Args:
            image (np.ndarray): Input image as numpy array (RGB format)
                               Shape: (height, width, 3)
                               Values: 0-255 for each channel
        
        Returns:
            dict: Comprehensive analysis result with:
            {
                "skin_analysis": {
                    "depth": str (Fair|Medium|Dark),
                    "undertone": str (Warm|Cool|Neutral),
                    "confidence": float (0-1)
                },
                "recommendations": {
                    "clothing": {color palette},
                    "makeup": {makeup shades},
                    "jewelry": {jewelry colors}
                },
                "analysis_details": {
                    technical metrics from analysis
                }
            }
            
            Or error response:
            {
                "status": "error",
                "message": str (error description)
            }
        
        Process Flow:
            Input Image (RGB)
                ↓
            Convert to BGR for OpenCV
                ↓
            Face Detection (MediaPipe)
                ↓
            Skin Region Extraction (HSV mask)
                ↓
            Convert to HSV
                ↓
            Extract Color Values
                ↓
            Classify Depth (brightness)
                ↓
            Classify Undertone (hue)
                ↓
            Calculate Confidence
                ↓
            Generate Recommendations
                ↓
            Format Response
        """
        try:
            logger.info("Starting skin tone analysis...")
            
            # Convert RGB to BGR for OpenCV processing
            # OpenCV uses BGR format, PIL/numpy typically use RGB
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            logger.info(f"Image size: {image_bgr.shape}")
            
            # Step 1: Detect face in image
            faces = self._detect_faces(image_bgr)
            if not faces:
                logger.warning("No face detected in image")
                return self._error_response("No face detected in image")
            
            logger.info(f"Found {len(faces)} face(s)")
            
            # Use the first detected face
            face_box = faces[0]
            logger.info(f"Face box: x={face_box['x']}, y={face_box['y']}, "
                       f"width={face_box['width']}, height={face_box['height']}")
            
            # Step 2: Extract skin region from face
            skin_mask, skin_region = self._extract_skin_region(image_bgr, face_box)
            if skin_mask is None or cv2.countNonZero(skin_mask) < 100:
                logger.warning("Could not extract sufficient skin region")
                return self._error_response("Could not extract sufficient skin region")
            
            logger.info(f"Extracted skin region with {cv2.countNonZero(skin_mask)} pixels")
            
            # Step 3: Convert to HSV color space
            # HSV is better for skin tone analysis than RGB
            image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
            
            # Step 4: Extract color values from skin pixels
            # skin_mask is binary (0 or 255), we use it to select only skin pixels
            skin_pixels = image_hsv[skin_mask == 255]
            
            # Extract H, S, V channels
            hue_values = skin_pixels[:, 0]        # Hue channel
            saturation_values = skin_pixels[:, 1] # Saturation channel
            value_values = skin_pixels[:, 2]      # Value (brightness) channel
            
            logger.info(f"Analyzing {len(hue_values)} skin pixels")
            logger.info(f"Hue range: {hue_values.min()}-{hue_values.max()}")
            logger.info(f"Value range: {value_values.min()}-{value_values.max()}")
            
            # Step 5: Classify skin depth based on brightness
            depth = self._classify_depth(value_values)
            logger.info(f"Skin depth: {depth}")
            
            # Step 6: Classify undertone based on hue
            undertone, undertone_hue = self._classify_undertone(hue_values)
            logger.info(f"Skin undertone: {undertone} (hue: {undertone_hue}°)")
            
            # Step 7: Calculate confidence score
            confidence = self._calculate_confidence(value_values, hue_values)
            logger.info(f"Confidence: {confidence:.2f}")
            
            # Step 8: Generate recommendations
            recommendations = self._generate_recommendations(depth, undertone)
            
            # Step 9: Prepare comprehensive response
            response = {
                "skin_analysis": {
                    "depth": depth,
                    "undertone": undertone,
                    "confidence": round(confidence, 2)
                },
                "recommendations": recommendations,
                "analysis_details": {
                    "hue": round(float(np.mean(hue_values)), 1),
                    "saturation": round(float(np.mean(saturation_values)) / 255, 2),
                    "brightness": round(float(np.mean(value_values)) / 255, 2),
                    "skin_pixels_detected": int(cv2.countNonZero(skin_mask)),
                    "undertone_hue": round(undertone_hue, 1)
                }
            }
            
            logger.info("Analysis completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error in analyze_skin_tone: {str(e)}", exc_info=True)
            return self._error_response(f"Analysis failed: {str(e)}")
    
    def _detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces in image using MediaPipe FaceMesh.
        
        Args:
            image (np.ndarray): Input image in BGR format
        
        Returns:
            List[Dict]: List of detected faces with bounding boxes
                       Each dict contains: x, y, width, height, confidence
        """
        try:
            if self.face_detector is None:
                logger.warning("Face detector not available, using Haar Cascade fallback")
                return self._detect_faces_cascade(image)
            
            # MediaPipe requires RGB format, so convert BGR to RGB
            results = self.face_detector.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            faces = []
            
            if results.detections:
                h, w, _ = image.shape
                
                for detection in results.detections:
                    # Extract bounding box in relative coordinates
                    bbox = detection.location_data.relative_bounding_box
                    
                    # Convert relative coordinates to absolute pixel coordinates
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    width = int(bbox.width * w)
                    height = int(bbox.height * h)
                    confidence = detection.score[0]
                    
                    faces.append({
                        'x': max(0, x),
                        'y': max(0, y),
                        'width': width,
                        'height': height,
                        'confidence': confidence
                    })
            
            return faces
        
        except Exception as e:
            logger.error(f"Face detection error: {str(e)}, using cascade fallback")
            return self._detect_faces_cascade(image)
    
    def _detect_faces_cascade(self, image: np.ndarray) -> List[Dict]:
        """
        Fallback face detection using Haar Cascade (no MediaPipe required).
        
        Args:
            image (np.ndarray): Input image in BGR format
        
        Returns:
            List[Dict]: List of detected faces
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            faces_cv = cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
            
            faces = []
            for (x, y, w, h) in faces_cv:
                faces.append({
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'confidence': 0.9
                })
            
            return faces
        except Exception as e:
            logger.error(f"Haar Cascade fallback failed: {str(e)}")
            return []
    
    def _extract_skin_region(self, image: np.ndarray, face_box: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract skin region from detected face.
        
        Process:
        1. Convert BGR to HSV
        2. Apply skin color filter using HSV ranges
        3. Apply morphological operations to clean mask
        4. Restrict to face region with padding
        5. Return binary mask of skin pixels
        
        Args:
            image (np.ndarray): Input image in BGR format
            face_box (Dict): Bounding box of detected face
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: (Skin mask, Skin region image)
                                           Mask is binary (0 or 255)
        """
        try:
            # Convert BGR to HSV for better skin detection
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Create binary mask using HSV ranges
            # This isolates pixels that look like skin
            skin_mask = cv2.inRange(image_hsv, self.SKIN_HSV_MIN, self.SKIN_HSV_MAX)
            logger.info(f"Initial skin pixels: {cv2.countNonZero(skin_mask)}")
            
            # Apply morphological operations to improve mask quality
            # These operations help remove noise and fill small holes
            
            # Kernel for morphological operations (5x5 ellipse)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            
            # Close operation: fills small holes in foreground
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
            
            # Open operation: removes small noise
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
            
            logger.info(f"After morphology: {cv2.countNonZero(skin_mask)} pixels")
            
            # Restrict mask to face region with padding
            h, w = image.shape[:2]
            x, y, fw, fh = face_box['x'], face_box['y'], face_box['width'], face_box['height']
            
            # Add 20% padding to face box to ensure we get all relevant skin
            padding = 0.2
            x = max(0, int(x - fw * padding))
            y = max(0, int(y - fh * padding))
            x2 = min(w, int(x + fw + fw * padding))
            y2 = min(h, int(y + fh + fh * padding))
            
            # Extract region of interest from mask
            face_region = skin_mask[y:y2, x:x2]
            
            # Create full mask with zeros everywhere except face region
            full_mask = np.zeros_like(skin_mask)
            full_mask[y:y2, x:x2] = face_region
            
            return full_mask, image[y:y2, x:x2]
        
        except Exception as e:
            logger.error(f"Skin extraction error: {str(e)}")
            return None, None
    
    def _classify_depth(self, value_values: np.ndarray) -> str:
        """
        Classify skin depth based on brightness value.
        
        The brightness (Value channel in HSV) is the best indicator of skin depth:
        - Fair skin: Bright/light (V > 165)
        - Medium skin: Medium brightness (115 < V ≤ 165)
        - Dark skin: Dark (V ≤ 115)
        
        Args:
            value_values (np.ndarray): V channel values (0-255) of skin pixels
        
        Returns:
            str: Skin depth classification (Fair, Medium, or Dark)
        """
        mean_value = np.mean(value_values)
        
        # Thresholds based on empirical testing with diverse skin tones
        if mean_value > 166:        # 0.65 * 255
            return 'Fair'
        elif mean_value > 115:      # 0.45 * 255
            return 'Medium'
        else:
            return 'Dark'
    
    def _classify_undertone(self, hue_values: np.ndarray) -> Tuple[str, float]:
        """
        Classify undertone based on hue distribution.
        
        Undertone is determined by the dominant hue in skin pixels:
        - Warm: Red-Yellow tones (0-35°)
        - Neutral: Yellow-Green tones (35-60°)
        - Cool: Purple-Red tones (340-360°)
        
        Note: OpenCV uses 0-180 for hue (half of 0-360), so we convert.
        
        Args:
            hue_values (np.ndarray): Hue values (0-180 in OpenCV) of skin pixels
        
        Returns:
            Tuple[str, float]: (Undertone classification, Mean hue in degrees)
        """
        # Convert OpenCV hue (0-180) to degrees (0-360)
        # OpenCV compresses hue to 0-180 range for 8-bit storage
        hue_degrees = (hue_values.astype(float) / 180) * 360
        mean_hue = np.mean(hue_degrees)
        
        # Normalize hue to 0-360 range
        if mean_hue > 180:
            mean_hue = mean_hue - 360
        
        logger.info(f"Mean hue: {mean_hue}°")
        
        # Classify based on hue ranges
        if self.WARM_HUE_RANGE[0] <= mean_hue <= self.WARM_HUE_RANGE[1]:
            undertone = 'Warm'
        elif self.NEUTRAL_HUE_RANGE[0] <= mean_hue <= self.NEUTRAL_HUE_RANGE[1]:
            undertone = 'Neutral'
        elif mean_hue >= self.COOL_HUE_RANGE[0] or mean_hue <= (self.COOL_HUE_RANGE[1] - 360):
            undertone = 'Cool'
        else:
            # Default to neutral if ambiguous
            undertone = 'Neutral'
        
        return undertone, mean_hue
    
    def _calculate_confidence(self, value_values: np.ndarray, hue_values: np.ndarray) -> float:
        """
        Calculate confidence score for the classification.
        
        Confidence increases when:
        - Skin pixel values are consistent (low std deviation)
        - Sufficient number of skin pixels detected
        
        Args:
            value_values (np.ndarray): V channel values
            hue_values (np.ndarray): H channel values
        
        Returns:
            float: Confidence score (0-1 range)
        """
        # Calculate standard deviation of brightness values
        # Low variation = more consistent skin tone = higher confidence
        value_std = np.std(value_values) / 255
        
        # Base confidence inversely proportional to variation
        # High std (variation) → low confidence
        confidence = max(0, 1 - value_std)
        
        # Boost confidence if sufficient pixels detected
        if len(hue_values) > 500:
            confidence = min(1, confidence + 0.1)
        
        logger.info(f"Confidence calculation: base={1 - value_std:.2f}, "
                   f"final={confidence:.2f}, pixels={len(hue_values)}")
        
        return confidence
    
    def _generate_recommendations(self, depth: str, undertone: str) -> Dict[str, Any]:
        """
        Generate personalized color recommendations based on skin tone.
        
        Looks up the predefined color palette for the given (depth, undertone)
        combination and formats it for frontend display.
        
        Args:
            depth (str): Skin depth (Fair, Medium, or Dark)
            undertone (str): Skin undertone (Warm, Cool, or Neutral)
        
        Returns:
            dict: Color recommendations with structure:
            {
                "clothing": {
                    "best_colors": [hex codes],
                    "description": str
                },
                "makeup": {
                    "foundation": {"shades": [...], "hex_codes": [...]},
                    "lipstick": {"shades": [...], "hex_codes": [...]},
                    "eyeshadow": {"shades": [...], "hex_codes": [...]}
                },
                "jewelry": {
                    "best_metals": [...],
                    "metal_hex": [...],
                    "stone_colors": [...],
                    "stone_hex": [...]
                }
            }
        """
        # Look up palette for this skin tone combination
        key = (depth, undertone)
        palette = self.palettes.get(key, self.palettes[('Medium', 'Neutral')])
        
        logger.info(f"Using palette for ({depth}, {undertone})")
        
        return {
            "clothing": {
                "best_colors": palette['clothing'][:6],
                "description": f"Recommended clothing colors for {depth} skin with {undertone} undertone"
            },
            "makeup": {
                "foundation": {
                    "shades": self._hex_to_names(palette['makeup']['foundation']),
                    "hex_codes": palette['makeup']['foundation']
                },
                "lipstick": {
                    "shades": self._hex_to_names(palette['makeup']['lipstick']),
                    "hex_codes": palette['makeup']['lipstick']
                },
                "eyeshadow": {
                    "shades": self._hex_to_names(palette['makeup']['eyeshadow']),
                    "hex_codes": palette['makeup']['eyeshadow']
                }
            },
            "jewelry": {
                "best_metals": self._metal_names(palette['jewelry']['metals']),
                "metal_hex": palette['jewelry']['metals'],
                "stone_colors": self._hex_to_names(palette['jewelry']['stones']),
                "stone_hex": palette['jewelry']['stones']
            }
        }
    
    def _hex_to_names(self, hex_colors: List[str]) -> List[str]:
        """
        Convert hex color codes to human-readable color names.
        
        Args:
            hex_colors (List[str]): List of hex color codes
        
        Returns:
            List[str]: Corresponding color names
        """
        color_names = {
            '#FFB347': 'Peach', '#FF8C00': 'Dark Orange', '#CD853F': 'Peru',
            '#DEB887': 'Burlywood', '#F4A460': 'Sandy Brown', '#DAA520': 'Goldenrod',
            '#8B4513': 'Saddle Brown', '#D2691E': 'Chocolate', '#FF6347': 'Tomato',
            '#FF7F50': 'Coral', '#E75480': 'Raspberry', '#FFD700': 'Gold',
            '#FFA500': 'Orange', '#FF4500': 'Orange Red', '#4B0082': 'Indigo',
            '#00CED1': 'Dark Turquoise', '#E0FFFF': 'Light Cyan', '#B0E0E6': 'Powder Blue',
            '#ADD8E6': 'Light Blue', '#87CEEB': 'Sky Blue', '#FF1493': 'Deep Pink',
            '#FF69B4': 'Hot Pink', '#C71585': 'Medium Violet Red', '#8A2BE2': 'Blue Violet',
            '#C0C0C0': 'Silver', '#E8E8E8': 'Ghost White', '#50C878': 'Emerald',
            '#008080': 'Teal', '#20B2AA': 'Light Sea Green', '#3CB371': 'Medium Sea Green',
            '#66CDAA': 'Medium Aquamarine', '#00FA9A': 'Medium Spring Green',
            '#483D8B': 'Dark Slate Blue', '#4169E1': 'Royal Blue', '#228B22': 'Forest Green',
            '#DC143C': 'Crimson', '#FF0000': 'Red', '#FFFFFF': 'White', '#000000': 'Black',
            '#808080': 'Gray', '#A9A9A9': 'Dark Gray', '#B76E79': 'Rose Gold',
            '#8B6914': 'Dark Yellow', '#A0522D': 'Sienna', '#704214': 'Sepia',
            '#545454': 'Dark Gray', '#696969': 'Dim Gray', '#3D3D3D': 'Very Dark Gray'
        }
        return [color_names.get(color, 'Color') for color in hex_colors]
    
    def _metal_names(self, metal_hex: List[str]) -> List[str]:
        """
        Convert metal hex codes to metal names.
        
        Args:
            metal_hex (List[str]): Hex codes for metals
        
        Returns:
            List[str]: Metal names
        """
        metal_map = {
            '#FFD700': 'Gold',
            '#C0C0C0': 'Silver',
            '#B76E79': 'Rose Gold',
            '#E8E8E8': 'Platinum'
        }
        return [metal_map.get(metal, 'Metal') for metal in metal_hex]
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """
        Generate standardized error response.
        
        Args:
            message (str): Error message
        
        Returns:
            dict: Error response object
        """
        return {
            "status": "error",
            "message": message,
            "skin_analysis": None,
            "recommendations": None
        }
