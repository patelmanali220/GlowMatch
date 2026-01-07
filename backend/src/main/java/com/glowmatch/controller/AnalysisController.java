package com.glowmatch.controller;

import com.glowmatch.model.AnalysisResponse;
import com.glowmatch.service.AnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AnalysisController {

    @Autowired
    private AnalysisService analysisService;

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> response = new HashMap<>();
        response.put("service", "GlowMatch Backend API");
        response.put("status", "healthy");
        response.put("version", "1.0.0");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/analyze")
    public ResponseEntity<?> analyzeImage(@RequestParam("file") MultipartFile file) {
        try {
            // Validate image
            if (!analysisService.validateImage(file)) {
                Map<String, String> error = new HashMap<>();
                error.put("error", "Invalid image file. Please upload a valid image (max 10MB)");
                return ResponseEntity.badRequest().body(error);
            }

            // Send to ML service for analysis
            AnalysisResponse result = analysisService.analyzeImage(file);
            return ResponseEntity.ok(result);

        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to analyze image: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}
