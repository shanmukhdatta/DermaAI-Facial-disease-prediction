"""
preprocessor.py - Image validation and preprocessing pipeline
"""

import cv2
import numpy as np
from PIL import Image
from typing import Dict, Tuple, Any


# ── Thresholds ────────────────────────────────────────────────────────────────
BRIGHTNESS_MIN = 50     # Too dark below this
BRIGHTNESS_MAX = 230    # Too bright / washed out above this
BLUR_THRESHOLD = 80     # Laplacian variance below = blurry
MIN_SKIN_RATIO  = 0.05  # At least 5% of image should look like skin


class ImagePreprocessor:
    """Validates and preprocesses skin images before model inference."""

    # ── Validation ────────────────────────────────────────────────────────────
    def validate_image(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Run all quality checks on a raw RGB numpy image.
        Returns a dict with 'passed' bool and per-check details.
        """
        checks = {}

        checks["brightness"] = self._check_brightness(image)
        checks["blur"]       = self._check_blur(image)
        checks["skin"]       = self._check_skin_region(image)
        checks["resolution"] = self._check_resolution(image)

        all_passed = all(c["passed"] for c in checks.values())

        return {
            "passed": all_passed,
            "checks": checks,
        }

    def _check_brightness(self, img: np.ndarray) -> dict:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mean_brightness = float(gray.mean())

        if mean_brightness < BRIGHTNESS_MIN:
            return {"passed": False, "msg": f"Too dark ({mean_brightness:.0f}/255). Use better lighting.", "value": mean_brightness}
        if mean_brightness > BRIGHTNESS_MAX:
            return {"passed": False, "msg": f"Too bright/overexposed ({mean_brightness:.0f}/255).", "value": mean_brightness}
        return {"passed": True, "msg": f"Brightness OK ({mean_brightness:.0f}/255)", "value": mean_brightness}

    def _check_blur(self, img: np.ndarray) -> dict:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        if lap_var < BLUR_THRESHOLD:
            return {"passed": False, "msg": f"Image too blurry (score: {lap_var:.1f}). Hold camera steady.", "value": lap_var}
        return {"passed": True, "msg": f"Focus OK (score: {lap_var:.1f})", "value": lap_var}

    def _check_skin_region(self, img: np.ndarray) -> dict:
        """HSV-based skin pixel detection."""
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # Skin hue range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([25, 255, 255], dtype=np.uint8)
        mask1 = cv2.inRange(hsv, lower_skin, upper_skin)

        lower_skin2 = np.array([160, 20, 70], dtype=np.uint8)
        upper_skin2 = np.array([180, 255, 255], dtype=np.uint8)
        mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)

        mask = cv2.bitwise_or(mask1, mask2)
        skin_ratio = float(mask.sum()) / (255 * img.shape[0] * img.shape[1])

        if skin_ratio < MIN_SKIN_RATIO:
            return {
                "passed": False,
                "msg": f"Low skin area detected ({skin_ratio*100:.1f}%). Center the skin region.",
                "value": skin_ratio
            }
        return {"passed": True, "msg": f"Skin region OK ({skin_ratio*100:.1f}%)", "value": skin_ratio}

    def _check_resolution(self, img: np.ndarray) -> dict:
        h, w = img.shape[:2]
        if h < 64 or w < 64:
            return {"passed": False, "msg": f"Image too small ({w}x{h}). Minimum 64x64.", "value": min(h, w)}
        return {"passed": True, "msg": f"Resolution OK ({w}x{h})", "value": min(h, w)}

    # ── Preprocessing for each model type ────────────────────────────────────
    def preprocess_for_cnn(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int] = (224, 224),
        normalize: bool = True
    ) -> np.ndarray:
        """Resize + normalize for CNN models (MobileNetV2, AlexNet, LeNet)."""
        resized = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        arr = resized.astype(np.float32)
        if normalize:
            arr /= 255.0
        return np.expand_dims(arr, axis=0)  # (1, H, W, 3)

    def preprocess_for_sklearn(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int] = (64, 64),
        scaler=None
    ) -> np.ndarray:
        """
        Flatten + optionally scale for SVM/RF models.
        Feature vector = HOG-like flattened normalized pixels.
        """
        resized = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        features = resized.flatten().astype(np.float32) / 255.0
        features = features.reshape(1, -1)

        if scaler is not None:
            try:
                features = scaler.transform(features)
            except Exception:
                pass  # Proceed without scaling if shape mismatch
        return features

    def extract_hog_features(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int] = (128, 128)
    ) -> np.ndarray:
        """Extract HOG features for sklearn models as alternative feature set."""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        resized = cv2.resize(gray, target_size)

        win_size = target_size
        block_size = (16, 16)
        block_stride = (8, 8)
        cell_size = (8, 8)
        nbins = 9

        hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
        features = hog.compute(resized).flatten()
        return features.reshape(1, -1).astype(np.float32)
