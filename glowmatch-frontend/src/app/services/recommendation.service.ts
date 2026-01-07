import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SkinAnalysisResponse } from '../models/skin-analysis.model';

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {
  private apiUrl = 'http://localhost:8080/api/v1/recommendations';

  constructor(private http: HttpClient) { }

  analyzeImage(file: File): Observable<SkinAnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<SkinAnalysisResponse>(`${this.apiUrl}/analyze`, formData);
  }

  checkHealth(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/health`);
  }

  getApiInfo(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/`);
  }
}
