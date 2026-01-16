/**
 * Extended Skin Depth Enum
 * 6-level classification based on brightness
 */
export enum SkinDepthExtended {
  VERY_FAIR = "Very Fair",
  FAIR = "Fair",
  MEDIUM = "Medium",
  TAN = "Tan",
  DARK = "Dark",
  DEEP = "Deep"
}

/**
 * Extended Undertone Enum
 * 5-type classification based on hue
 */
export enum UndertoneExtended {
  WARM = "Warm",
  COOL = "Cool",
  NEUTRAL = "Neutral",
  OLIVE = "Olive",
  GOLDEN = "Golden"
}

/**
 * Get all depth values
 */
export const ALL_DEPTHS: SkinDepthExtended[] = [
  SkinDepthExtended.VERY_FAIR,
  SkinDepthExtended.FAIR,
  SkinDepthExtended.MEDIUM,
  SkinDepthExtended.TAN,
  SkinDepthExtended.DARK,
  SkinDepthExtended.DEEP
];

/**
 * Get all undertone values
 */
export const ALL_UNDERTONES: UndertoneExtended[] = [
  UndertoneExtended.WARM,
  UndertoneExtended.COOL,
  UndertoneExtended.NEUTRAL,
  UndertoneExtended.OLIVE,
  UndertoneExtended.GOLDEN
];

/**
 * Get depth level (1-6)
 */
export function getDepthLevel(depth: SkinDepthExtended): number {
  const levels: { [key in SkinDepthExtended]: number } = {
    [SkinDepthExtended.VERY_FAIR]: 1,
    [SkinDepthExtended.FAIR]: 2,
    [SkinDepthExtended.MEDIUM]: 3,
    [SkinDepthExtended.TAN]: 4,
    [SkinDepthExtended.DARK]: 5,
    [SkinDepthExtended.DEEP]: 6
  };
  return levels[depth];
}

/**
 * Get hue range for undertone
 */
export function getHueRange(undertone: UndertoneExtended): [number, number] {
  const ranges: { [key in UndertoneExtended]: [number, number] } = {
    [UndertoneExtended.WARM]: [0, 30],
    [UndertoneExtended.COOL]: [330, 360],
    [UndertoneExtended.NEUTRAL]: [30, 60],
    [UndertoneExtended.OLIVE]: [60, 90],
    [UndertoneExtended.GOLDEN]: [90, 120]
  };
  return ranges[undertone];
}

/**
 * Check if undertone is cool spectrum
 */
export function isCoolSpectrum(undertone: UndertoneExtended): boolean {
  return [UndertoneExtended.COOL, UndertoneExtended.OLIVE].includes(undertone);
}

/**
 * Check if undertone is warm spectrum
 */
export function isWarmSpectrum(undertone: UndertoneExtended): boolean {
  return [UndertoneExtended.WARM, UndertoneExtended.GOLDEN].includes(undertone);
}
