"""
Skin Tone Enums and Configuration

Defines the extended skin tone classification system with 6 depths and 5 undertones.
"""

from enum import Enum
from typing import Dict, Tuple


class SkinDepth(Enum):
    """Extended skin depth classification (6 levels)."""
    
    VERY_FAIR = "Very Fair"
    FAIR = "Fair"
    MEDIUM = "Medium"
    TAN = "Tan"
    DARK = "Dark"
    DEEP = "Deep"
    
    @classmethod
    def from_value(cls, value: int) -> 'SkinDepth':
        """
        Classify depth from V channel value (0-255).
        
        Args:
            value: Mean V channel value
            
        Returns:
            SkinDepth enum value
        """
        if value > 210:
            return cls.VERY_FAIR
        elif value > 180:
            return cls.FAIR
        elif value > 140:
            return cls.MEDIUM
        elif value > 100:
            return cls.TAN
        elif value > 60:
            return cls.DARK
        else:
            return cls.DEEP
    
    def get_level(self) -> int:
        """Get numeric level (1-6)."""
        levels = {
            'Very Fair': 1,
            'Fair': 2,
            'Medium': 3,
            'Tan': 4,
            'Dark': 5,
            'Deep': 6
        }
        return levels.get(self.value, 3)
    
    def get_percentile(self) -> Tuple[int, int]:
        """Get brightness percentile range."""
        percentiles = {
            'Very Fair': (82, 100),
            'Fair': (71, 82),
            'Medium': (55, 71),
            'Tan': (39, 55),
            'Dark': (24, 39),
            'Deep': (0, 24)
        }
        return percentiles.get(self.value, (39, 55))


class Undertone(Enum):
    """Extended undertone classification (5 types)."""
    
    WARM = "Warm"
    COOL = "Cool"
    NEUTRAL = "Neutral"
    OLIVE = "Olive"
    GOLDEN = "Golden"
    
    @classmethod
    def from_hue(cls, hue_degrees: float) -> 'Undertone':
        """
        Classify undertone from hue value in degrees (0-360).
        
        Args:
            hue_degrees: Mean hue in degrees
            
        Returns:
            Undertone enum value
        """
        # Normalize to 0-360
        hue = hue_degrees % 360
        
        # Check ranges (in order of check)
        if 0 <= hue <= 30 or hue == 360:  # Wrap-around for cool
            return cls.WARM
        elif 30 < hue <= 60:
            return cls.NEUTRAL
        elif 60 < hue <= 90:
            return cls.OLIVE
        elif 90 < hue <= 120:
            return cls.GOLDEN
        elif 330 <= hue < 360:  # Cool wrap-around
            return cls.COOL
        else:
            return cls.NEUTRAL
    
    def get_hue_range(self) -> Tuple[int, int]:
        """Get hue range in degrees for this undertone."""
        ranges = {
            'Warm': (0, 30),
            'Cool': (330, 360),
            'Neutral': (30, 60),
            'Olive': (60, 90),
            'Golden': (90, 120)
        }
        return ranges.get(self.value, (30, 60))
    
    def is_cool_spectrum(self) -> bool:
        """Check if undertone is in cool spectrum."""
        return self in [Undertone.COOL, Undertone.OLIVE]
    
    def is_warm_spectrum(self) -> bool:
        """Check if undertone is in warm spectrum."""
        return self in [Undertone.WARM, Undertone.GOLDEN]


# Configuration constants

DEPTH_THRESHOLDS: Dict[SkinDepth, int] = {
    SkinDepth.VERY_FAIR: 210,
    SkinDepth.FAIR: 180,
    SkinDepth.MEDIUM: 140,
    SkinDepth.TAN: 100,
    SkinDepth.DARK: 60,
    SkinDepth.DEEP: 0
}

UNDERTONE_HUE_RANGES: Dict[Undertone, Tuple[int, int]] = {
    Undertone.WARM: (0, 30),
    Undertone.COOL: (330, 360),
    Undertone.NEUTRAL: (30, 60),
    Undertone.OLIVE: (60, 90),
    Undertone.GOLDEN: (90, 120)
}

# All 30 possible combinations
ALL_SKIN_TONE_COMBINATIONS = [
    (depth, undertone)
    for depth in SkinDepth
    for undertone in Undertone
]

# Legacy mapping for backward compatibility
LEGACY_DEPTH_MAPPING = {
    'Fair': SkinDepth.FAIR,
    'Medium': SkinDepth.MEDIUM,
    'Dark': SkinDepth.DARK
}

LEGACY_UNDERTONE_MAPPING = {
    'Warm': Undertone.WARM,
    'Cool': Undertone.COOL,
    'Neutral': Undertone.NEUTRAL
}
