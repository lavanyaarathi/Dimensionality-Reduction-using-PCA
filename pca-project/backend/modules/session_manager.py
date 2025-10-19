"""
Session management module for PCA project.
Handles user sessions, file tracking, and cleanup.
"""

import os
import uuid
from datetime import datetime

from config import Config


class Session:
    """
    Represents a single user session with metadata and file tracking
    """
    
    def __init__(self, session_id, directory):
        """
        Initialize a new session
        
        Args:
            session_id (str): Unique session identifier
            directory (str): Path to session directory
        """
        self.session_id = session_id
        self.directory = directory
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.files = []
        self.pca_results = {}
    
    def update_access_time(self):
        """Update the last accessed timestamp"""
        self.last_accessed = datetime.now()
    
    def add_file(self, file_info):
        """
        Add file information to session
        
        Args:
            file_info (dict): File metadata dictionary
        """
        self.files.append(file_info)
    
    def get_files(self):
        """
        Get all files in the session
        
        Returns:
            list: List of file information dictionaries
        """
        return self.files

    def set_pca_result(self, filename, result_dict):
        """
        Store PCA results for a given filename in this session.
        """
        self.pca_results[filename] = result_dict

    def get_pca_result(self, filename):
        """
        Retrieve PCA results for a given filename.
        """
        return self.pca_results.get(filename)
    
    def is_expired(self):
        """
        Check if session has expired
        
        Returns:
            bool: True if session is expired, False otherwise
        """
        elapsed = (datetime.now() - self.last_accessed).total_seconds()
        return elapsed > Config.SESSION_TIMEOUT
    
    def to_dict(self):
        """
        Convert session to dictionary format
        
        Returns:
            dict: Session information
        """
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'files_count': len(self.files)
        }


class SessionManager:
    """
    Manages all user sessions in the application.
    Implements singleton pattern to ensure single instance.
    """
    
    _instance = None
    _sessions = {}
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize session manager"""
        if not hasattr(self, 'initialized'):
            self._sessions = {}
            self.initialized = True

    def _ensure_session_loaded(self, session_id):
        """Load a session from disk if it exists but isn't in memory."""
        try:
            if session_id in self._sessions:
                return
            session_dir = os.path.join(Config.UPLOAD_FOLDER, session_id)
            if os.path.isdir(session_dir):
                self._sessions[session_id] = Session(session_id, session_dir)
        except Exception:
            # Ignore errors silently; session will be treated as non-existent
            pass

    def create_session(self):
        """
        Create a new session with unique ID and directory
        
        Returns:
            str: Session ID
        """
        session_id = str(uuid.uuid4())
        session_dir = os.path.join(Config.UPLOAD_FOLDER, session_id)
        
        # Create session directory
        os.makedirs(session_dir, exist_ok=True)
        
        # Create session object
        session = Session(session_id, session_dir)
        self._sessions[session_id] = session
        
        return session_id
    
    def get_session(self, session_id):
        """
        Get session by ID and update access time
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            Session or None: Session object if found, None otherwise
        """
        self._ensure_session_loaded(session_id)
        session = self._sessions.get(session_id)
        if session:
            session.update_access_time()
        return session
    
    def get_session_dir(self, session_id):
        """
        Get session directory path
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            str or None: Directory path if session exists, None otherwise
        """
        session = self.get_session(session_id)
        return session.directory if session else None
    
    def session_exists(self, session_id):
        """
        Check if session exists
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            bool: True if session exists, False otherwise
        """
        self._ensure_session_loaded(session_id)
        return session_id in self._sessions
    
    def delete_session(self, session_id):
        """
        Delete a session and all associated files
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            bool: True if session was deleted, False if not found
        """
        if session_id not in self._sessions:
            return False
        
        session = self._sessions[session_id]
        session_dir = session.directory
        
        # Delete all files in session directory
        if os.path.exists(session_dir):
            try:
                for file in os.listdir(session_dir):
                    file_path = os.path.join(session_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                
                # Remove directory
                os.rmdir(session_dir)
            except Exception as e:
                print(f"Error deleting session {session_id}: {e}")
                return False
        
        # Remove from sessions dictionary
        del self._sessions[session_id]
        return True
    
    def cleanup_expired_sessions(self):
        """
        Remove all expired sessions
        
        Returns:
            int: Number of sessions cleaned up
        """
        expired_sessions = []
        
        # Find expired sessions
        for session_id, session in self._sessions.items():
            if session.is_expired():
                expired_sessions.append(session_id)
        
        # Delete expired sessions
        cleaned_count = 0
        for session_id in expired_sessions:
            if self.delete_session(session_id):
                cleaned_count += 1
        
        if cleaned_count > 0:
            print(f"Cleaned up {cleaned_count} expired session(s)")
        
        return cleaned_count
    
    def get_all_sessions(self):
        """
        Get information about all active sessions
        
        Returns:
            list: List of session information dictionaries
        """
        return [session.to_dict() for session in self._sessions.values()]
    
    def get_session_count(self):
        """
        Get total number of active sessions
        
        Returns:
            int: Number of active sessions
        """
        return len(self._sessions)


# Create singleton instance
session_manager = SessionManager()
