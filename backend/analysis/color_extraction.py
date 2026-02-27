"""
Color extraction from facial regions.
Samples pixels from detected facial regions, removes outliers,
and computes average colors in RGB and LAB spaces.
"""

import cv2
import numpy as np
from typing import Optional


class ColorExtractor:
    """Extract skin color data from facial regions."""

    def extract(
        self,
        image: np.ndarray,
        regions: dict[str, np.ndarray],
        face_mask: np.ndarray,
    ) -> dict:
        """
        Extract color information from all facial regions.

        Args:
            image: BGR image.
            regions: Dict of region_name -> binary mask.
            face_mask: Overall face mask for background removal.

        Returns:
            Dict with per-region colors and overall skin color data.
        """
        region_colors = {}
        all_pixels = []

        for region_name, mask in regions.items():
            # Combine with face mask to remove background influence
            combined_mask = cv2.bitwise_and(mask, face_mask)
            pixels = self._sample_pixels(image, combined_mask)

            if pixels is not None and len(pixels) > 10:
                filtered = self._remove_outliers(pixels)
                avg_bgr = np.mean(filtered, axis=0).astype(int)
                avg_rgb = avg_bgr[::-1]  # BGR to RGB

                region_colors[region_name] = {
                    "rgb": avg_rgb.tolist(),
                    "hex": self._rgb_to_hex(avg_rgb),
                    "pixel_count": len(filtered),
                }
                all_pixels.extend(filtered.tolist())

        if not all_pixels:
            return {"error": "Could not extract skin color from any region"}

        all_pixels = np.array(all_pixels)
        filtered_all = self._remove_outliers(all_pixels)

        avg_bgr = np.mean(filtered_all, axis=0).astype(int)
        avg_rgb = avg_bgr[::-1].tolist()
        avg_lab = self._bgr_to_lab(avg_bgr)

        return {
            "regions": region_colors,
            "overall": {
                "rgb": avg_rgb,
                "lab": avg_lab,
                "hex": self._rgb_to_hex(np.array(avg_rgb)),
                "hsv": self._rgb_to_hsv(avg_rgb),
            },
        }

    def _sample_pixels(
        self, image: np.ndarray, mask: np.ndarray
    ) -> Optional[np.ndarray]:
        """Extract pixel values where mask is non-zero."""
        if mask is None or mask.sum() == 0:
            return None

        coords = np.where(mask > 0)
        if len(coords[0]) == 0:
            return None

        pixels = image[coords[0], coords[1]]
        return pixels

    def _remove_outliers(self, pixels: np.ndarray, z_threshold: float = 1.5) -> np.ndarray:
        """Remove outlier pixels using Z-score filtering on brightness."""
        if len(pixels) < 10:
            return pixels

        # Calculate brightness (simple luminance)
        brightness = 0.299 * pixels[:, 2] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 0]
        mean_b = np.mean(brightness)
        std_b = np.std(brightness)

        if std_b < 1e-6:
            return pixels

        z_scores = np.abs((brightness - mean_b) / std_b)
        mask = z_scores < z_threshold
        filtered = pixels[mask]

        return filtered if len(filtered) > 5 else pixels

    def _bgr_to_lab(self, bgr: np.ndarray) -> list:
        """Convert a single BGR color to LAB."""
        pixel = np.uint8([[bgr]])
        lab = cv2.cvtColor(pixel, cv2.COLOR_BGR2LAB)
        return lab[0][0].tolist()

    def _rgb_to_hsv(self, rgb: list) -> list:
        """Convert RGB to HSV."""
        pixel = np.uint8([[[rgb[2], rgb[1], rgb[0]]]])  # RGB to BGR
        hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
        return hsv[0][0].tolist()

    def _rgb_to_hex(self, rgb: np.ndarray) -> str:
        """Convert RGB array to hex color string."""
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        return f"#{r:02x}{g:02x}{b:02x}"
