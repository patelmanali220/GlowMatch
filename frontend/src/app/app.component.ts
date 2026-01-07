import { Component } from '@angular/core';
import { AnalysisResponse } from './services/analysis.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'GlowMatch';
  analysisResult: AnalysisResponse | null = null;

  onAnalysisComplete(result: AnalysisResponse): void {
    this.analysisResult = result;
  }

  onReset(): void {
    this.analysisResult = null;
  }
}
