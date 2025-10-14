"""
Main Flask Application for RIDRT
Integrates File Upload and Preprocessing Modules
"""

from flask import Flask, render_template
from config import Config
from routes.upload_routes import upload_bp
from routes.preprocessing_routes import preprocess_bp
from routes.visualization_routes import visualization_bp
from routes.pca_routes import pca_bp

from utils.cleanup import start_cleanup_thread
import os

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(preprocess_bp)
    app.register_blueprint(visualization_bp)
    app.register_blueprint(pca_bp)
    
    # Start background cleanup thread
    start_cleanup_thread()
    
    # Main route
    @app.route('/')
    def index():
        """Render main page"""
        return render_template('index.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
