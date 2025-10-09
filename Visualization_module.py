# ================================================
# visualization_module.py
# ================================================

"""
Visualization Module

Endpoints:
- /visualize/variance         : Variance explained plot (Matplotlib + Plotly)
- /visualize/scatter          : PCA scatter plot (2D/3D)
- /visualize/image            : Original vs Reconstructed image comparison
- /visualize/variance_download: Download variance plot as PNG
"""

from flask import Blueprint, request, jsonify, Flask, send_file
from flask_cors import CORS
import io
import base64
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont

# Create Blueprint
visualization_bp = Blueprint('visualization', __name__, url_prefix='/visualize')

# ============================================================
# Helper Functions
# ============================================================

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('ascii')

# ---------------- Variance Plots ----------------
def variance_plot_matplotlib(explained_variance_ratio, cutoff_line=True):
    ev = np.array(explained_variance_ratio, dtype=float)
    components = np.arange(1, len(ev)+1)
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(components, ev)
    ax.set_xlabel("Principal Component")
    ax.set_ylabel("Explained Variance Ratio")
    ax.set_title("Explained Variance by Components")

    # Cumulative variance
    ax2 = ax.twinx()
    cum_var = np.cumsum(ev)
    ax2.plot(components, cum_var, marker='o', color='orange', label='Cumulative')
    ax2.set_ylabel("Cumulative Variance")
    if cutoff_line:
        ax2.axhline(0.95, color='red', linestyle='--', label='95% cutoff')
    ax2.legend(loc='best')
    return fig

def variance_plot_plotly(explained_variance_ratio):
    ev = np.array(explained_variance_ratio, dtype=float)
    components = np.arange(1, len(ev)+1)
    fig = px.bar(x=components, y=ev, labels={'x':'Principal Component','y':'Explained Variance Ratio'})
    fig.add_scatter(x=components, y=np.cumsum(ev), mode='lines+markers', name='Cumulative')
    fig.update_layout(title='Explained Variance by Components')
    return fig.to_json()

# ---------------- Scatter Plots ----------------
def scatter_plot_matplotlib(components, comp_indices=(0,1), labels=None, three_d=False):
    arr = np.asarray(components)
    try:
        if three_d and arr.shape[1] >= 3:
            fig = plt.figure(figsize=(6,5))
            ax = fig.add_subplot(111, projection='3d')
            sc = ax.scatter(arr[:,0], arr[:,1], arr[:,2], c=labels if labels is not None else 'blue', cmap='viridis')
            ax.set_xlabel('PC1'); ax.set_ylabel('PC2'); ax.set_zlabel('PC3')
            ax.set_title('PCA Scatter Plot (3D)')
        else:
            i, j = comp_indices
            fig, ax = plt.subplots(figsize=(6,5))
            sc = ax.scatter(arr[:,i], arr[:,j], c=labels if labels is not None else 'blue', cmap='viridis')
            ax.set_xlabel(f'PC{i+1}'); ax.set_ylabel(f'PC{j+1}')
            ax.set_title('PCA Scatter Plot (2D)')
            if labels is not None:
                plt.colorbar(sc, ax=ax)
    except Exception as e:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"Error: {e}", ha='center')
    return fig

def scatter_plot_plotly(components, labels=None, three_d=False):
    arr = np.asarray(components)
    if three_d and arr.shape[1] >= 3:
        fig = px.scatter_3d(x=arr[:,0], y=arr[:,1], z=arr[:,2],
                            color=labels if labels is not None else None,
                            labels={'x':'PC1','y':'PC2','z':'PC3'})
        fig.update_layout(title='PCA Scatter Plot (3D)')
    else:
        fig = px.scatter(x=arr[:,0], y=arr[:,1],
                         color=labels if labels is not None else None,
                         labels={'x':'PC1','y':'PC2'})
        fig.update_layout(title='PCA Scatter Plot (2D)')
    return fig.to_json()

# ---------------- Image Comparison ----------------
def combine_images(original, reconstructed, orig_label="Original", recon_label="Reconstructed", max_width=800):
    orig = original.convert("RGB")
    recon = reconstructed.convert("RGB")

    # Resize if too wide
    def resize(im, h=None, w=None):
        if w:
            ratio = w / im.width
            h_new = int(im.height * ratio)
            return im.resize((w, h_new))
        elif h:
            ratio = h / im.height
            w_new = int(im.width * ratio)
            return im.resize((w_new, h))
        return im
    if orig.width > max_width: orig = resize(orig, w=max_width)
    if recon.width > max_width: recon = resize(recon, w=max_width)

    h = max(orig.height, recon.height)
    padding = 10
    label_height = 25
    canvas = Image.new("RGB", (orig.width + recon.width + 3*padding, h + label_height + 2*padding), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(orig, (padding, label_height + padding))
    canvas.paste(recon, (orig.width + 2*padding, label_height + padding))

    # Labels
    try:
        font = ImageFont.load_default()
    except:
        font = None
    draw.text((orig.width//2 - 20, 5), orig_label, fill="black", font=font)
    draw.text((orig.width + orig.width//2 + padding, 5), recon_label, fill="black", font=font)

    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("ascii")

# ============================================================
# Flask Routes
# ============================================================

@visualization_bp.route('/variance', methods=['POST'])
def variance_endpoint():
    data = request.get_json()
    if not data or "explained_variance_ratio" not in data:
        return jsonify({"error": "Missing explained_variance_ratio"}), 400
    ev = data["explained_variance_ratio"]
    try:
        fig = variance_plot_matplotlib(ev)
        png_b64 = fig_to_base64(fig)
        plotly_json = variance_plot_plotly(ev)
        return jsonify({"png": png_b64, "plotly": json.loads(plotly_json)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@visualization_bp.route('/scatter', methods=['POST'])
def scatter_endpoint():
    data = request.get_json()
    if not data or "components" not in data:
        return jsonify({"error": "Missing components"}), 400
    components = np.asarray(data["components"])
    labels = data.get("labels", None)
    three_d = data.get("three_d", False)
    comp_indices = tuple(data.get("comp_indices", [0,1]))
    try:
        fig = scatter_plot_matplotlib(components, comp_indices=comp_indices, labels=labels, three_d=three_d)
        png_b64 = fig_to_base64(fig)
        plotly_json = scatter_plot_plotly(components, labels=labels, three_d=three_d)
        return jsonify({"png": png_b64, "plotly": json.loads(plotly_json)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@visualization_bp.route('/image', methods=['POST'])
def image_endpoint():
    orig_file = request.files.get('original')
    recon_file = request.files.get('reconstructed')
    if not orig_file or not recon_file:
        return jsonify({"error": "Both images required"}), 400
    orig_label = request.form.get('original_label', "Original")
    recon_label = request.form.get('reconstructed_label', "Reconstructed")
    try:
        orig_img = Image.open(orig_file)
        recon_img = Image.open(recon_file)
        combined_b64 = combine_images(orig_img, recon_img, orig_label, recon_label)
        return jsonify({"png": combined_b64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@visualization_bp.route('/variance_download', methods=['POST'])
def variance_download():
    data = request.get_json()
    if not data or "explained_variance_ratio" not in data:
        return jsonify({"error": "Missing explained_variance_ratio"}), 400
    try:
        ev = data["explained_variance_ratio"]
        fig = variance_plot_matplotlib(ev)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='variance_plot.png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# Run Standalone
# ============================================================

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app)  # Allow cross-origin requests
    app.register_blueprint(visualization_bp)

    @app.route('/')
    def home():
        return "Visualization Module running! Use /visualize/variance, /visualize/scatter, /visualize/image."

    app.run(debug=True, port=5000)
