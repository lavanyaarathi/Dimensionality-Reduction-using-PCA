import pandas as pd
from PIL import Image
from config import Config


class FileValidator:
    """
    Main validator class that provides static methods for file validation.
    Designed to be easily extensible with new validation methods.
    """
    
    @staticmethod
    def allowed_file(filename, file_type='all'):
        """
        Check if file extension is allowed
        
        Args:
            filename (str): Name of the file to validate
            file_type (str): Type filter - 'all', 'tabular', or 'image'
            
        Returns:
            bool: True if file extension is allowed, False otherwise
        """
        if '.' not in filename:
            return False
        
        ext = filename.rsplit('.', 1)[1].lower()
        
        if file_type == 'all':
            all_extensions = (Config.ALLOWED_EXTENSIONS['tabular'] | 
                            Config.ALLOWED_EXTENSIONS['image'])
            return ext in all_extensions
        
        return ext in Config.ALLOWED_EXTENSIONS.get(file_type, set())
    
    @staticmethod
    def get_file_type(filename):
        """
        Determine the type of file based on extension
        
        Args:
            filename (str): Name of the file
            
        Returns:
            str or None: 'tabular', 'image', or None if unsupported
        """
        if '.' not in filename:
            return None
        
        ext = filename.rsplit('.', 1)[1].lower()
        
        if ext in Config.ALLOWED_EXTENSIONS['tabular']:
            return 'tabular'
        elif ext in Config.ALLOWED_EXTENSIONS['image']:
            return 'image'
        
        return None


class TabularValidator:
    """Validator for tabular data files (CSV, Excel)"""
    
    @staticmethod
    def validate_csv(filepath):
        """
        Validate CSV file structure and content
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            df = pd.read_csv(filepath)
            
            if df.empty:
                return False, "CSV file is empty"
            
            if df.shape[0] < Config.MIN_TABULAR_ROWS:
                return False, f"CSV must have at least {Config.MIN_TABULAR_ROWS} rows"
            
            # Additional validation: check for all NaN columns
            all_nan_cols = df.columns[df.isna().all()].tolist()
            if all_nan_cols:
                return False, f"CSV has columns with all NaN values: {all_nan_cols}"
            
            return True, f"Valid CSV with {df.shape[0]} rows and {df.shape[1]} columns"
            
        except pd.errors.EmptyDataError:
            return False, "CSV file is empty"
        except pd.errors.ParserError as e:
            return False, f"CSV parsing error: {str(e)}"
        except Exception as e:
            return False, f"Invalid CSV format: {str(e)}"
    
    @staticmethod
    def validate_excel(filepath):
        """
        Validate Excel file structure and content
        
        Args:
            filepath (str): Path to the Excel file
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            df = pd.read_excel(filepath)
            
            if df.empty:
                return False, "Excel file is empty"
            
            if df.shape[0] < Config.MIN_TABULAR_ROWS:
                return False, f"Excel must have at least {Config.MIN_TABULAR_ROWS} rows"
            
            # Additional validation: check for all NaN columns
            all_nan_cols = df.columns[df.isna().all()].tolist()
            if all_nan_cols:
                return False, f"Excel has columns with all NaN values: {all_nan_cols}"
            
            return True, f"Valid Excel with {df.shape[0]} rows and {df.shape[1]} columns"
            
        except Exception as e:
            return False, f"Invalid Excel format: {str(e)}"


class ImageValidator:
    """Validator for image files (JPG, PNG)"""
    
    @staticmethod
    def validate_image(filepath):
        """
        Validate image file format and dimensions
        
        Args:
            filepath (str): Path to the image file
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            # Open and verify the image
            img = Image.open(filepath)
            img.verify()  # Verify it's a valid image
            
            # Reopen after verify (verify closes the file)
            img = Image.open(filepath)
            width, height = img.size
            
            # Validate dimensions
            if width < Config.MIN_IMAGE_DIMENSION or height < Config.MIN_IMAGE_DIMENSION:
                return False, (f"Image dimensions too small "
                             f"(minimum {Config.MIN_IMAGE_DIMENSION}x{Config.MIN_IMAGE_DIMENSION})")
            
            if width > Config.MAX_IMAGE_DIMENSION or height > Config.MAX_IMAGE_DIMENSION:
                return False, (f"Image dimensions too large "
                             f"(maximum {Config.MAX_IMAGE_DIMENSION}x{Config.MAX_IMAGE_DIMENSION})")
            
            # Check if image is RGB or can be converted
            if img.mode not in ['RGB', 'L', 'RGBA']:
                return False, f"Unsupported image mode: {img.mode}. Expected RGB, RGBA, or grayscale"
            
            return True, f"Valid image: {width}x{height} pixels, mode: {img.mode}"
            
        except FileNotFoundError:
            return False, "Image file not found"
        except Image.UnidentifiedImageError:
            return False, "File is not a valid image"
        except Exception as e:
            return False, f"Invalid image format: {str(e)}"


class ValidationFactory:
    """
    Factory class to get appropriate validator based on file type.
    Makes it easy to extend with new file types.
    """
    
    @staticmethod
    def validate(filepath, file_type, file_ext):
        """
        Validate file based on its type
        
        Args:
            filepath (str): Path to the file
            file_type (str): Type of file ('tabular' or 'image')
            file_ext (str): File extension
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        if file_type == 'tabular':
            if file_ext == 'csv':
                return TabularValidator.validate_csv(filepath)
            else:  # xlsx, xls
                return TabularValidator.validate_excel(filepath)
        elif file_type == 'image':
            return ImageValidator.validate_image(filepath)
        else:
            return False, f"Unsupported file type: {file_type}"