/**
 * Downloadable result card — rendered off-screen,
 * captured to PNG with html-to-image.
 */
export default function ResultCard({ analysis }) {
  return (
    <div
      style={{
        width: 600,
        padding: 40,
        fontFamily: "'Inter', system-ui, sans-serif",
        background: 'linear-gradient(135deg, #fdf4f8 0%, #ffffff 50%, #f0f4ff 100%)',
        color: '#1f2937',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 32 }}>
        <div
          style={{
            width: 40,
            height: 40,
            borderRadius: 12,
            background: 'linear-gradient(135deg, #eb4488, #da2268)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold',
            fontSize: 20,
          }}
        >
          T
        </div>
        <div>
          <div style={{ fontSize: 20, fontWeight: 700, letterSpacing: -0.5 }}>
            ToneSense
          </div>
          <div style={{ fontSize: 11, color: '#9ca3af' }}>
            AI Color Analysis
          </div>
        </div>
      </div>

      {/* Season */}
      <div
        style={{
          fontSize: 36,
          fontWeight: 700,
          marginBottom: 8,
          fontFamily: "'Playfair Display', Georgia, serif",
          letterSpacing: -0.5,
        }}
      >
        {analysis.season}
      </div>

      <div style={{ fontSize: 14, color: '#6b7280', marginBottom: 28, lineHeight: 1.6 }}>
        {analysis.season_description}
      </div>

      {/* Stats row */}
      <div
        style={{
          display: 'flex',
          gap: 12,
          marginBottom: 28,
        }}
      >
        <StatPill label="Undertone" value={analysis.undertone.classification} />
        <StatPill label="Depth" value={analysis.depth.level} />
        <StatPill label="Contrast" value={analysis.contrast.level} />
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 16px',
            background: '#f3f4f6',
            borderRadius: 12,
          }}
        >
          <div
            style={{
              width: 24,
              height: 24,
              borderRadius: 8,
              backgroundColor: analysis.skin_color.hex,
              border: '1px solid rgba(0,0,0,0.1)',
            }}
          />
          <span style={{ fontSize: 12, fontWeight: 600 }}>
            {analysis.skin_color.hex}
          </span>
        </div>
      </div>

      {/* Best colours */}
      <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 10, textTransform: 'uppercase', letterSpacing: 1, color: '#9ca3af' }}>
        Your Best Colors
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 24 }}>
        {analysis.best_colors.map((c) => (
          <div
            key={c}
            style={{
              width: 36,
              height: 36,
              borderRadius: 8,
              backgroundColor: c,
              border: '1px solid rgba(0,0,0,0.06)',
            }}
          />
        ))}
      </div>

      {/* Avoid */}
      <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 10, textTransform: 'uppercase', letterSpacing: 1, color: '#9ca3af' }}>
        Colors to Avoid
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 28 }}>
        {analysis.worst_colors.map((c) => (
          <div
            key={c}
            style={{
              width: 36,
              height: 36,
              borderRadius: 8,
              backgroundColor: c,
              border: '1px solid rgba(0,0,0,0.06)',
              position: 'relative',
            }}
          >
            <div
              style={{
                position: 'absolute',
                inset: 4,
                borderTop: '2px solid rgba(239,68,68,0.7)',
                transform: 'rotate(45deg)',
                transformOrigin: 'center',
              }}
            />
          </div>
        ))}
      </div>

      {/* Footer */}
      <div
        style={{
          borderTop: '1px solid #e5e7eb',
          paddingTop: 16,
          fontSize: 11,
          color: '#9ca3af',
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <span>tonesense.app</span>
        <span>{new Date().toLocaleDateString()}</span>
      </div>
    </div>
  );
}

function StatPill({ label, value }) {
  return (
    <div
      style={{
        padding: '8px 16px',
        background: '#f3f4f6',
        borderRadius: 12,
        textAlign: 'center',
      }}
    >
      <div style={{ fontSize: 10, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 2 }}>
        {label}
      </div>
      <div style={{ fontSize: 14, fontWeight: 600, textTransform: 'capitalize' }}>
        {value}
      </div>
    </div>
  );
}
