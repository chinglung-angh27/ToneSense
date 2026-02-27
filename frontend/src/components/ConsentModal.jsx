export default function ConsentModal({ onAccept, onDecline }) {
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 animate-fade-in">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onDecline} />

      {/* Modal */}
      <div className="relative card p-8 max-w-md w-full animate-scale-in">
        <div className="w-14 h-14 mx-auto mb-4 bg-brand-100 dark:bg-brand-900/30 rounded-full flex items-center justify-center">
          <svg className="w-7 h-7 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </div>

        <h3 className="text-xl font-display font-semibold text-center mb-2">
          Camera Access
        </h3>
        <p className="text-gray-600 dark:text-gray-400 text-center mb-6 text-sm leading-relaxed">
          ToneSense needs access to your camera for live face analysis.
          Your camera feed is <strong>processed locally</strong> and images are
          <strong> only sent for analysis when you capture</strong>.
          We do not store any images.
        </p>

        <div className="flex gap-3">
          <button onClick={onDecline} className="btn-secondary flex-1">
            Cancel
          </button>
          <button onClick={onAccept} className="btn-primary flex-1">
            Allow Camera
          </button>
        </div>
      </div>
    </div>
  );
}
