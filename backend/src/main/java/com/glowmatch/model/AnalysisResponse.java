package com.glowmatch.model;

import java.util.Map;

public class AnalysisResponse {
    
    private boolean success;
    private SkinTone skinTone;
    private Map<String, Object> recommendations;
    private String error;

    public static class SkinTone {
        private String tone;
        private RGB rgb;
        private double luminance;

        public String getTone() {
            return tone;
        }

        public void setTone(String tone) {
            this.tone = tone;
        }

        public RGB getRgb() {
            return rgb;
        }

        public void setRgb(RGB rgb) {
            this.rgb = rgb;
        }

        public double getLuminance() {
            return luminance;
        }

        public void setLuminance(double luminance) {
            this.luminance = luminance;
        }
    }

    public static class RGB {
        private int r;
        private int g;
        private int b;

        public int getR() {
            return r;
        }

        public void setR(int r) {
            this.r = r;
        }

        public int getG() {
            return g;
        }

        public void setG(int g) {
            this.g = g;
        }

        public int getB() {
            return b;
        }

        public void setB(int b) {
            this.b = b;
        }
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public SkinTone getSkinTone() {
        return skinTone;
    }

    public void setSkinTone(SkinTone skinTone) {
        this.skinTone = skinTone;
    }

    public Map<String, Object> getRecommendations() {
        return recommendations;
    }

    public void setRecommendations(Map<String, Object> recommendations) {
        this.recommendations = recommendations;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }
}
