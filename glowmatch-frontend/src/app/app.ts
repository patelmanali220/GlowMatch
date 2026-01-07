import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageUploadComponent } from './components/image-upload/image-upload.component';
import { AnalysisResultsComponent } from './components/analysis-results/analysis-results.component';
import { RecommendationService } from './services/recommendation.service';
import { SkinAnalysisResponse } from './models/skin-analysis.model';

@Component({
  selector: 'app-root',
  imports: [CommonModule, ImageUploadComponent, AnalysisResultsComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
  providers: [RecommendationService]
})
export class App {
  title = 'GlowMatch';
  isAnalyzing = false;
  analysisResult: SkinAnalysisResponse | null = null;
  errorMessage: string = '';

  constructor(
    private recommendationService: RecommendationService,
    private cdr: ChangeDetectorRef
  ) {}

  onFileSelected(file: File) {
    console.log('📤 Starting analysis for file:', file.name, 'Size:', file.size, 'bytes');
    
    this.isAnalyzing = true;
    this.errorMessage = '';
    this.analysisResult = null;
    this.cdr.detectChanges();

    this.recommendationService.analyzeImage(file).subscribe({
      next: (result) => {
        console.log('✅ Analysis successful! Skin tone:', result.skinAnalysis.skinToneCategory);
        console.log('📊 Full response:', result);
        
        // Update state
        this.isAnalyzing = false;
        this.analysisResult = result;
        
        // Force change detection
        this.cdr.detectChanges();
        console.log('🎨 UI updated with results');
      },
      error: (error) => {
        console.error('❌ Analysis failed:', error);
        this.errorMessage = error.error?.message || 'Failed to analyze image. Please try again.';
        this.isAnalyzing = false;
        this.cdr.detectChanges();
      }
    });
  }

  startOver() {
    this.analysisResult = null;
    this.isAnalyzing = false;
    this.cdr.detectChanges();
    this.errorMessage = '';
  }
}

