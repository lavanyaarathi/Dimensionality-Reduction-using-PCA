from flask import Blueprint, request, jsonify, send_file
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from itertools import combinations


visualization_bp = Blueprint('visualization', __name__, url_prefix='/visualize')


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('ascii')


def variance_plot_matplotlib(explained_variance_ratio, cutoff_line=True):
    ev = np.array(explained_variance_ratio, dtype=float)
    components = np.arange(1, len(ev) + 1)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(components, ev)
    ax.set_xlabel("Principal Component")
    ax.set_ylabel("Explained Variance Ratio")
    ax.set_title("Explained Variance by Components")
    ax2 = ax.twinx()
    cum_var = np.cumsum(ev)
    ax2.plot(components, cum_var, marker='o', color='orange', label='Cumulative')
    ax2.set_ylabel("Cumulative Variance")
    if cutoff_line:
        ax2.axhline(0.95, color='red', linestyle='--', label='95% cutoff')
    ax2.legend(loc='best')
    return fig


def scatter_plot_k_dim(components, labels=None, three_d=False):
    arr = np.asarray(components)
    k = arr.shape[1]
    plots = {}

    if three_d and k >= 3:
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111, projection='3d')
        sc = ax.scatter(arr[:, 0], arr[:, 1], arr[:, 2], c=labels if labels is not None else 'blue', cmap='viridis')
        ax.set_xlabel('PC1'); ax.set_ylabel('PC2'); ax.set_zlabel('PC3')
        ax.set_title('PCA Scatter Plot (3D)')
        png_b64 = fig_to_base64(fig)
        plots["scatter_3d"] = png_b64
        plots["png"] = png_b64
        return plots

    if k <= 3:
        i, j = 0, min(1, k - 1)
        fig, ax = plt.subplots(figsize=(6, 5))
        sc = ax.scatter(arr[:, i], arr[:, j], c=labels if labels is not None else 'blue', cmap='viridis')
        ax.set_xlabel(f'PC{i + 1}'); ax.set_ylabel(f'PC{j + 1}')
        ax.set_title(f'PCA Scatter Plot (2D)')
        if labels is not None:
            plt.colorbar(sc, ax=ax)
        png_b64 = fig_to_base64(fig)
        plots["scatter_2d"] = png_b64
        plots["png"] = png_b64
        return plots

    first_plot = None
    for i, j in combinations(range(k), 2):
        fig, ax = plt.subplots(figsize=(6, 5))
        sc = ax.scatter(arr[:, i], arr[:, j], c=labels if labels is not None else 'blue', cmap='viridis')
        ax.set_xlabel(f'PC{i + 1}'); ax.set_ylabel(f'PC{j + 1}')
        ax.set_title(f'PCA Scatter Plot: PC{i + 1} vs PC{j + 1}')
        if labels is not None:
            plt.colorbar(sc, ax=ax)
        png_b64 = fig_to_base64(fig)
        key = f"PC{i + 1}_PC{j + 1}"
        plots[key] = png_b64
        if first_plot is None:
            first_plot = png_b64
    plots["png"] = first_plot
    return plots


@visualization_bp.route('/variance_download', methods=['GET'])
def variance_download():
    session_id = request.args.get('session_id')
    filename = request.args.get('filename')
    plots_key = request.args.get('plots_key')
    if not session_id or not filename:
        return jsonify({"error": "session_id and filename are required"}), 400
    from modules.session_manager import session_manager
    session = session_manager.get_session(session_id)
    if not session:
        return jsonify({"error": "Invalid session"}), 404
    key = plots_key if plots_key else filename
    pca_res = session.get_pca_result(key)
    if not pca_res or 'explained_variance_ratio' not in pca_res:
        return jsonify({"error": "PCA results not found for this file"}), 404
    ev = pca_res['explained_variance_ratio']

    try:
        fig = variance_plot_matplotlib(ev)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='variance_plot.png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@visualization_bp.route('/scatter_download', methods=['GET'])
def scatter_download():
    session_id = request.args.get('session_id')
    filename = request.args.get('filename')
    plots_key = request.args.get('plots_key')
    if not session_id or not filename:
        return jsonify({"error": "session_id and filename are required"}), 400
    from modules.session_manager import session_manager
    session = session_manager.get_session(session_id)
    if not session:
        return jsonify({"error": "Invalid session"}), 404
    key = plots_key if plots_key else filename
    pca_res = session.get_pca_result(key)
    if not pca_res or 'components' not in pca_res:
        return jsonify({"error": "PCA results not found for this file"}), 404
    components = np.asarray(pca_res['components'])
    labels = None
    three_d = components.shape[1] >= 3

    try:
        plots = scatter_plot_k_dim(components, labels=labels, three_d=three_d)
        buf = io.BytesIO(base64.b64decode(plots["png"]))
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='scatter_plot.png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


