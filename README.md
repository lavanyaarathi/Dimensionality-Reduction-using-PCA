# Dimensionality Reduction using PCA
## 1. File Upload Module
### Module Overview
Overview
The File Upload Module provides a robust, secure, and modular system for handling file uploads in the RIDRT application. It supports multiple file formats (CSV, Excel, Images) with comprehensive validation, session management, and automatic cleanup.
### Key Features
✅ Multi-Format Support - CSV, Excel (XLSX/XLS), Images (JPG/PNG)
✅ Comprehensive Validation - File type, size, content, and structure validation
✅ Session Management - Isolated user sessions with automatic cleanup
✅ Security - Filename sanitization, size limits, extension validation
✅ Modular Architecture - Easy to extend and maintain
✅ RESTful API - Clean API endpoints for all operations
✅ Background Cleanup - Automatic deletion of expired sessions


## 3. PCA Visualization & Download Modules

### Module Overview
This project provides a **Visualization Module** and a **Download Module** for exploring Principal Component Analysis (PCA) results.  

It allows users to:

- Generate **Variance Explained Plots** (Bar + Cumulative Line)
- Generate **PCA Scatter Plots** (2D/3D)
  
Currently, the modules use **dummy data** for demonstration. Actual datasets or images should be provided by other parts of the project.

---

### Features

#### Visualization Module
- Flask-based web service
- Endpoints:
  - /visualize/variance → Returns variance plots in PNG and Plotly JSON
  - /visualize/scatter → Returns PCA scatter plots in PNG and Plotly JSON
  - /visualize/image → Combines original and reconstructed images (if provided)
  - /visualize/variance_download → Downloadable variance plot as PNG
  - /visualize/scatter_download → Downloadable scatter plot as PNG

#### Download Module
- Python script to fetch plots from the visualization server
- Generates:
  - variance_plot.png
  - scatter_plot.json (or PNG if configured)
- Can simulate 2D/3D scatter plots with dummy data

---

### Project Structure

/project-root
│
├─ Visualization_module.py # Flask server for plotting
├─ Download_module.py # Script to fetch and save plots
├─ .gitignore # Ignore generated images, JSON, and virtual env
├─ README.md # Project documentation
├─ Requirements.txt # Python dependencies
└─ templates which in turn contains index.html  #UI for downloading the images

## 2. PCA Computation and Result Generation Modules

**Author:** Siddhi Dhawale (231IT072)  
**Project:** RGB Image Dimensionality Reduction Tool (RIDRT)  
**Course:** Software Engineering  
**Date:** September-October 2025

---

### Overview

This module implements the core PCA (Principal Component Analysis) computation and result generation functionality for the RIDRT project. It provides dimensionality reduction capabilities for both tabular datasets and RGB images.

#### Module Responsibilities (per SDD v1.0)

**PCA Computation Module (`pca_computation.py`)**
- Compute covariance matrix from normalized data
- Perform eigendecomposition
- Select top-k principal components (user-defined or variance-based)
- Project data into reduced subspace

**Result Generation Module (`result_generation.py`)**
- Reconstruct images from reduced representation
- Prepare transformed datasets
- Calculate explained variance ratio
- Calculate reconstruction error (MSE)

---

### Installation

#### Python Environment

It is recommended to create and activate a virtual environment before installing the required libraries:

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required libraries
pip install numpy 
```

#### Directory Structure
```
pca_result/
├── __init__.py
├── pca_computation.py
├── result_generation.py
└── sample_data/
    ├── iris.csv
    └── flower.png
├── download_datasets.py
├── requirements.txt
├── Readme.md
└── test_my_modules.py
```

---

### Quick Start

#### Download Datasets

Run this script to download actual datasets:

```bash
python download_datasets.py
```

This downloads:
- **iris.csv** - Famous Iris dataset from UCI (150 samples, 4 features)
- **flower.png** - Sample image of a flower

---

### Testing

Run this script to test the modules:

```bash
python test_my_modules.py
```

---

### Error Handling

The modules include comprehensive input validation:

```python
# These will raise ValueError with helpful messages:
run_pca(data_norm, k=0)  # k must be positive
run_pca(data_norm, k=100)  # k exceeds feature count
run_pca(data_norm, variance_threshold=1.5)  # must be 0-1
run_pca(data_norm)  # must provide k OR variance_threshold
```

