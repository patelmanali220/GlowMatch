package com.glowmatch.model;

/**
 * Extended skin depth enumeration (6 levels)
 * 
 * Represents the brightness/darkness of skin from very light to very dark.
 * Used for classification based on V channel (brightness) in HSV color space.
 */
public enum SkinDepth {
  VERY_FAIR("Very Fair", 1, 210, "82-100%"),
  FAIR("Fair", 2, 180, "71-82%"),
  MEDIUM("Medium", 3, 140, "55-71%"),
  TAN("Tan", 4, 100, "39-55%"),
  DARK("Dark", 5, 60, "24-39%"),
  DEEP("Deep", 6, 0, "0-24%");

  private final String displayName;
  private final int level;
  private final int brightnessThreshold;
  private final String percentile;

  SkinDepth(String displayName, int level, int brightnessThreshold, String percentile) {
    this.displayName = displayName;
    this.level = level;
    this.brightnessThreshold = brightnessThreshold;
    this.percentile = percentile;
  }

  public String getDisplayName() {
    return displayName;
  }

  public int getLevel() {
    return level;
  }

  public int getBrightnessThreshold() {
    return brightnessThreshold;
  }

  public String getPercentile() {
    return percentile;
  }

  /**
   * Classify depth from brightness value (0-255)
   */
  public static SkinDepth fromBrightnessValue(double brightnessValue) {
    if (brightnessValue > 210)
      return VERY_FAIR;
    if (brightnessValue > 180)
      return FAIR;
    if (brightnessValue > 140)
      return MEDIUM;
    if (brightnessValue > 100)
      return TAN;
    if (brightnessValue > 60)
      return DARK;
    return DEEP;
  }

  @Override
  public String toString() {
    return displayName;
  }
}
