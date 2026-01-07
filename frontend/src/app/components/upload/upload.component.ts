import { Component, EventEmitter, Output } from '@angular/core';
import { AnalysisService, AnalysisResponse } from '../../services/analysis.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  @Output() analysisComplete = new EventEmitter<AnalysisResponse>();
  
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  isAnalyzing = false;
  error: string | null = null;

  constructor(private analysisService: AnalysisService) { }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.error = null;

      // Create preview
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        this.selectedFile = file;
        this.error = null;

        const reader = new FileReader();
        reader.onload = (e: any) => {
          this.previewUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.error = 'Please upload an image file';
      }
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
  }

  analyzeImage(): void {
    if (!this.selectedFile) {
      this.error = 'Please select an image first';
      return;
    }

    this.isAnalyzing = true;
    this.error = null;

    this.analysisService.analyzeImage(this.selectedFile).subscribe({
      next: (response) => {
        this.isAnalyzing = false;
        this.analysisComplete.emit(response);
      },
      error: (err) => {
        this.isAnalyzing = false;
        this.error = err.error?.error || 'Failed to analyze image. Please try again.';
      }
    });
  }

  reset(): void {
    this.selectedFile = null;
    this.previewUrl = null;
    this.error = null;
  }
}
