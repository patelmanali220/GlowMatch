package com.glowmatch.service;

import com.glowmatch.exception.InvalidFileException;
import com.glowmatch.model.SkinAnalysisResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.Arrays;
import java.util.List;

@Slf4j
@Service
public class RecommendationService {

  private final MLServiceClient mlServiceClient;
  private static final List<String> ALLOWED_EXTENSIONS = Arrays.asList("jpg", "jpeg", "png");
  private static final long MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

  public RecommendationService(MLServiceClient mlServiceClient) {
    this.mlServiceClient = mlServiceClient;
  }

  public SkinAnalysisResponse analyzeImage(MultipartFile file) {
    log.info("Analyzing image: {}", file.getOriginalFilename());

    validateFile(file);

    return mlServiceClient.analyzeSkinTone(file);
  }

  private void validateFile(MultipartFile file) {
    if (file == null || file.isEmpty()) {
      throw new InvalidFileException("File is empty or null");
    }

    String originalFilename = file.getOriginalFilename();
    if (originalFilename == null || originalFilename.trim().isEmpty()) {
      throw new InvalidFileException("File name is invalid");
    }

    String extension = getFileExtension(originalFilename);
    if (!ALLOWED_EXTENSIONS.contains(extension.toLowerCase())) {
      throw new InvalidFileException(
          "Invalid file type. Allowed types: " + String.join(", ", ALLOWED_EXTENSIONS));
    }

    if (file.getSize() > MAX_FILE_SIZE) {
      throw new InvalidFileException("File size exceeds maximum limit of 5MB");
    }
  }

  private String getFileExtension(String filename) {
    int lastDotIndex = filename.lastIndexOf('.');
    if (lastDotIndex > 0 && lastDotIndex < filename.length() - 1) {
      return filename.substring(lastDotIndex + 1);
    }
    return "";
  }

  public boolean checkMLServiceHealth() {
    return mlServiceClient.isMLServiceHealthy();
  }
}
