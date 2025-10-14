# routes/upload_routes.py

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

# Fix the import to match your actual module name
from modules.preprocessing import PreprocessingModule
from modules.session_manager import session_manager
from modules.upload_handler import FileUploadHandler, FileMetadata
from modules.validators import FileValidator, ValidationFactory
from utils.cleanup import get_cleanup_status


upload_bp = Blueprint('upload', __name__, url_prefix='/api')

@upload_bp.route('/session/create', methods=['POST'])
def create_session():
    """
    Create a new upload session
    
    Returns:
        JSON response with session_id
    """
    try:
        session_id = session_manager.create_session()
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Session created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create session: {str(e)}'
        }), 500


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload
    
    Expected form data:
        - file: The file to upload
        - session_id: Valid session identifier
    
    Returns:
        JSON response with file information or error
    """
    # Validate session_id
    session_id = request.form.get('session_id')
    if not session_id:
        return jsonify({
            'success': False,
            'error': 'session_id is required'
        }), 400
    
    if not session_manager.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session_id'
        }), 400
    
    # Validate file presence
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided in request'
        }), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Validate file extension
    if not FileValidator.allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'File type not allowed. Supported: CSV, XLSX, XLS, JPG, PNG'
        }), 400
    
    # Process upload
    file_info, message = FileUploadHandler.process_upload(file, session_id)
    
    if file_info is None:
        return jsonify({
            'success': False,
            'error': message
        }), 400
    
    return jsonify({
        'success': True,
        'message': message,
        'file_info': FileMetadata.to_response_format(file_info)
    }), 200


@upload_bp.route('/session/<session_id>/files', methods=['GET'])
def get_session_files(session_id):
    """
    Get all files in a session
    
    Args:
        session_id: Session identifier from URL
    
    Returns:
        JSON response with list of files
    """
    if not session_manager.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session'
        }), 404
    
    session = session_manager.get_session(session_id)
    files = [FileMetadata.to_response_format(f) for f in session.get_files()]
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'files': files,
        'count': len(files)
    }), 200


@upload_bp.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """
    Delete a session and all its files
    
    Args:
        session_id: Session identifier from URL
    
    Returns:
        JSON response confirming deletion
    """
    if not session_manager.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session'
        }), 404
    
    success = session_manager.delete_session(session_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Session and all files deleted successfully'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to delete session'
        }), 500


@upload_bp.route('/session/<session_id>/file/<filename>', methods=['DELETE'])
def delete_file(session_id, filename):
    """
    Delete a specific file from a session
    
    Args:
        session_id: Session identifier from URL
        filename: Name of file to delete from URL
    
    Returns:
        JSON response confirming deletion
    """
    if not session_manager.session_exists(session_id):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired session'
        }), 404
    
    success, message = FileUploadHandler.delete_file(session_id, filename)
    
    if success:
        return jsonify({
            'success': True,
            'message': message
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': message
        }), 404


@upload_bp.route('/sessions', methods=['GET'])
def get_all_sessions():
    """
    Get information about all active sessions
    (Admin/Debug endpoint)
    
    Returns:
        JSON response with list of sessions
    """
    sessions = session_manager.get_all_sessions()
    
    return jsonify({
        'success': True,
        'sessions': sessions,
        'count': len(sessions)
    }), 200


@upload_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get system status information
    (Health check and monitoring endpoint)
    
    Returns:
        JSON response with system status
    """
    cleanup_status = get_cleanup_status()
    
    return jsonify({
        'success': True,
        'status': 'operational',
        'active_sessions': session_manager.get_session_count(),
        'cleanup_thread': cleanup_status
    }), 200


# Error handlers for the blueprint
@upload_bp.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeded error"""
    return jsonify({
        'success': False,
        'error': 'File size exceeds maximum allowed size (16MB)'
    }), 413


@upload_bp.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error occurred'
    }), 500