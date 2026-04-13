"""
model_loader.py - Handles loading of all ML/DL models
"""

import os
import numpy as np
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model file paths (relative to app root)
MODEL_PATHS = {
    "BEST_SVM":        "models/BEST_MODEL_SVM.joblib",
    "SVM":             "models/SVM.joblib",
    "RandomForest":    "models/RandomForest.joblib",
    "Scaler":          "models/feature_scaler.joblib",
    "MobileNetV2":     "models/MobileNetV2_best.h5",
    "MobileNetV2_fin": "models/MobileNetV2_final.h5",
    "MobileNetV2_p1":  "models/MobileNetV2_Phase1.h5",
    "AlexNet":         "models/AlexNet_best.h5",
    "LeNet":           "models/LeNet_best.h5",
}

# Model weights for ensemble (higher = more influence)
MODEL_WEIGHTS = {
    "BEST_SVM":        0.35,
    "SVM":             0.15,
    "RandomForest":    0.10,
    "MobileNetV2":     0.20,
    "MobileNetV2_fin": 0.08,
    "MobileNetV2_p1":  0.05,
    "AlexNet":         0.04,
    "LeNet":           0.03,
}

CLASS_NAMES = [
    "Acne",
    "Acne_Scars",
    "Contact_Dermatitis",
    "Eczema_Atopic_Dermatitis",
    "Folliculitis",
    "Fungal_Infection",
    "Hyperpigmentation",
    "NormalSkin",
    "Pseudofolliculitis_Barbae",
    "Rosacea",
    "Seborrheic_Dermatitis",
    "Sunburn",
    "Vitiligo",
]

NUM_CLASSES = len(CLASS_NAMES)


class ModelManager:
    """Manages loading and access to all models."""

    def __init__(self):
        self.models = {}
        self.scaler = None
        self._loaded_status = {}

    def load_all_models(self):
        """Load all available models; gracefully skip missing ones."""
        # Load scaler first (needed for SVM/RF)
        self._load_scaler()

        # Load sklearn models
        for key in ["BEST_SVM", "SVM", "RandomForest"]:
            self._load_sklearn_model(key)

        # Load Keras/TF models
        for key in ["MobileNetV2", "MobileNetV2_fin", "MobileNetV2_p1", "AlexNet", "LeNet"]:
            self._load_keras_model(key)

        loaded = [k for k, v in self._loaded_status.items() if v]
        logger.info(f"Loaded models: {loaded}")

    def _load_scaler(self):
        path = MODEL_PATHS["Scaler"]
        if os.path.exists(path):
            try:
                self.scaler = joblib.load(path)
                self._loaded_status["Scaler"] = True
                logger.info("Scaler loaded.")
            except Exception as e:
                logger.warning(f"Scaler load failed: {e}")
                self._loaded_status["Scaler"] = False
        else:
            logger.warning("Scaler not found.")
            self._loaded_status["Scaler"] = False

    def _load_sklearn_model(self, key: str):
        path = MODEL_PATHS[key]
        if os.path.exists(path):
            try:
                self.models[key] = joblib.load(path)
                self._loaded_status[key] = True
                logger.info(f"{key} loaded.")
            except Exception as e:
                logger.warning(f"{key} load failed: {e}")
                self._loaded_status[key] = False
        else:
            logger.warning(f"{key} not found at {path}.")
            self._loaded_status[key] = False

    def _load_keras_model(self, key: str):
        path = MODEL_PATHS[key]
        if os.path.exists(path):
            try:
                # Lazy import to avoid TF overhead if not needed
                import tensorflow as tf
                model = tf.keras.models.load_model(path)
                self.models[key] = model
                self._loaded_status[key] = True
                logger.info(f"{key} loaded.")
            except Exception as e:
                logger.warning(f"{key} load failed: {e}")
                self._loaded_status[key] = False
        else:
            logger.warning(f"{key} not found at {path}.")
            self._loaded_status[key] = False

    def get_loaded_models(self) -> dict:
        return self._loaded_status.copy()

    def has_any_model(self) -> bool:
        return any(self._loaded_status.values())

    def get_model(self, key: str):
        return self.models.get(key, None)

    def is_loaded(self, key: str) -> bool:
        return self._loaded_status.get(key, False)
