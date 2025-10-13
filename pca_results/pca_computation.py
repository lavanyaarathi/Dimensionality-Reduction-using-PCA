import numpy as np

def run_pca(data_matrix: np.ndarray, k: int = None, variance_threshold: float = None) -> tuple:
    """
    Perform PCA on normalized data matrix.
    
    Parameters:
        data_matrix (np.ndarray): Normalized data of shape (n_samples, n_features).
        k (int, optional): Number of principal components to keep. Ignored if variance_threshold is set.
        variance_threshold (float, optional): Cumulative variance ratio to determine k (e.g., 0.95).
    
    Returns:
        tuple: (pca_output, eigenpairs)
            - pca_output (np.ndarray): Transformed data in reduced dimensions.
            - eigenpairs (dict): {"eigenvalues": np.ndarray, "eigenvectors": np.ndarray}
    
    Raises:
        ValueError: If inputs are invalid or computation fails.
    """
    # Input validation
    if not isinstance(data_matrix, np.ndarray) or data_matrix.ndim != 2:
        raise ValueError("data_matrix must be a 2D NumPy array")
    n_samples, n_features = data_matrix.shape
    if n_samples == 0 or n_features == 0:
        raise ValueError("data_matrix cannot be empty")
    
    # Check k or variance_threshold
    if k is None and variance_threshold is None:
        raise ValueError("Either k or variance_threshold must be provided")
    if k is not None and (not isinstance(k, int) or k <= 0 or k > n_features):
        raise ValueError(f"k must be an integer between 1 and {n_features}")
    if variance_threshold is not None and (variance_threshold <= 0 or variance_threshold > 1):
        raise ValueError("variance_threshold must be between 0 and 1")

    try:
        # Step 1: Covariance matrix
        covariance_matrix = np.cov(data_matrix, rowvar=False)
        
        # Step 2: Eigen decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        
        # Step 3: Sort eigenvalues (descending order)
        sorted_idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_idx]
        eigenvectors = eigenvectors[:, sorted_idx]
        
        # Step 4: Determine k if variance_threshold is provided
        if variance_threshold is not None:
            cumulative_variance = np.cumsum(eigenvalues) / np.sum(eigenvalues)
            k = np.searchsorted(cumulative_variance, variance_threshold) + 1
        
        # Step 5: Select top-k eigenvectors
        eigenvectors_k = eigenvectors[:, :k]
        
        # Step 6: Project data into reduced subspace
        pca_output = np.dot(data_matrix, eigenvectors_k)
        
        eigenpairs = {
            "eigenvalues": eigenvalues,
            "eigenvectors": eigenvectors
        }
        
        return pca_output, eigenpairs
    
    except np.linalg.LinAlgError as e:
        raise ValueError(f"PCA computation failed: {str(e)}")

def run_pca_svd(data_matrix: np.ndarray, k: int = None, variance_threshold: float = None) -> tuple:
    """
    Perform PCA using SVD for efficiency.
    """
    # Center the data
    data_centered = data_matrix - np.mean(data_matrix, axis=0)
    # SVD
    U, S, Vt = np.linalg.svd(data_centered, full_matrices=False)
    eigenvalues = S**2 / (data_matrix.shape[0] - 1)
    eigenvectors = Vt.T
    # Determine k
    if variance_threshold is not None:
        cumulative_variance = np.cumsum(eigenvalues) / np.sum(eigenvalues)
        k = np.searchsorted(cumulative_variance, variance_threshold) + 1
    # Project data
    pca_output = U[:, :k] @ np.diag(S[:k])
    eigenpairs = {"eigenvalues": eigenvalues, "eigenvectors": eigenvectors}
    return pca_output, eigenpairs