import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SkinAnalysisResponse } from '../../models/skin-analysis.model';

@Component({
  selector: 'app-analysis-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analysis-results.component.html',
  styleUrl: './analysis-results.component.css'
})
export class AnalysisResultsComponent implements OnInit {
  @Input() result: SkinAnalysisResponse | null = null;

  ngOnInit() {
    if (this.result) {
      console.log('🎨 Displaying recommendations:', this.result);
    }
  }

  get rgbString(): string {
    if (!this.result) return '';
    const { r, g, b } = this.result.skinAnalysis.rgbColor;
    return `rgb(${r}, ${g}, ${b})`;
  }
}
