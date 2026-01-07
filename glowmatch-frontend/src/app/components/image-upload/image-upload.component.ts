import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-image-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './image-upload.component.html',
  styleUrl: './image-upload.component.css'
})
export class ImageUploadComponent {
  @Output() fileSelected = new EventEmitter<File>();
  
  isDragging = false;
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  errorMessage: string = '';

  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.validateAndEmitFile(file);
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.validateAndEmitFile(files[0]);
    }
  }

  private validateAndEmitFile(file: File) {
    this.errorMessage = '';
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
      this.errorMessage = 'Please upload a JPG or PNG image';
      return;
    }

    // Validate file size (5MB max)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      this.errorMessage = 'File size must be less than 5MB';
      return;
    }

    this.selectedFile = file;
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e: any) => {
      this.previewUrl = e.target.result;
    };
    reader.readAsDataURL(file);

    this.fileSelected.emit(file);
  }

  clearSelection() {
    this.selectedFile = null;
    this.previewUrl = null;
    this.errorMessage = '';
  }
}
