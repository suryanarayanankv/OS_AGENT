import React from 'react';

interface FreeTrialModalProps {
  open: boolean;
  code: string;
  loading?: boolean;
  successMessage?: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const FreeTrialModal: React.FC<FreeTrialModalProps> = ({ open, code, loading, successMessage, onConfirm, onCancel }) => {
  const [copied, setCopied] = React.useState(false);

  if (!open) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center relative">
        {successMessage ? (
          <>
            <div className="text-green-600 text-lg font-semibold mb-4">{successMessage}</div>
            <button
              className="mt-4 px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full font-semibold shadow hover:from-purple-700 hover:to-blue-700 transition"
              onClick={onCancel}
            >
              Close
            </button>
          </>
        ) : (
          <>
            <h2 className="text-xl font-bold mb-4 text-gray-800">This will create a free trial activation code valid for 1 month.</h2>
            <p className="mb-4 text-gray-600">A copy will be sent to your Gmail. Proceed?</p>
            <div className="flex items-center justify-center mb-6">
              <span className="font-mono text-lg bg-gray-100 px-4 py-2 rounded-l select-all border border-r-0 border-gray-300">{code}</span>
              <button
                className={`px-3 py-2 bg-blue-500 text-white rounded-r border border-blue-500 hover:bg-blue-600 transition ${copied ? 'bg-green-500 border-green-500' : ''}`}
                onClick={handleCopy}
                disabled={copied}
              >
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <div className="flex justify-center space-x-4">
              <button
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full font-semibold shadow hover:from-purple-700 hover:to-blue-700 transition disabled:opacity-60"
                onClick={onConfirm}
                disabled={loading}
              >
                {loading ? 'Activating...' : 'Confirm'}
              </button>
              <button
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-full font-semibold shadow hover:bg-gray-300 transition"
                onClick={onCancel}
                disabled={loading}
              >
                Cancel
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default FreeTrialModal; 