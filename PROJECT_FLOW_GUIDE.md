# 🎯 GlowMatch Project - Complete Step-by-Step Flow Guide

## 📋 Project Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   USER (Web Browser)                        │
│                   http://localhost:4200                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                    (HTTP Requests/Responses)
                             │
        ┌────────────────────▼────────────────────┐
        │      ANGULAR FRONTEND (Port 4200)       │
        │  - Image Upload UI                      │
        │  - Display Results                      │
        │  - Color Palette Cards                  │
        └────────────────────┬────────────────────┘
                             │
                   (REST API Calls)
                             │
        ┌────────────────────▼────────────────────┐
        │  SPRING BOOT BACKEND (Port 8080)        │
        │  - REST API Controller                  │
        │  - File Validation                      │
        │  - Error Handling                       │
        │  - Orchestration Layer                  │
        └────────────────────┬────────────────────┘
                             │
              (Forward image to ML Service)
                             │
        ┌────────────────────▼────────────────────┐
        │  PYTHON ML SERVICE (Port 8001)          │
        │  - Face Detection (MediaPipe)           │
        │  - Skin Extraction (OpenCV)             │
        │  - HSV Analysis                         │
        │  - Classification (Depth/Undertone)     │
        │  - Color Recommendation Generation      │
        └────────────────────┬────────────────────┘
                             │
                   (Analysis Results)
                             │
        ┌────────────────────▼────────────────────┐
        │      JSON Response with:                │
        │  - Skin Analysis                        │
        │  - Color Recommendations                │
        │  - Technical Details                    │
        └─────────────────────────────────────────┘
```

---

## 🚀 Build Order & Why

### **Why This Order?**

1. **ML Service First** ✅ (Bottom Layer)
   - Independent microservice
   - No dependencies on other components
   - Backend can test against it
   - Can work in isolation

2. **Backend Second** ✅ (Middle Layer)
   - Needs ML Service running to communicate with it
   - Provides REST API for frontend
   - Acts as bridge/orchestrator

3. **Frontend Last** ✅ (Top Layer)
   - Depends on working Backend API
   - Can connect and test all layers together
   - Final user interface

---

## 📁 Project Structure Created

```
GlowMatch/
│
├── ml-service/                    ← START HERE (Step 1)
│   ├── app/
│   │   ├── main.py               (FastAPI setup)
│   │   └── ml_service.py         (AI/ML logic)
│   ├── requirements.txt           (Python dependencies)
│   └── README.md                 (Instructions)
│
├── glowmatch-backend/             ← THEN DO THIS (Step 2)
│   ├── src/main/java/com/glowmatch/
│   │   ├── controller/            (REST endpoints)
│   │   ├── service/               (Business logic)
│   │   ├── model/                 (Data models)
│   │   ├── config/                (Configuration)
│   │   └── exception/             (Error handling)
│   ├── pom.xml                   (Maven dependencies)
│   └── README.md                 (Instructions)
│
├── glowmatch-frontend/            ← FINALLY THIS (Step 3)
│   ├── src/app/
│   │   ├── components/            (UI components)
│   │   ├── services/              (API communication)
│   │   └── models/                (TypeScript interfaces)
│   ├── package.json              (npm dependencies)
│   └── README.md                 (Instructions)
│
└── README.md                      (Main project overview)
```

---

## 🔧 Step 1: ML Service (FastAPI + Python)

### **What Does It Do?**

Takes an image, analyzes skin tone, returns color recommendations.

### **Why First?**

- Backend will call this service
- Can test independently
- Need it running before backend tests work
- Foundation for everything

### **What Happens Inside?**

```
User uploads image
        ↓
ML Service receives image
        ↓
Face Detection (MediaPipe)
   └─ Finds face in image
        ↓
Skin Region Extraction (OpenCV)
   └─ Isolates skin area
        ↓
Color Space Conversion (HSV)
   └─ Converts RGB to HSV color space
   └─ Easier to analyze skin tone
        ↓
Analysis:
   ├─ Brightness Value → Depth (Fair/Medium/Dark)
   ├─ Hue → Undertone (Warm/Cool/Neutral)
   └─ Confidence Score
        ↓
Generate Recommendations:
   ├─ Clothing colors
   ├─ Makeup shades (foundation, lipstick, eyeshadow)
   └─ Jewelry metals and stones
        ↓
Return JSON Response
```

### **Commands to Run**

```bash
# Step 1a: Navigate to ml-service folder
cd ml-service

# Step 1b: Create Python virtual environment
python -m venv venv

# Step 1c: Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Step 1d: Install dependencies
pip install -r requirements.txt

# Step 1e: Run the service
python -m uvicorn app.main:app --host 0.0.0.0 --reload --port 8001

# Output should show:
# Uvicorn running on http://127.0.0.1:8001
# Open browser to: http://localhost:8001/docs
```

### **Key Files Explained**

#### `requirements.txt`
```
fastapi           → Web framework
uvicorn          → Server to run FastAPI
opencv-python    → Image processing
mediapipe        → Face detection
numpy            → Math operations
scikit-learn     → ML utilities
pillow           → Image format handling
```

#### `app/main.py`
```python
- Sets up FastAPI server
- Defines /analyze-skin endpoint
- Receives image file
- Calls ML service
- Returns JSON
```

#### `app/ml_service.py`
```python
- SkinToneAnalyzer class (main logic)
- _detect_faces() → Find face in image
- _extract_skin_region() → Get skin pixels
- _classify_depth() → Fair/Medium/Dark
- _classify_undertone() → Warm/Cool/Neutral
- _generate_recommendations() → Color palettes
```

### **Test ML Service**

```bash
# After starting ML service, open browser:
http://localhost:8001/docs

# You'll see Swagger UI with:
- /analyze-skin endpoint
- /health endpoint

# Try uploading an image:
1. Click "Try it out"
2. Select image file
3. Click "Execute"
4. See JSON response with recommendations
```

---

## 🔌 Step 2: Backend (Spring Boot + Java)

### **What Does It Do?**

Bridges frontend and ML service. Provides REST API endpoints.

### **Why Second?**

- ML Service must be running
- Backend calls ML Service
- Backend validates files before sending to ML Service
- Frontend will call Backend endpoints

### **What Happens Inside?**

```
Frontend sends image to Backend
        ↓
RecommendationController receives request
        ↓
RecommendationService validates:
   ├─ File type (JPEG/PNG only)
   ├─ File size (max 5MB)
   └─ File not empty
        ↓
MLServiceClient sends to Python service
   └─ Calls: http://localhost:8001/analyze-skin
        ↓
Python ML Service processes
   └─ Returns analysis + recommendations
        ↓
Backend receives response
        ↓
Format JSON response
        ↓
Send to Frontend
```

### **Commands to Run**

```bash
# Step 2a: Navigate to backend folder
cd glowmatch-backend

# Step 2b: Build project (downloads dependencies)
mvn clean install

# Step 2c: Run backend server
./mvnw spring-boot:run

# Output should show:
# Started GlowMatchApplication in X seconds
# Server running on http://localhost:8080
```

### **Key Files Explained**

#### `pom.xml`
```xml
- Project configuration
- Maven dependencies (Spring, Jackson, etc.)
- Build settings
```

#### `src/main/resources/application.properties`
```properties
server.port=8080              → Backend port
ml.service.url=http://localhost:8001  → ML Service location
spring.servlet.multipart.max-file-size=5MB  → Upload limit
cors.allowed-origins=http://localhost:4200  → Frontend URL
```

#### `GlowMatchApplication.java`
```java
- Main entry point
- Creates RestTemplate bean for HTTP calls
```

#### `controller/RecommendationController.java`
```java
@PostMapping("/api/v1/recommendations/analyze")
public ApiResponse<AnalysisResult> analyzeImage(File)
   - Receives image from frontend
   - Calls service layer
   - Returns formatted response
```

#### `service/RecommendationService.java`
```java
public AnalysisResult analyzeImage(MultipartFile)
   - Validates file
   - Coordinates with ML client
```

#### `service/MLServiceClient.java`
```java
public AnalysisResult analyzeSkinTone(byte[], String)
   - Sends image to ML Service on port 8001
   - Parses response
   - Handles errors
```

#### `exception/GlobalExceptionHandler.java`
```java
- Catches all exceptions
- Returns consistent error messages
- Maps HTTP status codes
```

### **Test Backend**

```bash
# After starting backend, test with curl:
curl -X GET http://localhost:8080/api/v1/recommendations/health

# Response:
# {"status":"UP","service":"Recommendation Service"}

# Note: Image upload testing needs frontend (Step 3)
```

---

## 🎨 Step 3: Frontend (Angular)

### **What Does It Do?**

User interface for uploading images and viewing recommendations.

### **Why Last?**

- Calls Backend API
- Backend must be running
- ML Service must be running (Backend depends on it)
- All infrastructure ready for testing

### **What Happens Inside**

```
User opens http://localhost:4200
        ↓
Angular app loads (app.component.ts)
        ↓
Displays ImageUploadComponent
   ├─ Drag-drop area
   └─ File selector button
        ↓
User selects/drags image
        ↓
Client-side validation:
   ├─ File type (JPEG/PNG)
   └─ File size (max 5MB)
        ↓
Display image preview
        ↓
User clicks "Analyze My Skin Tone"
        ↓
Frontend sends to Backend
   ├─ URL: http://localhost:8080/api/v1/recommendations/analyze
   ├─ Method: POST
   └─ Body: FormData with image
        ↓
Backend processes (Step 2)
        ↓
Response arrives at Frontend
        ↓
Display RecommendationResultComponent
   ├─ Skin Analysis (Fair/Medium/Dark, Warm/Cool/Neutral)
   ├─ Clothing colors
   ├─ Makeup recommendations
   └─ Jewelry recommendations
        ↓
User can copy hex codes
        ↓
User can analyze another photo
```

### **Commands to Run**

```bash
# Step 3a: Navigate to frontend folder
cd glowmatch-frontend

# Step 3b: Install npm dependencies
npm install

# Step 3c: Start development server
npm start
# or
ng serve --open

# Output should show:
# ✔ Compiled successfully
# ✔ Compiled successfully
# Open browser to: http://localhost:4200
```

### **Key Files Explained**

#### `package.json`
```json
- Project metadata
- npm script commands
- Dependencies (Angular, RxJS, Tailwind)
```

#### `src/environments/environment.ts`
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api/v1'
}
// Points to backend URL for API calls
```

#### `src/app/models/recommendation.model.ts`
```typescript
- TypeScript interfaces (type definitions)
- SkinAnalysis
- ColorRecommendation
- AnalysisResult
- ApiResponse<T>
```

#### `src/app/services/recommendation.service.ts`
```typescript
export class RecommendationService {
  analyzeImage(file: File): Observable<AnalysisResult>
    - Calls: POST http://localhost:8080/api/v1/recommendations/analyze
    - Sends: FormData with image
    - Returns: Observable<AnalysisResult>
  
  getRecommendation(id): Observable<AnalysisResult>
    - Retrieves saved recommendation
  
  getHistory(): Observable<AnalysisResult[]>
    - Gets user history
}
```

#### `src/app/components/image-upload.component.ts`
```typescript
- Shows upload UI
- Handles drag-drop
- Validates file
- Shows preview
- Calls service.analyzeImage()
- Handles loading/error states
```

#### `src/app/components/recommendation-result.component.ts`
```typescript
- Shows analysis results
- Displays color cards
- Shows hex codes
- "Copy" button functionality
```

#### `src/app/app.component.ts`
```typescript
- Main app container
- Routes between upload and results view
- Orchestrates component communication
```

---

## 🔄 Complete Data Flow Example

### **When User Uploads Image**

```
1️⃣ FRONTEND (Angular)
   User selects image.jpg
   ↓
   ImageUploadComponent validates
   ├─ Is it JPEG/PNG? ✓
   ├─ Is it < 5MB? ✓
   └─ Not empty? ✓
   ↓
   Creates FormData
   ↓
   Calls: recommendationService.analyzeImage(file)
   ↓
   HTTP POST to http://localhost:8080/api/v1/recommendations/analyze
   ├─ Headers: Content-Type: multipart/form-data
   └─ Body: image file

2️⃣ BACKEND (Spring Boot)
   RecommendationController receives POST request
   ↓
   Extracts file from request
   ↓
   Calls: recommendationService.analyzeImage(file)
   ↓
   RecommendationService validates again
   ├─ File type check
   ├─ File size check
   └─ Not empty check
   ↓
   Calls: mlServiceClient.analyzeSkinTone(imageBytes, filename)
   ↓
   MLServiceClient creates HTTP request to ML Service
   ├─ URL: http://localhost:8001/analyze-skin
   ├─ Method: POST
   └─ Body: FormData with image
   ↓
   Waits for response from ML Service

3️⃣ ML SERVICE (Python FastAPI)
   app.main receives POST at /analyze-skin
   ↓
   Validates image format
   ↓
   Calls: analyzer.analyze_skin_tone(imageArray)
   ↓
   SkinToneAnalyzer processes:
   
   a) Face Detection
      ├─ Uses MediaPipe FaceMesh
      └─ Finds face bounding box
      ↓
   b) Skin Extraction
      ├─ Apply HSV mask
      ├─ Morphological operations
      └─ Extract skin region pixels
      ↓
   c) Color Analysis
      ├─ Get Hue values from skin pixels
      ├─ Calculate mean Hue
      ├─ Get Saturation values
      └─ Get Brightness (Value) values
      ↓
   d) Classification
      ├─ Depth: Check brightness
      │  - Bright? → Fair
      │  - Medium? → Medium
      │  - Dark? → Dark
      │
      └─ Undertone: Check hue
         - Red-Yellow range? → Warm
         - Yellow-Green range? → Neutral
         - Purple-Red range? → Cool
      ↓
   e) Confidence Calculation
      ├─ Low variance = high confidence
      └─ More pixels = high confidence
      ↓
   f) Generate Recommendations
      ├─ Look up color palette for (Depth, Undertone)
      ├─ Get clothing colors
      ├─ Get makeup shades
      └─ Get jewelry colors
      ↓
   Returns JSON:
   {
     "status": "success",
     "skin_analysis": {
       "depth": "Medium",
       "undertone": "Warm",
       "confidence": 0.92
     },
     "recommendations": {
       "clothing": ["#FF8C00", "#FFB347", ...],
       "makeup": {
         "foundation": [...],
         "lipstick": [...],
         "eyeshadow": [...]
       },
       "jewelry": {
         "best_metals": ["Gold", ...],
         ...
       }
     },
     "analysis_details": {...}
   }

4️⃣ BACKEND (Continued)
   Receives response from ML Service
   ↓
   MLServiceClient parses JSON
   ↓
   Converts to AnalysisResult object
   ↓
   Returns to RecommendationService
   ↓
   Returns to RecommendationController
   ↓
   Wraps in ApiResponse
   ↓
   Sends HTTP 200 OK response with JSON body

5️⃣ FRONTEND (Final)
   RecommendationService receives response
   ↓
   Extracts data from ApiResponse
   ↓
   Returns Observable<AnalysisResult>
   ↓
   ImageUploadComponent subscribes
   ↓
   Sets: currentResult = result
   ↓
   Sets: showResults = true
   ↓
   Hides ImageUploadComponent
   ↓
   Shows RecommendationResultComponent
   ↓
   RecommendationResultComponent displays:
   ├─ Skin Depth: Medium
   ├─ Undertone: Warm
   ├─ Confidence: 92%
   ├─ Clothing Colors: [color cards with hex codes]
   ├─ Makeup:
   │  ├─ Foundation shades
   │  ├─ Lipstick shades
   │  └─ Eyeshadow shades
   └─ Jewelry metals & stones
   ↓
   User sees beautiful color palette! 🎨
   ↓
   User can click "Copy" to copy hex codes
   ↓
   User can click "Analyze Another Photo"
   ↓
   Back to step 1
```

---

## ⚙️ Environment Setup Checklist

### **ML Service Setup**
- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] dependencies installed (`pip install -r requirements.txt`)
- [ ] Running on port 8001
- [ ] Can access `/docs` page

### **Backend Setup**
- [ ] Java 17+ installed
- [ ] Maven 3.8+ installed
- [ ] ML Service running on port 8001
- [ ] `application.properties` configured with ML Service URL
- [ ] Running on port 8080
- [ ] Can access health endpoint

### **Frontend Setup**
- [ ] Node.js 18+ installed
- [ ] npm installed
- [ ] Backend running on port 8080
- [ ] ML Service running on port 8001
- [ ] `environment.ts` points to `http://localhost:8080/api/v1`
- [ ] Running on port 4200
- [ ] Can upload and analyze images

---

## 🐛 Troubleshooting Common Issues

### **Frontend can't reach Backend**
```
Check:
1. Backend running on 8080?
   curl http://localhost:8080/api/v1/recommendations/health
2. CORS allowed?
   Check application.properties: cors.allowed-origins
3. API URL in environment.ts correct?
   http://localhost:8080/api/v1
```

### **Backend can't reach ML Service**
```
Check:
1. ML Service running on 8001?
   curl http://localhost:8001/health
2. URL in application.properties?
   ml.service.url=http://localhost:8001
3. ML Service listening on 0.0.0.0?
   Should be in uvicorn startup message
```

### **Image Upload Fails**
```
Check:
1. File format JPEG or PNG?
2. File size < 5MB?
3. Backend logs for error message
4. Browser console for network errors
```

---

## 📊 Order of Commands (Copy-Paste Ready)

```bash
# ===== TERMINAL 1: ML Service =====
cd ml-service
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001

# ===== TERMINAL 2: Backend =====
cd backend
mvn clean install
mvn spring-boot:run

# ===== TERMINAL 3: Frontend =====
cd frontend
npm install
npm install
npm start
```

Then open browser to: **http://localhost:4200**

---

## ✅ Success Indicators

- ML Service Swagger UI works: http://localhost:8001/docs
- Backend health check works: http://localhost:8080/api/v1/recommendations/health
- Frontend loads: http://localhost:4200
- Can upload image and see results ✨
