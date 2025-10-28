/**
 * UploadPage Component - COMPLETE FIX
 * - Downloads work correctly for all file types
 * - Image previews show original vs reconstructed
 * - Variance and scatter plots download properly
 */

import React, { useState, useRef, useEffect } from 'react';
import Logo from './Logo';
import ProfileDropdown from './ProfileDropdown';
import Footer from './Footer';
const BASE_URL = process.env.REACT_APP_API_BASE_URL;

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
      const token = localStorage.getItem('token');
      const response = await const BASE_URL = process.env.REACT_APP_API_URL;
fetch(`${BASE_URL}/api/session/create`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
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
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setUploadedFiles(prev => [...prev, data.file_info]);
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
        showStatus(`Invalid file format. Supported formats: ${validFormats.join(', ')}`, 'error');
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
      const file = e.dataTransfer.files[0];
      const validFormats = ['.csv', '.xlsx', '.xls', '.jpg', '.jpeg', '.png'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!validFormats.includes(fileExtension)) {
        showStatus(`Invalid file format. Supported formats: ${validFormats.join(', ')}`, 'error');
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

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const runPCA = async (filename, k) => {
    if (!k || k <= 0) {
      showStatus('Please enter a valid k value (must be a positive number)', 'error');
      return;
    }
    
    if (!Number.isInteger(Number(k))) {
      showStatus('k value must be an integer', 'error');
      return;
    }
    
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/pca/run', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: sessionId,
          filename: filename,
          k: parseInt(k)
        })
      });

      const data = await response.json();
      
      if (data.success) {
        console.log('PCA Results:', data);
        setPcaResults(prev => ({
          ...prev,
          [filename]: data
        }));
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
      showStatus('No PCA results available for download', 'error');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      let endpoint = '';
      let downloadFilename = '';
      
      // Determine correct endpoint based on download type
      switch(type) {
        case 'variance_plot':
          if (!result.variance_plot_endpoint) {
            showStatus('Variance plot not available', 'error');
            return;
          }
          endpoint = result.variance_plot_endpoint;
          downloadFilename = `${filename.replace(/\.[^/.]+$/, '')}_variance_plot.png`;
          break;
        
        case 'scatter_plot':
          if (!result.scatter_plot_endpoint) {
            showStatus('Scatter plot not available', 'error');
            return;
          }
          endpoint = result.scatter_plot_endpoint;
          downloadFilename = `${filename.replace(/\.[^/.]+$/, '')}_scatter_plot.png`;
          break;
        
        case 'reconstructed_image':
          if (!result.reconstructed_image_endpoint) {
            showStatus('Reconstructed image not available', 'error');
            return;
          }
          endpoint = result.reconstructed_image_endpoint;
          downloadFilename = `reconstructed_${filename.replace(/\.[^/.]+$/, '')}.png`;
          break;
        
        case 'result':
        default:
          endpoint = result.download_endpoint;
          if (result.type === 'image') {
            downloadFilename = `reconstructed_${filename.replace(/\.[^/.]+$/, '')}.png`;
          } else {
            downloadFilename = `pca_transformed_${filename.replace(/\.[^/.]+$/, '')}.csv`;
          }
          break;
      }
      
      console.log(`Downloading ${type} from:`, endpoint);
      
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = downloadFilename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        showStatus(`Downloaded ${downloadFilename}`, 'success');
      } else {
        const errorText = await response.text();
        showStatus(`Download failed: ${errorText}`, 'error');
      }
    } catch (error) {
      showStatus('Download error: ' + error.message, 'error');
      console.error('Download error:', error);
    }
  };

  const clearFiles = async () => {
    if (!window.confirm('Are you sure you want to clear all uploaded files?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/api/session/${sessionId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        setUploadedFiles([]);
        setPcaResults({});
        setPreviewImage(null);
        showStatus('Files cleared successfully', 'success');
        await createSession();
      }
    } catch (error) {
      showStatus('Failed to clear files: ' + error.message, 'error');
    }
  };

  useEffect(() => {
    if (!sessionId) {
      createSession();
    }
  }, []);

  return (
    <div className="min-h-screen bg-black flex flex-col relative overflow-hidden">
      {/* Space Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-black via-purple-900/20 to-black">
        <div className="absolute inset-0">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${1.5 + Math.random() * 2}s`
              }}
            />
          ))}
        </div>
        
        {/* Floating Gamma Symbols */}
        {[
          { side: 'left', top: '25%', color: 'purple', size: '4xl', delay: '0s' },
          { side: 'left', top: '33%', color: 'blue', size: '3xl', delay: '1s' },
          { side: 'left', top: '50%', color: 'pink', size: '5xl', delay: '1.5s' },
          { side: 'left', top: '66%', color: 'indigo', size: '2xl', delay: '0.7s' },
          { side: 'right', top: '25%', color: 'purple', size: '4xl', delay: '0s' },
          { side: 'right', top: '33%', color: 'blue', size: '3xl', delay: '1s' },
          { side: 'right', top: '50%', color: 'pink', size: '5xl', delay: '1.5s' },
          { side: 'right', top: '66%', color: 'indigo', size: '2xl', delay: '0.7s' }
        ].map((g, i) => (
          <div
            key={i}
            className={`absolute ${g.side === 'left' ? 'left-10' : 'right-10'} animate-float`}
            style={{ top: g.top, animationDelay: g.delay }}
          >
            <div className={`text-${g.color}-500 text-${g.size} opacity-70`}>γ</div>
          </div>
        ))}
        
        {/* Nebula Effect */}
        <div className="absolute top-0 left-0 w-full h-full opacity-30">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '3s' }} />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s', animationDuration: '3s' }} />
        </div>
      </div>

      {/* Header */}
      <nav className="relative z-40 bg-black/80 backdrop-blur-xl border-b border-purple-500/30 sticky top-0">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Logo size="sm" theme={theme} showText={true} />
          <ProfileDropdown theme={theme} />
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative z-10 flex-1 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent mb-4">
              🌌 PCA Dashboard
            </h1>
            <p className="text-gray-300 text-lg">
              Upload datasets or images for dimensionality reduction analysis
            </p>
          </div>

          {/* Upload Area */}
          <div className="bg-black/60 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30 shadow-2xl mb-8 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-3xl" />
            
            <div className="relative z-10">
              <h2 className="text-2xl font-semibold text-white mb-6 text-center">
                🚀 Upload Dataset or Image
              </h2>
              
              <div 
                className="border-2 border-dashed border-purple-500/50 rounded-2xl p-16 text-center hover:border-purple-400/70 transition-all duration-300 cursor-pointer group relative overflow-hidden"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-blue-500/5 group-hover:from-purple-500/10 group-hover:to-blue-500/10 transition-all duration-300" />
                
                <div className="relative z-10">
                  {previewImage ? (
                    <div className="mb-4">
                      <img 
                        src={previewImage} 
                        alt="Preview" 
                        className="max-w-full h-auto mx-auto rounded-lg border-2 border-purple-500/50 shadow-lg"
                        style={{ maxHeight: '200px' }}
                      />
                      <p className="text-white text-lg mt-4 font-medium">
                        Click to change file or drag and drop
                      </p>
                    </div>
                  ) : (
                    <>
                      <div className="text-8xl mb-6 animate-pulse">✨</div>
                      <p className="text-white text-xl mb-3 font-medium">
                        Click to upload or drag and drop
                      </p>
                      <p className="text-gray-400 text-sm">
                        Supported formats: CSV, XLSX, XLS, JPG, PNG (Max 16MB)
                      </p>
                    </>
                  )}
                </div>
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv,.xlsx,.xls,.jpg,.jpeg,.png"
                  onChange={handleFileInputChange}
                  className="hidden"
                />
              </div>

              {/* Loading */}
              {isLoading && (
                <div className="mt-6 text-center">
                  <div className="inline-block w-12 h-12 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin"></div>
                  <p className="text-gray-300 mt-3 text-lg">Processing your data...</p>
                </div>
              )}

              {/* Status */}
              {status.message && (
                <div className={`mt-6 p-4 rounded-xl ${
                  status.type === 'success' ? 'bg-green-500/20 border border-green-500/50 text-green-300' :
                  status.type === 'error' ? 'bg-red-500/20 border border-red-500/50 text-red-300' :
                  'bg-blue-500/20 border border-blue-500/50 text-blue-300'
                }`}>
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${
                      status.type === 'success' ? 'bg-green-400' :
                      status.type === 'error' ? 'bg-red-400' : 'bg-blue-400'
                    } animate-pulse`} />
                    {status.message}
                  </div>
                </div>
              )}

              {/* Session Info */}
              {sessionId && (
                <div className="mt-6 p-4 bg-black/40 border border-purple-500/30 rounded-xl">
                  <p className="text-gray-300 text-sm text-center">
                    <span className="text-purple-400">Session ID:</span> {sessionId.substring(0, 8)}...
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Uploaded Files */}
          {uploadedFiles.length > 0 && (
            <div className="bg-black/60 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30 shadow-2xl mb-8 relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-3xl" />
              
              <div className="relative z-10">
                <div className="flex justify-between items-center mb-8">
                  <h3 className="text-2xl font-semibold text-white">📊 Uploaded Files</h3>
                  <button
                    onClick={clearFiles}
                    className="px-6 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-300 border border-red-500/50 rounded-xl transition-all duration-300"
                  >
                    🗑️ Clear All
                  </button>
                </div>

                <div className="space-y-6">
                  {uploadedFiles.map((file, index) => (
                    <div key={index} className="bg-black/40 border border-purple-500/30 rounded-2xl p-6 hover:border-purple-400/50 transition-all duration-300">
                      <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-4">
                          <div className="text-4xl">
                            {file.file_type === 'image' ? '🖼️' : '📊'}
                          </div>
                          <div>
                            <h4 className="text-white font-medium text-lg">{file.filename}</h4>
                            <p className="text-gray-400 text-sm">{file.validation_message}</p>
                          </div>
                        </div>
                        <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                          file.file_type === 'image' 
                            ? 'bg-pink-500/20 text-pink-300 border border-pink-500/50' 
                            : 'bg-blue-500/20 text-blue-300 border border-blue-500/50'
                        }`}>
                          {file.file_type}
                        </span>
                      </div>

                      {/* PCA Controls */}
                      <div className="flex items-center gap-4 mb-6">
                        <input
                          type="number"
                          min="1"
                          placeholder="Enter k value"
                          className="px-4 py-3 bg-black/60 border border-purple-500/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-400 w-40"
                          id={`k-input-${index}`}
                        />
                        <button
                          onClick={() => {
                            const kInput = document.getElementById(`k-input-${index}`);
                            runPCA(file.filename, kInput.value);
                          }}
                          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white rounded-xl transition-all duration-300 font-medium"
                        >
                          🚀 Run PCA
                        </button>
                      </div>

                      {/* PCA Results */}
                      {pcaResults[file.filename] && (
                        <div className="mt-6 p-6 bg-black/60 border border-purple-500/30 rounded-2xl">
                          <h5 className="text-white font-medium mb-4 text-lg">✨ PCA Results</h5>
                          
                          <div className="mb-6">
                            <p className="text-gray-300 text-sm mb-2">
                              Components: <span className="text-purple-400">{pcaResults[file.filename].k}</span>
                            </p>
                            <p className="text-gray-300 text-sm mb-2">
                              Type: <span className="text-blue-400">{pcaResults[file.filename].type}</span>
                            </p>
                            
                            {/* Show which columns were used for tabular data */}
                            {pcaResults[file.filename].type === 'tabular' && pcaResults[file.filename].columns_used && (
                              <div className="mt-3 p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                                <p className="text-blue-300 text-xs font-medium mb-1">Numeric Columns Used:</p>
                                <p className="text-gray-300 text-xs">
                                  {pcaResults[file.filename].columns_used.join(', ')}
                                </p>
                                {pcaResults[file.filename].original_shape && pcaResults[file.filename].processed_shape && (
                                  <p className="text-gray-400 text-xs mt-1">
                                    Original: {pcaResults[file.filename].original_shape[0]}×{pcaResults[file.filename].original_shape[1]} → 
                                    Processed: {pcaResults[file.filename].processed_shape[0]}×{pcaResults[file.filename].processed_shape[1]}
                                  </p>
                                )}
                              </div>
                            )}
                            
                            {/* Download Buttons */}
                            <div className="flex gap-3 flex-wrap">
                              {pcaResults[file.filename].type === 'tabular' ? (
                                <button
                                  onClick={() => downloadResult(file.filename, 'result')}
                                  className="px-4 py-2 bg-green-600/20 hover:bg-green-600/30 text-green-300 border border-green-500/50 rounded-lg transition-all duration-300"
                                >
                                  📥 Download Transformed CSV
                                </button>
                              ) : (
                                <button
                                  onClick={() => downloadResult(file.filename, 'reconstructed_image')}
                                  className="px-4 py-2 bg-pink-600/20 hover:bg-pink-600/30 text-pink-300 border border-pink-500/50 rounded-lg transition-all duration-300"
                                >
                                  🖼️ Download Reconstructed Image
                                </button>
                              )}
                              
                              {pcaResults[file.filename].variance_plot_endpoint && (
                                <button
                                  onClick={() => downloadResult(file.filename, 'variance_plot')}
                                  className="px-4 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/50 rounded-lg transition-all duration-300"
                                >
                                  📊 Download Variance Plot
                                </button>
                              )}
                              
                              {pcaResults[file.filename].scatter_plot_endpoint && (
                                <button
                                  onClick={() => downloadResult(file.filename, 'scatter_plot')}
                                  className="px-4 py-2 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/50 rounded-lg transition-all duration-300"
                                >
                                  📈 Download Scatter Plot
                                </button>
                              )}
                            </div>
                          </div>

                          {/* Image Preview */}
                          {pcaResults[file.filename].type === 'image' && pcaResults[file.filename].preview && (
                            <div className="mt-6">
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <div className="bg-black/40 border border-purple-500/30 rounded-2xl p-4">
                                  <h6 className="text-white font-medium mb-4 text-center">🖼️ Original Image</h6>
                                  <div className="flex items-center justify-center min-h-[200px]">
                                    <img 
                                      src={`http://localhost:5000${pcaResults[file.filename].preview.original_preview_endpoint}`}
                                      alt="Original"
                                      onLoad={() => console.log('Original image loaded successfully')}
                                      onError={(e) => {
                                        console.error('Failed to load original image:', e.target.src);
                                        e.target.style.display = 'none';
                                        e.target.parentElement.innerHTML = '<p class="text-gray-400 text-sm">Image preview unavailable. Use download button to view.</p>';
                                      }}
                                      className="max-w-full h-auto rounded-xl border border-purple-500/50 shadow-xl"
                                      style={{ maxHeight: '400px', objectFit: 'contain' }}
                                    />
                                  </div>
                                </div>
                                <div className="bg-black/40 border border-blue-500/30 rounded-2xl p-4">
                                  <h6 className="text-white font-medium mb-4 text-center">✨ Reconstructed Image</h6>
                                  <div className="flex items-center justify-center min-h-[200px]">
                                    <img 
                                      src={`http://localhost:5000${pcaResults[file.filename].preview.reconstructed_preview_endpoint}`}
                                      alt="Reconstructed"
                                      onLoad={() => console.log('Reconstructed image loaded successfully')}
                                      onError={(e) => {
                                        console.error('Failed to load reconstructed image:', e.target.src);
                                        e.target.style.display = 'none';
                                        e.target.parentElement.innerHTML = '<p class="text-gray-400 text-sm">Image preview unavailable. Use download button to view.</p>';
                                      }}
                                      className="max-w-full h-auto rounded-xl border border-blue-500/50 shadow-xl"
                                      style={{ maxHeight: '400px', objectFit: 'contain' }}
                                    />
                                  </div>
                                </div>
                              </div>
                            </div>
                          )}

                          {/* Tabular Preview */}
                          {pcaResults[file.filename].type === 'tabular' && pcaResults[file.filename].preview && (
                            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                              <div>
                                <h6 className="text-white font-medium mb-3">📊 Original Data (head)</h6>
                                <div 
                                  className="text-xs text-gray-400 overflow-auto max-h-32 bg-black/40 p-3 rounded-lg"
                                  dangerouslySetInnerHTML={{ __html: pcaResults[file.filename].preview.original_head_html }}
                                />
                              </div>
                              <div>
                                <h6 className="text-white font-medium mb-3">🔄 Transformed Data (head)</h6>
                                <div 
                                  className="text-xs text-gray-400 overflow-auto max-h-32 bg-black/40 p-3 rounded-lg"
                                  dangerouslySetInnerHTML={{ __html: pcaResults[file.filename].preview.transformed_head_html }}
                                />
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer theme={theme} />
    </div>
  );
};


export default UploadPage;
