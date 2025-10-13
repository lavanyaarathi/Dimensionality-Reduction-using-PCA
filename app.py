from flask import Flask, render_template
from config import Config
from routes.upload_routes import upload_bp
from utils.cleanup import start_cleanup_thread
import os

def create_app(config_class=Config):
    """
    Application factory pattern for Flask app creation
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(upload_bp)
    
    # Start background cleanup thread
    start_cleanup_thread()
    
    # Main route
    @app.route('/')
    def index():
        """Render main page"""
        return render_template('index.html')
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)