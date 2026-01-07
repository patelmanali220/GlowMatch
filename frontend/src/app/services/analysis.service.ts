import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RGB {
  r: number;
  g: number;
  b: number;
}

export interface SkinTone {
  tone: string;
  rgb: RGB;
  luminance: number;
}

export interface ColorRecommendation {
  name: string;
  hex: string;
  reason: string;
}

export interface Recommendations {
  clothing: ColorRecommendation[];
  makeup: ColorRecommendation[];
  jewelry: ColorRecommendation[];
}

export interface AnalysisResponse {
  success: boolean;
  skinTone: SkinTone;
  recommendations: Recommendations;
}

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {
  private apiUrl = 'http://localhost:8080/api';

  constructor(private http: HttpClient) { }

  analyzeImage(file: File): Observable<AnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/analyze`, formData);
  }

  healthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }
}
