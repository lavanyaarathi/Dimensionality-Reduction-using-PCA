import threading
import time
from config import Config
from modules.session_manager import session_manager


class CleanupThread:
    """
    Background thread for automatic session cleanup
    """
    
    def __init__(self):
        """Initialize cleanup thread"""
        self.thread = None
        self.running = False
    
    def start(self):
        """Start the cleanup thread"""
        if self.running:
            print("Cleanup thread already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.thread.start()
        print("Cleanup thread started")
    
    def stop(self):
        """Stop the cleanup thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Cleanup thread stopped")
    
    def _cleanup_loop(self):
        """Main cleanup loop that runs periodically"""
        while self.running:
            try:
                # Run cleanup
                session_manager.cleanup_expired_sessions()
                
                # Sleep for configured interval
                time.sleep(Config.CLEANUP_INTERVAL)
                
            except Exception as e:
                print(f"Error in cleanup thread: {e}")
                # Continue running even if there's an error
                time.sleep(Config.CLEANUP_INTERVAL)


# Global cleanup thread instance
_cleanup_thread = CleanupThread()


def start_cleanup_thread():
    """
    Start the background cleanup thread
    Should be called once during application initialization
    """
    _cleanup_thread.start()


def stop_cleanup_thread():
    """
    Stop the background cleanup thread
    Can be called during application shutdown
    """
    _cleanup_thread.stop()


def get_cleanup_status():
    """
    Get the status of the cleanup thread
    
    Returns:
        dict: Status information
    """
    return {
        'running': _cleanup_thread.running,
        'interval_seconds': Config.CLEANUP_INTERVAL,
        'session_timeout_seconds': Config.SESSION_TIMEOUT
    }