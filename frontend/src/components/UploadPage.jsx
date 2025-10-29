/**
 * UploadPage Component - FIXED FOR DEPLOYMENT
 * - Uses BASE_URL from .env
 * - Works with backend on Render
 * - Supports full file upload + PCA + downloads
 */

import React, { useState, useRef, useEffect } from 'react';
import Logo from './Logo';
import ProfileDropdown from './ProfileDropdown';
import Footer from './Footer';

const BASE_URL = process.env.REACT_APP_API_URL;

const UploadPage = () => {
  const [theme] = useState('space');
  const [sessionId, setSessionId] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState({ message: '', type: '' });
  const [pcaResults, setPcaResults] = useState({});
  const [previewImage, setPreviewImage] = useState(null);
  const fileInputRef = useRef(null);

  const showStatus = (message, type) => {
    setStatus({ message, type });
    setTimeout(() => setStatus({ message: '', type: '' }), 5000);
  };

  const createSession = async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('token');
      
      const response = await fetch(`${BASE_URL}/session/create`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({})
      });
      const data = await response.json();

      if (data.success) {
        setSessionId(data.session_id);
        showStatus('Session created successfully', 'success');
      } else {
        showStatus(`Failed to create session: ${data.error}`, 'error');
      }
    } catch (error) {
      showStatus(`Failed to create session: ${error.message}`, 'error');
    }
  };

  const handleFileUpload = async (file) => {
    if (!sessionId) {
      showStatus('Please create a session first', 'error');
      return;
    }

    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
      showStatus('File size exceeds 16MB limit', 'error');
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);

    try {
      const token = localStorage.getItem('token');
     const response = await fetch(`${BASE_URL}/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        credentials: 'include',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setUploadedFiles((prev) => [...prev, data.file_info]);
        showStatus(data.message, 'success');
      } else {
        showStatus('Upload failed: ' + data.error, 'error');
      }
    } catch (error) {
      showStatus('Upload error: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      const validFormats = ['.csv', '.xlsx', '.xls', '.jpg', '.jpeg', '.png'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

      if (!validFormats.includes(fileExtension)) {
        showStatus(`Invalid file format. Supported: ${validFormats.join(', ')}`, 'error');
        return;
      }

      if (['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
        const reader = new FileReader();
        reader.onload = (e) => setPreviewImage(e.target.result);
        reader.readAsDataURL(file);
      } else {
        setPreviewImage(null);
      }

      handleFileUpload(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) {
      handleFileInputChange({ target: { files: e.dataTransfer.files } });
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const runPCA = async (filename, k) => {
    if (!k || k <= 0) {
      showStatus('Please enter a valid k value', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${BASE_URL}/pca/run`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ session_id: sessionId, filename, k: parseInt(k) }),
      });

      const data = await response.json();
      if (data.success) {
        setPcaResults((prev) => ({ ...prev, [filename]: data }));
        showStatus('PCA completed successfully', 'success');
      } else {
        showStatus('PCA failed: ' + data.error, 'error');
      }
    } catch (error) {
      showStatus('PCA error: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const downloadResult = async (filename, type = 'result') => {
    const result = pcaResults[filename];
    if (!result) {
      showStatus('No PCA results available', 'error');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      let endpoint = '';

      switch (type) {
        case 'variance_plot':
          endpoint = result.variance_plot_endpoint;
          break;
        case 'scatter_plot':
          endpoint = result.scatter_plot_endpoint;
          break;
        case 'reconstructed_image':
          endpoint = result.reconstructed_image_endpoint;
          break;
        default:
          endpoint = result.download_endpoint;
      }

      const response = await fetch(`${BASE_URL}${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${filename}_${type}.png`;
        link.click();
        showStatus('Download started', 'success');
      } else {
        showStatus('Download failed', 'error');
      }
    } catch (error) {
      showStatus('Download error: ' + error.message, 'error');
    }
  };

  const clearFiles = async () => {
    if (!sessionId) return;
    if (!window.confirm('Are you sure you want to clear all uploaded files?')) return;

    try {
      const token = localStorage.getItem('token');
      await fetch(`${BASE_URL}/session/${sessionId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
        credentials: 'include',
      });

      setUploadedFiles([]);
      setPcaResults({});
      setPreviewImage(null);
      showStatus('Files cleared successfully', 'success');
      await createSession();
    } catch (error) {
      showStatus('Failed to clear files: ' + error.message, 'error');
    }
  };

  useEffect(() => {
    if (!sessionId) createSession();
  }, []);

  return (
    <div className="min-h-screen bg-black flex flex-col relative overflow-hidden">
      {/* Header */}
      <nav className="relative z-40 bg-black/80 backdrop-blur-xl border-b border-purple-500/30 sticky top-0">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Logo size="sm" theme={theme} showText={true} />
          <ProfileDropdown theme={theme} />
        </div>
      </nav>

      {/* Main */}
      <main className="relative z-10 flex-1 p-8 text-white">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-center mb-8">🌌 PCA Dashboard</h1>
          <div
            className="border-2 border-dashed border-purple-500/50 rounded-2xl p-12 text-center"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.xlsx,.xls,.jpg,.jpeg,.png"
              onChange={handleFileInputChange}
              className="hidden"
            />
            <p>Click or drag file to upload</p>
          </div>
        </div>
      </main>

      <Footer theme={theme} />
    </div>
  );
};

export default UploadPage;
