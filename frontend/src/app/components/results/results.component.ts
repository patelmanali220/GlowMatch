import { Component, Input, Output, EventEmitter } from '@angular/core';
import { AnalysisResponse, ColorRecommendation } from '../../services/analysis.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent {
  @Input() result: AnalysisResponse | null = null;
  @Output() reset = new EventEmitter<void>();

  onReset(): void {
    this.reset.emit();
  }

  getRgbString(rgb: any): string {
    return `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
  }
}
