"""
Tone classifier: determines undertone, contrast level, and depth level
from extracted skin color data.
"""

import numpy as np


class ToneClassifier:
    """Classify skin undertone, contrast, and depth from LAB/RGB color data."""

    def classify(self, color_data: dict) -> dict:
        """
        Classify undertone, contrast level, and depth level.

        Args:
            color_data: Dict with 'overall' containing 'rgb', 'lab', 'hsv'.

        Returns:
            Dict with undertone, contrast_level, depth_level, and explanations.
        """
        overall = color_data["overall"]
        rgb = overall["rgb"]
        lab = overall["lab"]
        hsv = overall["hsv"]

        undertone = self._classify_undertone(lab, hsv, rgb)
        depth = self._classify_depth(lab)
        contrast = self._classify_contrast(lab, rgb)

        return {
            "undertone": undertone,
            "depth": depth,
            "contrast": contrast,
        }

    def _classify_undertone(self, lab: list, hsv: list, rgb: list) -> dict:
        """
        Classify undertone as warm, cool, or neutral.

        Uses LAB a* and b* channels:
        - a* > 0 = reddish (can be warm or cool depending on b*)
        - b* > 0 = yellowish (warm)
        - b* < 0 = bluish (cool)

        Also considers the hue value from HSV.
        """
        l, a, b = lab

        # LAB is stored as L: 0-255 (mapped from 0-100), a: 0-255 (mapped from -128 to 127), b: same
        # OpenCV LAB: L is 0-255, a is 0-255 (128 = 0), b is 0-255 (128 = 0)
        a_centered = a - 128  # Center around 0
        b_centered = b - 128

        hue = hsv[0]  # 0-180 in OpenCV

        # Scoring system
        warm_score = 0
        cool_score = 0

        # b* channel: positive = yellow/warm, negative = blue/cool
        if b_centered > 5:
            warm_score += 2
        elif b_centered < -5:
            cool_score += 2
        else:
            warm_score += 0.5
            cool_score += 0.5

        # a* channel: higher = more pink/red (cool), moderate = warm peach
        if a_centered > 10:
            cool_score += 1.5
        elif a_centered > 3:
            warm_score += 0.5
        else:
            cool_score += 0.5

        # Hue consideration (in OpenCV, ~10-25 orange/warm, ~0-10 and ~160+ can be cool)
        if 10 <= hue <= 30:
            warm_score += 1
        elif hue < 10 or hue > 160:
            cool_score += 1

        # Check green/yellow ratio in RGB
        r, g, b_val = rgb
        if r > b_val + 15:
            warm_score += 1
        elif b_val > r + 15:
            cool_score += 1

        total = warm_score + cool_score
        warm_pct = warm_score / total if total > 0 else 0.5

        if warm_pct > 0.6:
            classification = "warm"
            explanation = (
                "Your skin has warm undertones with golden, peachy, or yellow hues. "
                "Veins on your wrist likely appear green or olive. "
                "You tend to look best in earthy, warm colors like coral, cream, and olive."
            )
        elif warm_pct < 0.4:
            classification = "cool"
            explanation = (
                "Your skin has cool undertones with pink, red, or bluish hues. "
                "Veins on your wrist likely appear blue or purple. "
                "You tend to look best in jewel tones, blues, and true pinks."
            )
        else:
            classification = "neutral"
            explanation = (
                "Your skin has a balanced mix of warm and cool undertones. "
                "Your veins may appear blue-green. "
                "You have the versatility to wear both warm and cool colors beautifully."
            )

        return {
            "classification": classification,
            "warm_score": round(warm_pct, 2),
            "cool_score": round(1 - warm_pct, 2),
            "explanation": explanation,
        }

    def _classify_depth(self, lab: list) -> dict:
        """
        Classify depth level based on L* (lightness) in LAB.

        OpenCV LAB: L is 0-255 (original L* 0-100 mapped to 0-255).
        """
        l_value = lab[0]
        # Convert to 0-100 scale
        l_normalized = (l_value / 255) * 100

        if l_normalized >= 70:
            level = "light"
            description = "Light skin depth — your skin has a high reflectance and appears fair or light."
        elif l_normalized >= 45:
            level = "medium"
            description = "Medium skin depth — your skin has a balanced lightness, neither very fair nor very deep."
        else:
            level = "deep"
            description = "Deep skin depth — your skin has rich, deep pigmentation with lower lightness values."

        return {
            "level": level,
            "l_value": round(l_normalized, 1),
            "description": description,
        }

    def _classify_contrast(self, lab: list, rgb: list) -> dict:
        """
        Estimate contrast level based on skin lightness.

        In a full implementation this would compare skin to hair and eye color.
        Here we approximate based on skin characteristics.
        """
        l_value = (lab[0] / 255) * 100
        r, g, b = rgb

        # Saturation of skin color as a proxy
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        chroma = max_c - min_c

        # Very light or very deep skin tends to create higher contrast
        # Medium skin tends to have softer contrast
        if l_value > 75 or l_value < 35:
            base_contrast = "high"
        elif 50 <= l_value <= 70:
            base_contrast = "medium"
        else:
            base_contrast = "low"

        # Adjust with chroma
        if chroma > 60:
            if base_contrast == "low":
                base_contrast = "medium"
        elif chroma < 25:
            if base_contrast == "high":
                base_contrast = "medium"

        descriptions = {
            "low": "Low contrast — your overall coloring is soft and muted. Gentle, blended colors suit you best.",
            "medium": "Medium contrast — you have a balanced level of contrast. Both soft and moderately vivid colors work well.",
            "high": "High contrast — your features have high contrast. Bold, vivid, and rich colors complement you.",
        }

        return {
            "level": base_contrast,
            "chroma": int(chroma),
            "description": descriptions[base_contrast],
        }
