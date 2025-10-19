# Manual Setup Guide for PCA Project

## 🔧 **For Systems Using `py` Command**

If your system uses `py` instead of `python` and `py -m pip` instead of `pip`, follow these steps:

### **Step 1: Navigate to Project Directory**
```cmd
cd "C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project"
```

### **Step 2: Backend Setup**
```cmd
cd backend
py -m venv venv
venv\Scripts\activate.bat
py -m pip install -r Requirements.txt
py app.py
```

### **Step 3: Frontend Setup (New Terminal)**
```cmd
cd "C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project\frontend"
npm install
npm start
```

## 🚀 **Quick Commands for Your System**

### **Backend Commands:**
```cmd
# Navigate to backend
cd backend

# Create virtual environment
py -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install dependencies
py -m pip install -r Requirements.txt

# Run the application
py app.py
```

### **Frontend Commands:**
```cmd
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run the application
npm start
```

## 📍 **Exact File Locations**

Make sure you're in the correct directory structure:
```
pca-project/
├── backend/
│   ├── app.py
│   ├── Requirements.txt
│   ├── venv/          ← Created after setup
│   └── ...
├── frontend/
│   ├── package.json
│   ├── node_modules/  ← Created after npm install
│   └── ...
├── setup_project.bat
├── start_project.bat
└── MANUAL_SETUP.md
```

## 🔍 **Troubleshooting**

### **If `py` command doesn't work:**
```cmd
# Try these alternatives:
python -m venv venv
python -m pip install -r Requirements.txt
python app.py
```

### **If virtual environment activation fails:**
```cmd
# Try PowerShell activation:
venv\Scripts\Activate.ps1
```

### **If npm doesn't work:**
```cmd
# Check Node.js installation:
node --version
npm --version

# If not installed, download from: https://nodejs.org/
```

## ✅ **Verification Steps**

### **Backend Verification:**
1. Open http://localhost:5000/api/health
2. Should return: `{"status": "healthy", ...}`

### **Frontend Verification:**
1. Open http://localhost:3000
2. Should show the login page

### **Full Application Test:**
1. Login with: admin/admin123
2. Upload a CSV file
3. Run PCA analysis
4. Download results

## 🎯 **Expected Output**

### **Backend Terminal:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### **Frontend Terminal:**
```
webpack compiled with 0 errors
Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

## 📞 **Support Commands**

### **Check Python Version:**
```cmd
py --version
```

### **Check pip Version:**
```cmd
py -m pip --version
```

### **Check Node.js Version:**
```cmd
node --version
npm --version
```

### **List Installed Packages:**
```cmd
py -m pip list
```

This manual setup should work with your system configuration using `py` commands!
