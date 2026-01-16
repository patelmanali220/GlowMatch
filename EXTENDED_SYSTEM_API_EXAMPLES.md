# Extended Skin Tone System - API Response Examples

## Response v1 (Legacy - Backward Compatible)

```json
{
  "success": true,
  "message": "Skin tone analysis completed successfully",
  "skinAnalysis": {
    "depth": "Medium",
    "undertone": "Warm",
    "skinToneCategory": "Medium-Warm",
    "hexColor": "#D2B48C",
    "rgbColor": {
      "r": 210,
      "g": 180,
      "b": 140
    },
    "hsvColor": {
      "h": 30,
      "s": 0.33,
      "v": 0.82
    }
  },
  "recommendations": {
    "clothing": {
      "best_colors": ["#8B4513", "#D2691E", "#CD853F", "#FF8C00", "#FFB347", "#DAA520"],
      "description": "Recommended clothing colors for Medium skin with Warm undertone"
    },
    "makeup": {
      "foundation": {
        "shades": ["Beige", "Tan", "Sand"],
        "hex_codes": ["#C9A877", "#D4A574", "#DEB887"]
      },
      "lipstick": {
        "shades": ["Coral", "Tomato", "Red"],
        "hex_codes": ["#E75480", "#FF6347", "#FF8C00"]
      },
      "eyeshadow": {
        "shades": ["Sienna", "Peru", "Gold"],
        "hex_codes": ["#8B4513", "#CD853F", "#FFD700"]
      }
    },
    "jewelry": {
      "best_metals": ["Gold", "Rose Gold"],
      "metal_hex": ["#FFD700", "#B76E79"],
      "stone_colors": ["Amber", "Topaz"],
      "stone_hex": ["#FF8C00", "#DAA520"]
    }
  },
  "analysisDetails": {
    "processingTime": "< 1s",
    "faceDetectionMethod": "MediaPipe Face Detection",
    "skinPixelsDetected": 15847,
    "hueDistribution": [30, 28, 0.15],
    "saturationLevel": 0.33,
    "brightnessLevel": 0.82,
    "confidenceScore": 0.92,
    "recommendedRetryIfBelow": 0.70
  }
}
```

---

## Response v2 (Extended - NEW FIELDS)

```json
{
  "success": true,
  "message": "Skin tone analysis completed successfully",
  "version": "2.0",
  "skinAnalysis": {
    "depth": "Medium",
    "undertone": "Warm",
    "skinToneCategory": "Medium-Warm",
    "hexColor": "#D2B48C",
    "rgbColor": {
      "r": 210,
      "g": 180,
      "b": 140
    },
    "hsvColor": {
      "h": 30,
      "s": 0.33,
      "v": 0.82
    },
    "_NEW_": {
      "extendedDepth": "Medium",
      "depthLevel": 3,
      "depthPercentile": "55-71%",
      "extendedUndertone": "Warm",
      "undertoneHueRange": [0, 30],
      "undertoneIntensity": 0.85,
      "skinToneConfidence": 0.92,
      "skinCharacteristics": {
        "hasOliveUndertones": false,
        "isWarmDominant": true,
        "undertoneBalance": "Warm dominant"
      }
    }
  },
  "recommendations": {
    "clothing": {
      "best_colors": ["#8B4513", "#D2691E", "#CD853F", "#FF8C00", "#FFB347", "#DAA520"],
      "description": "Recommended clothing colors for Medium skin with Warm undertone"
    },
    "makeup": {
      "foundation": {
        "shades": ["Beige", "Tan", "Sand"],
        "hex_codes": ["#C9A877", "#D4A574", "#DEB887"]
      },
      "lipstick": {
        "shades": ["Coral", "Tomato", "Red"],
        "hex_codes": ["#E75480", "#FF6347", "#FF8C00"]
      },
      "eyeshadow": {
        "shades": ["Sienna", "Peru", "Gold"],
        "hex_codes": ["#8B4513", "#CD853F", "#FFD700"]
      }
    },
    "jewelry": {
      "best_metals": ["Gold", "Rose Gold"],
      "metal_hex": ["#FFD700", "#B76E79"],
      "stone_colors": ["Amber", "Topaz"],
      "stone_hex": ["#FF8C00", "#DAA520"]
    },
    "_NEW_": {
      "seasonal": {
        "spring": ["#FFB6C1", "#98FB98", "#87CEEB", "#FFE4B5"],
        "summer": ["#00CED1", "#87CEEB", "#00FA9A", "#20B2AA"],
        "autumn": ["#8B4513", "#CD853F", "#FFD700", "#FF8C00"],
        "winter": ["#4B0082", "#00008B", "#C0C0C0", "#FFFFFF"]
      },
      "skinConditionAdjustments": {
        "dry": "Use hydrating makeup with luminous finish for dry skin",
        "oily": "Choose matte foundation for oily skin",
        "normal": "Any well-matched shade works",
        "sensitive": "Use hypoallergenic, fragrance-free formulas"
      }
    }
  },
  "analysisDetails": {
    "processingTime": "< 1s",
    "faceDetectionMethod": "MediaPipe Face Detection",
    "skinPixelsDetected": 15847,
    "hueDistribution": [30, 28.5, 0.33],
    "saturationLevel": 0.33,
    "brightnessLevel": 0.82,
    "confidenceScore": 0.92,
    "recommendedRetryIfBelow": 0.70
  }
}
```

---

## All 30 Classification Combinations

### Very Fair Skin (Level 1)
- Very Fair-Warm
- Very Fair-Cool
- Very Fair-Neutral
- Very Fair-Olive
- Very Fair-Golden

### Fair Skin (Level 2)
- Fair-Warm
- Fair-Cool
- Fair-Neutral
- Fair-Olive
- Fair-Golden

### Medium Skin (Level 3)
- Medium-Warm
- Medium-Cool
- Medium-Neutral
- Medium-Olive
- Medium-Golden

### Tan Skin (Level 4)
- Tan-Warm
- Tan-Cool
- Tan-Neutral
- Tan-Olive
- Tan-Golden

### Dark Skin (Level 5)
- Dark-Warm
- Dark-Cool
- Dark-Neutral
- Dark-Olive
- Dark-Golden

### Deep Skin (Level 6)
- Deep-Warm
- Deep-Cool
- Deep-Neutral
- Deep-Olive
- Deep-Golden

---

## Response Parsing Examples

### TypeScript/Angular

```typescript
import { ExtendedSkinAnalysisResponse, isExtendedResponse, getExtendedClassification } from './extended-skin-analysis.model';

// Check if response is v2
if (isExtendedResponse(response)) {
  const extended = getExtendedClassification(response);
  console.log(`Depth: ${extended.extendedDepth} (Level ${extended.depthLevel})`);
  console.log(`Undertone: ${extended.extendedUndertone}`);
  console.log(`Confidence: ${extended.skinToneConfidence}`);
  
  // Use seasonal recommendations
  const seasonalColors = response.recommendations._NEW_?.seasonal;
  if (seasonalColors) {
    console.log('Summer colors:', seasonalColors.summer);
  }
} else {
  // Fallback to v1 parsing
  console.log(`Depth: ${response.skinAnalysis.depth}`);
  console.log(`Undertone: ${response.skinAnalysis.undertone}`);
}
```

### Java

```java
ExtendedSkinAnalysisResponse response = // ... from API

// Access legacy fields (always available)
String legacyDepth = response.getSkinAnalysis().getDepth();
String legacyUndertone = response.getSkinAnalysis().getUndertone();

// Access extended fields (if available)
ExtendedClassification extended = response.getSkinAnalysis().getExtendedClassification();
if (extended != null) {
    int depthLevel = extended.getDepthLevel();
    String depthPercentile = extended.getDepthPercentile();
    List<String> seasonalSpring = response.getRecommendations()
        .getSeasonalRecommendations()
        .getSpring();
}
```

### Python

```python
response = response.json()

# Legacy access
legacy_depth = response['skinAnalysis']['depth']
legacy_undertone = response['skinAnalysis']['undertone']

# Extended access
if '_NEW_' in response['skinAnalysis']:
    extended = response['skinAnalysis']['_NEW_']
    depth_level = extended['depthLevel']
    undertone_intensity = extended['undertoneIntensity']
    
    seasonal = response['recommendations']['_NEW_']['seasonal']
    spring_colors = seasonal['spring']
```

---

## Backward Compatibility Matrix

| Aspect | v1 | v2 | Changes |
|--------|----|----|---------|
| Depth | 3 levels | 6 levels | New fields only, old fields unchanged |
| Undertone | 3 types | 5 types | New fields only, old fields unchanged |
| Recommendations | Basic | Extended | New `_NEW_` field with seasonal |
| Analysis Details | Standard | Extended | New metrics in analysisDetails |
| API URL | `/analyze-skin` | `/analyze-skin` | Same endpoint, version in response |

---

## Client Migration Path

### Step 1: Accept v2 Responses (No Breaking Changes)
- Existing v1 clients continue to work
- New v2 fields are optional and nested under `_NEW_`
- Version field helps identify response type

### Step 2: Gracefully Handle v2 Fields
```typescript
// Before
const depth = response.skinAnalysis.depth;

// After (with fallback)
const depth = response.skinAnalysis?._NEW_?.extendedDepth 
  || response.skinAnalysis.depth;
```

### Step 3: Gradually Adopt Extended Features
- Add seasonal color display
- Show undertone intensity
- Display confidence score
- Add skin condition adjustments

### Step 4: Full v2 Migration (Optional)
- Migrate to new data models
- Use extended enums
- Implement all extended features

---

## API Versioning Strategy

### Query Parameter (Optional)
```
GET /analyze-skin?version=2.0
```

### Request Header (Optional)
```
Accept: application/vnd.glowmatch.v2+json
```

### Response Indicator (Current)
```json
"version": "2.0"
```

---

## Error Handling

### Confidence Below Threshold
```json
{
  "success": false,
  "message": "Insufficient skin tone data detected",
  "analysisDetails": {
    "confidenceScore": 0.65,
    "recommendedRetryIfBelow": 0.70,
    "suggestion": "Try with better lighting or clearer face visibility"
  }
}
```

### Face Not Detected
```json
{
  "success": false,
  "message": "No face detected in image",
  "analysisDetails": {
    "confidenceScore": 0.0,
    "suggestion": "Ensure face is clearly visible and well-lit"
  }
}
```

---

## Performance Metrics

| Metric | v1 | v2 | Notes |
|--------|----|----|-------|
| Processing Time | <1s | <1s | Same ML algorithm |
| Response Size | ~2KB | ~3-4KB | Additional fields |
| Backward Compat | 100% | 100% | No breaking changes |
| New Features | 0% | +40% | Seasonal, extended class |

