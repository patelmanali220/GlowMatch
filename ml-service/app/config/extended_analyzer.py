"""
Refactored ML Service with Extended Skin Tone Classification

This module demonstrates the key changes for extended skin tone classification:
- Extended depth classification (6 levels)
- Extended undertone classification (5 types)
- Dynamic palette resolution
- Backward compatibility
"""

import numpy as np
from typing import Dict, Tuple, Any
from app.config.skin_tone_enums import SkinDepth, Undertone, DEPTH_THRESHOLDS, UNDERTONE_HUE_RANGES


class ExtendedSkinToneAnalyzer:
    """
    Extended version of SkinToneAnalyzer supporting 6 depths × 5 undertones = 30 combinations.
    
    This class extends the original analyzer with:
    - Extended classification algorithms
    - Dynamic palette resolution
    - Backward compatibility support
    - Enhanced metadata in responses
    """
    
    def __init__(self, palettes_config: Dict[str, Any]):
        """
        Initialize with extended palette configuration.
        
        Args:
            palettes_config: Dictionary loaded from extended_skin_palettes.json
        """
        self.palettes = palettes_config['palettes']
        self.depth_thresholds = palettes_config['depthThresholds']
        self.undertone_ranges = palettes_config['undertoneHueRanges']
    
    def _classify_depth_extended(self, value_values: np.ndarray) -> Tuple[SkinDepth, int, Tuple[int, int]]:
        """
        Classify skin depth using extended 6-level system.
        
        Args:
            value_values: V channel values (0-255) of skin pixels
            
        Returns:
            Tuple of (depth_enum, depth_level, percentile_range)
        """
        mean_value = np.mean(value_values)
        depth_enum = SkinDepth.from_value(int(mean_value))
        level = depth_enum.get_level()
        percentile = depth_enum.get_percentile()
        
        return depth_enum, level, percentile
    
    def _classify_undertone_extended(self, hue_values: np.ndarray) -> Tuple[Undertone, float, bool]:
        """
        Classify undertone using extended 5-type system.
        
        Args:
            hue_values: H channel values (0-180 OpenCV scale)
            
        Returns:
            Tuple of (undertone_enum, mean_hue_degrees, is_cool_spectrum)
        """
        # Convert OpenCV hue (0-180) to degrees (0-360)
        hue_degrees = (hue_values.astype(float) / 180) * 360
        mean_hue = np.mean(hue_degrees)
        mean_hue = mean_hue % 360
        
        undertone_enum = Undertone.from_hue(mean_hue)
        is_cool = undertone_enum.is_cool_spectrum()
        
        return undertone_enum, mean_hue, is_cool
    
    def _get_palette(self, depth: SkinDepth, undertone: Undertone) -> Dict[str, Any]:
        """
        Dynamically resolve palette for depth + undertone combination.
        
        Falls back to default if exact combination not found.
        
        Args:
            depth: SkinDepth enum
            undertone: Undertone enum
            
        Returns:
            Palette dictionary with colors and recommendations
        """
        key = f"{depth.value}-{undertone.value}"
        
        # Try exact match
        if key in self.palettes:
            return self.palettes[key]
        
        # Fallback to Medium-Neutral
        default_key = "Medium-Neutral"
        return self.palettes.get(default_key, {})
    
    def generate_extended_response(
        self,
        depth: SkinDepth,
        undertone: Undertone,
        mean_hue: float,
        confidence: float,
        skin_pixels_detected: int,
        saturation: float,
        brightness: float
    ) -> Dict[str, Any]:
        """
        Generate extended API response with v2 fields.
        
        Args:
            depth: Classified depth enum
            undertone: Classified undertone enum
            mean_hue: Mean hue in degrees
            confidence: Confidence score (0-1)
            skin_pixels_detected: Number of skin pixels found
            saturation: Mean saturation (0-1)
            brightness: Mean brightness (0-1)
            
        Returns:
            Complete extended response dictionary
        """
        depth_level, level_num, percentile = self._classify_depth_extended(
            np.array([brightness * 255])
        )
        
        palette = self._get_palette(depth, undertone)
        
        response = {
            "version": "2.0",
            "success": True,
            "message": "Skin tone analysis completed successfully",
            "skinAnalysis": {
                # Legacy fields (backward compatibility)
                "depth": depth.value,
                "undertone": undertone.value,
                "skinToneCategory": f"{depth.value}-{undertone.value}",
                
                # New extended fields
                "_NEW_": {
                    "extendedDepth": depth.value,
                    "depthLevel": level_num,
                    "depthPercentile": f"{percentile[0]}-{percentile[1]}%",
                    "extendedUndertone": undertone.value,
                    "undertoneHueRange": list(undertone.get_hue_range()),
                    "undertoneIntensity": round(saturation, 2),
                    "skinToneConfidence": round(confidence, 2),
                    "skinCharacteristics": {
                        "hasOliveUndertones": undertone == Undertone.OLIVE,
                        "isWarmDominant": undertone.is_warm_spectrum(),
                        "undertoneBalance": f"{'Cool' if undertone.is_cool_spectrum() else 'Warm'} dominant"
                    }
                }
            },
            "recommendations": {
                "clothing": palette.get("clothing", []),
                "makeup": palette.get("makeup", {}),
                "jewelry": palette.get("jewelry", {})
            },
            "analysisDetails": {
                "processingTime": "< 1s",
                "faceDetectionMethod": "MediaPipe Face Detection",
                "skinPixelsDetected": int(skin_pixels_detected),
                "hueDistribution": [
                    int(mean_hue),
                    round(mean_hue, 2),
                    round(saturation, 2)
                ],
                "saturationLevel": round(saturation, 2),
                "brightnessLevel": round(brightness, 2),
                "confidenceScore": round(confidence, 2),
                "recommendedRetryIfBelow": 0.70
            }
        }
        
        return response
    
    @staticmethod
    def map_to_legacy(depth: SkinDepth, undertone: Undertone) -> Tuple[str, str]:
        """
        Map extended classification to legacy 3x3 system.
        
        Used for backward compatibility with v1 clients.
        
        Args:
            depth: Extended SkinDepth
            undertone: Extended Undertone
            
        Returns:
            Tuple of (legacy_depth, legacy_undertone)
        """
        legacy_depth_map = {
            SkinDepth.VERY_FAIR: 'Fair',
            SkinDepth.FAIR: 'Fair',
            SkinDepth.MEDIUM: 'Medium',
            SkinDepth.TAN: 'Medium',
            SkinDepth.DARK: 'Dark',
            SkinDepth.DEEP: 'Dark'
        }
        
        legacy_undertone_map = {
            Undertone.WARM: 'Warm',
            Undertone.COOL: 'Cool',
            Undertone.NEUTRAL: 'Neutral',
            Undertone.OLIVE: 'Neutral',  # Closest match
            Undertone.GOLDEN: 'Warm'     # Closest match
        }
        
        return (
            legacy_depth_map.get(depth, 'Medium'),
            legacy_undertone_map.get(undertone, 'Neutral')
        )


# Example usage and integration points
"""
INTEGRATION POINTS IN EXISTING CODE:

1. In ml_service.py _classify_depth() method:
   OLD:
       def _classify_depth(self, value_values: np.ndarray) -> str:
           mean_value = np.mean(value_values)
           if mean_value > 166:
               return 'Fair'
           ...
   
   NEW:
       def _classify_depth_extended(self, value_values: np.ndarray) -> Tuple[SkinDepth, int]:
           mean_value = np.mean(value_values)
           depth_enum = SkinDepth.from_value(int(mean_value))
           return depth_enum, depth_enum.get_level()

2. In main.py response formatting:
   OLD:
       "depth": results["skin_analysis"]["depth"]
   
   NEW:
       extended_analyzer = ExtendedSkinToneAnalyzer(palettes_config)
       response = extended_analyzer.generate_extended_response(
           depth, undertone, mean_hue, confidence, 
           skin_pixels_detected, saturation, brightness
       )

3. For backward compatibility:
   legacy_depth, legacy_undertone = ExtendedSkinToneAnalyzer.map_to_legacy(depth, undertone)
   response['legacy'] = {
       'depth': legacy_depth,
       'undertone': legacy_undertone
   }
"""
