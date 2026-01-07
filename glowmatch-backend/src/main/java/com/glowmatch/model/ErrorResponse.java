package com.glowmatch.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ErrorResponse {
  private boolean success;
  private String message;
  private String error;
  private long timestamp;
}
