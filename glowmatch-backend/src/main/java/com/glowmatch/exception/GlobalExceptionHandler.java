package com.glowmatch.exception;

import com.glowmatch.model.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

@RestControllerAdvice
public class GlobalExceptionHandler {

  @ExceptionHandler(InvalidFileException.class)
  public ResponseEntity<ErrorResponse> handleInvalidFile(InvalidFileException ex) {
    ErrorResponse error = new ErrorResponse(
        false,
        "Invalid file",
        ex.getMessage(),
        System.currentTimeMillis());
    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
  }

  @ExceptionHandler(MLServiceException.class)
  public ResponseEntity<ErrorResponse> handleMLServiceException(MLServiceException ex) {
    ErrorResponse error = new ErrorResponse(
        false,
        "ML Service Error",
        ex.getMessage(),
        System.currentTimeMillis());
    return ResponseEntity.status(HttpStatus.BAD_GATEWAY).body(error);
  }

  @ExceptionHandler(MaxUploadSizeExceededException.class)
  public ResponseEntity<ErrorResponse> handleMaxSizeException(MaxUploadSizeExceededException ex) {
    ErrorResponse error = new ErrorResponse(
        false,
        "File too large",
        "Maximum file size is 5MB",
        System.currentTimeMillis());
    return ResponseEntity.status(413).body(error);
  }

  @ExceptionHandler(Exception.class)
  public ResponseEntity<ErrorResponse> handleGeneralException(Exception ex) {
    ErrorResponse error = new ErrorResponse(
        false,
        "Server error",
        ex.getMessage(),
        System.currentTimeMillis());
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
  }
}
