import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Menu, X, Bot, LogIn, UserPlus, User, LogOut, Download } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LoginModal from './auth/LoginModal';
import SignupModal from './auth/SignupModal';
import DownloadDropdown from './DownloadDropdown';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showDownloadMenu, setShowDownloadMenu] = useState(false);
  const location = useLocation();
  const { currentUser, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { name: 'Home', path: '/', section: 'home' },
    { name: 'Features', path: '/features', section: 'features' },
    { name: 'Pricing', path: '/pricing', section: 'pricing' },
    { name: 'About', path: '/about', section: 'about' },
  ];

  const scrollToSection = (sectionId: string) => {
    if (location.pathname !== '/') {
      // Navigate to home page first, then scroll
      window.location.href = `/#${sectionId}`;
      return;
    }
    
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsOpen(false);
  };

  const handleNavigation = (item: typeof navItems[0]) => {
    if (item.path === '/') {
      if (location.pathname !== '/') {
        window.location.href = '/';
      } else {
        scrollToSection('home');
      }
    } else if (location.pathname === '/' && item.section) {
      scrollToSection(item.section);
    } else {
      window.location.href = item.path;
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      setShowUserMenu(false);
    } catch (error) {
      console.error('Failed to log out');
    }
  };

  const switchToSignup = () => {
    setShowLoginModal(false);
    setShowSignupModal(true);
  };

  const switchToLogin = () => {
    setShowSignupModal(false);
    setShowLoginModal(true);
  };

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className={`fixed w-full z-50 transition-all duration-300 ${
          scrolled 
            ? 'bg-white/95 backdrop-blur-md shadow-lg border-b border-gray-200' 
            : 'bg-transparent'
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-2 cursor-pointer"
              onClick={() => handleNavigation({ name: 'Home', path: '/', section: 'home' })}
            >
              <Bot className="h-8 w-8 text-purple-600" />
              <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                Axiom
              </span>
            </motion.div>

            {/* Centered Desktop Menu */}
            <div className="hidden lg:flex items-center justify-center flex-1">
              <div className="flex items-center space-x-8">
                {navItems.map((item) => (
                  <motion.button
                    key={item.name}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleNavigation(item)}
                    className={`text-sm font-medium transition-colors ${
                      scrolled ? 'text-gray-700 hover:text-purple-600' : 'text-white hover:text-purple-200'
                    }`}
                  >
                    {item.name}
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Auth Section - Desktop */}
            <div className="hidden lg:flex items-center space-x-4">
              {/* Download Button */}
              <div className="relative">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowDownloadMenu(!showDownloadMenu)}
                  className={`px-4 py-2 rounded-full font-medium flex items-center space-x-2 transition-all ${
                    scrolled 
                      ? 'text-gray-700 hover:text-purple-600 hover:bg-purple-50' 
                      : 'text-white hover:text-purple-200 hover:bg-white/10'
                  }`}
                >
                  <Download className="h-4 w-4" />
                  <span>Download</span>
                </motion.button>
                <DownloadDropdown 
                  isOpen={showDownloadMenu} 
                  onClose={() => setShowDownloadMenu(false)}
                  scrolled={scrolled}
                />
              </div>

              {currentUser ? (
                <div className="relative">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className={`px-4 py-2 rounded-full font-medium flex items-center space-x-2 transition-all ${
                      scrolled 
                        ? 'text-gray-700 hover:text-purple-600 hover:bg-purple-50' 
                        : 'text-white hover:text-purple-200 hover:bg-white/10'
                    }`}
                  >
                    <User className="h-4 w-4" />
                    <span>{currentUser.displayName || 'User'}</span>
                  </motion.button>

                  {showUserMenu && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2"
                    >
                      <div className="px-4 py-2 border-b border-gray-100">
                        <p className="text-sm font-medium text-gray-900">{currentUser.displayName}</p>
                        <p className="text-xs text-gray-500">{currentUser.email}</p>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
                      >
                        <LogOut className="h-4 w-4" />
                        <span>Sign Out</span>
                      </button>
                    </motion.div>
                  )}
                </div>
              ) : (
                <>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowLoginModal(true)}
                    className={`px-4 py-2 rounded-full font-medium flex items-center space-x-2 transition-all ${
                      scrolled 
                        ? 'text-gray-700 hover:text-purple-600 hover:bg-purple-50' 
                        : 'text-white hover:text-purple-200 hover:bg-white/10'
                    }`}
                  >
                    <LogIn className="h-4 w-4" />
                    <span>Login</span>
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowSignupModal(true)}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-full font-medium flex items-center space-x-2 hover:shadow-lg transition-all"
                  >
                    <UserPlus className="h-4 w-4" />
                    <span>Sign Up</span>
                  </motion.button>
                </>
              )}
            </div>

            {/* Mobile Menu Button */}
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsOpen(!isOpen)}
              className="lg:hidden p-2"
            >
              {isOpen ? (
                <X className={`h-6 w-6 ${scrolled ? 'text-gray-700' : 'text-white'}`} />
              ) : (
                <Menu className={`h-6 w-6 ${scrolled ? 'text-gray-700' : 'text-white'}`} />
              )}
            </motion.button>
          </div>
        </div>

        {/* Mobile Menu */}
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ 
            opacity: isOpen ? 1 : 0, 
            height: isOpen ? 'auto' : 0 
          }}
          className="lg:hidden bg-white border-t border-gray-200 overflow-hidden"
        >
          <div className="px-4 py-4 space-y-3">
            {navItems.map((item) => (
              <motion.button
                key={item.name}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  handleNavigation(item);
                  setIsOpen(false);
                }}
                className="block w-full text-left py-2 text-gray-700 hover:text-purple-600 font-medium"
              >
                {item.name}
              </motion.button>
            ))}
            
            {/* Mobile Download Button */}
            <div className="pt-2 border-t border-gray-200">
              <DownloadDropdown 
                isOpen={true} 
                onClose={() => {}}
                scrolled={true}
                mobile={true}
              />
            </div>
            
            {/* Mobile Auth Section */}
            <div className="pt-4 border-t border-gray-200 space-y-3">
              {currentUser ? (
                <>
                  <div className="px-3 py-2 bg-gray-50 rounded-lg">
                    <p className="text-sm font-medium text-gray-900">{currentUser.displayName}</p>
                    <p className="text-xs text-gray-500">{currentUser.email}</p>
                  </div>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center space-x-2 py-3 text-gray-700 hover:text-red-600 font-medium border border-gray-300 rounded-full hover:border-red-300 transition-colors"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>Sign Out</span>
                  </motion.button>
                </>
              ) : (
                <>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => {
                      setShowLoginModal(true);
                      setIsOpen(false);
                    }}
                    className="w-full flex items-center justify-center space-x-2 py-3 text-gray-700 hover:text-purple-600 font-medium border border-gray-300 rounded-full hover:border-purple-300 transition-colors"
                  >
                    <LogIn className="h-4 w-4" />
                    <span>Login</span>
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => {
                      setShowSignupModal(true);
                      setIsOpen(false);
                    }}
                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-full font-medium flex items-center justify-center space-x-2"
                  >
                    <UserPlus className="h-4 w-4" />
                    <span>Sign Up</span>
                  </motion.button>
                </>
              )}
            </div>
          </div>
        </motion.div>
      </motion.nav>

      {/* Auth Modals */}
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={() => setShowLoginModal(false)}
        onSwitchToSignup={switchToSignup}
      />
      <SignupModal 
        isOpen={showSignupModal} 
        onClose={() => setShowSignupModal(false)}
        onSwitchToLogin={switchToLogin}
      />
    </>
  );
};

export default Navbar;