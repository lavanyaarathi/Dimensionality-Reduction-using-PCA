# visualization_module.py

from flask import Blueprint, request, jsonify, Flask, send_file, render_template
from flask_cors import CORS
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import combinations

# Blueprint
visualization_bp = Blueprint('visualization', __name__, url_prefix='/visualize')

# Helper Functions

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('ascii')

def variance_plot_matplotlib(explained_variance_ratio, cutoff_line=True):
    ev = np.array(explained_variance_ratio, dtype=float)
    components = np.arange(1, len(ev)+1)
    fig, ax = plt.subplots(figsize=(6,4))
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
        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(111, projection='3d')
        sc = ax.scatter(arr[:,0], arr[:,1], arr[:,2], c=labels if labels is not None else 'blue', cmap='viridis')
        ax.set_xlabel('PC1'); ax.set_ylabel('PC2'); ax.set_zlabel('PC3')
        ax.set_title('PCA Scatter Plot (3D)')
        png_b64 = fig_to_base64(fig)
        plots["scatter_3d"] = png_b64
        plots["png"] = png_b64
        return plots

    if k <= 3:
        i, j = 0, min(1,k-1)
        fig, ax = plt.subplots(figsize=(6,5))
        sc = ax.scatter(arr[:,i], arr[:,j], c=labels if labels is not None else 'blue', cmap='viridis')
        ax.set_xlabel(f'PC{i+1}'); ax.set_ylabel(f'PC{j+1}')
        ax.set_title(f'PCA Scatter Plot (2D)')
        if labels is not None:
            plt.colorbar(sc, ax=ax)
        png_b64 = fig_to_base64(fig)
        plots["scatter_2d"] = png_b64
        plots["png"] = png_b64
        return plots

    first_plot = None
    for i, j in combinations(range(k), 2):
        fig, ax = plt.subplots(figsize=(6,5))
        sc = ax.scatter(arr[:,i], arr[:,j], c=labels if labels is not None else 'blue', cmap='viridis')
        ax.set_xlabel(f'PC{i+1}'); ax.set_ylabel(f'PC{j+1}')
        ax.set_title(f'PCA Scatter Plot: PC{i+1} vs PC{j+1}')
        if labels is not None:
            plt.colorbar(sc, ax=ax)
        png_b64 = fig_to_base64(fig)
        key = f"PC{i+1}_PC{j+1}"
        plots[key] = png_b64
        if first_plot is None:
            first_plot = png_b64
    plots["png"] = first_plot
    return plots

# Routes

@visualization_bp.route('/variance_download', methods=['GET', 'POST'])
def variance_download():
    # Use default dummy data if GET request
    if request.method == 'GET':
        ev = [0.5, 0.3, 0.15, 0.05]
    else:
        data = request.get_json()
        if not data or "explained_variance_ratio" not in data:
            return jsonify({"error": "Missing explained_variance_ratio"}), 400
        ev = data["explained_variance_ratio"]

    try:
        fig = variance_plot_matplotlib(ev)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='variance_plot.png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@visualization_bp.route('/scatter_download', methods=['GET', 'POST'])
def scatter_download():
    # Default dummy PCA components
    if request.method == 'GET':
        components = [
            [1, 2, 3, 4],
            [4, 5, 6, 3],
            [7, 8, 9, 2],
            [2, 3, 1, 5],
            [5, 1, 2, 6]
        ]
        labels = [0, 1, 0, 1, 0]
        three_d = True
    else:
        data = request.get_json()
        if not data or "components" not in data:
            return jsonify({"error": "Missing components"}), 400
        components = np.asarray(data["components"])
        labels = data.get("labels", None)
        three_d = data.get("three_d", False)

    try:
        plots = scatter_plot_k_dim(components, labels=labels, three_d=three_d)
        buf = io.BytesIO(base64.b64decode(plots["png"]))
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='scatter_plot.png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve UI

app = Flask(__name__)
CORS(app)
app.register_blueprint(visualization_bp)

@app.route('/')
def home():
    return render_template('index.html')  # Flask serves the HTML

# Run

if __name__ == "__main__":
    app.run(debug=True, port=5000)
