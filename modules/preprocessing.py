import numpy as np
import pandas as pd
from PIL import Image
import os

class PreprocessingModule:
    def __init__(self):
        pass

    def detect_file_type(self, filename):
        filename = filename.lower()
        if filename.endswith(('.csv', '.xlsx')):
            return "tabular"
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            return "image"
        else:
            raise ValueError("Unsupported file type")

    def process_file(self, filepath):
        file_type = self.detect_file_type(filepath)
        if file_type == "tabular":
            return self._process_tabular(filepath)
        else:
            return self._process_image(filepath)

    def _process_tabular(self, filepath):
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        df = df.dropna()
        numeric_df = df.select_dtypes(include=np.number)
        normalized = (numeric_df - numeric_df.mean()) / numeric_df.std()

        return {
            "type": "tabular",
            "original_head": df.head().to_html(classes="data-table"),
            "normalized_head": normalized.head().to_html(classes="data-table")
        }

    def _process_image(self, filepath, resize_shape=(128, 128)):
        img = Image.open(filepath).convert("RGB")
        img_resized = img.resize(resize_shape)
        img_array = np.asarray(img_resized, dtype=np.float32) / 255.0
        vectorized = img_array.reshape(-1, 3)

        return {
            "type": "image",
            "original": filepath,
            "resized": img_resized,
            "shape": vectorized.shape
        }
