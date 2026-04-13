"""
predictor.py - Ensemble prediction engine
"""

import numpy as np
import logging
from typing import Dict, List, Any, Optional

from model_loader import ModelManager, CLASS_NAMES, NUM_CLASSES, MODEL_WEIGHTS
from preprocessor import ImagePreprocessor

logger = logging.getLogger(__name__)

# CNN input sizes per model
CNN_INPUT_SIZES = {
    "MobileNetV2":     (224, 224),
    "MobileNetV2_fin": (224, 224),
    "MobileNetV2_p1":  (224, 224),
    "AlexNet":         (227, 227),
    "LeNet":           (32, 32),
}


class EnsemblePredictor:
    """Runs all loaded models and fuses predictions via weighted voting."""

    def __init__(self, model_manager: ModelManager):
        self.manager = model_manager
        self.preprocessor = ImagePreprocessor()

    def predict(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Main entry point. Returns dict with:
          - top_class: str
          - confidence: float (0-1)
          - top3: list of (class, prob) tuples
          - all_probs: np.ndarray of shape (NUM_CLASSES,)
          - models_used: list of model names
        """
        weighted_probs = np.zeros(NUM_CLASSES, dtype=np.float64)
        total_weight = 0.0
        models_used = []

        # ── SVM models ────────────────────────────────────────────
        for key in ["BEST_SVM", "SVM"]:
            if self.manager.is_loaded(key):
                probs = self._predict_sklearn(key, image)
                if probs is not None:
                    w = MODEL_WEIGHTS[key]
                    weighted_probs += w * probs
                    total_weight += w
                    models_used.append(key)

        # ── Random Forest ─────────────────────────────────────────
        if self.manager.is_loaded("RandomForest"):
            probs = self._predict_sklearn("RandomForest", image)
            if probs is not None:
                w = MODEL_WEIGHTS["RandomForest"]
                weighted_probs += w * probs
                total_weight += w
                models_used.append("RandomForest")

        # ── CNN models ────────────────────────────────────────────
        for key in ["MobileNetV2", "MobileNetV2_fin", "MobileNetV2_p1", "AlexNet", "LeNet"]:
            if self.manager.is_loaded(key):
                probs = self._predict_cnn(key, image)
                if probs is not None:
                    w = MODEL_WEIGHTS[key]
                    weighted_probs += w * probs
                    total_weight += w
                    models_used.append(key)

        # ── Fallback if no model loaded ───────────────────────────
        if total_weight == 0:
            logger.warning("No models available; using random prediction.")
            weighted_probs = np.random.dirichlet(np.ones(NUM_CLASSES))
            total_weight = 1.0
            models_used = ["demo_random"]

        # Normalize
        final_probs = weighted_probs / total_weight

        # Apply temperature softmax to sharpen low-confidence outputs
        final_probs = self._temperature_softmax(final_probs, temperature=0.7)

        top_idx = int(np.argmax(final_probs))
        top_class = CLASS_NAMES[top_idx]
        confidence = float(final_probs[top_idx])

        # Top 3
        top3_indices = np.argsort(final_probs)[::-1][:3]
        top3 = [(CLASS_NAMES[i], float(final_probs[i])) for i in top3_indices]

        return {
            "top_class": top_class,
            "confidence": confidence,
            "top3": top3,
            "all_probs": final_probs,
            "models_used": models_used,
        }

    def _predict_sklearn(self, key: str, image: np.ndarray) -> Optional[np.ndarray]:
        """Get probability vector from sklearn model."""
        model = self.manager.get_model(key)
        if model is None:
            return None

        try:
            # Try flat pixel features first, then HOG features if shape mismatch
            scaler = self.manager.scaler

            features = self.preprocessor.preprocess_for_sklearn(image, scaler=scaler)

            # Check if model supports predict_proba
            if hasattr(model, "predict_proba"):
                # Adjust feature length if model expects different size
                expected = self._get_sklearn_feature_count(model)
                if expected and features.shape[1] != expected:
                    features = self.preprocessor.preprocess_for_sklearn(
                        image, target_size=(int(expected**0.5), int(expected**0.5)), scaler=scaler
                    )
                    # If still wrong, try HOG
                    if features.shape[1] != expected:
                        features = self.preprocessor.extract_hog_features(image)
                        if scaler is not None:
                            try:
                                features = scaler.transform(features)
                            except Exception:
                                pass

                proba = model.predict_proba(features)[0]
                # Handle cases where model has different number of classes
                return self._align_probs(proba, model)
            else:
                # Decision function → softmax
                pred = model.predict(features)[0]
                probs = np.zeros(NUM_CLASSES)
                if isinstance(pred, (int, np.integer)) and 0 <= pred < NUM_CLASSES:
                    probs[pred] = 1.0
                return probs

        except Exception as e:
            logger.warning(f"{key} prediction failed: {e}")
            return None

    def _predict_cnn(self, key: str, image: np.ndarray) -> Optional[np.ndarray]:
        """Get probability vector from Keras CNN model."""
        model = self.manager.get_model(key)
        if model is None:
            return None

        try:
            size = CNN_INPUT_SIZES.get(key, (224, 224))
            inp = self.preprocessor.preprocess_for_cnn(image, target_size=size)

            # Handle grayscale LeNet
            if key == "LeNet":
                import cv2
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                import numpy as np
                gray_resized = cv2.resize(gray, size)
                inp = gray_resized.astype(np.float32) / 255.0
                # Try (1, H, W, 1) first, fallback to (1, H*W)
                inp = np.expand_dims(inp, axis=(0, -1))

            preds = model.predict(inp, verbose=0)[0]
            return self._align_probs(preds, model)

        except Exception as e:
            logger.warning(f"{key} CNN prediction failed: {e}")
            return None

    def _align_probs(self, probs: np.ndarray, model=None) -> np.ndarray:
        """Align model output to NUM_CLASSES length."""
        if len(probs) == NUM_CLASSES:
            return probs.astype(np.float64)

        aligned = np.ones(NUM_CLASSES, dtype=np.float64) / NUM_CLASSES
        min_len = min(len(probs), NUM_CLASSES)
        aligned[:min_len] = probs[:min_len]
        # Renormalize
        s = aligned.sum()
        if s > 0:
            aligned /= s
        return aligned

    def _get_sklearn_feature_count(self, model) -> Optional[int]:
        """Try to infer expected feature count from sklearn model."""
        if hasattr(model, "n_features_in_"):
            return model.n_features_in_
        if hasattr(model, "coef_"):
            return model.coef_.shape[-1]
        return None

    def _temperature_softmax(self, probs: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """Apply temperature scaling to sharpen/soften probability distribution."""
        log_probs = np.log(probs + 1e-10) / temperature
        log_probs -= log_probs.max()
        exp_probs = np.exp(log_probs)
        return exp_probs / exp_probs.sum()
