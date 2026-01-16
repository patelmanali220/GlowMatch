package com.glowmatch.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Extended version 2.0 response maintaining backward compatibility
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExtendedSkinAnalysisResponse {
  private boolean success;
  private String message;
  private String version;
  private ExtendedSkinAnalysis skinAnalysis;
  private ExtendedRecommendations recommendations;
  private ExtendedAnalysisDetails analysisDetails;

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class ExtendedSkinAnalysis {
    // Legacy fields (backward compatibility)
    private String depth;
    private String undertone;
    private String skinToneCategory;
    private String hexColor;
    private RGB rgbColor;
    private HSV hsvColor;

    // New extended fields
    @JsonProperty("_NEW_")
    private ExtendedClassification extendedClassification;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class ExtendedClassification {
    private String extendedDepth;
    private int depthLevel;
    private String depthPercentile;
    private String extendedUndertone;
    private List<Integer> undertoneHueRange;
    private double undertoneIntensity;
    private double skinToneConfidence;
    private SkinCharacteristics skinCharacteristics;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class SkinCharacteristics {
    private boolean hasOliveUndertones;
    private boolean isWarmDominant;
    private String undertoneBalance;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class RGB {
    private int r;
    private int g;
    private int b;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class HSV {
    private double h;
    private double s;
    private double v;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class ExtendedRecommendations {
    private ClothingRecommendation clothing;
    private MakeupRecommendation makeup;
    private JewelryRecommendation jewelry;

    // New seasonal recommendations
    @JsonProperty("_NEW_")
    private SeasonalRecommendations seasonalRecommendations;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class SeasonalRecommendations {
    private List<String> spring;
    private List<String> summer;
    private List<String> autumn;
    private List<String> winter;
    private SkinConditionAdjustments skinConditionAdjustments;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class SkinConditionAdjustments {
    private String dry;
    private String oily;
    private String normal;
    private String sensitive;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class ClothingRecommendation {
    @JsonProperty("best_colors")
    private List<String> bestColors;
    private String description;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class MakeupRecommendation {
    private MakeupCategory foundation;
    private MakeupCategory lipstick;
    private MakeupCategory eyeshadow;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class MakeupCategory {
    private List<String> shades;
    @JsonProperty("hex_codes")
    private List<String> hexCodes;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class JewelryRecommendation {
    @JsonProperty("best_metals")
    private List<String> bestMetals;
    @JsonProperty("metal_hex")
    private List<String> metalHex;
    @JsonProperty("stone_colors")
    private List<String> stoneColors;
    @JsonProperty("stone_hex")
    private List<String> stoneHex;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class ExtendedAnalysisDetails {
    private String processingTime;
    private String faceDetectionMethod;
    private int skinPixelsDetected;
    private List<Object> hueDistribution;
    private double saturationLevel;
    private double brightnessLevel;
    private double confidenceScore;
    private double recommendedRetryIfBelow;
  }
}
