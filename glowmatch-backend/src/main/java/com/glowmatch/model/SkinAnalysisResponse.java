package com.glowmatch.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SkinAnalysisResponse {
  private boolean success;
  private String message;
  private SkinAnalysis skinAnalysis;
  private Recommendations recommendations;
  private AnalysisDetails analysisDetails;

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class SkinAnalysis {
    private String depth;
    private String undertone;
    private String skinToneCategory;
    private String hexColor;
    private RGB rgbColor;
    private HSV hsvColor;
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
  public static class Recommendations {
    private ClothingRecommendation clothing;
    private MakeupRecommendation makeup;
    private JewelryRecommendation jewelry;
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
  public static class AnalysisDetails {
    private String processingTime;
    private String faceDetectionMethod;
    private String confidence;
  }
}
