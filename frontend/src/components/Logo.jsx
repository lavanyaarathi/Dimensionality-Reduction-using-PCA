import React from 'react';

const Logo = ({ size = 'md', showText = true, theme = 'cyber' }) => {
  const themes = {
    space: { primary: '#8b5cf6', secondary: '#ec4899', accent: '#06b6d4' },
    cyber: { primary: '#a855f7', secondary: '#ec4899' },
    matrix: { primary: '#10b981', secondary: '#22d3ee' },
    sunset: { primary: '#f97316', secondary: '#ef4444' },
    ocean: { primary: '#06b6d4', secondary: '#3b82f6' },
    neon: { primary: '#ec4899', secondary: '#a855f7' }
  };

  const currentTheme = themes[theme] || themes.space;
  
  const sizes = {
    sm: { container: 'w-10 h-10', svg: 'w-6 h-6', text: 'text-sm' },
    md: { container: 'w-14 h-14', svg: 'w-8 h-8', text: 'text-base' },
    lg: { container: 'w-20 h-20', svg: 'w-12 h-12', text: 'text-xl' }
  };

  return (
    <div className="flex items-center gap-3">
      <div 
        className={`${sizes[size].container} rounded-xl flex items-center justify-center shadow-lg relative`}
        style={{ 
          background: `linear-gradient(135deg, ${currentTheme.primary}, ${currentTheme.secondary})` 
        }}
      >
        {/* PCA Dimensionality Reduction Icon */}
        <svg className={sizes[size].svg} viewBox="0 0 100 100">
          {/* 3D Cube */}
          <g opacity="0.6">
            <line x1="20" y1="30" x2="40" y2="20" stroke="white" strokeWidth="2.5" />
            <line x1="40" y1="20" x2="60" y2="30" stroke="white" strokeWidth="2.5" />
            <line x1="60" y1="30" x2="40" y2="40" stroke="white" strokeWidth="2.5" />
            <line x1="40" y1="40" x2="20" y2="30" stroke="white" strokeWidth="2.5" />
            <line x1="20" y1="50" x2="20" y2="30" stroke="white" strokeWidth="2.5" />
            <line x1="60" y1="50" x2="60" y2="30" stroke="white" strokeWidth="2.5" />
            <line x1="40" y1="60" x2="40" y2="40" stroke="white" strokeWidth="2.5" />
          </g>
          
          {/* Arrow */}
          <line x1="45" y1="50" x2="55" y2="50" stroke="white" strokeWidth="2.5" />
          <polyline points="52,47 55,50 52,53" stroke="white" strokeWidth="2.5" fill="none" />
          
          {/* 2D Plane */}
          <rect x="65" y="45" width="20" height="15" fill="none" stroke="white" strokeWidth="2.5" rx="1" />
          <circle cx="70" cy="50" r="1.5" fill="white" />
          <circle cx="77" cy="52" r="1.5" fill="white" />
          <circle cx="80" cy="55" r="1.5" fill="white" />
        </svg>
      </div>
      
      {showText && (
        <div>
          <h1 className={`${sizes[size].text} font-bold text-white`}>🌌 PCA Tool</h1>
          <p className="text-xs" style={{ color: currentTheme.primary }}>
            PCA Dimensionality Reduction
          </p>
        </div>
      )}
    </div>
  );
};

export default Logo;