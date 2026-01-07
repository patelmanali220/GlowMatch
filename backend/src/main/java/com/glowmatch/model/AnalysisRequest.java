package com.glowmatch.model;

import jakarta.validation.constraints.NotNull;

public class AnalysisRequest {
    
    @NotNull(message = "Image data is required")
    private byte[] imageData;
    
    private String fileName;

    public byte[] getImageData() {
        return imageData;
    }

    public void setImageData(byte[] imageData) {
        this.imageData = imageData;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }
}
