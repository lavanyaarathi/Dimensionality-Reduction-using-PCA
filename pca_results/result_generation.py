import numpy as np

def generate_results(data_matrix: np.ndarray, pca_output: np.ndarray, eigenpairs: dict, k: int, 
                    is_image: bool = False, image_shape: tuple = None) -> dict:
    """
    Generate reconstructed data and PCA metrics.
    
    Parameters:
        data_matrix (np.ndarray): Original normalized data of shape (n_samples, n_features).
        pca_output (np.ndarray): Reduced dimensional data of shape (n_samples, k).
        eigenpairs (dict): Dictionary with keys "eigenvalues" and "eigenvectors".
        k (int): Number of components used.
        is_image (bool): Flag indicating if data is an image (requires reshaping).
        image_shape (tuple, optional): Shape of original image (height, width, channels).
    
    Returns:
        dict: {
            "reconstructed": np.ndarray,
            "explained_variance_ratio": np.ndarray,
            "reconstruction_error": float
        }
    
    Raises:
        ValueError: If inputs are invalid or computation fails.
    """
    # Input validation
    if not isinstance(data_matrix, np.ndarray) or data_matrix.ndim != 2:
        raise ValueError("data_matrix must be a 2D NumPy array")
    if not isinstance(pca_output, np.ndarray) or pca_output.ndim != 2:
        raise ValueError("pca_output must be a 2D NumPy array")
    if not isinstance(eigenpairs, dict) or "eigenvalues" not in eigenpairs or "eigenvectors" not in eigenpairs:
        raise ValueError("eigenpairs must be a dict with 'eigenvalues' and 'eigenvectors'")
    if pca_output.shape[1] != k or eigenpairs["eigenvectors"].shape[1] < k:
        raise ValueError("Inconsistent dimensions for k, pca_output, or eigenvectors")
    if is_image and (image_shape is None or len(image_shape) != 3):
        raise ValueError("image_shape must be provided as (height, width, channels) for image data")

    try:
        eigenvectors_k = eigenpairs["eigenvectors"][:, :k]
        # Reconstruct from reduced data
        reconstructed = np.dot(pca_output, eigenvectors_k.T)
        
        # For images, reshape and clip to valid pixel range
        if is_image:
            reconstructed = reconstructed.reshape(-1, *image_shape)
            reconstructed = np.clip(reconstructed, 0, 255)
        
        # Calculate explained variance ratio
        total_variance = np.sum(eigenpairs["eigenvalues"])
        if total_variance == 0:
            raise ValueError("Total variance is zero, cannot compute explained variance ratio")
        explained_variance_ratio = eigenpairs["eigenvalues"][:k] / total_variance
        
        # Calculate reconstruction error (Mean Squared Error)
        reconstruction_error = np.mean((data_matrix - reconstructed) ** 2)
        
        results = {
            "reconstructed": reconstructed,
            "explained_variance_ratio": explained_variance_ratio,
            "reconstruction_error": reconstruction_error
        }
        
        return results
    
    except Exception as e:
        raise ValueError(f"Result generation failed: {str(e)}")