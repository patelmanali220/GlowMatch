import { SkinDepthExtended, UndertoneExtended } from './skin-tone-extended.enum';

/**
 * Extended v2.0 API Response Models
 * Maintains backward compatibility with v1 while adding new extended fields
 */

export interface ExtendedSkinAnalysisResponse {
  success: boolean;
  message: string;
  version: string;
  skinAnalysis: ExtendedSkinAnalysis;
  recommendations: ExtendedRecommendations;
  analysisDetails: ExtendedAnalysisDetails;
}

export interface ExtendedSkinAnalysis {
  // Legacy fields (v1 backward compatibility)
  depth: string;
  undertone: string;
  skinToneCategory: string;
  hexColor: string;
  rgbColor: RGB;
  hsvColor: HSV;

  // New extended fields (v2)
  _NEW_?: ExtendedClassification;
}

export interface ExtendedClassification {
  extendedDepth: SkinDepthExtended;
  depthLevel: number;
  depthPercentile: string;
  extendedUndertone: UndertoneExtended;
  undertoneHueRange: [number, number];
  undertoneIntensity: number;
  skinToneConfidence: number;
  skinCharacteristics: SkinCharacteristics;
}

export interface SkinCharacteristics {
  hasOliveUndertones: boolean;
  isWarmDominant: boolean;
  undertoneBalance: string;
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

export interface ExtendedRecommendations {
  clothing: ClothingRecommendation;
  makeup: MakeupRecommendation;
  jewelry: JewelryRecommendation;

  // New seasonal recommendations
  _NEW_?: SeasonalRecommendations;
}

export interface SeasonalRecommendations {
  spring: string[];
  summer: string[];
  autumn: string[];
  winter: string[];
  skinConditionAdjustments: SkinConditionAdjustments;
}

export interface SkinConditionAdjustments {
  dry: string;
  oily: string;
  normal: string;
  sensitive: string;
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

export interface ExtendedAnalysisDetails {
  processingTime: string;
  faceDetectionMethod: string;
  skinPixelsDetected: number;
  hueDistribution: [number, number, number];
  saturationLevel: number;
  brightnessLevel: number;
  confidenceScore: number;
  recommendedRetryIfBelow: number;
}

/**
 * Helper function to check if response has extended fields
 */
export function isExtendedResponse(
  response: any
): response is ExtendedSkinAnalysisResponse {
  return (
    response?.version === '2.0' &&
    response?.skinAnalysis?._NEW_ !== undefined
  );
}

/**
 * Helper function to safely access extended fields with fallback
 */
export function getExtendedClassification(
  response: ExtendedSkinAnalysisResponse
): ExtendedClassification {
  return (
    response.skinAnalysis._NEW_ || {
      extendedDepth: response.skinAnalysis.depth as any,
      depthLevel: 3,
      depthPercentile: '55-71%',
      extendedUndertone: response.skinAnalysis.undertone as any,
      undertoneHueRange: [30, 60],
      undertoneIntensity: 0.5,
      skinToneConfidence: response.analysisDetails.confidenceScore,
      skinCharacteristics: {
        hasOliveUndertones: false,
        isWarmDominant: false,
        undertoneBalance: 'Balanced'
      }
    }
  );
}
