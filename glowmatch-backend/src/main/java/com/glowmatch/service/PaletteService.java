package com.glowmatch.service;

import com.glowmatch.model.*;
import org.springframework.stereotype.Service;
import java.util.*;

/**
 * Service for dynamic palette resolution and color recommendation generation
 * 
 * Resolves color palettes based on extended skin tone classification
 * (6 depths × 5 undertones = 30 combinations)
 */
@Service
public class PaletteService {

  /**
   * Get palette configuration for depth + undertone combination
   */
  public PaletteConfig getPalette(String depth, String undertone) {
    String key = depth + "-" + undertone;

    // In production, load from database or JSON config
    // This is a simplified example showing the structure
    return buildPaletteConfig(key);
  }

  /**
   * Generate extended recommendations for a skin tone
   */
  public ExtendedSkinAnalysisResponse.ExtendedRecommendations generateExtendedRecommendations(
      String depth,
      String undertone) {

    PaletteConfig palette = getPalette(depth, undertone);

    ExtendedSkinAnalysisResponse.ExtendedRecommendations recommendations = new ExtendedSkinAnalysisResponse.ExtendedRecommendations();

    // Basic recommendations
    recommendations.setClothing(new ExtendedSkinAnalysisResponse.ClothingRecommendation(
        palette.clothingColors,
        String.format("Recommended clothing colors for %s skin with %s undertone", depth, undertone)));

    recommendations.setMakeup(new ExtendedSkinAnalysisResponse.MakeupRecommendation(
        new ExtendedSkinAnalysisResponse.MakeupCategory(
            convertHexToNames(palette.makeupFoundation),
            palette.makeupFoundation),
        new ExtendedSkinAnalysisResponse.MakeupCategory(
            convertHexToNames(palette.makeupLipstick),
            palette.makeupLipstick),
        new ExtendedSkinAnalysisResponse.MakeupCategory(
            convertHexToNames(palette.makeupEyeshadow),
            palette.makeupEyeshadow)));

    recommendations.setJewelry(new ExtendedSkinAnalysisResponse.JewelryRecommendation(
        palette.jewelryMetalNames,
        palette.jewelryMetals,
        palette.jewelryStoneNames,
        palette.jewelryStones));

    // New seasonal recommendations
    ExtendedSkinAnalysisResponse.SeasonalRecommendations seasonal = new ExtendedSkinAnalysisResponse.SeasonalRecommendations();

    seasonal.setSpring(generateSeasonalPalette(palette, "spring"));
    seasonal.setSummer(generateSeasonalPalette(palette, "summer"));
    seasonal.setAutumn(generateSeasonalPalette(palette, "autumn"));
    seasonal.setWinter(generateSeasonalPalette(palette, "winter"));

    seasonal.setSkinConditionAdjustments(new ExtendedSkinAnalysisResponse.SkinConditionAdjustments(
        "Use hydrating makeup with luminous finish for dry skin",
        "Choose matte foundation for oily skin",
        "Any well-matched shade works",
        "Use hypoallergenic, fragrance-free formulas"));

    recommendations.setSeasonalRecommendations(seasonal);

    return recommendations;
  }

  /**
   * Map extended classification to legacy 3x3 system for backward compatibility
   */
  public LegacyClassification mapToLegacy(String extendedDepth, String extendedUndertone) {
    String legacyDepth = mapDepthToLegacy(extendedDepth);
    String legacyUndertone = mapUndertoneToLegacy(extendedUndertone);

    return new LegacyClassification(legacyDepth, legacyUndertone);
  }

  private String mapDepthToLegacy(String extendedDepth) {
    switch (extendedDepth) {
      case "Very Fair":
      case "Fair":
        return "Fair";
      case "Medium":
      case "Tan":
        return "Medium";
      case "Dark":
      case "Deep":
        return "Dark";
      default:
        return "Medium";
    }
  }

  private String mapUndertoneToLegacy(String extendedUndertone) {
    switch (extendedUndertone) {
      case "Warm":
      case "Golden":
        return "Warm";
      case "Cool":
      case "Olive":
        return "Cool";
      case "Neutral":
      default:
        return "Neutral";
    }
  }

  private List<String> convertHexToNames(List<String> hexColors) {
    List<String> names = new ArrayList<>();
    for (String hex : hexColors) {
      names.add(getColorName(hex));
    }
    return names;
  }

  private String getColorName(String hexColor) {
    // Map hex to color names (simplified)
    Map<String, String> colorMap = new HashMap<>();
    colorMap.put("#FFD700", "Gold");
    colorMap.put("#FFA500", "Orange");
    colorMap.put("#FF8C00", "Dark Orange");
    colorMap.put("#FF6347", "Tomato");
    colorMap.put("#DC143C", "Crimson");
    colorMap.put("#00CED1", "Turquoise");
    colorMap.put("#C0C0C0", "Silver");
    colorMap.put("#E8E8E8", "Platinum");
    // Add more mappings as needed
    return colorMap.getOrDefault(hexColor, "Color " + hexColor);
  }

  private List<String> generateSeasonalPalette(PaletteConfig palette, String season) {
    // Generate season-specific colors based on undertone and depth
    List<String> seasonal = new ArrayList<>(palette.clothingColors);

    // Adjust brightness/saturation based on season
    switch (season) {
      case "spring":
        // Pastels and light colors
        return Arrays.asList("#FFB6C1", "#98FB98", "#87CEEB", "#FFE4B5");
      case "summer":
        // Bright, cool colors
        return Arrays.asList("#00CED1", "#87CEEB", "#00FA9A", "#20B2AA");
      case "autumn":
        // Warm, earthy colors
        return Arrays.asList("#8B4513", "#CD853F", "#FFD700", "#FF8C00");
      case "winter":
        // Deep, cool colors
        return Arrays.asList("#4B0082", "#00008B", "#C0C0C0", "#FFFFFF");
      default:
        return seasonal;
    }
  }

  private PaletteConfig buildPaletteConfig(String key) {
    // In production, this would load from database or JSON config file
    // Example structure
    return new PaletteConfig(
        Arrays.asList("#FFB347", "#FFA500", "#FF8C00", "#FF6347", "#DC143C", "#CD853F"),
        Arrays.asList("#F5DEB3", "#FFE4B5", "#FFDAB9"),
        Arrays.asList("#FF7F50", "#FF6347", "#E75480"),
        Arrays.asList("#FFD700", "#FFA500", "#FF8C00"),
        Arrays.asList("Gold", "Rose Gold"),
        Arrays.asList("#FFD700", "#B76E79"),
        Arrays.asList("Amber", "Topaz"),
        Arrays.asList("#FF8C00", "#DAA520"));
  }

  /**
   * Inner class for palette configuration
   */
  public static class PaletteConfig {
    public List<String> clothingColors;
    public List<String> makeupFoundation;
    public List<String> makeupLipstick;
    public List<String> makeupEyeshadow;
    public List<String> jewelryMetalNames;
    public List<String> jewelryMetals;
    public List<String> jewelryStoneNames;
    public List<String> jewelryStones;

    public PaletteConfig(
        List<String> clothingColors,
        List<String> makeupFoundation,
        List<String> makeupLipstick,
        List<String> makeupEyeshadow,
        List<String> jewelryMetalNames,
        List<String> jewelryMetals,
        List<String> jewelryStoneNames,
        List<String> jewelryStones) {
      this.clothingColors = clothingColors;
      this.makeupFoundation = makeupFoundation;
      this.makeupLipstick = makeupLipstick;
      this.makeupEyeshadow = makeupEyeshadow;
      this.jewelryMetalNames = jewelryMetalNames;
      this.jewelryMetals = jewelryMetals;
      this.jewelryStoneNames = jewelryStoneNames;
      this.jewelryStones = jewelryStones;
    }
  }

  /**
   * Legacy classification for backward compatibility
   */
  public static class LegacyClassification {
    public String depth;
    public String undertone;

    public LegacyClassification(String depth, String undertone) {
      this.depth = depth;
      this.undertone = undertone;
    }
  }
}
