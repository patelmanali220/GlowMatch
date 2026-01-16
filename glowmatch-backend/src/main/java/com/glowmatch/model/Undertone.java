package com.glowmatch.model;

/**
 * Extended undertone enumeration (5 types)
 * 
 * Represents the undertone/hue of skin tone based on hue distribution in HSV
 * color space.
 */
public enum Undertone {
  WARM("Warm", 0, 30, true, false),
  COOL("Cool", 330, 360, false, true),
  NEUTRAL("Neutral", 30, 60, false, false),
  OLIVE("Olive", 60, 90, false, true),
  GOLDEN("Golden", 90, 120, true, false);

  private final String displayName;
  private final int hueStart;
  private final int hueEnd;
  private final boolean isWarmSpectrum;
  private final boolean isCoolSpectrum;

  Undertone(String displayName, int hueStart, int hueEnd, boolean isWarmSpectrum, boolean isCoolSpectrum) {
    this.displayName = displayName;
    this.hueStart = hueStart;
    this.hueEnd = hueEnd;
    this.isWarmSpectrum = isWarmSpectrum;
    this.isCoolSpectrum = isCoolSpectrum;
  }

  public String getDisplayName() {
    return displayName;
  }

  public int getHueStart() {
    return hueStart;
  }

  public int getHueEnd() {
    return hueEnd;
  }

  public boolean isWarmSpectrum() {
    return isWarmSpectrum;
  }

  public boolean isCoolSpectrum() {
    return isCoolSpectrum;
  }

  /**
   * Classify undertone from hue value in degrees (0-360)
   */
  public static Undertone fromHueDegrees(double hueDegrees) {
    double hue = hueDegrees % 360;

    // Check ranges in order
    if (hue >= 0 && hue <= 30)
      return WARM;
    if (hue > 30 && hue <= 60)
      return NEUTRAL;
    if (hue > 60 && hue <= 90)
      return OLIVE;
    if (hue > 90 && hue <= 120)
      return GOLDEN;
    if (hue >= 330 && hue < 360)
      return COOL;

    return NEUTRAL; // Default fallback
  }

  @Override
  public String toString() {
    return displayName;
  }
}
