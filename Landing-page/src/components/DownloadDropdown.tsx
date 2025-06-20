import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Monitor, Smartphone, Download } from 'lucide-react';

interface DownloadDropdownProps {
  isOpen: boolean;
  onClose: () => void;
  scrolled: boolean;
  mobile?: boolean;
}

const DownloadDropdown: React.FC<DownloadDropdownProps> = ({ 
  isOpen, 
  onClose, 
  scrolled, 
  mobile = false 
}) => {
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen && !mobile) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose, mobile]);

  const detectOS = () => {
    const userAgent = window.navigator.userAgent;
    if (userAgent.indexOf('Win') !== -1) return 'Windows';
    if (userAgent.indexOf('Mac') !== -1) return 'macOS';
    if (userAgent.indexOf('Linux') !== -1) return 'Linux';
    return 'Unknown';
  };

  const downloadOptions = [
    {
      name: 'Windows',
      icon: Monitor,
      url: 'https://releases.agentflow.ai/windows/AgentFlow-Setup.exe',
      size: '45.2 MB',
      recommended: detectOS() === 'Windows'
    },
    {
      name: 'macOS',
      icon: Monitor,
      url: 'https://releases.agentflow.ai/macos/AgentFlow.dmg',
      size: '52.1 MB',
      recommended: detectOS() === 'macOS'
    },
    {
      name: 'Linux',
      icon: Monitor,
      url: 'https://releases.agentflow.ai/linux/AgentFlow.AppImage',
      size: '48.7 MB',
      recommended: detectOS() === 'Linux'
    }
  ];

  const handleDownload = (url: string, platform: string) => {
    // In a real app, this would trigger the actual download
    window.open(url, '_blank');
    onClose();
  };

  if (mobile) {
    return (
      <div className="space-y-2">
        <div className="text-sm font-medium text-gray-700 mb-2 flex items-center space-x-2">
          <Download className="h-4 w-4" />
          <span>Download AgentFlow</span>
        </div>
        {downloadOptions.map((option, index) => (
          <motion.button
            key={option.name}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleDownload(option.url, option.name)}
            className="w-full flex items-center justify-between p-3 text-gray-700 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
          >
            <div className="flex items-center space-x-3">
              <option.icon className="h-4 w-4" />
              <div className="text-left">
                <div className="font-medium">{option.name}</div>
                <div className="text-xs text-gray-500">{option.size}</div>
              </div>
            </div>
            {option.recommended && (
              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                Recommended
              </span>
            )}
          </motion.button>
        ))}
      </div>
    );
  }

  return (
    <div ref={dropdownRef} className="relative">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            className="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
          >
            <div className="px-4 py-2 border-b border-gray-100">
              <h3 className="text-sm font-semibold text-gray-900">Download AgentFlow</h3>
              <p className="text-xs text-gray-500">Choose your platform</p>
            </div>
            
            <div className="py-2">
              {downloadOptions.map((option, index) => (
                <motion.button
                  key={option.name}
                  whileHover={{ backgroundColor: 'rgba(139, 92, 246, 0.05)' }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleDownload(option.url, option.name)}
                  className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-purple-50 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                      <option.icon className="h-4 w-4 text-gray-600" />
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">{option.name}</div>
                      <div className="text-xs text-gray-500">{option.size}</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {option.recommended && (
                      <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                        Recommended
                      </span>
                    )}
                    <Download className="h-4 w-4 text-gray-400" />
                  </div>
                </motion.button>
              ))}
            </div>
            
            <div className="px-4 py-2 border-t border-gray-100">
              <p className="text-xs text-gray-500">
                System requirements: 4GB RAM, 1GB storage
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default DownloadDropdown;