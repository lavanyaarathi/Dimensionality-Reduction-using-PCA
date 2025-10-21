import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Eye, EyeOff, UserPlus, Mail, Lock, User as UserIcon } from 'lucide-react';
import Logo from './Logo';
import authService from '../services/authService';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [theme] = useState('cyber'); // Match with login theme
  const navigate = useNavigate();

  const themes = {
    cyber: { primary: '#a855f7', secondary: '#ec4899', bg: 'from-slate-950 via-purple-950 to-slate-950' },
    // Add other themes as needed
  };

  const currentTheme = themes[theme];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    setError('');

    // Validation
    if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('All fields are required');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return;
    }

    setIsLoading(true);

    const result = await authService.register(formData.username, formData.email, formData.password);

    if (result.success) {
      // Auto-login after registration
      const loginResult = await authService.login(formData.username, formData.password);
      if (loginResult.success) {
        navigate('/upload');
      }
    } else {
      setError(result.message || 'Registration failed');
    }

    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleRegister();
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br ${currentTheme.bg} flex items-center justify-center p-4 relative overflow-hidden`}>
      
      {/* Background Grid */}
      <div className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: `linear-gradient(${currentTheme.primary} 1px, transparent 1px),
                           linear-gradient(90deg, ${currentTheme.primary} 1px, transparent 1px)`,
          backgroundSize: '50px 50px'
        }}
      />

      {/* Register Card */}
      <div className="w-full max-w-md relative z-10">
        <div className="relative">
          <div 
            className="absolute -inset-1 rounded-3xl blur-2xl animate-pulse"
            style={{ background: `linear-gradient(135deg, ${currentTheme.primary}, ${currentTheme.secondary})`, opacity: 0.3 }}
          />
          
          <div className="relative bg-slate-800/95 backdrop-blur-2xl rounded-3xl shadow-2xl border border-slate-700/50 p-8 md:p-10">
            
            {/* Header */}
            <div className="text-center mb-8">
              <div className="flex justify-center mb-4">
                <Logo size="md" theme={theme} />
              </div>
              
              <h2 className="text-2xl font-bold text-slate-100 mb-2">Create Account</h2>
              <p className="text-sm text-slate-400">Join the PCA Tool platform</p>
            </div>

            {/* Form */}
            <div className="space-y-4">
              {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-xl text-sm animate-shake">
                  {error}
                </div>
              )}

              {/* Username */}
              <div>
                <label className="text-xs text-slate-400 mb-1.5 block font-medium flex items-center gap-2">
                  <UserIcon size={14} />
                  Username
                </label>
                <input
                  type="text"
                  name="username"
                  placeholder="Choose a username"
                  value={formData.username}
                  onChange={handleChange}
                  onKeyPress={handleKeyPress}
                  className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl focus:outline-none transition-all duration-300 text-slate-100 placeholder-slate-500"
                  style={{
                    borderColor: formData.username ? currentTheme.primary : undefined,
                    boxShadow: formData.username ? `0 0 20px ${currentTheme.primary}30` : undefined
                  }}
                />
              </div>

              {/* Email */}
              <div>
                <label className="text-xs text-slate-400 mb-1.5 block font-medium flex items-center gap-2">
                  <Mail size={14} />
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  placeholder="your.email@example.com"
                  value={formData.email}
                  onChange={handleChange}
                  onKeyPress={handleKeyPress}
                  className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl focus:outline-none transition-all duration-300 text-slate-100 placeholder-slate-500"
                  style={{
                    borderColor: formData.email ? currentTheme.primary : undefined,
                    boxShadow: formData.email ? `0 0 20px ${currentTheme.primary}30` : undefined
                  }}
                />
              </div>

              {/* Password */}
              <div>
                <label className="text-xs text-slate-400 mb-1.5 block font-medium flex items-center gap-2">
                  <Lock size={14} />
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    placeholder="Create a strong password"
                    value={formData.password}
                    onChange={handleChange}
                    onKeyPress={handleKeyPress}
                    className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl focus:outline-none transition-all duration-300 text-slate-100 placeholder-slate-500 pr-11"
                    style={{
                      borderColor: formData.password ? currentTheme.primary : undefined,
                      boxShadow: formData.password ? `0 0 20px ${currentTheme.primary}30` : undefined
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white transition-colors"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
                {formData.password && (
                  <div className="mt-2">
                    <div className="flex gap-1">
                      {[...Array(4)].map((_, i) => (
                        <div
                          key={i}
                          className="h-1 flex-1 rounded-full transition-all"
                          style={{
                            background: formData.password.length > i * 3 ? currentTheme.primary : '#334155'
                          }}
                        />
                      ))}
                    </div>
                    <p className="text-xs text-slate-500 mt-1">
                      {formData.password.length < 6 ? 'Weak' : formData.password.length < 10 ? 'Medium' : 'Strong'} password
                    </p>
                  </div>
                )}
              </div>

              {/* Confirm Password */}
              <div>
                <label className="text-xs text-slate-400 mb-1.5 block font-medium flex items-center gap-2">
                  <Lock size={14} />
                  Confirm Password
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    name="confirmPassword"
                    placeholder="Re-enter your password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    onKeyPress={handleKeyPress}
                    className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl focus:outline-none transition-all duration-300 text-slate-100 placeholder-slate-500 pr-11"
                    style={{
                      borderColor: formData.confirmPassword && formData.password === formData.confirmPassword ? currentTheme.primary : formData.confirmPassword ? '#ef4444' : undefined,
                      boxShadow: formData.confirmPassword ? `0 0 20px ${formData.password === formData.confirmPassword ? currentTheme.primary : '#ef4444'}30` : undefined
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white transition-colors"
                  >
                    {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
                {formData.confirmPassword && (
                  <p className={`text-xs mt-1 ${formData.password === formData.confirmPassword ? 'text-green-400' : 'text-red-400'}`}>
                    {formData.password === formData.confirmPassword ? '✓ Passwords match' : '✗ Passwords do not match'}
                  </p>
                )}
              </div>

              {/* Register Button */}
              <button
                type="button"
                onClick={handleRegister}
                disabled={isLoading}
                className="w-full text-white font-semibold py-3.5 rounded-xl shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mt-6 relative overflow-hidden group"
                style={{
                  background: `linear-gradient(135deg, ${currentTheme.primary}, ${currentTheme.secondary})`,
                  boxShadow: `0 10px 30px ${currentTheme.primary}40`
                }}
              >
                <span className="relative z-10 flex items-center justify-center gap-2">
                  {isLoading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Creating Account...
                    </>
                  ) : (
                    <>
                      <UserPlus size={18} />
                      Create Account
                    </>
                  )}
                </span>
              </button>
            </div>

            {/* Login Link */}
            <div className="mt-6 text-center text-sm text-slate-400">
              Already have an account?{' '}
              <Link 
                to="/login" 
                className="font-semibold transition-colors"
                style={{ color: currentTheme.primary }}
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-8px); }
          75% { transform: translateX(8px); }
        }

        .animate-shake {
          animation: shake 0.3s ease-in-out;
        }
      `}</style>
    </div>
  );
};

export default RegisterPage;