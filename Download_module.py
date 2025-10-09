# ===============================================
# download_module.py
# ===============================================
import requests
import json
import os
import base64

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

# ---------- 3D Scatter Plot ----------
scatter_data = {
    "components": [[1,2,3],[4,5,6],[7,8,9], [23,0,-1], [44,2,0]],
    "labels": [0,1,0],
    "three_d": True
}
scatter_file = "scatter_3d_plot.png"

resp = requests.post(f"{SERVER_URL}/scatter", json=scatter_data)
if resp.status_code == 200:
    data = resp.json()
    with open(scatter_file, "wb") as f:
        f.write(base64.b64decode(data["png"]))
    print(f"[✓] 3D Scatter plot saved as {scatter_file}")
else:
    print(f"[✗] Scatter plot failed: {resp.text}")

# Optional: open variance image automatically (Windows)
try:
    os.startfile(variance_file)
    os.startfile(scatter_file)
except:
    pass
