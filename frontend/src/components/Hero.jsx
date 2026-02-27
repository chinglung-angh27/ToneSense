import { Camera, Upload, Sparkles, Shield, Palette } from 'lucide-react';

export default function Hero({ onCamera, onUpload }) {
  return (
    <div className="relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-brand-50/50 to-transparent dark:from-brand-950/20 dark:to-transparent" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 text-sm font-medium mb-8 animate-fade-in">
          <Sparkles size={14} />
          AI-Powered Color Analysis
        </div>

        {/* Heading */}
        <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 animate-fade-in-up">
          Discover Your
          <br />
          <span className="text-gradient">Perfect Colors</span>
        </h1>

        <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-12 animate-fade-in-up animate-delay-100">
          Using advanced facial analysis, ToneSense identifies your skin undertone,
          depth, and contrast to reveal your ideal seasonal color palette.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16 animate-fade-in-up animate-delay-200">
          <button onClick={onCamera} className="btn-primary text-lg px-8 py-4">
            <Camera size={20} />
            Use Camera
          </button>
          <button onClick={onUpload} className="btn-secondary text-lg px-8 py-4">
            <Upload size={20} />
            Upload Photo
          </button>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto animate-fade-in-up animate-delay-300">
          <FeatureCard
            icon={<Palette size={24} />}
            title="12 Seasonal Palettes"
            text="Precise classification into Spring, Summer, Autumn, or Winter sub-seasons."
          />
          <FeatureCard
            icon={<Sparkles size={24} />}
            title="Style Recommendations"
            text="Clothing, jewelry, hair color, and makeup suggestions tailored to you."
          />
          <FeatureCard
            icon={<Shield size={24} />}
            title="Privacy First"
            text="Images processed on-the-fly. Nothing stored without your consent."
          />
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, text }) {
  return (
    <div className="card p-6 text-left">
      <div className="w-10 h-10 rounded-lg bg-brand-100 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 flex items-center justify-center mb-3">
        {icon}
      </div>
      <h3 className="font-semibold mb-1">{title}</h3>
      <p className="text-sm text-gray-500 dark:text-gray-400">{text}</p>
    </div>
  );
}
