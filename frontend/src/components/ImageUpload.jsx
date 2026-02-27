import { useState, useRef, useCallback } from 'react';
import { Upload, Image as ImageIcon, ArrowLeft, X } from 'lucide-react';

export default function ImageUpload({ onUpload, onBack }) {
  const inputRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFile = useCallback((f) => {
    if (!f) return;
    if (!f.type.startsWith('image/')) {
      alert('Please select a valid image file (JPEG, PNG, etc.)');
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      alert('Image must be less than 10 MB.');
      return;
    }

    setFile(f);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(f);
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      const f = e.dataTransfer.files[0];
      handleFile(f);
    },
    [handleFile]
  );

  const handleAnalyze = useCallback(() => {
    if (file) onUpload(file);
  }, [file, onUpload]);

  const clearFile = useCallback(() => {
    setFile(null);
    setPreview(null);
    if (inputRef.current) inputRef.current.value = '';
  }, []);

  return (
    <div className="space-y-4">
      <button onClick={onBack} className="btn-ghost mb-2">
        <ArrowLeft size={18} /> Back
      </button>

      <div className="card p-6">
        {!preview ? (
          <div
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            className={`
              border-2 border-dashed rounded-xl p-12 text-center cursor-pointer 
              transition-all duration-200
              ${dragOver
                ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/10'
                : 'border-gray-300 dark:border-gray-700 hover:border-brand-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
              }
            `}
          >
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <Upload className="w-7 h-7 text-gray-400" />
            </div>
            <h3 className="font-semibold mb-1">
              {dragOver ? 'Drop your photo here' : 'Upload a Photo'}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Drag & drop or click to browse. JPEG, PNG up to 10 MB.
            </p>
            <span className="btn-secondary text-sm px-4 py-2">
              <ImageIcon size={16} /> Choose File
            </span>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative rounded-xl overflow-hidden bg-black">
              <img
                src={preview}
                alt="Upload preview"
                className="w-full max-h-[500px] object-contain mx-auto"
              />
              <button
                onClick={clearFile}
                className="absolute top-3 right-3 w-8 h-8 bg-black/60 text-white rounded-full flex items-center justify-center hover:bg-black/80 transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            <div className="flex justify-center gap-3">
              <button onClick={clearFile} className="btn-secondary">
                Choose Different Photo
              </button>
              <button onClick={handleAnalyze} className="btn-primary">
                <Upload size={18} />
                Analyze Photo
              </button>
            </div>
          </div>
        )}

        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          onChange={(e) => handleFile(e.target.files[0])}
          className="hidden"
        />
      </div>

      <p className="text-center text-xs text-gray-500 dark:text-gray-400">
        For best results, use a well-lit photo showing your face clearly with minimal makeup.
      </p>
    </div>
  );
}
