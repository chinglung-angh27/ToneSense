"""
Face detection and landmark extraction using MediaPipe Face Landmarker (Tasks API).
Isolates facial regions (forehead, cheeks, jawline, neck) for color sampling.
"""

import os
import cv2
import numpy as np
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "face_landmarker.task")


class FaceDetector:
    """Detect faces and extract facial region masks using MediaPipe Face Landmarker."""

    # MediaPipe Face Mesh landmark indices for specific facial regions
    FOREHEAD_INDICES = [10, 67, 69, 104, 108, 109, 151, 299, 297, 333, 337, 338]
    LEFT_CHEEK_INDICES = [50, 101, 116, 117, 118, 119, 123, 132, 147, 187, 192, 205, 206, 207, 212]
    RIGHT_CHEEK_INDICES = [280, 330, 345, 346, 347, 348, 352, 361, 376, 411, 416, 425, 426, 427, 432]
    JAWLINE_INDICES = [132, 136, 150, 172, 176, 194, 197, 201, 208, 210, 211, 361, 365, 379, 397, 400, 418, 421, 428, 430, 431]
    NECK_INDICES = [152, 175, 199, 200, 421, 396, 369, 395, 394, 17]

    # Face boundary for segmentation
    FACE_OVAL_INDICES = [
        10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
        397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
        172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
    ]

    def __init__(self):
        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=VisionRunningMode.IMAGE,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
        )
        self.landmarker = FaceLandmarker.create_from_options(options)

    def detect(self, image: np.ndarray) -> dict | None:
        """
        Detect face landmarks and extract region masks.

        Args:
            image: BGR image as numpy array.

        Returns:
            Dict with 'landmarks', 'regions', 'face_mask', and 'bbox', or None if no face.
        """
        h, w, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert to MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        results = self.landmarker.detect(mp_image)

        if not results.face_landmarks or len(results.face_landmarks) == 0:
            return None

        face_lms = results.face_landmarks[0]
        landmarks = []
        for lm in face_lms:
            landmarks.append((int(lm.x * w), int(lm.y * h)))

        landmarks = np.array(landmarks)

        # Create face mask (oval)
        face_mask = self._create_polygon_mask(landmarks, self.FACE_OVAL_INDICES, (h, w))

        # Create region masks
        regions = {
            "forehead": self._create_region_mask(landmarks, self.FOREHEAD_INDICES, (h, w)),
            "left_cheek": self._create_region_mask(landmarks, self.LEFT_CHEEK_INDICES, (h, w)),
            "right_cheek": self._create_region_mask(landmarks, self.RIGHT_CHEEK_INDICES, (h, w)),
            "jawline": self._create_region_mask(landmarks, self.JAWLINE_INDICES, (h, w)),
            "neck": self._create_neck_region(landmarks, (h, w)),
        }

        # Bounding box
        xs, ys = landmarks[:, 0], landmarks[:, 1]
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

        return {
            "landmarks": landmarks,
            "regions": regions,
            "face_mask": face_mask,
            "bbox": bbox,
        }

    def _create_polygon_mask(
        self, landmarks: np.ndarray, indices: list, shape: tuple
    ) -> np.ndarray:
        """Create a filled polygon mask from landmark indices."""
        mask = np.zeros(shape[:2], dtype=np.uint8)
        pts = landmarks[indices].reshape(-1, 1, 2)
        cv2.fillConvexPoly(mask, pts, 255)
        return mask

    def _create_region_mask(
        self, landmarks: np.ndarray, indices: list, shape: tuple
    ) -> np.ndarray:
        """Create a region mask by making a convex hull of points with padding."""
        mask = np.zeros(shape[:2], dtype=np.uint8)
        pts = landmarks[indices]
        hull = cv2.convexHull(pts)
        cv2.fillConvexPoly(mask, hull, 255)
        return mask

    def _create_neck_region(
        self, landmarks: np.ndarray, shape: tuple
    ) -> np.ndarray:
        """Estimate neck region below the chin."""
        mask = np.zeros(shape[:2], dtype=np.uint8)
        h, w = shape[:2]

        chin_pts = landmarks[self.NECK_INDICES]
        chin_y = int(chin_pts[:, 1].max())
        chin_x_min = int(chin_pts[:, 0].min())
        chin_x_max = int(chin_pts[:, 0].max())

        # Neck region extends below chin
        neck_height = int((chin_x_max - chin_x_min) * 0.4)
        neck_top = chin_y
        neck_bottom = min(chin_y + neck_height, h)

        # Slightly narrower than jaw
        margin = int((chin_x_max - chin_x_min) * 0.15)
        neck_left = chin_x_min + margin
        neck_right = chin_x_max - margin

        pts = np.array([
            [neck_left, neck_top],
            [neck_right, neck_top],
            [neck_right, neck_bottom],
            [neck_left, neck_bottom],
        ]).reshape(-1, 1, 2)

        cv2.fillConvexPoly(mask, pts, 255)
        return mask

    def close(self):
        self.landmarker.close()
