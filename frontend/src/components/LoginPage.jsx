import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';
import authService from '../services/authService';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError('');
    setIsLoading(true);

    if (!username || !password) {
      setError('Please enter both username and password');
      setIsLoading(false);
      return;
    }

    try {
      const result = await authService.login(username, password);
      
      if (result.success) {
        navigate('/upload');
      } else {
        setError(result.message || 'Login failed');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    }
    
    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  return (
    <div className="min-h-screen w-full bg-black flex items-center justify-center p-4 relative overflow-hidden">
      
      {/* Space-themed Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-black via-purple-900/20 to-black">
        {/* Animated Stars */}
        <div className="absolute inset-0">
          {[...Array(100)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 3}s`
              }}
            />
          ))}
        </div>
        
        {/* Nebula Effect */}
        <div className="absolute top-0 left-0 w-full h-full opacity-30">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-pink-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
        </div>
      </div>

      {/* Moving Data Streams */}
      {[...Array(6)].map((_, i) => (
        <div
          key={`stream-${i}`}
          className="absolute h-0.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent"
          style={{
            width: '250px',
            top: `${15 + i * 14}%`,
            left: '-250px',
            animation: 'dataStream 8s ease-in-out infinite',
            animationDelay: `${i * 1.5}s`,
            opacity: 0.6
          }}
        />
      ))}

      {/* Scatter Plot with Connected Points */}
      <svg className="absolute inset-0 w-full h-full opacity-20 pointer-events-none">
        <line 
          x1="10%" y1="20%" x2="10%" y2="80%" 
          stroke="#22d3ee" 
          strokeWidth="1.5" 
          style={{ animation: 'pulse 2s ease-in-out infinite' }}
        />
        <line 
          x1="10%" y1="80%" x2="90%" y2="80%" 
          stroke="#22d3ee" 
          strokeWidth="1.5"
          style={{ animation: 'pulse 2s ease-in-out infinite', animationDelay: '0.5s' }}
        />
        
        {[...Array(25)].map((_, i) => {
          const x = 15 + (i % 8) * 9;
          const y = 30 + Math.sin(i * 0.6) * 18 + Math.random() * 8;
          const nextX = 15 + ((i + 1) % 8) * 9;
          const nextY = 30 + Math.sin((i + 1) * 0.6) * 18 + Math.random() * 8;
          
          return (
            <g key={i}>
              {i % 8 !== 7 && (
                <line
                  x1={`${x}%`}
                  y1={`${y}%`}
                  x2={`${nextX}%`}
                  y2={`${nextY}%`}
                  stroke="#22d3ee"
                  strokeWidth="0.5"
                  opacity="0.3"
                  style={{
                    animation: 'pulse 4s ease-in-out infinite',
                    animationDelay: `${i * 0.15}s`
                  }}
                />
              )}
              <circle
                cx={`${x}%`}
                cy={`${y}%`}
                r="3"
                fill="#22d3ee"
                opacity="0.7"
                style={{
                  animation: 'pointPulse 3s ease-in-out infinite',
                  animationDelay: `${i * 0.1}s`
                }}
              />
            </g>
          );
        })}
        
        {[65, 48, 32, 22, 16].map((height, i) => (
          <rect
            key={`bar-${i}`}
            x={`${73 + i * 3.5}%`}
            y={`${80 - height * 0.75}%`}
            width="2.5%"
            height={`${height * 0.75}%`}
            fill="#22d3ee"
            opacity="0.5"
            style={{
              animation: 'barGrow 2s ease-out',
              animationDelay: `${i * 0.2}s`,
              transformOrigin: 'bottom'
            }}
          />
        ))}
        
        <path
          d="M 73,65 Q 76,28 79,22 T 85,18 T 91,16"
          stroke="#22d3ee"
          strokeWidth="2"
          fill="none"
          opacity="0.4"
          strokeDasharray="6,6"
          style={{ animation: 'dashMove 2s linear infinite' }}
        />
      </svg>

      {/* Floating Eigenvalues */}
      {[
        { val: 'λ₁=0.87', x: 72, delay: 0 },
        { val: 'λ₂=0.65', x: 78, delay: 1 },
        { val: 'λ₃=0.42', x: 84, delay: 2 },
        { val: 'λ₄=0.28', x: 90, delay: 3 }
      ].map((item, i) => (
        <div
          key={`eigen-${i}`}
          className="absolute text-cyan-400 font-mono text-xs pointer-events-none"
          style={{
            left: `${item.x}%`,
            bottom: '8%',
            animation: 'floatUp 8s ease-in-out infinite',
            animationDelay: `${item.delay}s`,
            opacity: 0.4
          }}
        >
          {item.val}
        </div>
      ))}

      {/* Rotating Circles */}
      {[...Array(3)].map((_, i) => (
        <div
          key={`circle-${i}`}
          className="absolute rounded-full border-2 border-cyan-400"
          style={{
            width: `${150 + i * 100}px`,
            height: `${150 + i * 100}px`,
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            opacity: 0.05,
            animation: `rotate ${20 + i * 10}s linear infinite ${i % 2 === 0 ? 'normal' : 'reverse'}`
          }}
        />
      ))}

      {/* Login Card */}
      <div className="w-full max-w-md relative z-10">
        <div className="relative">
          <div className="absolute -inset-1 bg-cyan-500/20 rounded-3xl blur-2xl animate-pulse" />
          
          <div className="relative bg-slate-800/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-slate-700/50 p-10 md:p-12">
            
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-cyan-500/10 border border-cyan-500/30 rounded-xl mb-4 relative">
                <svg className="w-7 h-7 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <div className="absolute inset-0 rounded-xl border-2 border-cyan-400 animate-ping opacity-20" />
              </div>

              <h1 className="text-xl font-bold text-slate-100 mb-1 tracking-wide">
                SOFTWARE ENGINEERING (IT303)
              </h1>
              <p className="text-sm text-slate-400 font-semibold mb-6">
                COURSE PROJECT
              </p>
              
              <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 mb-8 italic leading-relaxed px-4">
                "DIMENSIONALITY REDUCTION USING PCA"
              </h2>
              
              <div className="inline-block bg-slate-900/50 border border-slate-700/50 rounded-xl p-4 mb-8">
                <div className="text-sm text-slate-300 space-y-2">
                  {['Siddhi Dhawale - 231IT072', 'Lavanya Rathi - 231IT034', 'Sarayu Narayanan - 231IT064'].map((name, i) => (
                    <div key={i} className="flex items-center justify-center gap-2 font-mono">
                      <div 
                        className="w-1.5 h-1.5 bg-cyan-400 rounded-full"
                        style={{ 
                          animation: 'pulse 2s ease-in-out infinite',
                          animationDelay: `${i * 0.3}s`
                        }}
                      />
                      <span className="text-slate-400">{name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-4">
              {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm backdrop-blur-sm flex items-center gap-2">
                  <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse" />
                  {error}
                </div>
              )}

              <div>
                <label className="text-xs text-slate-400 mb-1.5 block font-medium">Username</label>
                <input
                  type="text"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-lg focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30 transition-all duration-200 text-slate-100 placeholder-slate-500"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 mb-1.5 block font-medium">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-lg focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30 transition-all duration-200 text-slate-100 placeholder-slate-500 pr-11"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-cyan-400 transition-colors"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <button
                type="button"
                onClick={handleLogin}
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-semibold py-3 rounded-lg shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mt-6 relative overflow-hidden group"
              >
                <span className="relative z-10 flex items-center justify-center gap-2">
                  {isLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Authenticating...
                    </>
                  ) : (
                    'Login'
                  )}
                </span>
                <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/10 to-transparent" />
              </button>

              <div className="mt-6 text-center text-sm text-slate-400">
                Don't have an account?{' '}
                <a 
                  href="/register" 
                  className="text-cyan-400 hover:text-cyan-300 font-semibold transition-colors hover:underline"
                >
                  Create Account
                </a>
              </div>
            </div>

            <div className="mt-6 flex items-center justify-center gap-2">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="w-1.5 h-1.5 bg-cyan-500 rounded-full"
                  style={{
                    animation: 'pulse 2s ease-in-out infinite',
                    animationDelay: `${i * 0.3}s`,
                    opacity: 0.3 + (i * 0.2)
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes gridMove {
          0% { transform: translate(0, 0); }
          100% { transform: translate(50px, 50px); }
        }

        @keyframes dataStream {
          0% { left: -250px; opacity: 0; }
          10% { opacity: 0.6; }
          90% { opacity: 0.6; }
          100% { left: 110%; opacity: 0; }
        }

        @keyframes pointPulse {
          0%, 100% { opacity: 0.7; }
          50% { opacity: 1; }
        }

        @keyframes barGrow {
          0% { transform: scaleY(0); }
          60% { transform: scaleY(1.1); }
          100% { transform: scaleY(1); }
        }

        @keyframes dashMove {
          to { stroke-dashoffset: -12; }
        }

        @keyframes floatUp {
          0% { transform: translateY(0); opacity: 0; }
          10% { opacity: 0.4; }
          90% { opacity: 0.4; }
          100% { transform: translateY(-120px); opacity: 0; }
        }

        @keyframes rotate {
          from { transform: translate(-50%, -50%) rotate(0deg); }
          to { transform: translate(-50%, -50%) rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default LoginPage;