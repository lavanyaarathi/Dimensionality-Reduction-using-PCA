import React from 'react';
import Logo from './Logo';

const Footer = ({ theme = 'cyber' }) => {
  const themes = {
    space: '#8b5cf6',
    cyber: '#a855f7',
    matrix: '#10b981',
    sunset: '#f97316',
    ocean: '#06b6d4',
    neon: '#ec4899'
  };

  const currentTheme = themes[theme] || themes.space;

  return (
    <footer className="bg-black/80 border-t border-purple-500/30 py-8 mt-auto backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8 mb-6">
          
          {/* Logo & Description */}
          <div className="space-y-3">
            <Logo size="sm" theme={theme} />
            <p className="text-gray-300 text-sm leading-relaxed">
              🌌 A web-based tool for Principal Component Analysis on datasets and RGB images.
            </p>
          </div>

          {/* Project Info */}
          <div>
            <h3 className="text-slate-100 font-semibold mb-3 text-sm">
              Project Information
            </h3>
            <div className="space-y-2 text-xs text-slate-400">
              <p>Software Engineering (IT303)</p>
              <p>Course Project - Version 1.0</p>
              <p>NITK Surathkal, 2025</p>
            </div>
          </div>

          {/* Developers */}
          <div>
            <h3 className="text-slate-100 font-semibold mb-3 text-sm">
              Developed By
            </h3>
            <div className="space-y-2 text-xs text-slate-400 font-mono">
              {[
                'Siddhi Dhawale - 231IT072',
                'Lavanya Rathi - 231IT034',
                'Sarayu Narayanan - 231IT064'
              ].map((dev, i) => (
                <div key={i} className="flex items-center gap-2">
                  <div 
                    className="w-1.5 h-1.5 rounded-full"
                    style={{ background: currentTheme }}
                  />
                  <span>{dev}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Copyright Bar */}
        <div className="pt-6 border-t border-purple-500/30 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-gray-400">
          <p>
            © 2025 PCA Dimensionality Reduction Tool. All rights reserved.
          </p>
          <div className="flex gap-4">
            <span>Built with Python, Flask, React & scikit-learn</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;