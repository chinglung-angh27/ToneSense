export default function AnalysisLoader() {
  const steps = [
    'Detecting face...',
    'Sampling skin regions...',
    'Analyzing undertone...',
    'Calculating depth & contrast...',
    'Matching seasonal palette...',
  ];

  return (
    <div className="max-w-md mx-auto px-4 py-20 text-center animate-fade-in">
      {/* Animated circle */}
      <div className="relative w-32 h-32 mx-auto mb-8">
        <div className="absolute inset-0 rounded-full border-4 border-brand-200 dark:border-brand-900" />
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-brand-500 animate-spin" />
        <div className="absolute inset-4 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 dark:from-brand-900/40 dark:to-brand-950/40 flex items-center justify-center">
          <svg
            className="w-10 h-10 text-brand-500 animate-pulse-soft"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
            />
          </svg>
        </div>
      </div>

      <h2 className="font-display text-2xl font-semibold mb-6">
        Analyzing Your Colors
      </h2>

      <div className="space-y-2">
        {steps.map((step, i) => (
          <div
            key={step}
            className="text-sm text-gray-500 dark:text-gray-400 animate-fade-in"
            style={{ animationDelay: `${i * 400}ms`, animationFillMode: 'both' }}
          >
            {step}
          </div>
        ))}
      </div>
    </div>
  );
}
