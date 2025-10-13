import os
import urllib.request
from PIL import Image

# Create sample_data directory
os.makedirs('sample_data', exist_ok=True)

def download_iris_dataset():
    """Download the famous Iris dataset from UCI repository"""
    print("Downloading Iris dataset...")
    
    url = "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/iris.csv"
    output_file = 'sample_data/iris.csv'
    
    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"✓ Downloaded iris.csv (150 samples, 4 features)")
        print(f"  Features: sepal_length, sepal_width, petal_length, petal_width")
        print(f"  Classes: setosa, versicolor, virginica")
        return True
    except Exception as e:
        print(f"✗ Failed to download Iris dataset: {e}")
        print("  You can manually download from: https://archive.ics.uci.edu/dataset/53/iris")
        return False


def download_sample_images():
    """Download sample RGB images for PCA testing"""
    print("\nDownloading sample RGB images...")
    
    images = [
        {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/481px-Cat03.jpg',
            'name': 'cat.jpg',
            'description': 'Cat image (481×361 RGB)'
        },
        {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png',
            'name': 'butterfly.png',
            'description': 'Butterfly image (280×280 RGB)'
        }
    ]
    
    success_count = 0
    
    for img_info in images:
        try:
            output_file = f"sample_data/{img_info['name']}"
            urllib.request.urlretrieve(img_info['url'], output_file)
            
            # Verify it's a valid image and convert to RGB if needed
            img = Image.open(output_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                img.save(output_file)
            
            print(f"✓ Downloaded {img_info['name']} - {img_info['description']}")
            success_count += 1
        except Exception as e:
            print(f"✗ Failed to download {img_info['name']}: {e}")
    
    return success_count > 0


def use_fallback_image():
    """Use a real fallback image instead of generating one"""
    print("\nUsing local fallback image instead of generating synthetic one...")
    
    fallback_path = 'sample_data/flower.png'
    if os.path.exists(fallback_path):
        try:
            img = Image.open(fallback_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                img.save(fallback_path)
            print(f"✓ Found and verified fallback image: {img.size[0]}×{img.size[1]} RGB")
            return True
        except Exception as e:
            print(f"⚠ Fallback image exists but could not be opened: {e}")
            return False
    else:
        print("✗ Fallback image 'flower.png' not found in sample_data/.")
        print("  Please place a small RGB image named 'flower.png' in sample_data/ folder.")
        return False


def verify_datasets():
    """Verify all datasets are present and valid"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    files_to_check = {
        'sample_data/iris.csv': 'Tabular dataset',
        'sample_data/cat.jpg': 'RGB image 1',
        'sample_data/butterfly.png': 'RGB image 2',
        'sample_data/flower.png': 'Fallback image'
    }
    
    for filepath, description in files_to_check.items():
        if os.path.exists(filepath):
            if filepath.endswith('.csv'):
                try:
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                        print(f"✓ {description}: {len(lines)-1} rows")
                except Exception as e:
                    print(f"⚠ {description}: could not read CSV ({e})")
            else:
                try:
                    img = Image.open(filepath)
                    print(f"✓ {description}: {img.size[0]}×{img.size[1]} {img.mode}")
                except Exception as e:
                    print(f"⚠ {description}: exists but may be corrupted ({e})")
        else:
            print(f"✗ {description}: not found")


def main():
    print("\n" + "="*60)
    print("REAL DATASET DOWNLOADER FOR PCA MODULE")
    print("="*60 + "\n")
    
    iris_success = download_iris_dataset()
    images_success = download_sample_images()
    
    # If image downloads fail, use local fallback image
    if not images_success:
        print("\nImage downloads failed. Falling back to local image...")
        use_fallback_image()
    else:
        # Also verify fallback exists for consistency
        use_fallback_image()
    
    verify_datasets()
    
    print("\n" + "="*60)
    if iris_success:
        print("✅ Dataset download complete!")
        print("\nDatasets available in sample_data/ folder:")
        print("  - iris.csv (tabular data for PCA)")
        print("  - cat.jpg / butterfly.png / flower.png (RGB images for PCA)")
    else:
        print("⚠ Some downloads failed.")
        print("\nManual download instructions:")
        print("1. Iris dataset: https://archive.ics.uci.edu/dataset/53/iris")
        print("2. Or use any small CSV with numeric columns")
        print("3. Add any JPG/PNG images to sample_data/ folder")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
