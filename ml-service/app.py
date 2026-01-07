from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import io
from typing import Dict, List

app = FastAPI(title="GlowMatch ML Service", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_skin_tone(image_array: np.ndarray) -> Dict:
    """
    Analyze skin tone from image using color analysis.
    Returns skin tone classification and RGB values.
    """
    # Convert to HSV color space for better skin detection
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create mask for skin pixels
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply mask to get skin pixels
    skin_pixels = cv2.bitwise_and(image_array, image_array, mask=skin_mask)
    
    # Calculate average skin color
    skin_pixels_flat = skin_pixels.reshape(-1, 3)
    skin_pixels_flat = skin_pixels_flat[skin_pixels_flat.sum(axis=1) > 0]
    
    if len(skin_pixels_flat) == 0:
        raise HTTPException(status_code=400, detail="No skin detected in image")
    
    avg_color = np.mean(skin_pixels_flat, axis=0)
    r, g, b = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
    
    # Classify skin tone based on luminance
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    
    if luminance < 100:
        tone = "Deep"
    elif luminance < 150:
        tone = "Dark"
    elif luminance < 180:
        tone = "Medium"
    elif luminance < 210:
        tone = "Light"
    else:
        tone = "Fair"
    
    return {
        "tone": tone,
        "rgb": {"r": r, "g": g, "b": b},
        "luminance": float(luminance)
    }

def get_color_recommendations(skin_tone: str, luminance: float) -> Dict[str, List[Dict]]:
    """
    Get color recommendations for clothing, makeup, and jewelry based on skin tone.
    """
    recommendations = {
        "Deep": {
            "clothing": [
                {"name": "Royal Blue", "hex": "#4169E1", "reason": "Creates stunning contrast"},
                {"name": "Emerald Green", "hex": "#50C878", "reason": "Complements warm undertones"},
                {"name": "Coral", "hex": "#FF7F50", "reason": "Brightens complexion"},
                {"name": "Gold Yellow", "hex": "#FFD700", "reason": "Enhances natural glow"}
            ],
            "makeup": [
                {"name": "Berry Lipstick", "hex": "#8B0A50", "reason": "Rich and vibrant"},
                {"name": "Bronze Eyeshadow", "hex": "#CD7F32", "reason": "Warm and flattering"},
                {"name": "Plum Blush", "hex": "#8E4585", "reason": "Natural flush"}
            ],
            "jewelry": [
                {"name": "Gold", "hex": "#FFD700", "reason": "Complements warm undertones"},
                {"name": "Rose Gold", "hex": "#B76E79", "reason": "Adds warmth"},
                {"name": "Copper", "hex": "#B87333", "reason": "Rich contrast"}
            ]
        },
        "Dark": {
            "clothing": [
                {"name": "Burgundy", "hex": "#800020", "reason": "Sophisticated and rich"},
                {"name": "Teal", "hex": "#008080", "reason": "Enhances complexion"},
                {"name": "Orange", "hex": "#FF8C00", "reason": "Vibrant contrast"},
                {"name": "Olive Green", "hex": "#808000", "reason": "Earthy complement"}
            ],
            "makeup": [
                {"name": "Mauve Lipstick", "hex": "#E0B0FF", "reason": "Soft and elegant"},
                {"name": "Copper Eyeshadow", "hex": "#B87333", "reason": "Warm glow"},
                {"name": "Terracotta Blush", "hex": "#E2725B", "reason": "Natural warmth"}
            ],
            "jewelry": [
                {"name": "Gold", "hex": "#FFD700", "reason": "Classic warmth"},
                {"name": "Bronze", "hex": "#CD7F32", "reason": "Natural complement"},
                {"name": "Amber", "hex": "#FFBF00", "reason": "Warm accent"}
            ]
        },
        "Medium": {
            "clothing": [
                {"name": "Navy Blue", "hex": "#000080", "reason": "Versatile and flattering"},
                {"name": "Sage Green", "hex": "#9DC183", "reason": "Fresh and balanced"},
                {"name": "Rose Pink", "hex": "#FF66CC", "reason": "Soft complement"},
                {"name": "Turquoise", "hex": "#40E0D0", "reason": "Bright and cheerful"}
            ],
            "makeup": [
                {"name": "Nude Lipstick", "hex": "#E3BC9A", "reason": "Natural enhancement"},
                {"name": "Taupe Eyeshadow", "hex": "#B38B6D", "reason": "Subtle definition"},
                {"name": "Peach Blush", "hex": "#FFE5B4", "reason": "Healthy glow"}
            ],
            "jewelry": [
                {"name": "Mixed Metals", "hex": "#C0C0C0", "reason": "Versatile choice"},
                {"name": "Rose Gold", "hex": "#B76E79", "reason": "Flattering warmth"},
                {"name": "White Gold", "hex": "#FFFFF0", "reason": "Clean elegance"}
            ]
        },
        "Light": {
            "clothing": [
                {"name": "Lavender", "hex": "#E6E6FA", "reason": "Soft and delicate"},
                {"name": "Mint Green", "hex": "#98FF98", "reason": "Fresh complement"},
                {"name": "Soft Pink", "hex": "#FFB6C1", "reason": "Enhances natural tone"},
                {"name": "Sky Blue", "hex": "#87CEEB", "reason": "Light and airy"}
            ],
            "makeup": [
                {"name": "Pink Lipstick", "hex": "#FFC0CB", "reason": "Fresh and youthful"},
                {"name": "Champagne Eyeshadow", "hex": "#F7E7CE", "reason": "Subtle shimmer"},
                {"name": "Rose Blush", "hex": "#FF007F", "reason": "Natural flush"}
            ],
            "jewelry": [
                {"name": "Silver", "hex": "#C0C0C0", "reason": "Cool elegance"},
                {"name": "White Gold", "hex": "#FFFFF0", "reason": "Delicate shine"},
                {"name": "Platinum", "hex": "#E5E4E2", "reason": "Sophisticated"}
            ]
        },
        "Fair": {
            "clothing": [
                {"name": "Powder Blue", "hex": "#B0E0E6", "reason": "Gentle complement"},
                {"name": "Soft Yellow", "hex": "#FFFFE0", "reason": "Brightens complexion"},
                {"name": "Blush Pink", "hex": "#FE828C", "reason": "Soft warmth"},
                {"name": "Lilac", "hex": "#C8A2C8", "reason": "Delicate beauty"}
            ],
            "makeup": [
                {"name": "Coral Lipstick", "hex": "#FF7F50", "reason": "Warm pop of color"},
                {"name": "Vanilla Eyeshadow", "hex": "#F3E5AB", "reason": "Soft glow"},
                {"name": "Peach Blush", "hex": "#FFDAB9", "reason": "Natural warmth"}
            ],
            "jewelry": [
                {"name": "Silver", "hex": "#C0C0C0", "reason": "Bright contrast"},
                {"name": "White Gold", "hex": "#FFFFF0", "reason": "Elegant complement"},
                {"name": "Pearl", "hex": "#EAE0C8", "reason": "Classic beauty"}
            ]
        }
    }
    
    return recommendations.get(skin_tone, recommendations["Medium"])

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "service": "GlowMatch ML Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image to detect skin tone and provide color recommendations.
    """
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Analyze skin tone
        skin_analysis = analyze_skin_tone(image_array)
        
        # Get color recommendations
        recommendations = get_color_recommendations(
            skin_analysis["tone"],
            skin_analysis["luminance"]
        )
        
        return {
            "success": True,
            "skinTone": skin_analysis,
            "recommendations": recommendations
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
