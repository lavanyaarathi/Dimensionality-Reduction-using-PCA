# Python 3.13 Compatibility Fix

## 🚨 **Problem**: Python 3.13 Compatibility Issues

The error you're seeing is because Python 3.13 removed the `distutils` module, which some packages still depend on.

## 🔧 **Solution 1: Use Python 3.11 or 3.12 (Recommended)**

### **Step 1: Install Python 3.11 or 3.12**
1. Download Python 3.11 or 3.12 from [python.org](https://www.python.org/downloads/)
2. Install it alongside your current Python 3.13
3. Use the Python Launcher to specify version

### **Step 2: Create Virtual Environment with Specific Python Version**
```cmd
# For Python 3.11
py -3.11 -m venv venv

# For Python 3.12
py -3.12 -m venv venv

# Activate and install
venv\Scripts\activate.bat
py -m pip install -r Requirements.txt
```

## 🔧 **Solution 2: Fix Python 3.13 (Advanced)**

### **Step 1: Install setuptools and wheel first**
```cmd
cd backend
py -m venv venv
venv\Scripts\activate.bat
py -m pip install --upgrade pip setuptools wheel
```

### **Step 2: Install packages individually**
```cmd
py -m pip install Flask
py -m pip install Flask-CORS
py -m pip install PyJWT
py -m pip install python-dotenv
py -m pip install Werkzeug
py -m pip install numpy
py -m pip install pandas
py -m pip install scikit-learn
py -m pip install matplotlib
py -m pip install Pillow
py -m pip install openpyxl
py -m pip install plotly
```

### **Step 3: If still having issues, try this order**
```cmd
# Install core packages first
py -m pip install setuptools wheel
py -m pip install numpy
py -m pip install pandas
py -m pip install Flask
py -m pip install Flask-CORS
py -m pip install PyJWT
py -m pip install python-dotenv
py -m pip install Werkzeug
py -m pip install scikit-learn
py -m pip install matplotlib
py -m pip install Pillow
py -m pip install openpyxl
py -m pip install plotly
```

## 🔧 **Solution 3: Use Conda (Alternative)**

### **Step 1: Install Anaconda or Miniconda**
Download from [anaconda.com](https://www.anaconda.com/download)

### **Step 2: Create conda environment**
```cmd
conda create -n pca-project python=3.11
conda activate pca-project
conda install flask flask-cors numpy pandas scikit-learn matplotlib pillow
pip install PyJWT python-dotenv Werkzeug openpyxl plotly
```

## 🚀 **Quick Fix Commands**

### **For Python 3.11/3.12:**
```cmd
cd "C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project\backend"
py -3.11 -m venv venv
venv\Scripts\activate.bat
py -m pip install -r Requirements.txt
py app.py
```

### **For Python 3.13 (if you want to keep it):**
```cmd
cd "C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project\backend"
py -m venv venv
venv\Scripts\activate.bat
py -m pip install --upgrade pip setuptools wheel
py -m pip install -r requirements_python313.txt
py app.py
```

## 🔍 **Check Your Python Version**
```cmd
py --version
py -0  # List all installed Python versions
```

## ✅ **Recommended Approach**

**Use Python 3.11 or 3.12** as they have better package compatibility. Most packages are tested and work well with these versions.

### **Steps:**
1. Install Python 3.11 or 3.12
2. Use `py -3.11` or `py -3.12` commands
3. Create virtual environment with specific version
4. Install packages normally

This will resolve all compatibility issues!
