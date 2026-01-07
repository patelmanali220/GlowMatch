# GlowMatch

A full-stack application that analyzes face photos to detect skin tone and recommends matching colors for clothing, makeup, and jewelry.

## Architecture

GlowMatch consists of three microservices:

1. **Angular Frontend** - User interface for photo upload and results display
2. **Spring Boot Backend** - API gateway and validation layer
3. **FastAPI ML Service** - Image analysis and skin tone detection

## Features

- 📸 Photo upload with drag-and-drop support
- 🎨 Skin tone detection using computer vision
- 👗 Personalized color recommendations for:
  - Clothing
  - Makeup
  - Jewelry
- 🎯 Real-time image analysis
- 📱 Responsive design

## Technology Stack

### Frontend
- Angular 16
- TypeScript
- CSS3 with modern gradients and animations
- HttpClient for API communication

### Backend
- Spring Boot 3.1.5
- Java 17
- Maven
- RestTemplate for ML service communication

### ML Service
- FastAPI
- Python 3.11
- OpenCV for image processing
- NumPy for numerical computations
- Pillow for image handling

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Java 17+ (for local backend development)
- Python 3.11+ (for local ML service development)
- Maven 3.6+ (for local backend development)

### Running with Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd GlowMatch
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:4200
- Backend API: http://localhost:8080/api
- ML Service: http://localhost:8000

### Running Services Individually

#### ML Service

```bash
cd ml-service
pip install -r requirements.txt
python app.py
```

The service will be available at http://localhost:8000

#### Backend

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

The service will be available at http://localhost:8080

#### Frontend

```bash
cd frontend
npm install
ng serve
```

The application will be available at http://localhost:4200

## API Documentation

### ML Service Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze image and return skin tone with color recommendations
  - Request: multipart/form-data with `file` parameter
  - Response: JSON with skin tone analysis and recommendations

### Backend Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze` - Upload image for analysis (proxies to ML service)
  - Request: multipart/form-data with `file` parameter
  - Response: JSON with analysis results

## Project Structure

```
GlowMatch/
├── ml-service/           # FastAPI ML service
│   ├── app.py           # Main application
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # ML service container
├── backend/             # Spring Boot backend
│   ├── src/
│   │   └── main/
│   │       ├── java/    # Java source files
│   │       └── resources/
│   ├── pom.xml         # Maven dependencies
│   └── Dockerfile      # Backend container
├── frontend/           # Angular frontend
│   ├── src/
│   │   ├── app/       # Application components
│   │   └── assets/    # Static assets
│   ├── package.json   # npm dependencies
│   ├── nginx.conf     # Nginx configuration
│   └── Dockerfile     # Frontend container
└── docker-compose.yml # Docker orchestration
```

## How It Works

1. User uploads a face photo through the Angular frontend
2. Frontend sends the image to Spring Boot backend for validation
3. Backend validates the image and forwards it to the ML service
4. ML service:
   - Detects skin pixels using HSV color space analysis
   - Calculates average skin tone RGB values
   - Classifies skin tone (Deep, Dark, Medium, Light, Fair)
   - Returns color recommendations based on skin tone
5. Results are displayed to the user with:
   - Detected skin tone with RGB values
   - Recommended colors for clothing, makeup, and jewelry
   - Visual color swatches and descriptions

## Skin Tone Classification

The application classifies skin tones into five categories based on luminance:

- **Deep**: Luminance < 100
- **Dark**: Luminance 100-150
- **Medium**: Luminance 150-180
- **Light**: Luminance 180-210
- **Fair**: Luminance > 210

## Color Recommendations

Each skin tone category includes:
- 4 clothing color recommendations
- 3 makeup color recommendations
- 3 jewelry color recommendations

Recommendations are based on color theory and complementary/contrasting principles.

## Development

### Adding New Color Recommendations

Edit the `get_color_recommendations` function in `ml-service/app.py` to add or modify color recommendations.

### Modifying Skin Tone Detection

Adjust the HSV ranges and luminance thresholds in `analyze_skin_tone` function in `ml-service/app.py`.

### Frontend Customization

- Components are located in `frontend/src/app/components/`
- Styles can be modified in respective `.css` files
- Service configuration in `frontend/src/app/services/`

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
