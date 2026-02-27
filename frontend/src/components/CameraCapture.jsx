import { useRef, useState, useEffect, useCallback } from 'react';
import { Camera, RotateCcw, ArrowLeft } from 'lucide-react';

export default function CameraCapture({ onCapture, onBack }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const [ready, setReady] = useState(false);
  const [facingMode, setFacingMode] = useState('user');
  const [cameraError, setCameraError] = useState(null);

  const startCamera = useCallback(async () => {
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });

      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play();
          setReady(true);
        };
      }
    } catch (err) {
      setCameraError('Could not access camera. Please check permissions.');
    }
  }, [facingMode]);

  useEffect(() => {
    startCamera();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }
    };
  }, [startCamera]);

  const handleCapture = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    onCapture(dataUrl);
  }, [onCapture]);

  const toggleCamera = useCallback(() => {
    setFacingMode((prev) => (prev === 'user' ? 'environment' : 'user'));
  }, []);

  if (cameraError) {
    return (
      <div className="card p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
          <Camera className="w-8 h-8 text-red-500" />
        </div>
        <h3 className="text-lg font-semibold mb-2">Camera Unavailable</h3>
        <p className="text-gray-600 dark:text-gray-400 mb-6">{cameraError}</p>
        <button onClick={onBack} className="btn-secondary">
          <ArrowLeft size={18} /> Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <button onClick={onBack} className="btn-ghost mb-2">
        <ArrowLeft size={18} /> Back
      </button>

      <div className="card overflow-hidden">
        <div className="relative aspect-video bg-black rounded-t-2xl overflow-hidden">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
            style={{ transform: facingMode === 'user' ? 'scaleX(-1)' : 'none' }}
          />

          {!ready && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
              <div className="animate-pulse-soft text-white text-sm">
                Starting camera...
              </div>
            </div>
          )}

          {/* Guide overlay */}
          {ready && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="w-52 h-72 sm:w-64 sm:h-80 border-2 border-white/40 rounded-[50%] relative">
                <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 bg-black/50 text-white text-xs px-3 py-1 rounded-full whitespace-nowrap backdrop-blur-sm">
                  Position your face here
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center justify-center gap-4 p-4">
          <button onClick={toggleCamera} className="btn-ghost" title="Switch camera">
            <RotateCcw size={18} />
            <span className="text-sm">Flip</span>
          </button>

          <button
            onClick={handleCapture}
            disabled={!ready}
            className="btn-primary text-lg px-10 py-3"
          >
            <Camera size={20} />
            Capture & Analyze
          </button>
        </div>
      </div>

      <canvas ref={canvasRef} className="hidden" />

      <p className="text-center text-xs text-gray-500 dark:text-gray-400">
        Ensure good lighting and a clear view of your face for best results.
      </p>
    </div>
  );
}
