import os
from datetime import datetime
from werkzeug.utils import secure_filename
from modules.validators import FileValidator, ValidationFactory
from modules.session_manager import session_manager


class UploadError(Exception):
    """Custom exception for upload-related errors"""
    pass


class FileUploadHandler:
    """
    Main handler for file upload operations.
    Coordinates file saving, validation, and metadata management.
    """
    
    @staticmethod
    def process_upload(file, session_id):
        """
        Process an uploaded file
        
        Args:
            file: FileStorage object from Flask request
            session_id (str): Session identifier
            
        Returns:
            tuple: (file_info dict or None, message str)
            
        Raises:
            UploadError: If upload processing fails
        """
        try:
            # Validate session exists
            if not session_manager.session_exists(session_id):
                raise UploadError("Invalid session ID")
            
            # Secure the filename
            filename = secure_filename(file.filename)
            if not filename:
                raise UploadError("Invalid filename")
            
            # Determine file type
            file_type = FileValidator.get_file_type(filename)
            if not file_type:
                raise UploadError("Unsupported file type")
            
            file_ext = filename.rsplit('.', 1)[1].lower()
            
            # Get session directory
            session_dir = session_manager.get_session_dir(session_id)
            if not session_dir:
                raise UploadError("Session directory not found")
            
            # Save file
            filepath = os.path.join(session_dir, filename)
            file.save(filepath)
            
            # Validate file
            is_valid, validation_message = ValidationFactory.validate(
                filepath, file_type, file_ext
            )
            
            if not is_valid:
                # Clean up invalid file
                os.remove(filepath)
                raise UploadError(validation_message)
            
            # Create file metadata
            file_info = FileMetadata.create(
                filename=filename,
                filepath=filepath,
                file_type=file_type,
                file_ext=file_ext,
                validation_message=validation_message
            )
            
            # Add to session
            session = session_manager.get_session(session_id)
            session.add_file(file_info)
            
            return file_info, "File uploaded successfully"
            
        except UploadError as e:
            return None, str(e)
        except Exception as e:
            # Clean up file if it was saved
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            return None, f"Upload failed: {str(e)}"
    
    @staticmethod
    def get_file_path(session_id, filename):
        """
        Get the full path to an uploaded file
        
        Args:
            session_id (str): Session identifier
            filename (str): Name of the file
            
        Returns:
            str or None: Full file path if exists, None otherwise
        """
        session_dir = session_manager.get_session_dir(session_id)
        if not session_dir:
            return None
        
        filepath = os.path.join(session_dir, filename)
        return filepath if os.path.exists(filepath) else None
    
    @staticmethod
    def delete_file(session_id, filename):
        """
        Delete a specific file from a session
        
        Args:
            session_id (str): Session identifier
            filename (str): Name of the file to delete
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            filepath = FileUploadHandler.get_file_path(session_id, filename)
            if not filepath:
                return False, "File not found"
            
            os.remove(filepath)
            
            # Update session file list
            session = session_manager.get_session(session_id)
            if session:
                session.files = [f for f in session.files if f['filename'] != filename]
            
            return True, "File deleted successfully"
            
        except Exception as e:
            return False, f"Failed to delete file: {str(e)}"


class FileMetadata:
    """
    Helper class for creating and managing file metadata
    """
    
    @staticmethod
    def create(filename, filepath, file_type, file_ext, validation_message):
        """
        Create a file metadata dictionary
        
        Args:
            filename (str): Original filename
            filepath (str): Full path to saved file
            file_type (str): Type of file ('tabular' or 'image')
            file_ext (str): File extension
            validation_message (str): Validation result message
            
        Returns:
            dict: File metadata
        """
        return {
            'filename': filename,
            'filepath': filepath,
            'file_type': file_type,
            'file_ext': file_ext,
            'uploaded_at': datetime.now().isoformat(),
            'validation_message': validation_message,
            'file_size': os.path.getsize(filepath)
        }
    
    @staticmethod
    def to_response_format(file_info):
        """
        Convert file metadata to API response format
        (excludes sensitive information like full filepath)
        
        Args:
            file_info (dict): Full file metadata
            
        Returns:
            dict: Sanitized file info for API response
        """
        return {
            'filename': file_info['filename'],
            'file_type': file_info['file_type'],
            'file_ext': file_info['file_ext'],
            'uploaded_at': file_info['uploaded_at'],
            'validation_message': file_info['validation_message'],
            'file_size': file_info.get('file_size', 0)
        }