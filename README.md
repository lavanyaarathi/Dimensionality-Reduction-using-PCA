# 🧠 Dimensionality Reduction Using PCA

## 🎯 Project Overview
This project implements a **modular system** for performing **Dimensionality Reduction using Principal Component Analysis (PCA)** on both **tabular** and **image** datasets.

It provides an **end-to-end preprocessing and analysis pipeline**, enabling users to:
- Upload data (CSV, Excel, JPG, PNG)
- Clean and normalize datasets
- Perform PCA transformations
- Visualize reduced dimensions interactively

---

## ⚙️ System Architecture

The project follows a **modular architecture** with a **Flask backend** and **React frontend**, ensuring scalability, reusability, and clean separation of components.

### **Architecture Diagram**
Frontend (React)<br>
│<br>
▼<br>
Backend (Flask)<br>
├── Upload Module<br>
├── Preprocessing Module<br>
├── PCA Module<br>
└── Visualization Module<br>

Each backend module is encapsulated within its own Flask **Blueprint** and operates independently or in coordination with others.

---

## 🧩 Modules Overview

### 1️⃣ Upload Module
Handles file uploads and input validation.

**Key Features**
- Supports CSV, Excel, JPG, PNG formats  
- Validates data type and structure  
- Stores uploaded data securely  
- Integrates directly with preprocessing pipeline  

---

### 2️⃣ Preprocessing Module
Provides comprehensive preprocessing capabilities for both tabular and image data.

**Key Features**
- ✅ **Dual Data Support** – Tabular (CSV/Excel) and Image (JPG/PNG) preprocessing  
- ✅ **Flexible Strategies** – Multiple options for handling missing values and normalization  
- ✅ **Quality Analysis** – Built-in data quality checking and profiling  
- ✅ **Modular Design** – Easy to extend with custom preprocessors  
- ✅ **Standalone Operation** – Works independently or integrates with other modules  
- ✅ **Batch Processing** – Handles multiple files efficiently  
- ✅ **Comprehensive Utilities** – Outlier detection, transformations, augmentation  

---

### 3️⃣ PCA Module
Applies **Principal Component Analysis** to preprocessed data.

**Key Features**
- Computes principal components and explained variance  
- Reduces dimensionality for visualization and analysis  
- Supports both 2D and 3D PCA transformations  
- Exports reduced datasets for further modeling  

---

### 4️⃣ Visualization Module
Generates graphical outputs and visual insights.

**Key Features**
- PCA scatter plots and variance ratio charts  
- Integration with Plotly / Matplotlib for interactive displays  
- Exports plots for reports or dashboards  

---

## 🧱 Backend Routes Structure

routes/<br>
│<br>
├── upload_routes.py → Handles file uploads<br>
├── preprocessing_routes.py → Manages preprocessing requests<br>
├── pca_routes.py → Executes PCA computation<br>
└── visualization_routes.py → Returns generated PCA plots<br>


Each route is registered as a Flask **Blueprint** in `app.py`.

---

## 🧮 Workflow Summary

1. 🗂️ **Upload** dataset (CSV, Excel, JPG, or PNG)  
2. 🧹 **Preprocessing** – clean, normalize, and handle missing data  
3. 📉 **PCA Computation** – reduce data dimensions  
4. 📊 **Visualization** – display transformed results interactively  

---

## 🚀 Key Highlights

- 🔹 Modular and extensible Flask architecture  
- 🔹 Works for both **tabular and image** data  
- 🔹 Clean API endpoints for integration  
- 🔹 Scalable for large dataset handling  
- 🔹 Easy visualization and export options  

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React.js , HTML , CSS|
| **Backend** | Flask (Python) |
| **Data Processing** | NumPy, Pandas, OpenCV, Scikit-learn |
| **Visualization** | Matplotlib / Plotly |
| **File Handling** | Flask-Uploads, Pandas |
| **Environment** | Python 3.10+, Node.js, npm |

---

## 🪜 Setup Instructions

### 🔧 Backend and Frontend  Setup
```bash
# Clone repository
git clone https://github.com/<your-username>/Dimensionality-Reduction-using-PCA.git
cd Dimensionality-Reduction-using-PCA

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # on Windows
source venv/bin/activate  # on macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

```
