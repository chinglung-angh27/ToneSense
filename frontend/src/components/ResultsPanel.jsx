import { useRef, useState, useCallback } from 'react';
import { toPng } from 'html-to-image';
import {
  Download,
  RotateCcw,
  Palette,
  Shirt,
  Gem,
  Scissors,
  Sparkles,
  Eye,
  ChevronDown,
  ChevronUp,
  Info,
} from 'lucide-react';
import ColorSwatch from './ColorSwatch';
import ResultCard from './ResultCard';

export default function ResultsPanel({ results, onReset }) {
  const cardRef = useRef(null);
  const [downloading, setDownloading] = useState(false);
  const analysis = results.analysis;

  const handleDownload = useCallback(async () => {
    if (!cardRef.current) return;
    setDownloading(true);
    try {
      const dataUrl = await toPng(cardRef.current, {
        pixelRatio: 2,
        backgroundColor: '#ffffff',
      });
      const link = document.createElement('a');
      link.download = `tonesense-${analysis.season.toLowerCase().replace(/\s+/g, '-')}.png`;
      link.href = dataUrl;
      link.click();
    } catch (e) {
      console.error('Download failed:', e);
    } finally {
      setDownloading(false);
    }
  }, [analysis.season]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 animate-fade-in">
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <div>
          <h2 className="font-display text-3xl font-bold">Your Color Analysis</h2>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Based on AI facial color analysis
          </p>
        </div>
        <div className="flex gap-3">
          <button onClick={onReset} className="btn-secondary">
            <RotateCcw size={18} /> New Analysis
          </button>
          <button onClick={handleDownload} disabled={downloading} className="btn-primary">
            <Download size={18} /> {downloading ? 'Saving...' : 'Save Card'}
          </button>
        </div>
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column — Season & Preview */}
        <div className="lg:col-span-1 space-y-6">
          <SeasonCard analysis={analysis} preview={results.preview} />
          <SkinColorCard analysis={analysis} />
        </div>

        {/* Right column — Details */}
        <div className="lg:col-span-2 space-y-6">
          <UndertoneCard analysis={analysis} />
          <BestColorsCard analysis={analysis} />
          <AvoidColorsCard analysis={analysis} />
          <ClothingCard analysis={analysis} />
          <JewelryCard analysis={analysis} />
          <HairCard analysis={analysis} />
          <MakeupCard analysis={analysis} />
        </div>
      </div>

      {/* Hidden downloadable card */}
      <div className="fixed -left-[9999px] top-0">
        <div ref={cardRef}>
          <ResultCard analysis={analysis} />
        </div>
      </div>
    </div>
  );
}


/* ── Sub-components ─────────────────────────────────────────── */

function SeasonCard({ analysis, preview }) {
  return (
    <div className="card overflow-hidden animate-fade-in-up">
      {preview && (
        <div className="relative">
          <img
            src={preview}
            alt="Analysis preview"
            className="w-full aspect-[4/3] object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4">
            <div className="text-white/70 text-sm font-medium uppercase tracking-wider mb-1">
              Your Season
            </div>
            <div className="text-white font-display text-3xl font-bold">
              {analysis.season}
            </div>
          </div>
        </div>
      )}
      <div className="p-5">
        <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
          {analysis.season_description}
        </p>
      </div>
    </div>
  );
}

function SkinColorCard({ analysis }) {
  const { skin_color, depth, contrast } = analysis;
  return (
    <div className="card p-5 animate-fade-in-up animate-delay-100">
      <h3 className="section-title flex items-center gap-2">
        <Eye size={18} /> Skin Analysis
      </h3>
      <div className="space-y-4">
        {/* Color preview */}
        <div className="flex items-center gap-4">
          <div
            className="w-16 h-16 rounded-xl shadow-inner border border-black/10"
            style={{ backgroundColor: skin_color.hex }}
          />
          <div className="text-sm space-y-1">
            <div>
              <span className="text-gray-500 dark:text-gray-400">HEX:</span>{' '}
              <span className="font-mono font-medium">{skin_color.hex}</span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">RGB:</span>{' '}
              <span className="font-mono">{skin_color.rgb.join(', ')}</span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">LAB:</span>{' '}
              <span className="font-mono">{skin_color.lab.join(', ')}</span>
            </div>
          </div>
        </div>

        {/* Depth & Contrast */}
        <div className="grid grid-cols-2 gap-3">
          <MetricBadge label="Depth" value={depth.level} description={`L*: ${depth.l_value}`} />
          <MetricBadge label="Contrast" value={contrast.level} description={`Chroma: ${contrast.chroma}`} />
        </div>
      </div>
    </div>
  );
}

function UndertoneCard({ analysis }) {
  const { undertone } = analysis;
  const colorMap = {
    warm: 'from-amber-400 to-orange-500',
    cool: 'from-blue-400 to-indigo-500',
    neutral: 'from-gray-400 to-gray-600',
  };

  return (
    <div className="card p-6 animate-fade-in-up animate-delay-100">
      <h3 className="section-title flex items-center gap-2">
        <Info size={18} /> Undertone
      </h3>
      <div className="flex flex-col sm:flex-row items-start gap-5">
        <div className="flex-shrink-0">
          <div
            className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${colorMap[undertone.classification]} 
                         flex items-center justify-center text-white font-bold text-2xl shadow-lg`}
          >
            {undertone.classification[0].toUpperCase()}
          </div>
        </div>
        <div>
          <div className="text-2xl font-display font-bold capitalize mb-2">
            {undertone.classification}
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
            {undertone.explanation}
          </p>

          {/* Score bars */}
          <div className="mt-4 space-y-2">
            <ScoreBar label="Warm" value={undertone.warm_score} color="bg-amber-400" />
            <ScoreBar label="Cool" value={undertone.cool_score} color="bg-blue-400" />
          </div>
        </div>
      </div>
    </div>
  );
}

function BestColorsCard({ analysis }) {
  return (
    <div className="card p-6 animate-fade-in-up animate-delay-200">
      <h3 className="section-title flex items-center gap-2">
        <Palette size={18} /> Colors That Suit You
      </h3>
      <div className="flex flex-wrap gap-2">
        {analysis.best_colors.map((color) => (
          <ColorSwatch key={color} color={color} size="lg" />
        ))}
      </div>
    </div>
  );
}

function AvoidColorsCard({ analysis }) {
  return (
    <div className="card p-6 animate-fade-in-up animate-delay-300">
      <h3 className="section-title flex items-center gap-2">
        <Palette size={18} /> Colors to Avoid
      </h3>
      <div className="flex flex-wrap gap-2">
        {analysis.worst_colors.map((color) => (
          <ColorSwatch key={color} color={color} size="lg" showX />
        ))}
      </div>
    </div>
  );
}

function ClothingCard({ analysis }) {
  return (
    <CollapsibleCard
      icon={<Shirt size={18} />}
      title="Clothing Suggestions"
      defaultOpen
    >
      <ul className="space-y-2">
        {analysis.clothing_suggestions.map((item, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-400">
            <span className="w-1.5 h-1.5 rounded-full bg-brand-400 mt-1.5 flex-shrink-0" />
            {item}
          </li>
        ))}
      </ul>
    </CollapsibleCard>
  );
}

function JewelryCard({ analysis }) {
  return (
    <CollapsibleCard icon={<Gem size={18} />} title="Jewelry Tone">
      <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
        {analysis.jewelry_tone}
      </p>
    </CollapsibleCard>
  );
}

function HairCard({ analysis }) {
  return (
    <CollapsibleCard icon={<Scissors size={18} />} title="Hair Color Suggestions">
      <ul className="space-y-2">
        {analysis.hair_color_suggestions.map((item, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-400">
            <span className="w-1.5 h-1.5 rounded-full bg-brand-400 mt-1.5 flex-shrink-0" />
            {item}
          </li>
        ))}
      </ul>
    </CollapsibleCard>
  );
}

function MakeupCard({ analysis }) {
  const makeup = analysis.makeup_palette;
  return (
    <CollapsibleCard icon={<Sparkles size={18} />} title="Makeup Palette">
      <div className="space-y-3">
        {Object.entries(makeup).map(([key, value]) => (
          <div key={key}>
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500">
              {key}
            </span>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
              {value}
            </p>
          </div>
        ))}
      </div>
    </CollapsibleCard>
  );
}


/* ── Utility components ─────────────────────────────────────── */

function CollapsibleCard({ icon, title, children, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="card animate-fade-in-up">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-6 text-left"
      >
        <h3 className="text-lg font-display font-semibold flex items-center gap-2">
          {icon} {title}
        </h3>
        {open ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>
      {open && <div className="px-6 pb-6 -mt-2">{children}</div>}
    </div>
  );
}

function MetricBadge({ label, value, description }) {
  const bgMap = {
    light: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300',
    medium: 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300',
    deep: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300',
    low: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300',
    high: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300',
  };

  return (
    <div className="rounded-xl bg-gray-50 dark:bg-gray-800/50 p-3 text-center">
      <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
        {label}
      </div>
      <div
        className={`inline-block px-3 py-1 rounded-full text-sm font-semibold capitalize ${bgMap[value] || 'bg-gray-100 text-gray-700'}`}
      >
        {value}
      </div>
      {description && (
        <div className="text-xs text-gray-400 mt-1">{description}</div>
      )}
    </div>
  );
}

function ScoreBar({ label, value, color }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-gray-500 dark:text-gray-400 w-10">{label}</span>
      <div className="flex-1 h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color} transition-all duration-700`}
          style={{ width: `${Math.round(value * 100)}%` }}
        />
      </div>
      <span className="text-xs text-gray-500 dark:text-gray-400 w-10 text-right">
        {Math.round(value * 100)}%
      </span>
    </div>
  );
}
