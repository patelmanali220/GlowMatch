package com.glowmatch.controller;

import com.glowmatch.model.SkinAnalysisResponse;
import com.glowmatch.service.RecommendationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/v1/recommendations")
public class RecommendationController {

  private final RecommendationService recommendationService;

  public RecommendationController(RecommendationService recommendationService) {
    this.recommendationService = recommendationService;
  }

  @PostMapping("/analyze")
  public ResponseEntity<SkinAnalysisResponse> analyzeImage(
      @RequestParam("file") MultipartFile file) {
    try {
      log.info("✅ Received analyze request for file: {}", file.getOriginalFilename());
      log.info("📊 File size: {} bytes", file.getSize());
      
      SkinAnalysisResponse response = recommendationService.analyzeImage(file);
      
      log.info("✅ Analysis complete - Skin tone: {}", 
          response.getSkinAnalysis().getSkinToneCategory());
      
      return ResponseEntity.ok(response);
    } catch (Exception e) {
      log.error("❌ Error analyzing image: {}", e.getMessage(), e);
      throw e;
    }
  }

  @GetMapping("/health")
  public ResponseEntity<Map<String, Object>> healthCheck() {
    Map<String, Object> health = new HashMap<>();
    health.put("status", "UP");
    health.put("service", "GlowMatch Backend");

    boolean mlServiceHealthy = recommendationService.checkMLServiceHealth();
    health.put("mlService", mlServiceHealthy ? "UP" : "DOWN");

    HttpStatus status = mlServiceHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE;
    return ResponseEntity.status(status).body(health);
  }

  @GetMapping("/")
  public ResponseEntity<Map<String, String>> info() {
    Map<String, String> info = new HashMap<>();
    info.put("service", "GlowMatch Backend API");
    info.put("version", "1.0.0");
    info.put("description", "Skin tone analysis and beauty recommendations");
    return ResponseEntity.ok(info);
  }


  
}
