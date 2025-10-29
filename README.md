# PCA Dimensionality Reduction Project

## 🎯 Project Overview
A comprehensive web application for Principal Component Analysis (PCA) with user authentication, modern UI, and full integration testing. This project follows all Software Engineering (IT303) coding standards and best practices.

## 📋 Coding Standards Compliance

### ✅ Python (PEP 8 – Style Guide for Python Code)
1. Proper module docstrings and function documentation
2. Consistent import organization
3. Line length limits (79 characters)
4. Proper naming conventions (snake_case)
5. Comprehensive error handling

### ✅ JavaScript (Airbnb JavaScript Style Guide)
1. ES6+ syntax and modern React patterns
2. Proper component structure and naming
3. Template literals and arrow functions
4. Consistent code formatting
5. Proper error handling and async/await

## 🚀 Quick Start Guide

### Prerequisites
Ensure you have the following installed:
1. Python 3.8+
2. Node.js 16+
3. Git 

## ⚙️ Setup Instructions by Operating System

### 🪟 Windows

#### Step 1: Automated Setup (Recommended)
```bash
# Navigate to your project directory
cd "C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project"
# (or whatever is the name of your directory your project is saved in)

# Run automated setup
setup_project.bat

# Start the project
start_project.bat
```

#### Step 2: Manual Setup (Alternative)

**Backend Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r Requirements.txt
python app.py
```

**Frontend Setup (new terminal):**
```bash
cd frontend
npm install
npm start
```

### 🐧 Linux / Ubuntu / WSL

#### Step 1: Automated Setup (Recommended)
```bash
# Navigate to project directory
cd ~/Documents/pca-project

# Grant execution permission (first time only)
chmod +x setup_project.sh start_project.sh

# Run setup and start scripts
./setup_project.sh
./start_project.sh
```

#### Step 2: Manual Setup (Alternative)

**Backend Setup:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r Requirements.txt
python3 app.py
```

**Frontend Setup (new terminal):**
```bash
cd frontend
npm install
npm start
```

### 💡 Note for Git Bash Users (Windows)
If you're using Git Bash on Windows, follow the same commands as Linux setup above — just ensure:
1. Your path starts with `/c/Users/...` instead of `/home/...`
2. Use `python` instead of `python3` if Python is installed on Windows
3. You can still use `.sh` scripts like `./setup_project.sh` and `./start_project.sh`

Git Bash emulates a Linux-like shell environment and supports all standard commands used in this project.

### 🍎 macOS

#### Step 1: Automated Setup (Recommended)
```bash
# Navigate to project directory
cd ~/Projects/pca-project

# Grant permission and run setup scripts
chmod +x setup_project.sh start_project.sh
./setup_project.sh
./start_project.sh
```

#### Step 2: Manual Setup (Alternative)

**Backend Setup:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r Requirements.txt
python3 app.py
```

**Frontend Setup (new terminal):**
```bash
cd frontend
npm install
npm start
```

## 🔧 Project Architecture

### Backend (Flask + Python)
```
backend/
├── app.py                      # Main Flask application with auth + PCA
├── config.py                   # Configuration settings (PEP 8 compliant)
├── modules/
│   ├── session_manager.py      # Session management (PEP 8 compliant)
│   ├── upload_handler.py       # File upload handling (PEP 8 compliant)
│   └── validators.py           # File validation (PEP 8 compliant)
├── pca_results/
│   └── pca_computation.py      # PCA algorithms (PEP 8 compliant)
├── venv/                       # Python virtual environment
└── Requirements.txt            # Python dependencies
```

### Frontend (React + JavaScript)
```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadPage.jsx      # Main upload component (Airbnb style)
│   │   ├── LoginPage.jsx       # Authentication (Airbnb style)
│   │   └── ...                 # Other components (Airbnb style)
│   ├── services/
│   │   └── authService.js      # API services (Airbnb style)
│   └── App.js                  # Main React app (Airbnb style)
├── node_modules/               # Node.js dependencies
└── package.json                # Node.js configuration
```

## 🧪 Testing and Quality Assurance

### Integration Testing
```bash
python test_integration.py
```

### Manual Testing Checklist
- [ ] Backend health check (http://localhost:5000/api/health)
- [ ] Frontend accessibility (http://localhost:3000)
- [ ] User authentication (login/logout)
- [ ] File upload (CSV, Excel, JPG, PNG)
- [ ] PCA processing (tabular and image data)
- [ ] Results download
- [ ] Session management
- [ ] Error handling

## 🔐 Authentication System

### Default Credentials
| Username | Password |
|----------|----------|
| admin    | admin123 |
| lavanya  | pca2025  |
| sarayu   | pca2025  |
| siddhi   | pca2025  |

### Security Features
1. JWT-based authentication
2. Token expiration (24 hours)
3. Protected API endpoints
4. Secure file upload validation
5. Session-based file management

## 📊 PCA Functionality
1. Supports both tabular data (CSV, Excel) and image data (JPG, PNG) with:
2. Real-time PCA computation
3. Interactive k-value input
4. Variance analysis and visualization
5. Data transformation and reconstruction
6. Downloadable results

## 🎨 User Interface

### Design Principles
1. Modern dark theme with cyber aesthetics
2. Responsive design for all screen sizes
3. Intuitive drag-and-drop interface
4. Real-time status updates
5. Professional error handling
6. Consistent UI components

## 📁 File Structure
```
pca-project/
├── backend/                  
├── frontend/                 
├── setup_project.bat / setup_project.sh  
├── start_project.bat / start_project.sh  
├── test_integration.py       
├── SETUP_GUIDE.md            
├── FINAL_README.md           
└── README.md                 
```

## 📈 Performance and Scalability

### Backend Optimizations
1. Efficient SVD-based PCA implementation
2. Session-based file management
3. Automatic cleanup of expired sessions
4. Memory-efficient file handling

### Frontend Optimizations
1. Optimized React rendering
2. Lazy-loaded components
3. Responsive design
4. Efficient API communication

## 🛠️ Troubleshooting

### Common Issues

#### Backend
```bash
# Reset virtual environment
python -m venv --clear venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS
pip install -r Requirements.txt

# Free port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

#### Frontend
```bash
# Reinstall dependencies
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Free port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

## 📚 Documentation
- **Python:** PEP 257 docstrings
- **JavaScript:** JSDoc comments
- **API:** Endpoint documentation
- **Components:** React component documentation

## 👥 Team Members
- **Siddhi Dhawale (231IT072)** – Backend Development & Integration
- **Lavanya Rathi (231IT034)** – PCA Algorithms and Testing
- **Sarayu Narayanan (231IT064)** – Frontend Development & UI/UX 

## 🏆 Project Achievements
- ✅ Fully integrated modules
- ✅ Follows PEP 8 & Airbnb JS style guides
- ✅ Secure authentication system
- ✅ PCA for multiple data types
- ✅ Modern, responsive UI
- ✅ Comprehensive testing and documentation

## 📞 Support
For technical support or questions:
- Refer to `SETUP_GUIDE.md`
- Run `python test_integration.py` to verify functionality
- Review troubleshooting section
- Contact the development team
