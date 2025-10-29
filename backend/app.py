"""
Main Flask Application for PCA Dimensionality Reduction Project.
FIXED: CORS, error handling, and security improvements
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from functools import wraps
import jwt
import datetime
import os
import io
from urllib.parse import quote

from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Import PCA modules
from modules.session_manager import session_manager
from modules.upload_handler import FileUploadHandler, FileMetadata
from modules.validators import FileValidator, ValidationFactory
from pca_results.pca_computation import run_pca_svd

load_dotenv()

app = Flask(__name__)

# FIXED: Dynamic CORS configuration
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:3001').split(',')

CORS(
    app,
    resources={r"/*": {"origins": ALLOWED_ORIGINS}},
    supports_credentials=True,
    methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# FIXED: Require SECRET_KEY in production
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set!")

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp_uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory user storage (no database as per SRS)
users = {
    'admin': generate_password_hash('admin123'),
    'lavanya': generate_password_hash('pca2025'),
    'sarayu': generate_password_hash('pca2025'),
    'siddhi': generate_password_hash('pca2025')
}

# Token required decorator
def token_required(f):
    """Decorator to require JWT token for protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            print(f"Token validation error: {e}")
            return jsonify({'message': 'Token validation failed!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def generate_variance_plot(eigenvalues, k_used, session_dir, base_filename):
    """Generate explained variance plot"""
    try:
        # Calculate variance ratios
        total_variance = np.sum(eigenvalues)
        variance_ratio = eigenvalues[:k_used] / total_variance
        cumulative_variance = np.cumsum(variance_ratio)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot bars
        x = np.arange(1, k_used + 1)
        ax.bar(x, variance_ratio, alpha=0.6, label='Individual', color='steelblue')
        
        # Plot cumulative line
        ax2 = ax.twinx()
        ax2.plot(x, cumulative_variance, 'o-', color='darkorange', linewidth=2, label='Cumulative')
        ax2.axhline(y=0.95, color='red', linestyle='--', linewidth=1, label='95% cutoff')
        
        # Labels and styling
        ax.set_xlabel('Principal Component', fontsize=12)
        ax.set_ylabel('Explained Variance Ratio', fontsize=12)
        ax2.set_ylabel('Cumulative Variance', fontsize=12)
        ax.set_title('Explained Variance by Components', fontsize=14, fontweight='bold')
        
        # Legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='best')
        
        # Grid
        ax.grid(True, alpha=0.3)
        ax.set_xticks(x)
        
        plt.tight_layout()
        
        # Save
        variance_plot_name = f"{base_filename}_variance_plot.png"
        variance_plot_path = os.path.join(session_dir, variance_plot_name)
        plt.savefig(variance_plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return variance_plot_name
    except Exception as e:
        print(f"Error generating variance plot: {e}")
        return None

def generate_scatter_plot(pca_output, k_used, session_dir, base_filename):
    """Generate 3D scatter plot of principal components"""
    try:
        # Sample data if too large
        max_points = 1000
        if pca_output.shape[0] > max_points:
            indices = np.random.choice(pca_output.shape[0], max_points, replace=False)
            pca_sample = pca_output[indices]
        else:
            pca_sample = pca_output
        
        # Create 3D scatter plot if k >= 3, otherwise 2D
        if k_used >= 3:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            scatter = ax.scatter(
                pca_sample[:, 0], 
                pca_sample[:, 1], 
                pca_sample[:, 2],
                c=pca_sample[:, 0],  # Color by PC1
                cmap='viridis',
                alpha=0.6,
                s=20
            )
            
            ax.set_xlabel('PC1', fontsize=11)
            ax.set_ylabel('PC2', fontsize=11)
            ax.set_zlabel('PC3', fontsize=11)
            ax.set_title('PCA Scatter Plot (3D)', fontsize=14, fontweight='bold')
            
            # Add colorbar
            plt.colorbar(scatter, ax=ax, shrink=0.5, label='PC1 value')
            
        else:
            # 2D plot
            fig, ax = plt.subplots(figsize=(10, 8))
            
            scatter = ax.scatter(
                pca_sample[:, 0], 
                pca_sample[:, 1] if k_used >= 2 else np.zeros_like(pca_sample[:, 0]),
                c=pca_sample[:, 0],
                cmap='viridis',
                alpha=0.6,
                s=20
            )
            
            ax.set_xlabel('PC1', fontsize=12)
            ax.set_ylabel('PC2' if k_used >= 2 else 'PC2 (zero)', fontsize=12)
            ax.set_title('PCA Scatter Plot (2D)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            plt.colorbar(scatter, ax=ax, label='PC1 value')
        
        plt.tight_layout()
        
        # Save
        scatter_plot_name = f"{base_filename}_scatter_plot.png"
        scatter_plot_path = os.path.join(session_dir, scatter_plot_name)
        plt.savefig(scatter_plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return scatter_plot_name
    except Exception as e:
        print(f"Error generating scatter plot: {e}")
        return None

# AUTHENTICATION ENDPOINTS
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password required!'}), 400
        
        username = data['username']
        password = data['password']
        
        if username in users and check_password_hash(users[username], password):
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'message': 'Login successful!',
                'token': token,
                'username': username
            }), 200
        
        return jsonify({'message': 'Invalid username or password!'}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': 'An error occurred during login'}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Username, email, and password required!'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        # Check if user already exists
        if username in users:
            return jsonify({'message': 'Username already exists!'}), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({'message': 'Password must be at least 6 characters!'}), 400
        
        # Add new user (in-memory storage)
        users[username] = generate_password_hash(password)
        
        return jsonify({
            'message': 'User registered successfully!',
            'username': username,
            'email': email
        }), 201
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'message': 'An error occurred during registration'}), 500

@app.route('/api/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({
        'message': 'Token is valid!',
        'username': current_user
    }), 200

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    # Client-side token deletion
    return jsonify({'message': 'Logout successful!'}), 200

# SESSION MANAGEMENT ENDPOINTS
@app.route('/api/session/create', methods=['POST'])
@token_required
def create_session(current_user):
    """Create a new upload session"""
    try:
        session_id = session_manager.create_session()
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Session created successfully'
        }), 201
    except Exception as e:
        print(f"Session creation error: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to create session: {str(e)}'
        }), 500

@app.route('/api/session/<session_id>', methods=['DELETE'])
@token_required
def delete_session(current_user, session_id):
    """Delete a session and all its files"""
    try:
        if not session_manager.session_exists(session_id):
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session'
            }), 404
        
        success = session_manager.delete_session(session_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Session and all files deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete session'
            }), 500
    except Exception as e:
        print(f"Session deletion error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while deleting session'
        }), 500

# FILE UPLOAD ENDPOINTS
@app.route('/api/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    """Handle file upload"""
    try:
        # Validate session_id
        session_id = request.form.get('session_id')
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'session_id is required'
            }), 400
        
        if not session_manager.session_exists(session_id):
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session_id'
            }), 400
        
        # Validate file presence
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided in request'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file extension
        if not FileValidator.allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'File type not allowed. Supported: CSV, XLSX, XLS, JPG, PNG'
            }), 400
        
        # Process upload
        file_info, message = FileUploadHandler.process_upload(file, session_id)
        
        if file_info is None:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        return jsonify({
            'success': True,
            'message': message,
            'file_info': FileMetadata.to_response_format(file_info)
        }), 200
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred during file upload'
        }), 500

# PCA COMPUTATION ENDPOINTS
@app.route('/api/pca/run', methods=['POST'])
@token_required
def run_pca_endpoint(current_user):
    """Run PCA on uploaded file"""
    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get('session_id')
        filename = data.get('filename')
        k = data.get('k')
        variance_threshold = data.get('variance_threshold')

        if not session_id or not filename:
            return jsonify({'success': False, 'error': 'session_id and filename are required'}), 400

        filepath = FileUploadHandler.get_file_path(session_id, filename)
        if not filepath:
            return jsonify({'success': False, 'error': 'File not found for given session'}), 404

        file_type = FileValidator.get_file_type(filename)
        base_filename = os.path.splitext(filename)[0]
        
        if file_type == 'tabular':
            df = pd.read_csv(filepath) if filename.lower().endswith('.csv') else pd.read_excel(filepath)
            
            # Store original for reference
            original_shape = df.shape
            
            # Drop completely empty rows
            df = df.dropna(how='all')
            
            # Try to convert date columns to numeric (days since epoch)
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        # Try parsing as datetime
                        date_col = pd.to_datetime(df[col], errors='coerce')
                        if date_col.notna().sum() > len(df) * 0.5:  # If >50% are valid dates
                            # Convert to days since epoch
                            df[col] = (date_col - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')
                    except:
                        pass
            
            # Coerce all columns to numeric when possible
            coerced = df.apply(pd.to_numeric, errors='coerce')
            numeric_df = coerced.dropna(axis=1, how='all')
            numeric_df = numeric_df.select_dtypes(include=np.number)
            
            # Fill remaining NaN values with column mean
            numeric_df = numeric_df.fillna(numeric_df.mean())
            
            # Check if we have at least 2 numeric columns
            if numeric_df.shape[1] < 2:
                available_cols = list(df.columns)
                return jsonify({
                    'success': False, 
                    'error': f'Insufficient numeric columns for PCA. Found {numeric_df.shape[1]} numeric column(s). Need at least 2. Available columns: {", ".join(available_cols)}'
                }), 400
            
            if numeric_df.empty:
                return jsonify({'success': False, 'error': 'No numeric data found after processing'}), 400
            
            data_matrix = numeric_df.to_numpy(dtype=float)
            n_features = data_matrix.shape[1]
            
            print(f"Original data shape: {original_shape}")
            print(f"Numeric columns used: {list(numeric_df.columns)}")
            print(f"Final data matrix shape: {data_matrix.shape}")
            
            # Validate k
            if k is None and variance_threshold is None:
                return jsonify({'success': False, 'error': 'Provide k or variance_threshold'}), 400
            if k is not None:
                try:
                    k = int(k)
                except Exception:
                    return jsonify({'success': False, 'error': 'k must be an integer'}), 400
                if k <= 0 or k > n_features:
                    return jsonify({'success': False, 'error': f'k must be between 1 and {n_features}'}), 400
            
            mean_vec = np.mean(data_matrix, axis=0)
            data_centered = data_matrix - mean_vec
            pca_output, eigenpairs = run_pca_svd(data_centered, k=k, variance_threshold=variance_threshold)
            k_used = pca_output.shape[1]
            eigenvectors_k = eigenpairs['eigenvectors'][:, :k_used]
            reconstructed_centered = np.dot(pca_output, eigenvectors_k.T)
            reconstructed = reconstructed_centered + mean_vec
            
            # Build transformed lower-dimensional dataset
            pc_cols = [f'PC{i+1}' for i in range(k_used)]
            transformed_df = pd.DataFrame(pca_output, columns=pc_cols, index=numeric_df.index)
            
            # Save transformed dataset
            session_dir = os.path.dirname(filepath)
            out_name = f"pca_transformed_{base_filename}.csv"
            out_path = os.path.join(session_dir, out_name)
            transformed_df.to_csv(out_path, index=False)
            
            # Generate plots
            variance_plot_name = generate_variance_plot(eigenpairs['eigenvalues'], k_used, session_dir, base_filename)
            scatter_plot_name = generate_scatter_plot(pca_output, k_used, session_dir, base_filename)
            
            # Build preview tables
            original_head_html = numeric_df.head().to_html(classes="data-table")
            transformed_head_html = transformed_df.head().to_html(classes="data-table")
            
            # Store PCA summary
            session = session_manager.get_session(session_id)
            if session:
                sample_idx = np.linspace(0, pca_output.shape[0]-1, num=min(200, pca_output.shape[0]), dtype=int)
                session.set_pca_result(filename, {
                    'explained_variance_ratio': (eigenpairs['eigenvalues'][:k_used] / np.sum(eigenpairs['eigenvalues'])).tolist(),
                    'components': pca_output[sample_idx].tolist(),
                    'k': int(k_used)
                })

            response_data = {
                'success': True,
                'message': 'PCA completed',
                'k': k_used,
                'explained_variance_ratio': (eigenpairs['eigenvalues'][:k_used] / np.sum(eigenpairs['eigenvalues'])).tolist(),
                'download_endpoint': f"/api/pca/download?session_id={session_id}&outfile={out_name}",
                'type': 'tabular',
                'columns_used': list(numeric_df.columns),
                'original_shape': list(original_shape),
                'processed_shape': list(data_matrix.shape),
                'preview': {
                    'original_head_html': original_head_html,
                    'transformed_head_html': transformed_head_html
                }
            }
            
            # Add plot endpoints if generated
            if variance_plot_name:
                response_data['variance_plot_endpoint'] = f"/api/pca/download?session_id={session_id}&outfile={variance_plot_name}"
            if scatter_plot_name:
                response_data['scatter_plot_endpoint'] = f"/api/pca/download?session_id={session_id}&outfile={scatter_plot_name}"
            
            return jsonify(response_data), 200

        elif file_type == 'image':
            img = Image.open(filepath).convert('RGB')
            img_array = np.asarray(img, dtype=float)
            h, w, c = img_array.shape
            
            if k is None and variance_threshold is None:
                return jsonify({'success': False, 'error': 'Provide k or variance_threshold'}), 400
            if k is not None:
                try:
                    k = int(k)
                except Exception:
                    return jsonify({'success': False, 'error': 'k must be an integer'}), 400
                if k <= 0 or k > c:
                    return jsonify({'success': False, 'error': f'k must be between 1 and {c} for images'}), 400
            
            flat = img_array.reshape(-1, c)
            mean_vec = np.mean(flat, axis=0)
            data_centered = flat - mean_vec
            pca_output, eigenpairs = run_pca_svd(data_centered, k=k, variance_threshold=variance_threshold)
            k_used = pca_output.shape[1]
            eigenvectors_k = eigenpairs['eigenvectors'][:, :k_used]
            reconstructed_centered = np.dot(pca_output, eigenvectors_k.T)
            reconstructed = reconstructed_centered + mean_vec
            recon_img = np.clip(reconstructed.reshape(h, w, c), 0, 255).astype(np.uint8)
            recon_pil = Image.fromarray(recon_img)
            
            session_dir = os.path.dirname(filepath)
            recon_name = f"reconstructed_{base_filename}.png"
            recon_path = os.path.join(session_dir, recon_name)
            recon_pil.save(recon_path, format='PNG')
            
            # Generate plots for image PCA
            variance_plot_name = generate_variance_plot(eigenpairs['eigenvalues'], k_used, session_dir, base_filename)
            scatter_plot_name = generate_scatter_plot(pca_output, k_used, session_dir, base_filename)

            session = session_manager.get_session(session_id)
            if session:
                sample_idx = np.linspace(0, pca_output.shape[0]-1, num=min(200, pca_output.shape[0]), dtype=int)
                session.set_pca_result(filename, {
                    'explained_variance_ratio': (eigenpairs['eigenvalues'][:k_used] / np.sum(eigenpairs['eigenvalues'])).tolist(),
                    'components': pca_output[sample_idx].tolist(),
                    'k': int(k_used),
                    'image_shape': [int(h), int(w), int(c)]
                })

            response_data = {
                'success': True,
                'message': 'PCA completed',
                'k': k_used,
                'download_endpoint': f"/api/pca/download?session_id={session_id}&outfile={recon_name}",
                'reconstructed_image_endpoint': f"/api/pca/download?session_id={session_id}&outfile={recon_name}",
                'type': 'image',
                'preview': {
                    'original_preview_endpoint': f"/api/pca/preview_image?session_id={quote(session_id)}&filename={quote(filename)}",
                    'reconstructed_preview_endpoint': f"/api/pca/preview_image?session_id={quote(session_id)}&filename={quote(recon_name)}"
                }
            }
            
            # Add plot endpoints if generated
            if variance_plot_name:
                response_data['variance_plot_endpoint'] = f"/api/pca/download?session_id={session_id}&outfile={variance_plot_name}"
            if scatter_plot_name:
                response_data['scatter_plot_endpoint'] = f"/api/pca/download?session_id={session_id}&outfile={scatter_plot_name}"
            
            return jsonify(response_data), 200

        else:
            return jsonify({'success': False, 'error': 'Unsupported file type for PCA'}), 400

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/pca/download', methods=['GET'])
@token_required
def download_reconstructed(current_user):
    """Download PCA results"""
    try:
        session_id = request.args.get('session_id')
        outfile = request.args.get('outfile')
        
        if not session_id or not outfile:
            return jsonify({'success': False, 'error': 'session_id and outfile are required'}), 400
        
        session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        full_path = os.path.join(session_dir, outfile)
        
        if not os.path.exists(full_path):
            print(f"Download file not found: {full_path}")
            return jsonify({'success': False, 'error': f'Output file not found: {outfile}'}), 404
        
        # Determine MIME type
        ext = os.path.splitext(outfile)[1].lower()
        if ext == '.csv':
            mime = 'text/csv'
        elif ext in ['.png', '.jpg', '.jpeg']:
            mime = 'image/png' if ext == '.png' else 'image/jpeg'
        else:
            mime = 'application/octet-stream'
        
        return send_file(full_path, mimetype=mime, as_attachment=True, download_name=outfile)
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'success': False, 'error': 'An error occurred during download'}), 500

@app.route('/api/pca/preview_image', methods=['GET'])
def preview_image():
    """Preview image files - NO AUTH REQUIRED for img tags to work"""
    try:
        session_id = request.args.get('session_id')
        filename = request.args.get('filename')
        
        if not session_id or not filename:
            return jsonify({'success': False, 'error': 'session_id and filename are required'}), 400
        
        # Validate session exists (security check without token)
        if not session_manager.session_exists(session_id):
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        
        # Try with original filename first
        full_path = os.path.join(session_dir, filename)
        
        # If not found, try URL decoding
        if not os.path.exists(full_path):
            try:
                from urllib.parse import unquote
                decoded = unquote(filename)
                full_path = os.path.join(session_dir, decoded)
            except Exception as e:
                print(f"Error decoding filename: {e}")
        
        # Check if file exists
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            print(f"Session dir contents: {os.listdir(session_dir) if os.path.exists(session_dir) else 'Dir not found'}")
            return jsonify({'success': False, 'error': f'File not found: {filename}'}), 404
        
        # Determine MIME type
        ext = os.path.splitext(full_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif'
        }
        mime = mime_types.get(ext, 'application/octet-stream')
        
        return send_file(full_path, mimetype=mime, as_attachment=False)
    except Exception as e:
        print(f"Preview error: {e}")
        return jsonify({'success': False, 'error': 'An error occurred during preview'}), 500

# HEALTH CHECK
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'registered_users': len(users),
        'active_sessions': session_manager.get_session_count()
    }), 200

# FIXED: Add error handler for large files
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

# FIXED: Add error handler for 500 errors
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error occurred'
    }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
