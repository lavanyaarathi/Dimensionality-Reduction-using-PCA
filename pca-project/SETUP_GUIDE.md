# PCA Project Setup and Run Guide

## Prerequisites

### Required Software:
1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download here](https://nodejs.org/)
3. **Git** - [Download here](https://git-scm.com/)

### Verify Installation:
```bash
python --version
node --version
npm --version
```

## Step-by-Step Setup

### Method 1: Automated Setup (Recommended)

1. **Open Command Prompt/PowerShell as Administrator**
2. **Navigate to project directory:**
   ```bash
   cd "C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project"
   ```

3. **Run the setup script:**
   ```bash
   setup_project.bat
   ```

4. **Start the project:**
   ```bash
   start_project.bat
   ```

### Method 2: Manual Setup

#### Backend Setup:

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows Command Prompt
   venv\Scripts\activate.bat
   
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r Requirements.txt
   ```

5. **Run backend server:**
   ```bash
   python app.py
   ```

#### Frontend Setup (New Terminal):

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start frontend server:**
   ```bash
   npm start
   ```

## Accessing the Application

### URLs:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

### Default Login Credentials:
- **Username**: admin, **Password**: admin123
- **Username**: lavanya, **Password**: pca2025
- **Username**: sarayu, **Password**: pca2025
- **Username**: siddhi, **Password**: pca2025

## Usage Instructions

### 1. Login
1. Open http://localhost:3000
2. Enter credentials from the list above
3. Click "Login"

### 2. Upload Files
1. Click "Upload Dataset or Image" area
2. Select files (CSV, Excel, JPG, PNG)
3. Or drag and drop files
4. Wait for upload confirmation

### 3. Run PCA Analysis
1. Enter k value (number of principal components)
2. Click "Run PCA"
3. Wait for processing to complete
4. View results and download outputs

### 4. Download Results
- **Tabular Data**: Download transformed CSV
- **Images**: Download reconstructed images
- **Visualizations**: View variance plots

## Troubleshooting

### Common Issues:

#### 1. Python Virtual Environment Issues:
```bash
# If activation fails, try:
python -m venv --clear venv
venv\Scripts\activate.bat
pip install -r Requirements.txt
```

#### 2. Node.js Issues:
```bash
# Clear npm cache and reinstall:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 3. Port Already in Use:
```bash
# Kill processes on ports 3000 and 5000:
netstat -ano | findstr :3000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

#### 4. Permission Issues:
- Run Command Prompt as Administrator
- Check antivirus software blocking ports
- Ensure Windows Firewall allows the applications

### Backend Error Messages:
- **"Module not found"**: Run `pip install -r Requirements.txt`
- **"Port 5000 in use"**: Kill process using port 5000
- **"Permission denied"**: Run as Administrator

### Frontend Error Messages:
- **"Module not found"**: Run `npm install`
- **"Port 3000 in use"**: Kill process using port 3000
- **"Cannot connect to backend"**: Ensure backend is running on port 5000

## Development Mode

### Backend Development:
```bash
cd backend
venv\Scripts\activate.bat
python app.py
```

### Frontend Development:
```bash
cd frontend
npm start
```

### Testing API Endpoints:
Use Postman or curl to test:
```bash
# Test login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Test health check
curl http://localhost:5000/api/health
```

## Project Structure

```
pca-project/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py             # Configuration
│   ├── modules/              # Backend modules
│   ├── pca_results/          # PCA algorithms
│   ├── venv/                 # Python virtual environment
│   └── Requirements.txt      # Python dependencies
├── frontend/
│   ├── src/                  # React source code
│   ├── public/               # Static files
│   ├── node_modules/         # Node.js dependencies
│   └── package.json          # Node.js configuration
├── setup_project.bat         # Automated setup
├── start_project.bat         # Automated start
└── README.md                 # Project documentation
```

## Coding Standards Compliance

### Python (PEP 8):
- ✅ Proper imports organization
- ✅ Docstrings for all modules and functions
- ✅ Consistent naming conventions
- ✅ Line length limits (79 characters)
- ✅ Proper spacing and indentation

### JavaScript (Airbnb Style Guide):
- ✅ ES6+ syntax
- ✅ Proper component structure
- ✅ Consistent naming conventions
- ✅ Template literals for strings
- ✅ Proper error handling

## Support

For issues or questions:
1. Check this guide first
2. Verify all prerequisites are installed
3. Check the console for error messages
4. Contact the development team

## Team Members:
- **Siddhi Dhawale** (231IT072)
- **Lavanya Rathi** (231IT034)
- **Sarayu Narayanan** (231IT064)
