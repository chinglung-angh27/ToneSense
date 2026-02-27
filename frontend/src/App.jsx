import { useState, useCallback } from 'react';
import { useDarkMode } from './hooks/useDarkMode';
import Header from './components/Header';
import Hero from './components/Hero';
import CameraCapture from './components/CameraCapture';
import ImageUpload from './components/ImageUpload';
import AnalysisLoader from './components/AnalysisLoader';
import ResultsPanel from './components/ResultsPanel';
import Footer from './components/Footer';
import ConsentModal from './components/ConsentModal';
import { analyzeImage, analyzeBase64 } from './utils/api';

export default function App() {
  const [dark, setDark] = useDarkMode();
  const [mode, setMode] = useState(null); // null | 'camera' | 'upload'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [showConsent, setShowConsent] = useState(false);
  const [pendingAction, setPendingAction] = useState(null);

  const handleStartCamera = useCallback(() => {
    setPendingAction('camera');
    setShowConsent(true);
  }, []);

  const handleStartUpload = useCallback(() => {
    setMode('upload');
    setError(null);
    setResults(null);
  }, []);

  const handleConsent = useCallback((accepted) => {
    setShowConsent(false);
    if (accepted && pendingAction === 'camera') {
      setMode('camera');
      setError(null);
      setResults(null);
    }
    setPendingAction(null);
  }, [pendingAction]);

  const handleCapture = useCallback(async (dataUrl) => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeBase64(dataUrl);
      setResults(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleUpload = useCallback(async (file) => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeImage(file);
      setResults(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleReset = useCallback(() => {
    setMode(null);
    setResults(null);
    setError(null);
    setLoading(false);
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Header dark={dark} setDark={setDark} onReset={handleReset} />

      <main className="flex-1">
        {!mode && !results && (
          <Hero onCamera={handleStartCamera} onUpload={handleStartUpload} />
        )}

        {mode === 'camera' && !results && !loading && (
          <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in">
            <CameraCapture onCapture={handleCapture} onBack={handleReset} />
          </div>
        )}

        {mode === 'upload' && !results && !loading && (
          <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in">
            <ImageUpload onUpload={handleUpload} onBack={handleReset} />
          </div>
        )}

        {loading && <AnalysisLoader />}

        {error && !loading && (
          <div className="max-w-lg mx-auto px-4 py-8 text-center animate-fade-in">
            <div className="card p-8">
              <div className="w-16 h-16 mx-auto mb-4 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Analysis Error</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">{error}</p>
              <button onClick={handleReset} className="btn-primary">
                Try Again
              </button>
            </div>
          </div>
        )}

        {results && !loading && (
          <ResultsPanel results={results} onReset={handleReset} />
        )}
      </main>

      <Footer />

      {showConsent && (
        <ConsentModal onAccept={() => handleConsent(true)} onDecline={() => handleConsent(false)} />
      )}
    </div>
  );
}
