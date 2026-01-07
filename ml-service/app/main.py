"""
GlowMatch ML Service - FastAPI Application

Main entry point for the machine learning service that analyzes skin tone
and generates personalized color recommendations.

Features:
- Face detection using MediaPipe
- Skin tone extraction using OpenCV
- Color space analysis (HSV)
- Skin depth and undertone classification
- Personalized color palette generation
- RESTful API with automatic documentation

Author: GlowMatch Development Team
Version: 1.0.0
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
from PIL import Image
import numpy as np
from app.ml_service import SkinToneAnalyzer
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with metadata
app = FastAPI(
    title="GlowMatch ML Service",
    description="Skin Tone Analysis and Color Recommendation Engine",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc documentation
)

# Configure CORS (Cross-Origin Resource Sharing) to allow requests from frontend
# This allows the Angular frontend (http://localhost:4200) to communicate with
# this Python service (http://localhost:8001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins like ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Initialize the Skin Tone Analyzer on service startup
analyzer = SkinToneAnalyzer()
logger.info("SkinToneAnalyzer initialized successfully")

# Helper function to get hex color based on skin tone
def _get_hex_color(depth: str, undertone: str) -> str:
    """Get representative hex color for skin tone."""
    color_map = {
        "Fair-Warm": "#F5D7C3",
        "Fair-Cool": "#F5E6D3",
        "Fair-Neutral": "#F5DCC8",
        "Medium-Warm": "#D4A574",
        "Medium-Cool": "#C9A57B",
        "Medium-Neutral": "#CD9A68",
        "Dark-Warm": "#8D5524",
        "Dark-Cool": "#8B6342",
        "Dark-Neutral": "#704214"
    }
    return color_map.get(f"{depth}-{undertone}", "#D4A574")

def _get_rgb_color(depth: str, undertone: str) -> dict:
    """Get RGB values for skin tone."""
    hex_color = _get_hex_color(depth, undertone)
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return {"r": r, "g": g, "b": b}

# Helper function to get hex color based on skin tone
def _get_hex_color(depth: str, undertone: str) -> str:
    """Get representative hex color for skin tone."""
    color_map = {
        "Fair-Warm": "#F5D7C3",
        "Fair-Cool": "#F5E6D3",
        "Fair-Neutral": "#F5DCC8",
        "Medium-Warm": "#D4A574",
        "Medium-Cool": "#C9A57B",
        "Medium-Neutral": "#CD9A68",
        "Dark-Warm": "#8D5524",
        "Dark-Cool": "#8B6342",
        "Dark-Neutral": "#704214"
    }
    return color_map.get(f"{depth}-{undertone}", "#D4A574")

def _get_rgb_color(depth: str, undertone: str) -> dict:
    """Get RGB values for skin tone."""
    hex_color = _get_hex_color(depth, undertone)
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return {"r": r, "g": g, "b": b}


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message and service information.
    
    Provides basic information about the service and available endpoints.
    
    Returns:
        dict: Service information with available endpoints
        
    Example:
        GET http://localhost:8001/
        Response:
        {
            "message": "Welcome to GlowMatch ML Service",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "analyze_skin": "/analyze-skin (POST)",
                "docs": "/docs",
                "redoc": "/redoc"
            }
        }
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to GlowMatch ML Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze_skin": "/analyze-skin (POST)",
            "docs": "/docs - Swagger Interactive API Documentation",
            "redoc": "/redoc - ReDoc API Documentation"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify service is running and operational.
    
    This endpoint is called by the backend to verify the ML service is available.
    Can also be used for monitoring and load balancer health checks.
    
    Returns:
        dict: Service status and metadata
        
    Status Codes:
        200 OK: Service is healthy and ready
        
    Example:
        GET http://localhost:8001/health
        Response:
        {
            "status": "healthy",
            "service": "Skin Tone Analysis ML Service",
            "version": "1.0.0",
            "timestamp": "2024-01-02T10:30:00.123456"
        }
    """
    logger.info("Health check performed")
    return {
        "status": "healthy",
        "service": "Skin Tone Analysis ML Service",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/analyze-skin")
async def analyze_skin(file: UploadFile = File(...)):
    """
    Analyze skin tone from uploaded face image and generate color recommendations.
    
    This is the main endpoint that receives an image file from the backend,
    performs comprehensive skin tone analysis, and returns personalized
    color recommendations for clothing, makeup, and jewelry.
    
    Processing Pipeline:
    1. Validate file type (JPEG/PNG only)
    2. Check file size (max 5MB)
    3. Load image using PIL
    4. Convert to appropriate color space
    5. Detect face using MediaPipe
    6. Extract skin region from detected face
    7. Analyze skin tone (depth and undertone)
    8. Generate personalized color recommendations
    9. Return comprehensive JSON response
    
    Args:
        file (UploadFile): Image file from client
                          Supported: JPEG, PNG
                          Max size: 5MB
    
    Returns:
        dict: Analysis results with structure:
        {
            "status": "success",
            "filename": str,
            "timestamp": str,
            "skin_analysis": {
                "depth": "Fair|Medium|Dark",
                "undertone": "Warm|Cool|Neutral",
                "confidence": 0.0-1.0
            },
            "recommendations": {
                "clothing": {...},
                "makeup": {...},
                "jewelry": {...}
            },
            "analysis_details": {
                "hue": float,
                "saturation": float,
                "brightness": float,
                "skin_pixels_detected": int,
                "undertone_hue": float
            }
        }
    
    Status Codes:
        200 OK: Analysis successful
        400 Bad Request: Invalid file type or format
        413 Payload Too Large: File exceeds 5MB limit
        422 Unprocessable Entity: Image processing failed
        500 Internal Server Error: Unexpected server error
    
    Raises:
        HTTPException: 400 for invalid file types
        HTTPException: 413 for oversized files
        HTTPException: 422 for processing errors
        HTTPException: 500 for server errors
    
    Example:
        POST http://localhost:8001/analyze-skin
        Content-Type: multipart/form-data
        Body: file=<image.jpg>
        
        Response (200):
        {
            "status": "success",
            "filename": "photo.jpg",
            "timestamp": "2024-01-02T10:30:00",
            "skin_analysis": {
                "depth": "Medium",
                "undertone": "Warm",
                "confidence": 0.92
            },
            ...
        }
    """
    try:
        # Step 1: Validate file type
        # Only accept JPEG and PNG image formats
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            logger.warning(f"Invalid file type received: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Allowed types: JPEG, PNG"
            )
        
        # Step 2: Read file data into memory
        logger.info(f"Reading file: {file.filename}")
        image_data = await file.read()
        
        # Step 3: Validate file size (max 5MB = 5,242,880 bytes)
        max_file_size = 5 * 1024 * 1024  # 5MB in bytes
        if len(image_data) > max_file_size:
            logger.warning(f"File too large: {len(image_data)} bytes")
            raise HTTPException(
                status_code=413,
                detail=f"File size {len(image_data)} bytes exceeds 5MB limit"
            )
        
        # Step 4: Convert bytes to PIL Image
        # PIL is used for safe image format handling and conversion
        logger.info(f"Converting image to PIL format")
        image = Image.open(io.BytesIO(image_data))
        
        # Step 5: Handle different image modes
        # Convert RGBA, grayscale, etc. to RGB format that OpenCV expects
        if image.mode != 'RGB':
            logger.info(f"Converting image from {image.mode} to RGB")
            image = image.convert('RGB')
        
        # Step 6: Convert PIL Image to numpy array for OpenCV processing
        # Note: PIL uses RGB, but numpy/OpenCV typically work with arrays
        image_array = np.array(image)
        logger.info(f"Image loaded successfully: {image.size}, Mode: {image.mode}")
        
        # Step 7: Call ML service for analysis
        # This performs all the heavy lifting: face detection, skin analysis, etc.
        logger.info(f"Starting skin tone analysis for: {file.filename}")
        results = analyzer.analyze_skin_tone(image_array)
        
        # Step 8: Return success response
        # Include filename and timestamp for reference
        response = {
            "success": True,
            "message": "Skin tone analysis completed successfully",
            "skinAnalysis": {
                "depth": results["skin_analysis"]["depth"],
                "undertone": results["skin_analysis"]["undertone"],
                "skinToneCategory": f"{results['skin_analysis']['depth']}-{results['skin_analysis']['undertone']}",
                "hexColor": _get_hex_color(results["skin_analysis"]["depth"], results["skin_analysis"]["undertone"]),
                "rgbColor": _get_rgb_color(results["skin_analysis"]["depth"], results["skin_analysis"]["undertone"]),
                "hsvColor": {
                    "h": results["analysis_details"]["hue"],
                    "s": results["analysis_details"]["saturation"],
                    "v": results["analysis_details"]["brightness"]
                }
            },
            "recommendations": results["recommendations"],
            "analysisDetails": {
                "processingTime": "< 1s",
                "faceDetectionMethod": "MediaPipe Face Detection",
                "confidence": str(results["skin_analysis"]["confidence"])
            }
        }
        
        logger.info(f"Analysis complete for {file.filename}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    
    except Exception as e:
        # Catch unexpected errors and return 422 Unprocessable Entity
        logger.error(f"Error analyzing image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=422,
            detail=f"Error processing image: {str(e)}"
        )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 Not Found errors with custom JSON response."""
    logger.warning(f"404 Not Found: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "error": "NOT_FOUND",
            "message": f"Endpoint not found: {request.url.path}",
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    """Handle 500 Internal Server Error with custom JSON response."""
    logger.error(f"500 Server Error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.now().isoformat()
        }
    )


# Startup event - runs when server starts
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler - runs when FastAPI server starts.
    
    Can be used for:
    - Loading models
    - Initializing connections
    - Printing startup messages
    """
    logger.info("=" * 60)
    logger.info("🎨 GlowMatch ML Service Starting")
    logger.info("=" * 60)
    logger.info(f"Service Version: 1.0.0")
    logger.info(f"API Documentation: http://localhost:8001/docs")
    logger.info(f"Health Check: http://localhost:8001/health")
    logger.info("=" * 60)


# Shutdown event - runs when server shuts down
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler - runs when FastAPI server shuts down.
    
    Can be used for:
    - Cleanup operations
    - Closing connections
    - Logging shutdown message
    """
    logger.info("🛑 GlowMatch ML Service Shutting Down")


if __name__ == "__main__":
    # This block runs if the script is executed directly
    # Import uvicorn for running the server
    import uvicorn
    
    # Run the FastAPI application
    # host="0.0.0.0" means listen on all network interfaces
    # port=8001 is the port number
    # reload=True enables auto-reload on file changes (development only)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
