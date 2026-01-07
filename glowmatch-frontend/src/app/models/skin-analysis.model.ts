export interface SkinAnalysisResponse {
  success: boolean;
  message: string;
  skinAnalysis: SkinAnalysis;
  recommendations: Recommendations;
  analysisDetails: AnalysisDetails;
}

export interface SkinAnalysis {
  depth: string;
  undertone: string;
  skinToneCategory: string;
  hexColor: string;
  rgbColor: RGB;
  hsvColor: HSV;
}

export interface RGB {
  r: number;
  g: number;
  b: number;
}

export interface HSV {
  h: number;
  s: number;
  v: number;
}

export interface Recommendations {
  clothing: ClothingRecommendation;
  makeup: MakeupRecommendation;
  jewelry: JewelryRecommendation;
}

export interface ClothingRecommendation {
  best_colors: string[];
  description: string;
}

export interface MakeupRecommendation {
  foundation: MakeupCategory;
  lipstick: MakeupCategory;
  eyeshadow: MakeupCategory;
}

export interface MakeupCategory {
  shades: string[];
  hex_codes: string[];
}

export interface JewelryRecommendation {
  best_metals: string[];
  metal_hex: string[];
  stone_colors: string[];
  stone_hex: string[];
}

export interface AnalysisDetails {
  processingTime: string;
  faceDetectionMethod: string;
  confidence: string;
}

export interface ErrorResponse {
  success: boolean;
  message: string;
  error: string;
  timestamp: number;
}
