# PCA Dimensionality Reduction Project

A comprehensive web application for Principal Component Analysis (PCA) with user authentication and modern UI.

## Features

### 🔐 Authentication System
- JWT-based authentication
- User registration and login
- Protected routes
- Session management

### 📊 PCA Functionality
- **Tabular Data**: CSV, Excel file support
- **Image Data**: JPG, PNG file support
- **Real-time Processing**: Interactive PCA computation
- **Visualization**: Variance plots and scatter plots
- **Download Results**: Transformed datasets and reconstructed images

### 🎨 Modern UI
- React-based frontend with Tailwind CSS
- Responsive design
- Dark theme with cyber aesthetics
- Drag-and-drop file upload
- Real-time status updates

## Project Structure

```
pca-project/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py          # Configuration settings
│   ├── modules/
│   │   ├── session_manager.py # Session management
│   │   ├── upload_handler.py  # File upload handling
│   │   └── validators.py      # File validation
│   ├── pca_results/
│   │   └── pca_computation.py # PCA algorithms
│   └── Requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/         # API services
│   │   └── App.js            # Main React app
│   └── package.json         # Node.js dependencies
└── README.md
```

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r Requirements.txt
   ```

5. **Run the backend:**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   Frontend will run on `http://localhost:3000`

## Usage

### 1. Authentication
- **Login**: Use existing credentials or register new account
- **Default Users**: 
  - admin/admin123
  - lavanya/pca2025
  - sarayu/pca2025
  - siddhi/pca2025

### 2. Upload Files
- **Supported Formats**:
  - Tabular: CSV, XLSX, XLS
  - Images: JPG, PNG
- **File Size Limit**: 16MB
- **Upload Methods**: Click to browse or drag-and-drop

### 3. Run PCA Analysis
- Enter k value (number of principal components)
- Click "Run PCA" to process
- View results and download outputs

### 4. Results
- **Tabular Data**: Download transformed CSV with principal components
- **Images**: Download reconstructed images
- **Visualizations**: View variance plots and scatter plots

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `GET /api/verify` - Token verification
- `POST /api/logout` - User logout

### File Management
- `POST /api/session/create` - Create upload session
- `POST /api/upload` - Upload file
- `DELETE /api/session/{id}` - Delete session

### PCA Processing
- `POST /api/pca/run` - Run PCA analysis
- `GET /api/pca/download` - Download results
- `GET /api/pca/preview_image` - Preview images

## Technical Details

### Backend Technologies
- **Flask**: Web framework
- **JWT**: Authentication tokens
- **NumPy/Pandas**: Data processing
- **PIL**: Image processing
- **scikit-learn**: PCA algorithms

### Frontend Technologies
- **React**: UI framework
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **React Router**: Navigation

### Key Features
- **Session Management**: Automatic cleanup of expired sessions
- **File Validation**: Comprehensive file type and content validation
- **Error Handling**: Robust error handling and user feedback
- **Security**: JWT-based authentication with token expiration

## Development

### Backend Development
```bash
cd backend
python app.py
```

### Frontend Development
```bash
cd frontend
npm start
```

### Testing
- Backend: Use Postman or curl to test API endpoints
- Frontend: Use browser developer tools for debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for educational purposes as part of the Software Engineering course (IT303) at NITK Surathkal.

## Team

- **Siddhi Dhawale** (231IT072)
- **Lavanya Rathi** (231IT034)  
- **Sarayu Narayanan** (231IT064)

## Support

For issues or questions, please contact the development team or create an issue in the repository.