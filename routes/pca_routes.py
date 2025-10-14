from flask import Blueprint, request, jsonify, send_file
from modules.upload_handler import FileUploadHandler
from modules.validators import FileValidator
from modules.session_manager import session_manager
from pca_results.pca_computation import run_pca_svd
import numpy as np
import pandas as pd
from PIL import Image
from urllib.parse import quote
import os
import io


pca_bp = Blueprint('pca', __name__, url_prefix='/api/pca')


def _load_tabular(filepath: str) -> pd.DataFrame:
    if filepath.lower().endswith('.csv'):
        return pd.read_csv(filepath)
    return pd.read_excel(filepath)


@pca_bp.route('/run', methods=['POST'])
def run_pca_endpoint():
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id')
    filename = data.get('filename')
    k = data.get('k')
    variance_threshold = data.get('variance_threshold')
    # single-image/tabular flow only

    if not session_id or not filename:
        return jsonify({'success': False, 'error': 'session_id and filename are required'}), 400

    filepath = FileUploadHandler.get_file_path(session_id, filename)
    if not filepath:
        return jsonify({'success': False, 'error': 'File not found for given session'}), 404

    file_type = FileValidator.get_file_type(filename)
    try:
        if file_type == 'tabular':
            df = _load_tabular(filepath).dropna()
            # Coerce all columns to numeric when possible to avoid 'object' dtype blocking PCA
            coerced = df.apply(pd.to_numeric, errors='coerce')
            # Drop columns that are entirely NaN after coercion
            numeric_df = coerced.dropna(axis=1, how='all')
            # Still ensure we only work with numeric values
            numeric_df = numeric_df.select_dtypes(include=np.number)
            if numeric_df.empty:
                return jsonify({'success': False, 'error': 'No numeric columns found for PCA'}), 400
            data_matrix = numeric_df.to_numpy(dtype=float)
            n_features = data_matrix.shape[1]
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
            # Build transformed lower-dimensional dataset (PC scores)
            pc_cols = [f'PC{i+1}' for i in range(k_used)]
            transformed_df = pd.DataFrame(pca_output, columns=pc_cols, index=numeric_df.index)
            # Save transformed dataset for download
            session_dir = os.path.dirname(filepath)
            out_name = f"pca_transformed_{os.path.splitext(filename)[0]}.csv"
            out_path = os.path.join(session_dir, out_name)
            transformed_df.to_csv(out_path, index=False)
            # Build preview tables (original numeric vs transformed PCs)
            original_head_html = numeric_df.head().to_html(classes="data-table")
            transformed_head_html = transformed_df.head().to_html(classes="data-table")
            # Store PCA summary into session for plots
            session = session_manager.get_session(session_id)
            if session:
                # sample up to 200 rows for plotting
                sample_idx = np.linspace(0, pca_output.shape[0]-1, num=min(200, pca_output.shape[0]), dtype=int)
                session.set_pca_result(filename, {
                    'explained_variance_ratio': (eigenpairs['eigenvalues'][:k_used] / np.sum(eigenpairs['eigenvalues'])).tolist(),
                    'components': pca_output[sample_idx].tolist(),
                    'k': int(k_used)
                })

            return jsonify({
                'success': True,
                'message': 'PCA completed',
                'k': k_used,
                'explained_variance_ratio': (eigenpairs['eigenvalues'][:k_used] / np.sum(eigenpairs['eigenvalues'])).tolist(),
                'download_endpoint': f"/api/pca/download?session_id={session_id}&outfile={out_name}",
                'type': 'tabular',
                'preview': {
                    'original_head_html': original_head_html,
                    'transformed_head_html': transformed_head_html
                }
            }), 200

        elif file_type == 'image':
            img = Image.open(filepath).convert('RGB')
            img_array = np.asarray(img, dtype=float)
            h, w, c = img_array.shape
            # For RGB images features are channels=3
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
            recon_name = f"reconstructed_{os.path.splitext(filename)[0]}.png"
            recon_path = os.path.join(session_dir, recon_name)
            recon_pil.save(recon_path, format='PNG')

            session = session_manager.get_session(session_id)
            if session:
                sample_idx = np.linspace(0, pca_output.shape[0]-1, num=min(200, pca_output.shape[0]), dtype=int)
                session.set_pca_result(filename, {
                    'explained_variance_ratio': (eigenpairs['eigenvalues'][:k_used] / np.sum(eigenpairs['eigenvalues'])).tolist(),
                    'components': pca_output[sample_idx].tolist(),
                    'k': int(k_used),
                    'image_shape': [int(h), int(w), int(c)]
                })

            return jsonify({
                'success': True,
                'message': 'PCA completed',
                'k': k_used,
                'download_endpoint': f"/api/pca/download?session_id={session_id}&outfile={recon_name}",
                'type': 'image',
                'preview': {
                    'original_preview_endpoint': f"/api/pca/preview_image?session_id={quote(session_id)}&filename={quote(filename)}",
                    'reconstructed_preview_endpoint': f"/api/pca/preview_image?session_id={quote(session_id)}&filename={quote(recon_name)}"
                }
            }), 200


        else:
            return jsonify({'success': False, 'error': 'Unsupported file type for PCA'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@pca_bp.route('/download', methods=['GET'])
def download_reconstructed():
    session_id = request.args.get('session_id')
    outfile = request.args.get('outfile')
    if not session_id or not outfile:
        return jsonify({'success': False, 'error': 'session_id and outfile are required'}), 400
    # reconstruct full path
    # We saved under session directory
    # Get any original file in session to derive directory
    # Better: use upload handler path helper
    session_dir = os.path.join(os.getcwd(), 'temp_uploads', session_id)
    full_path = os.path.join(session_dir, outfile)
    if not os.path.exists(full_path):
        return jsonify({'success': False, 'error': 'Output file not found'}), 404
    mime = 'text/csv' if full_path.lower().endswith('.csv') else 'image/png'
    return send_file(full_path, mimetype=mime, as_attachment=True, download_name=outfile)


@pca_bp.route('/preview_image', methods=['GET'])
def preview_image():
    session_id = request.args.get('session_id')
    filename = request.args.get('filename')
    if not session_id or not filename:
        return jsonify({'success': False, 'error': 'session_id and filename are required'}), 400
    # original: filename is original; reconstructed: filename is the reconstructed file name
    session_dir = os.path.join(os.getcwd(), 'temp_uploads', session_id)
    full_path = os.path.join(session_dir, filename)
    if not os.path.exists(full_path):
        # Some browsers double-encode; try unquote once
        try:
            from urllib.parse import unquote
            decoded = unquote(filename)
            full_path = os.path.join(session_dir, decoded)
        except Exception:
            pass
        if not os.path.exists(full_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
    ext = os.path.splitext(full_path)[1].lower()
    if ext in ['.jpg', '.jpeg']:
        mime = 'image/jpeg'
    elif ext == '.png':
        mime = 'image/png'
    else:
        mime = 'application/octet-stream'
    return send_file(full_path, mimetype=mime, as_attachment=False)


