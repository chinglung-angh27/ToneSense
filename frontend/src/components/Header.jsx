import { Sun, Moon, RotateCcw } from 'lucide-react';

export default function Header({ dark, setDark, onReset }) {
  return (
    <header className="sticky top-0 z-50 glass">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <button
            onClick={onReset}
            className="flex items-center gap-2.5 hover:opacity-80 transition-opacity"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-lg shadow-brand-500/20">
              <span className="text-white font-bold text-lg">T</span>
            </div>
            <span className="font-display font-semibold text-xl tracking-tight">
              Tone<span className="text-gradient">Sense</span>
            </span>
          </button>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={onReset}
              className="btn-ghost"
              title="Start over"
            >
              <RotateCcw size={18} />
              <span className="hidden sm:inline text-sm">New Analysis</span>
            </button>

            <button
              onClick={() => setDark(!dark)}
              className="btn-ghost"
              title={dark ? 'Light mode' : 'Dark mode'}
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
