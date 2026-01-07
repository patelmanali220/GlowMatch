package com.glowmatch.service;

import com.glowmatch.exception.MLServiceException;
import com.glowmatch.model.SkinAnalysisResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Service
public class MLServiceClient {

  private final RestTemplate restTemplate;

  @Value("${ml.service.url}")
  private String mlServiceUrl;

  public MLServiceClient(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public SkinAnalysisResponse analyzeSkinTone(MultipartFile file) {
    try {
      String url = mlServiceUrl + "/analyze-skin";

      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.MULTIPART_FORM_DATA);

      MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
      body.add("file", new ByteArrayResource(file.getBytes()) {
        @Override
        public String getFilename() {
          return file.getOriginalFilename();
        }
      });

      HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

      log.info("Sending request to ML service: {}", url);
      ResponseEntity<SkinAnalysisResponse> response = restTemplate.exchange(
          url,
          HttpMethod.POST,
          requestEntity,
          SkinAnalysisResponse.class);

      log.info("Received response from ML service");
      return response.getBody();

    } catch (Exception e) {
      log.error("Error calling ML service: {}", e.getMessage());
      throw new MLServiceException("Failed to analyze skin tone: " + e.getMessage(), e);
    }
  }

  public boolean isMLServiceHealthy() {
    try {
      String healthUrl = mlServiceUrl + "/health";
      ResponseEntity<String> response = restTemplate.getForEntity(healthUrl, String.class);
      return response.getStatusCode() == HttpStatus.OK;
    } catch (Exception e) {
      log.error("ML service health check failed: {}", e.getMessage());
      return false;
    }
  }
}
