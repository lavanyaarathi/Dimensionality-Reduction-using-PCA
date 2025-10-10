# download_module.py

import requests
import base64
from PIL import Image
import os

SERVER_URL = "http://127.0.0.1:5000/visualize"

# ---------- Variance Plot ----------
variance_data = {"explained_variance_ratio": [0.5, 0.3, 0.15, 0.05]}
variance_file = "variance_plot.png"

resp = requests.post(f"{SERVER_URL}/variance_download", json=variance_data)
if resp.status_code == 200:
    with open(variance_file, "wb") as f:
        f.write(resp.content)
    print(f"[✓] Variance plot saved as {variance_file}")
else:
    print(f"[✗] Variance plot failed: {resp.text}")

# ---------- k-Dimensional Scatter Plot ----------
scatter_components = [
    [1, 2, 3, 4],
    [4, 5, 6, 3],
    [7, 8, 9, 2],
    [2, 3, 1, 5],
    [5, 1, 2, 6]
]
scatter_labels = [0, 1, 0, 1, 0]

scatter_data = {
    "components": scatter_components,
    "labels": scatter_labels,
    "three_d": True if len(scatter_components[0]) >= 3 else False
}

scatter_file = "scatter_plot.png"

resp = requests.post(f"{SERVER_URL}/scatter_download", json=scatter_data)
if resp.status_code == 200:
    with open(scatter_file, "wb") as f:
        f.write(resp.content)
    print(f"[✓] Scatter plot saved as {scatter_file}")
else:
    print(f"[✗] Scatter plot failed: {resp.text}")

# ---------- Open files automatically (Windows) ----------
for file in [variance_file, scatter_file]:
    try:
        os.startfile(file)
    except Exception as e:
        print(f"[!] Could not open {file} automatically: {e}")
