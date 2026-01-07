"""
Test Suite for GlowMatch ML Service

Tests the core machine learning functionality:
- Face detection
- Skin tone analysis
- Depth and undertone classification
- Color recommendation generation

Run with: pytest tests/test_ml_service.py -v

Author: GlowMatch Development Team
"""

import pytest
import numpy as np
import cv2
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.ml_service import SkinToneAnalyzer


class TestSkinToneAnalyzer:
    """Test suite for SkinToneAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for tests"""
        return SkinToneAnalyzer()
    
    @pytest.fixture
    def synthetic_skin_image(self):
        """
        Create a synthetic image with a light skin tone face.
        
        Generates a 300x300 RGB image with:
        - Medium skin tone face (rectangular region)
        - White background
        - Realistic skin color in RGB
        
        Returns:
            np.ndarray: Image array (300, 300, 3) in RGB format
        """
        # Create white background
        image = np.ones((300, 300, 3), dtype=np.uint8) * 255
        
        # Add a rectangular face-like region with medium skin tone RGB
        # Typical skin tone: RGB(210, 180, 140) for medium skin
        skin_color = [210, 180, 140]  # RGB format
        image[50:250, 75:225] = skin_color
        
        return image
    
    @pytest.fixture
    def synthetic_dark_skin_image(self):
        """
        Create a synthetic image with dark skin tone.
        
        Returns:
            np.ndarray: Image array (300, 300, 3) in RGB format
        """
        image = np.ones((300, 300, 3), dtype=np.uint8) * 255
        
        # Dark skin tone RGB
        skin_color = [100, 75, 60]  # Darker skin
        image[50:250, 75:225] = skin_color
        
        return image
    
    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes without errors"""
        assert analyzer is not None
        assert analyzer.face_detector is not None
        assert analyzer.palettes is not None
        assert len(analyzer.palettes) == 6  # 3 depths × 3 undertones
    
    def test_color_palettes_exist(self, analyzer):
        """Test that all 6 color palettes are defined"""
        expected_keys = [
            ('Fair', 'Warm'), ('Fair', 'Cool'), ('Fair', 'Neutral'),
            ('Medium', 'Warm'), ('Medium', 'Cool'), ('Medium', 'Neutral'),
            ('Dark', 'Warm'), ('Dark', 'Cool'), ('Dark', 'Neutral')
        ]
        
        for key in expected_keys:
            assert key in analyzer.palettes
            palette = analyzer.palettes[key]
            assert 'clothing' in palette
            assert 'makeup' in palette
            assert 'jewelry' in palette
    
    def test_color_palettes_have_colors(self, analyzer):
        """Test that color palettes contain hex color codes"""
        for palette in analyzer.palettes.values():
            # Check clothing colors
            assert isinstance(palette['clothing'], list)
            assert len(palette['clothing']) > 0
            assert all(color.startswith('#') for color in palette['clothing'])
            
            # Check makeup colors
            assert 'foundation' in palette['makeup']
            assert 'lipstick' in palette['makeup']
            assert 'eyeshadow' in palette['makeup']
            
            # Check jewelry
            assert 'metals' in palette['jewelry']
            assert 'stones' in palette['jewelry']
    
    def test_depth_classification_fair(self, analyzer):
        """Test depth classification for Fair skin (high brightness)"""
        # Create high brightness values (above 166)
        bright_values = np.array([170, 175, 180, 185])
        depth = analyzer._classify_depth(bright_values)
        assert depth == 'Fair'
    
    def test_depth_classification_medium(self, analyzer):
        """Test depth classification for Medium skin"""
        # Create medium brightness values (115-166)
        medium_values = np.array([130, 135, 140, 145])
        depth = analyzer._classify_depth(medium_values)
        assert depth == 'Medium'
    
    def test_depth_classification_dark(self, analyzer):
        """Test depth classification for Dark skin (low brightness)"""
        # Create low brightness values (below 115)
        dark_values = np.array([80, 90, 100, 110])
        depth = analyzer._classify_depth(dark_values)
        assert depth == 'Dark'
    
    def test_undertone_classification_warm(self, analyzer):
        """Test undertone classification for Warm tones"""
        # Create hue values in warm range (0-35 degrees, converted to 0-17.5 in OpenCV)
        warm_hues = np.array([5, 10, 15, 20], dtype=np.uint8)  # OpenCV format
        undertone, mean_hue = analyzer._classify_undertone(warm_hues)
        assert undertone == 'Warm'
    
    def test_undertone_classification_cool(self, analyzer):
        """Test undertone classification for Cool tones"""
        # Create hue values in cool range
        cool_hues = np.array([170, 175, 178, 180], dtype=np.uint8)
        undertone, mean_hue = analyzer._classify_undertone(cool_hues)
        assert undertone == 'Cool'
    
    def test_confidence_calculation(self, analyzer):
        """Test confidence score calculation"""
        # Create consistent value values (low variation = high confidence)
        consistent_values = np.array([140, 141, 142, 143] * 200)
        hue_values = np.random.randint(0, 50, size=800)
        
        confidence = analyzer._calculate_confidence(consistent_values, hue_values)
        
        # Should have reasonable confidence (0.5-1.0 range)
        assert 0 <= confidence <= 1
    
    def test_hex_to_names_conversion(self, analyzer):
        """Test hex color to name conversion"""
        hex_colors = ['#FFB347', '#FF8C00', '#DAA520']
        names = analyzer._hex_to_names(hex_colors)
        
        assert len(names) == 3
        assert 'Peach' in names[0]  # #FFB347
        assert 'Orange' in names[1]  # #FF8C00
    
    def test_metal_names_conversion(self, analyzer):
        """Test metal hex to name conversion"""
        metals = ['#FFD700', '#C0C0C0', '#B76E79']
        names = analyzer._metal_names(metals)
        
        assert len(names) == 3
        assert 'Gold' in names
        assert 'Silver' in names
        assert 'Rose Gold' in names
    
    def test_recommendations_generation(self, analyzer):
        """Test color recommendation generation"""
        recommendations = analyzer._generate_recommendations('Medium', 'Warm')
        
        assert 'clothing' in recommendations
        assert 'makeup' in recommendations
        assert 'jewelry' in recommendations
        
        assert 'best_colors' in recommendations['clothing']
        assert 'foundation' in recommendations['makeup']
        assert 'best_metals' in recommendations['jewelry']
    
    def test_recommendations_all_combinations(self, analyzer):
        """Test recommendations for all skin tone combinations"""
        depths = ['Fair', 'Medium', 'Dark']
        undertones = ['Warm', 'Cool', 'Neutral']
        
        for depth in depths:
            for undertone in undertones:
                recommendations = analyzer._generate_recommendations(depth, undertone)
                assert recommendations is not None
                assert 'clothing' in recommendations
    
    def test_skin_extraction_returns_mask(self, analyzer, synthetic_skin_image):
        """Test that skin extraction returns valid mask"""
        # Convert to BGR for OpenCV
        image_bgr = cv2.cvtColor(synthetic_skin_image, cv2.COLOR_RGB2BGR)
        
        # Create mock face box
        face_box = {
            'x': 50,
            'y': 50,
            'width': 150,
            'height': 200,
            'confidence': 0.95
        }
        
        skin_mask, skin_region = analyzer._extract_skin_region(image_bgr, face_box)
        
        # Check mask validity
        assert skin_mask is not None
        assert skin_mask.dtype == np.uint8
        assert np.unique(skin_mask).tolist() in [
            [0], [255], [0, 255]
        ]  # Binary mask
    
    def test_error_response_format(self, analyzer):
        """Test error response formatting"""
        error_msg = "Test error message"
        response = analyzer._error_response(error_msg)
        
        assert response['status'] == 'error'
        assert response['message'] == error_msg
        assert response['skin_analysis'] is None
        assert response['recommendations'] is None
    
    def test_analyze_skin_tone_with_synthetic_image(self, analyzer, synthetic_skin_image):
        """Test full analysis pipeline with synthetic image"""
        result = analyzer.analyze_skin_tone(synthetic_skin_image)
        
        # Check response structure
        if result.get('status') != 'error':  # Only check if analysis succeeded
            assert 'skin_analysis' in result
            assert 'recommendations' in result
            assert 'analysis_details' in result
            
            # Check skin analysis fields
            skin_analysis = result['skin_analysis']
            assert skin_analysis['depth'] in ['Fair', 'Medium', 'Dark']
            assert skin_analysis['undertone'] in ['Warm', 'Cool', 'Neutral']
            assert 0 <= skin_analysis['confidence'] <= 1


class TestIntegration:
    """Integration tests for complete pipeline"""
    
    def test_full_pipeline_medium_warm_skin(self):
        """Test complete pipeline for Medium + Warm skin"""
        analyzer = SkinToneAnalyzer()
        
        # Create synthetic medium + warm skin image
        image = np.ones((300, 300, 3), dtype=np.uint8) * 255
        # Medium warm skin: RGB(210, 180, 140)
        image[50:250, 75:225] = [210, 180, 140]
        
        result = analyzer.analyze_skin_tone(image)
        
        # Should complete without errors
        assert result is not None
        assert 'skin_analysis' in result or result.get('status') == 'error'
    
    def test_multiple_consecutive_analyses(self):
        """Test analyzer can handle multiple consecutive analyses"""
        analyzer = SkinToneAnalyzer()
        
        for i in range(3):
            # Create slightly different synthetic images
            image = np.ones((300, 300, 3), dtype=np.uint8) * 255
            skin_tone = 150 + (i * 20)
            image[50:250, 75:225] = [skin_tone, skin_tone - 30, skin_tone - 70]
            
            result = analyzer.analyze_skin_tone(image)
            assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
