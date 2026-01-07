# GlowMatch - Quick Start Guide

## ⚡ Quick Start (3 Commands)

### Terminal 1 - ML Service:
```bash
cd ml-service
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2 - Backend:
```bash
cd glowmatch-backend
./mvnw spring-boot:run
```

### Terminal 3 - Frontend:
```bash
cd glowmatch-frontend
npm install
npm start
```

**Open http://localhost:4200** 🎉

---

## 🔧 All Code Fixes Applied

### ✅ 1. API Response Structure (ML Service → Backend → Frontend)
- Fixed inconsistent response keys (snake_case vs camelCase)
- Added missing fields (`hexColor`, `rgbColor`, complete recommendations)
- Aligned all three services to use the same structure

### ✅ 2. Port Configuration
- Fixed ML service URL: `8000` → `8001`
- Updated backend application startup message

### ✅ 3. Data Model Synchronization
- Backend `SkinAnalysisResponse.java` updated with proper nested classes
- Frontend TypeScript models updated to match
- Added `@JsonProperty` annotations for field mapping

### ✅ 4. Angular HttpClient Configuration
- Removed duplicate `HttpClientModule` import
- Using global HTTP provider from `app.config.ts`

### ✅ 5. UI Template Updates
- Updated HTML to display new structure:
  - Color swatches with hex codes
  - Foundation, lipstick, eyeshadow with visual colors
  - Jewelry metals and gemstones
- Improved visual presentation

### ✅ 6. Code Quality
- Fixed deprecated `HttpStatus.PAYLOAD_TOO_LARGE` (use status code 413)
- Removed unused imports
- Added proper error handling

---

## 📊 Complete API Flow

```
User uploads image (Frontend)
    ↓
Angular sends FormData to Backend (Port 8080)
    ↓
Spring Boot validates & forwards to ML Service (Port 8001)
    ↓
FastAPI analyzes image using MediaPipe + OpenCV
    ↓
Returns JSON response with:
    - Skin analysis (depth, undertone, colors)
    - Recommendations (clothing, makeup, jewelry)
    - Analysis details
    ↓
Backend passes response to Frontend
    ↓
Angular displays results with color swatches
```

---

## 🎯 What Works Now

✅ **Complete end-to-end flow**  
✅ **Face detection and skin analysis**  
✅ **Personalized color recommendations**  
✅ **Visual color swatches**  
✅ **Proper error handling**  
✅ **Type-safe data models**  
✅ **CORS configuration**  
✅ **File upload validation (5MB limit, JPG/PNG only)**  

---

## 🧪 Test the Application

1. **Start all 3 services** (see Quick Start above)

2. **Verify services are running:**
   - ML Service: http://localhost:8001/health
   - Backend: http://localhost:8080/api/v1/recommendations/health
   - Frontend: http://localhost:4200

3. **Upload a test image:**
   - Must be JPG or PNG
   - Max 5MB
   - Should contain a visible face
   - Well-lit, front-facing photos work best

4. **Expected result:**
   - Processing takes < 5 seconds
   - Shows skin tone analysis
   - Displays color recommendations with swatches
   - Includes confidence score

---

## 🐛 Troubleshooting

### ML Service won't start:
```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Backend build fails:
```bash
mvn clean install -U
```

### Frontend errors:
```bash
npm install
npm start
```

### Port already in use:
- ML Service (8001): Change port in `app/main.py`
- Backend (8080): Change in `application.properties`
- Frontend (4200): Use `ng serve --port 4201`

---

## 📝 Key Files Changed

1. **ml-service/app/main.py** - Response structure, color helpers
2. **glowmatch-backend/src/main/java/com/glowmatch/model/SkinAnalysisResponse.java** - Data model
3. **glowmatch-backend/src/main/resources/application.properties** - ML service URL
4. **glowmatch-frontend/src/app/models/skin-analysis.model.ts** - TypeScript interfaces
5. **glowmatch-frontend/src/app/components/analysis-results/analysis-results.component.html** - UI template
6. **glowmatch-frontend/src/app/app.ts** - Removed duplicate import

---

## 🎨 Response Example

```json
{
  "success": true,
  "message": "Skin tone analysis completed successfully",
  "skinAnalysis": {
    "depth": "Medium",
    "undertone": "Warm",
    "skinToneCategory": "Medium-Warm",
    "hexColor": "#D4A574",
    "rgbColor": {"r": 212, "g": 165, "b": 116},
    "hsvColor": {"h": 30.6, "s": 0.45, "v": 0.83}
  },
  "recommendations": {
    "clothing": {
      "best_colors": ["#FFB347", "#CD853F", "#DEB887"],
      "description": "Recommended clothing colors for Medium skin with Warm undertone"
    },
    "makeup": {
      "foundation": {
        "shades": ["Peach", "Sandy Brown"],
        "hex_codes": ["#FFB347", "#F4A460"]
      },
      "lipstick": {...},
      "eyeshadow": {...}
    },
    "jewelry": {
      "best_metals": ["Gold", "Rose Gold"],
      "metal_hex": ["#FFD700", "#B76E79"],
      "stone_colors": ["Emerald", "Topaz"],
      "stone_hex": ["#50C878", "#FFB347"]
    }
  },
  "analysisDetails": {
    "processingTime": "< 1s",
    "faceDetectionMethod": "MediaPipe Face Detection",
    "confidence": "0.89"
  }
}
```

---

## ✨ That's It!

All code errors have been fixed and the application should work perfectly. Upload an image and see your personalized beauty recommendations! 🎉
