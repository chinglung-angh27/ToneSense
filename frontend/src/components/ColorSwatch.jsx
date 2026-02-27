import { useState } from 'react';

export default function ColorSwatch({ color, size = 'md', showX = false }) {
  const [copied, setCopied] = useState(false);

  const sizeClasses = {
    sm: 'w-8 h-8 rounded-md',
    md: 'w-10 h-10 rounded-lg',
    lg: 'w-12 h-12 rounded-xl',
  };

  const handleClick = () => {
    navigator.clipboard.writeText(color).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    });
  };

  return (
    <div className="relative group">
      <button
        onClick={handleClick}
        className={`${sizeClasses[size]} shadow-sm border border-black/5 dark:border-white/10 
                    transition-transform duration-200 hover:scale-110 cursor-pointer relative`}
        style={{ backgroundColor: color }}
        title={color}
      >
        {showX && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-full h-0.5 bg-red-500 rotate-45 absolute" />
            <div className="w-full h-0.5 bg-red-500 -rotate-45 absolute" />
          </div>
        )}
      </button>

      {/* Tooltip */}
      <div className="absolute -top-8 left-1/2 -translate-x-1/2 
                      bg-gray-900 text-white text-xs px-2 py-1 rounded 
                      opacity-0 group-hover:opacity-100 transition-opacity 
                      pointer-events-none whitespace-nowrap z-10">
        {copied ? 'Copied!' : color}
      </div>
    </div>
  );
}
