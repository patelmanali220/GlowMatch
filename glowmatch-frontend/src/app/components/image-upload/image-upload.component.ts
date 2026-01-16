import { Component, ElementRef, EventEmitter, OnDestroy, Output, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-image-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './image-upload.component.html',
  styleUrl: './image-upload.component.css'
})
export class ImageUploadComponent implements OnDestroy {
  @Output() fileSelected = new EventEmitter<File>();

  @ViewChild('videoElement') videoElement?: ElementRef<HTMLVideoElement>;
  @ViewChild('canvas') canvas?: ElementRef<HTMLCanvasElement>;
  
  isDragging = false;
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  errorMessage: string = '';
  activeMode: 'upload' | 'camera' = 'upload';
  isCapturing = false;
  isCameraActive = false;
  showCameraModal = false;
  private stream: MediaStream | null = null;

  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.validateAndEmitFile(file);
  }

  switchMode(mode: 'upload' | 'camera') {
    this.activeMode = mode;
    this.errorMessage = '';

    if (mode === 'camera') {
      this.openCameraModal();
    }
  }

  openCameraModal() {
    this.showCameraModal = true;
    this.errorMessage = '';
    setTimeout(() => this.startCamera(), 100);
  }

  closeCameraModal() {
    this.showCameraModal = false;
    this.stopCamera();
    this.activeMode = 'upload';
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

  async startCamera() {
    if (this.isCameraActive) return;

    this.errorMessage = '';
    this.isCapturing = true; // Show loading state

    if (!navigator.mediaDevices?.getUserMedia) {
      this.errorMessage = 'Camera not supported in this browser.';
      this.isCapturing = false;
      return;
    }

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'user',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        } 
      });

      const videoEl = this.videoElement?.nativeElement;
      if (!videoEl) {
        setTimeout(() => this.startCamera(), 100);
        return;
      }

      videoEl.srcObject = this.stream;
      videoEl.play();
      this.isCameraActive = true;
      this.isCapturing = false;
    } catch (error) {
      console.error('Unable to start camera', error);
      this.errorMessage = 'Unable to access camera. Please allow permissions and try again.';
      this.isCameraActive = false;
      this.isCapturing = false;
    }
  }

  capturePhoto() {
    if (!this.isCameraActive || this.isCapturing) return;

    this.errorMessage = '';
    this.isCapturing = true;

    try {
      const video = this.videoElement?.nativeElement;
      const canvas = this.canvas?.nativeElement;

      if (!video || !canvas) {
        throw new Error('Camera not ready');
      }

      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;

      const context = canvas.getContext('2d');
      if (!context) {
        throw new Error('Unable to get canvas context');
      }

      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      const dataUrl = canvas.toDataURL('image/png');
      fetch(dataUrl)
        .then(r => r.blob())
        .then(blob => {
          const file = new File([blob], `glowmatch-capture-${Date.now()}.png`, { type: 'image/png' });
          this.validateAndEmitFile(file);
          this.closeCameraModal();
          this.isCapturing = false;
        })
        .catch(error => {
          console.error('Capture failed', error);
          this.errorMessage = 'Failed to capture image. Please try again.';
          this.isCapturing = false;
        });
    } catch (error) {
      console.error('Unable to capture photo', error);
      this.errorMessage = 'Unable to capture photo. Please try again.';
      this.isCapturing = false;
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
      this.stream = null;
    }
    this.isCameraActive = false;
  }

  private validateAndEmitFile(file: File) {
    this.errorMessage = '';

    if (!file) {
      this.errorMessage = 'No image found. Please try again.';
      return;
    }
    
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

  ngOnDestroy() {
    this.stopCamera();
  }
}
