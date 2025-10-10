# PCA Visualization & Download Modules

## Module Overview
This project provides a **Visualization Module** and a **Download Module** for exploring Principal Component Analysis (PCA) results.  

It allows users to:

- Generate **Variance Explained Plots** (Bar + Cumulative Line)
- Generate **PCA Scatter Plots** (2D/3D)
  
Currently, the modules use **dummy data** for demonstration. Actual datasets or images should be provided by other parts of the project.

---

## Features

### Visualization Module
- Flask-based web service
- Endpoints:
  - /visualize/variance → Returns variance plots in PNG and Plotly JSON
  - /visualize/scatter → Returns PCA scatter plots in PNG and Plotly JSON
  - /visualize/image → Combines original and reconstructed images (if provided)
  - /visualize/variance_download → Downloadable variance plot as PNG
  - /visualize/scatter_download → Downloadable scatter plot as PNG

### Download Module
- Python script to fetch plots from the visualization server
- Generates:
  - variance_plot.png
  - scatter_plot.json (or PNG if configured)
- Can simulate 2D/3D scatter plots with dummy data

---

## Project Structure

/project-root
│
├─ Visualization_module.py # Flask server for plotting
├─ Download_module.py # Script to fetch and save plots
├─ .gitignore # Ignore generated images, JSON, and virtual env
├─ README.md # Project documentation
├─ Requirements.txt # Python dependencies
└─ templates which in turn contains index.html  #UI for downloading the images
