/**
 * ProfileDropdown Component
 * User profile dropdown with space-themed styling
 */

import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, LogOut, Settings, ChevronDown, Star, Sparkles } from 'lucide-react';
import authService from '../services/authService';

const ProfileDropdown = ({ theme = 'space' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();
  const username = authService.getUsername();

  const themes = {
    space: { primary: '#8b5cf6', secondary: '#ec4899', accent: '#06b6d4' },
    cyber: { primary: '#a855f7', secondary: '#ec4899' },
    matrix: { primary: '#10b981', secondary: '#22d3ee' },
    sunset: { primary: '#f97316', secondary: '#ef4444' },
    ocean: { primary: '#06b6d4', secondary: '#3b82f6' },
    neon: { primary: '#ec4899', secondary: '#a855f7' }
  };

  const currentTheme = themes[theme] || themes.space;

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    // Add CSS for animation
    const styleId = 'profile-dropdown-styles';
    if (!document.getElementById(styleId)) {
      const style = document.createElement('style');
      style.id = styleId;
      style.textContent = `
        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-10px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        .animate-slideDown {
          animation: slideDown 0.3s ease-out;
        }
      `;
      document.head.appendChild(style);
    }

    return () => {
      const style = document.getElementById(styleId);
      if (style) {
        style.remove();
      }
    };
  }, []);

  const handleLogout = async () => {
    try {
      await authService.logout();
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
      // Force logout even if API call fails
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      navigate('/login');
    }
  };

  const handleProfileSettings = () => {
    setIsOpen(false);
    // Create a simple profile settings modal
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center';
    modal.innerHTML = `
      <div class="bg-black/90 border border-purple-500/30 rounded-2xl p-8 max-w-md w-full mx-4 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-2xl"></div>
        <div class="relative z-10">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-white text-xl font-semibold">Profile Settings</h3>
              <p class="text-gray-400 text-sm">Manage your account</p>
            </div>
          </div>
          
          <div class="space-y-4">
            <div class="p-4 bg-black/40 border border-purple-500/30 rounded-xl">
              <label class="text-gray-300 text-sm block mb-2">Username</label>
              <input type="text" value="${username}" readonly class="w-full px-3 py-2 bg-black/60 border border-purple-500/50 rounded-lg text-white" />
            </div>
            
            <div class="p-4 bg-black/40 border border-purple-500/30 rounded-xl">
              <label class="text-gray-300 text-sm block mb-2">Email</label>
              <input type="email" value="${username}@pca-analytics.com" readonly class="w-full px-3 py-2 bg-black/60 border border-purple-500/50 rounded-lg text-white" />
            </div>
            
            <div class="p-4 bg-black/40 border border-purple-500/30 rounded-xl">
              <label class="text-gray-300 text-sm block mb-2">Role</label>
              <input type="text" value="Data Analyst" readonly class="w-full px-3 py-2 bg-black/60 border border-purple-500/50 rounded-lg text-white" />
            </div>
          </div>
          
          <div class="flex gap-3 mt-6">
            <button id="closeProfileModal" class="flex-1 px-4 py-2 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/50 rounded-lg transition-all duration-300">
              Close
            </button>
            <button id="saveProfileChanges" class="flex-1 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white rounded-lg transition-all duration-300">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add event listeners for buttons
    document.getElementById('closeProfileModal').addEventListener('click', () => {
      modal.remove();
    });
    
    document.getElementById('saveProfileChanges').addEventListener('click', () => {
      modal.remove();
    });
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 px-4 py-3 bg-black/60 border border-purple-500/30 rounded-2xl hover:border-purple-400/50 transition-all duration-300 group relative overflow-hidden"
        style={{ borderColor: isOpen ? currentTheme.primary : undefined }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-blue-500/5 group-hover:from-purple-500/10 group-hover:to-blue-500/10 transition-all duration-300" />
        
        <div className="relative z-10 flex items-center gap-3">
          <div 
            className="w-10 h-10 rounded-xl flex items-center justify-center relative overflow-hidden"
            style={{ 
              background: `linear-gradient(135deg, ${currentTheme.primary}, ${currentTheme.secondary})`
            }}
          >
            <User className="w-5 h-5 text-white" />
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse" />
          </div>
          
          <div className="text-left hidden sm:block">
            <p className="text-white text-sm font-medium">{username}</p>
          </div>
          
          <ChevronDown 
            className={`w-4 h-4 text-gray-400 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} 
          />
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-3 w-72 bg-black/90 border border-purple-500/30 rounded-2xl shadow-2xl overflow-hidden z-[9999] animate-slideDown backdrop-blur-xl">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-blue-500/10 pointer-events-none" />
          
          <div className="relative z-10 p-6 border-b border-purple-500/20">
            <div className="flex items-center gap-4">
              <div 
                className="w-12 h-12 rounded-xl flex items-center justify-center"
                style={{ 
                  background: `linear-gradient(135deg, ${currentTheme.primary}, ${currentTheme.secondary})`
                }}
              >
                <User className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-gray-300 text-xs mb-1">Signed in as</p>
                <p className="text-white font-semibold text-lg">{username}</p>
              </div>
            </div>
          </div>
          
          <div className="relative z-10 p-3">
            <button
              onClick={handleProfileSettings}
              className="w-full flex items-center gap-4 px-4 py-3 text-gray-300 hover:bg-purple-500/20 rounded-xl transition-all duration-300 text-left group"
            >
              <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center group-hover:bg-purple-500/30 transition-colors">
                <Settings className="w-4 h-4" />
              </div>
              <div>
                <span className="text-sm font-medium">Profile Settings</span>
                <p className="text-xs text-gray-500">Manage your account</p>
              </div>
              <Sparkles className="w-4 h-4 text-purple-400 ml-auto" />
            </button>
            
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-4 px-4 py-3 text-red-400 hover:bg-red-500/20 rounded-xl transition-all duration-300 text-left group mt-2"
            >
              <div className="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center group-hover:bg-red-500/30 transition-colors">
                <LogOut className="w-4 h-4" />
              </div>
              <div>
                <span className="text-sm font-medium">Logout</span>
                <p className="text-xs text-gray-500">Sign out of your account</p>
              </div>
              <Star className="w-4 h-4 text-red-400 ml-auto" />
            </button>
          </div>

          <div className="relative z-10 p-4 border-t border-purple-500/20 bg-black/40">
            <div className="flex items-center justify-center gap-2">
              <Star className="w-4 h-4 text-purple-400" />
              <p className="text-xs text-gray-400 text-center">
                PCA Analytics Tool v1.0
              </p>
              <Star className="w-4 h-4 text-blue-400" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileDropdown;