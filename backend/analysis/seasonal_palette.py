"""
Seasonal color palette classifier.
Maps undertone + depth + contrast to one of 12 seasonal palettes
and provides comprehensive style recommendations.
"""


# ──────────────────────────────────────────────────────────────
#  Full palette data for all 12 seasons
# ──────────────────────────────────────────────────────────────

PALETTE_DATA = {
    "Light Spring": {
        "description": "Delicate warmth with light, clear coloring. Think of a sunny spring morning with soft pastels and light golden tones.",
        "best_colors": [
            "#FADADD", "#FFDAB9", "#FFE4B5", "#98FB98", "#87CEEB",
            "#F0E68C", "#FAFAD2", "#FFB6C1", "#DDA0DD", "#FFA07A",
            "#E0FFFF", "#F5DEB3"
        ],
        "worst_colors": ["#000000", "#191970", "#800000", "#2F4F4F", "#4B0082", "#3B3B3B"],
        "clothing": [
            "Soft peach blouses", "Light coral dresses", "Warm ivory knits",
            "Buttercup yellow tops", "Mint green cardigans", "Light aqua accessories"
        ],
        "jewelry": "Light gold, rose gold, warm champagne metals. Delicate pieces with soft sparkle.",
        "hair_colors": [
            "Honey blonde", "Strawberry blonde", "Light golden brown",
            "Warm light caramel", "Sun-kissed highlights"
        ],
        "makeup": {
            "foundation": "Warm beige with golden undertones",
            "blush": "Peach, light coral, warm pink",
            "lips": "Nude peach, soft coral, warm rose",
            "eyes": "Soft gold, warm peach, light brown, champagne shimmer",
            "avoid": "Dark smoky eyes, cool berry lips, heavy contour"
        }
    },
    "True Spring": {
        "description": "Warm, bright, and clear coloring. Like a vibrant spring garden in full bloom with saturated, warm colors.",
        "best_colors": [
            "#FF6347", "#FF8C00", "#FFD700", "#32CD32", "#00CED1",
            "#FF7F50", "#FFDEAD", "#EE82EE", "#20B2AA", "#F0A500",
            "#FF4500", "#7CFC00"
        ],
        "worst_colors": ["#808080", "#708090", "#C0C0C0", "#2F4F4F", "#4A4A4A", "#DCDCDC"],
        "clothing": [
            "Bright tomato red tops", "Warm coral dresses", "Vivid turquoise blouses",
            "Golden yellow knits", "Bright warm greens", "Tangerine accessories"
        ],
        "jewelry": "Bright yellow gold, polished brass, warm copper. Bold statement pieces.",
        "hair_colors": [
            "Golden blonde", "Warm auburn", "Bright copper",
            "Clear warm brown", "Rich golden highlights"
        ],
        "makeup": {
            "foundation": "Warm with golden-peach undertones",
            "blush": "Warm coral, bright peach, apricot",
            "lips": "Bright coral, warm red, tangerine, peach",
            "eyes": "Warm gold, bright teal, clear brown, vivid green",
            "avoid": "Muted tones, cool pastels, ashy colors"
        }
    },
    "Deep Spring": {
        "description": "Rich warmth with depth and intensity. Like a lush tropical landscape with deep, warm, saturated hues.",
        "best_colors": [
            "#B8860B", "#CD853F", "#D2691E", "#228B22", "#008080",
            "#FF4500", "#8B4513", "#9ACD32", "#DC143C", "#DAA520",
            "#2E8B57", "#FF8C00"
        ],
        "worst_colors": ["#E6E6FA", "#FFC0CB", "#F5F5DC", "#ADD8E6", "#D3D3D3", "#FAFAD2"],
        "clothing": [
            "Deep terracotta jackets", "Rich olive pants", "Warm brown leather",
            "Bold teal dresses", "Deep coral tops", "Warm red accessories"
        ],
        "jewelry": "Rich yellow gold, antique brass, warm bronze. Substantial, textured pieces.",
        "hair_colors": [
            "Rich warm brown", "Deep auburn", "Dark golden brown",
            "Chocolate with copper", "Warm espresso"
        ],
        "makeup": {
            "foundation": "Warm beige to deep warm tan",
            "blush": "Deep peach, warm brick, terracotta",
            "lips": "Warm red, deep coral, cinnamon, warm nude",
            "eyes": "Deep bronze, warm olive, rich copper, dark teal",
            "avoid": "Icy pastels, cool silver tones, light ashy colors"
        }
    },
    "Light Summer": {
        "description": "Soft, cool, and light coloring. Like a misty summer morning with gentle, cool pastels and soft grey undertones.",
        "best_colors": [
            "#B0C4DE", "#D8BFD8", "#E6E6FA", "#C0D6E4", "#F0C0C0",
            "#ACE5EE", "#CFCFC4", "#E8D0D0", "#B5C7D3", "#D4B5D8",
            "#C8DFC8", "#E0D0E0"
        ],
        "worst_colors": ["#FF4500", "#FF8C00", "#FFD700", "#8B4513", "#B8860B", "#FF6347"],
        "clothing": [
            "Soft lavender blouses", "Powder blue dresses", "Dusty rose knits",
            "Soft grey suits", "Pale mauve cardigans", "Light slate accessories"
        ],
        "jewelry": "White gold, platinum, soft silver, rose gold. Delicate, refined pieces.",
        "hair_colors": [
            "Light ash blonde", "Cool light brown", "Soft platinum",
            "Light mousy brown", "Cool-toned highlights"
        ],
        "makeup": {
            "foundation": "Cool pink-beige undertones",
            "blush": "Soft rose, cool pink, light mauve",
            "lips": "Dusty rose, soft berry, cool nude pink",
            "eyes": "Soft grey, cool lavender, rose, soft plum",
            "avoid": "Warm oranges, heavy dark colors, golden tones"
        }
    },
    "True Summer": {
        "description": "Cool, soft, and medium coloring. Like a summer sky with gentle blues, soft roses, and muted cool tones.",
        "best_colors": [
            "#6A5ACD", "#DB7093", "#4682B4", "#BC8F8F", "#9370DB",
            "#708090", "#778899", "#5F9EA0", "#C08081", "#6B8E9B",
            "#87879B", "#A0829B"
        ],
        "worst_colors": ["#FF6347", "#FFD700", "#FF4500", "#FFA500", "#CD853F", "#B8860B"],
        "clothing": [
            "Medium blue blazers", "Dusty rose dresses", "Soft teal tops",
            "Cool grey trousers", "Mauve blouses", "Slate blue accessories"
        ],
        "jewelry": "Sterling silver, white gold, platinum. Classic and elegant styles.",
        "hair_colors": [
            "Medium ash brown", "Cool mousy brown", "Soft ash blonde",
            "Cool medium brown", "Subtle cool highlights"
        ],
        "makeup": {
            "foundation": "Neutral to cool undertones",
            "blush": "Mauve, cool rose, soft raspberry",
            "lips": "Rose, cool berry, plum, soft mauve",
            "eyes": "Cool grey, soft navy, taupe, muted plum",
            "avoid": "Warm peach, orange, yellow gold, bright warm colors"
        }
    },
    "Soft Summer": {
        "description": "Muted, cool-neutral coloring. Like a gentle summer dusk with soft, greyed tones and understated elegance.",
        "best_colors": [
            "#8B8589", "#C4AEAD", "#7B9DAF", "#9CAF88", "#B7A9C4",
            "#A0937D", "#8DA0AA", "#9B8B7D", "#838B8B", "#B5A9C4",
            "#8FBC8F", "#D2B48C"
        ],
        "worst_colors": ["#FF0000", "#FF4500", "#FFD700", "#00FF00", "#0000FF", "#FF00FF"],
        "clothing": [
            "Muted sage tops", "Soft cocoa knits", "Dusty blue-grey dresses",
            "Warm grey blazers", "Soft olive pants", "Muted rose accessories"
        ],
        "jewelry": "Brushed silver, matte gold, antiqued metals. Understated, textured pieces.",
        "hair_colors": [
            "Soft ash brown", "Mushroom brown", "Dark blonde",
            "Cool medium brown", "Subtle balayage"
        ],
        "makeup": {
            "foundation": "Neutral with slight cool undertones",
            "blush": "Soft mauve, muted rose, dusty pink",
            "lips": "Muted berry, soft mauve, dusty rose, neutral pink",
            "eyes": "Soft taupe, muted plum, grey-green, cool brown",
            "avoid": "Neon colors, bright oranges, stark black, vivid primaries"
        }
    },
    "Soft Autumn": {
        "description": "Muted, warm-neutral coloring. Like early autumn with soft, earthy tones and a gentle, warm haze.",
        "best_colors": [
            "#C4A882", "#BC9B7E", "#9B8E6E", "#8E9B7E", "#C4A59B",
            "#A89078", "#8B8378", "#B5A27E", "#9B8B78", "#7E8B6E",
            "#C4B5A5", "#D2B48C"
        ],
        "worst_colors": ["#FF0000", "#0000FF", "#FF00FF", "#00FFFF", "#FFFF00", "#000000"],
        "clothing": [
            "Soft camel coats", "Muted olive tops", "Warm taupe knits",
            "Dusty teal dresses", "Warm grey blazers", "Soft terra cotta scarves"
        ],
        "jewelry": "Matte gold, antique brass, warm copper. Organic, textured designs.",
        "hair_colors": [
            "Warm mousy brown", "Soft caramel", "Golden brown",
            "Dark blonde with warm tones", "Subtle warm highlights"
        ],
        "makeup": {
            "foundation": "Warm neutral with peachy tones",
            "blush": "Soft peach, warm dusty rose, light terracotta",
            "lips": "Warm nude, soft brick, muted coral, dusty peach",
            "eyes": "Warm taupe, soft olive, muted copper, warm grey",
            "avoid": "Bright cool pinks, icy colors, stark white, neon"
        }
    },
    "True Autumn": {
        "description": "Warm, rich, and earthy coloring. Like peak autumn with golden foliage, rich harvest colors, and warm depth.",
        "best_colors": [
            "#B8860B", "#D2691E", "#8B6914", "#6B8E23", "#CD853F",
            "#A0522D", "#DAA520", "#808000", "#BC8F8F", "#CC7722",
            "#9B7653", "#B87333"
        ],
        "worst_colors": ["#FF69B4", "#E6E6FA", "#ADD8E6", "#FFC0CB", "#F0F8FF", "#E0FFFF"],
        "clothing": [
            "Rich camel blazers", "Deep olive coats", "Warm rust dresses",
            "Mustard knits", "Chocolate brown pants", "Burnt sienna accessories"
        ],
        "jewelry": "Rich yellow gold, antique gold, warm copper, bronze. Substantial, earthy pieces.",
        "hair_colors": [
            "Rich auburn", "Warm copper", "Golden brown",
            "Chestnut", "Dark warm brown with red tones"
        ],
        "makeup": {
            "foundation": "Warm golden or peachy undertones",
            "blush": "Warm peach, terracotta, burnt sienna",
            "lips": "Warm rust, brick red, warm nude, copper",
            "eyes": "Rich bronze, warm olive, golden brown, deep copper",
            "avoid": "Cool pinks, icy blues, silver shimmer, stark black"
        }
    },
    "Deep Autumn": {
        "description": "Dark, warm, and rich coloring. Like a deep autumn evening with warm, saturated, and intense earthy tones.",
        "best_colors": [
            "#8B0000", "#556B2F", "#8B4513", "#B22222", "#006400",
            "#800020", "#4B3621", "#704214", "#8B6508", "#483C32",
            "#654321", "#2E1A00"
        ],
        "worst_colors": ["#E6E6FA", "#FFC0CB", "#E0FFFF", "#FAFAD2", "#F5F5DC", "#FFB6C1"],
        "clothing": [
            "Deep chocolate jackets", "Dark olive coats", "Rich burgundy dresses",
            "Warm espresso knits", "Dark teal blazers", "Deep gold accessories"
        ],
        "jewelry": "Antique gold, burnished bronze, dark copper. Bold, dramatic pieces with warm tones.",
        "hair_colors": [
            "Dark warm brown", "Deep auburn", "Rich espresso",
            "Dark chocolate", "Black with warm undertones"
        ],
        "makeup": {
            "foundation": "Warm with deep golden-bronze undertones",
            "blush": "Deep terracotta, warm plum, rich peach",
            "lips": "Deep wine, warm dark red, rich berry, warm brown",
            "eyes": "Deep bronze, dark olive, warm burgundy, espresso",
            "avoid": "Pastels, icy tones, cool light colors, baby pink"
        }
    },
    "Light Winter": {
        "description": "Cool, bright, and light coloring. Like a crisp winter day with icy brightness, cool pastels, and clear contrast.",
        "best_colors": [
            "#E0B0FF", "#89CFF0", "#FFB7C5", "#A7C7E7", "#CCCCFF",
            "#C0E8D5", "#F2F3F4", "#BFEFFF", "#DDA0DD", "#98D8C8",
            "#E0E0FF", "#F0C0C8"
        ],
        "worst_colors": ["#8B4513", "#D2691E", "#B8860B", "#CD853F", "#808000", "#CC7722"],
        "clothing": [
            "Icy pink blouses", "Clear light blue dresses", "Bright white tops",
            "Cool lavender knits", "Soft fuchsia cardigans", "Icy mint accessories"
        ],
        "jewelry": "Platinum, white gold, bright silver. Sparkling, clear stones like diamonds and crystals.",
        "hair_colors": [
            "Cool ash blonde", "Icy platinum", "Cool light brown",
            "Silver-toned highlights", "Cool dark blonde"
        ],
        "makeup": {
            "foundation": "Cool pink or neutral undertones",
            "blush": "Cool pink, bright rose, soft fuchsia",
            "lips": "Bright pink, cool berry, icy rose, clear red",
            "eyes": "Cool silver, icy blue, bright lavender, soft charcoal",
            "avoid": "Golden tones, warm earthy colors, muted shades"
        }
    },
    "True Winter": {
        "description": "Cool, clear, and high-contrast coloring. Like a dramatic winter night with jewel tones, pure white snow, and dark skies.",
        "best_colors": [
            "#000080", "#DC143C", "#006400", "#4B0082", "#FF0000",
            "#008B8B", "#C71585", "#191970", "#0000CD", "#8B008B",
            "#FFFFFF", "#000000"
        ],
        "worst_colors": ["#DEB887", "#F5DEB3", "#FFDAB9", "#FFE4B5", "#D2B48C", "#C4A882"],
        "clothing": [
            "Bright true red dresses", "Navy blue blazers", "Emerald green tops",
            "Black and white combos", "Jewel purple knits", "Bright fuchsia accents"
        ],
        "jewelry": "Bright silver, platinum, white gold. High-contrast pieces with vivid stones.",
        "hair_colors": [
            "Blue-black", "Cool dark brown", "Jet black",
            "Cool espresso", "Stark platinum blonde"
        ],
        "makeup": {
            "foundation": "Cool with pink or neutral undertones",
            "blush": "Cool bright pink, berry, clear rose",
            "lips": "True red, bright berry, deep plum, cool wine",
            "eyes": "Deep charcoal, bright silver, navy, vivid plum",
            "avoid": "Warm oranges, gold shimmer, muted earthy colors"
        }
    },
    "Deep Winter": {
        "description": "Dark, cool, and intensely rich coloring. Like the deep night sky with darkened jewel tones and dramatic depth.",
        "best_colors": [
            "#191970", "#800020", "#006400", "#4B0082", "#2F4F4F",
            "#301934", "#1B1B3A", "#3B0000", "#002D04", "#1C1C3E",
            "#2C003E", "#0D0D0D"
        ],
        "worst_colors": ["#FFDAB9", "#FFE4B5", "#F0E68C", "#FAFAD2", "#F5F5DC", "#FFF5EE"],
        "clothing": [
            "Deep navy suits", "Rich burgundy dresses", "Dark emerald coats",
            "Black formal wear", "Deep plum knits", "Dark teal accessories"
        ],
        "jewelry": "Dark silver, gunmetal, white gold with dark stones. Dramatic, bold designs.",
        "hair_colors": [
            "Jet black", "Deepest cool brown", "Blue-black",
            "Very dark espresso", "Cool-toned black"
        ],
        "makeup": {
            "foundation": "Cool to neutral with deep undertones",
            "blush": "Deep berry, cool plum, rich wine",
            "lips": "Deep wine, dark berry, rich plum, dark red",
            "eyes": "Deep charcoal, dark plum, midnight blue, emerald",
            "avoid": "Pastels, warm peach, golden shades, light camel"
        }
    },
}


class SeasonalPaletteClassifier:
    """Classify into one of 12 seasonal color palettes."""

    def classify(self, tone_data: dict, color_data: dict) -> dict:
        """
        Determine the seasonal palette based on undertone, depth, and contrast.

        Args:
            tone_data: Dict with undertone, depth, contrast info.
            color_data: Original color data.

        Returns:
            Dict with season, palette details, and recommendations.
        """
        undertone = tone_data["undertone"]["classification"]
        depth = tone_data["depth"]["level"]
        contrast = tone_data["contrast"]["level"]

        season = self._determine_season(undertone, depth, contrast)
        palette = PALETTE_DATA[season]

        return {
            "season": season,
            "description": palette["description"],
            "best_colors": palette["best_colors"],
            "worst_colors": palette["worst_colors"],
            "clothing_suggestions": palette["clothing"],
            "jewelry_tone": palette["jewelry"],
            "hair_color_suggestions": palette["hair_colors"],
            "makeup_palette": palette["makeup"],
        }

    def _determine_season(self, undertone: str, depth: str, contrast: str) -> str:
        """
        Map undertone + depth + contrast to a specific season.

        Mapping logic:
        SPRING (warm, bright)
          - Light Spring: warm + light + low/medium
          - True Spring: warm + medium + medium/high
          - Deep Spring: warm + deep + high

        SUMMER (cool, muted)
          - Light Summer: cool + light + low
          - True Summer: cool + medium + medium
          - Soft Summer: cool/neutral + medium + low

        AUTUMN (warm, muted)
          - Soft Autumn: neutral/warm + medium + low
          - True Autumn: warm + medium + medium
          - Deep Autumn: warm + deep + medium/high

        WINTER (cool, bright)
          - Light Winter: cool + light + medium/high
          - True Winter: cool + medium + high
          - Deep Winter: cool + deep + high
        """
        # Build a scoring system for all 12 seasons
        scores = {}

        for season_name in PALETTE_DATA:
            scores[season_name] = 0

        # ── Warm undertone seasons ──
        if undertone == "warm":
            scores["Light Spring"] += 3 if depth == "light" else 0
            scores["True Spring"] += 3 if depth == "medium" else 1
            scores["Deep Spring"] += 3 if depth == "deep" else 1
            scores["Soft Autumn"] += 1
            scores["True Autumn"] += 3 if depth == "medium" else 1
            scores["Deep Autumn"] += 3 if depth == "deep" else 1

        # ── Cool undertone seasons ──
        elif undertone == "cool":
            scores["Light Summer"] += 3 if depth == "light" else 0
            scores["True Summer"] += 3 if depth == "medium" else 1
            scores["Soft Summer"] += 1
            scores["Light Winter"] += 3 if depth == "light" else 0
            scores["True Winter"] += 3 if depth == "medium" else 1
            scores["Deep Winter"] += 3 if depth == "deep" else 1

        # ── Neutral undertone seasons ──
        else:  # neutral
            scores["Soft Summer"] += 2
            scores["Soft Autumn"] += 2
            scores["Light Spring"] += 1 if depth == "light" else 0
            scores["Light Summer"] += 1 if depth == "light" else 0
            scores["True Summer"] += 1 if depth == "medium" else 0
            scores["True Autumn"] += 1 if depth == "medium" else 0

        # ── Contrast refinements ──
        if contrast == "high":
            scores["True Winter"] += 2
            scores["Deep Winter"] += 2
            scores["Deep Spring"] += 1
            scores["Deep Autumn"] += 1
            scores["True Spring"] += 1
        elif contrast == "low":
            scores["Soft Summer"] += 2
            scores["Soft Autumn"] += 2
            scores["Light Summer"] += 1
            scores["Light Spring"] += 1
        else:  # medium
            scores["True Summer"] += 1
            scores["True Autumn"] += 1
            scores["True Spring"] += 1
            scores["Light Winter"] += 1

        # ── Depth refinements ──
        if depth == "light":
            scores["Light Spring"] += 1
            scores["Light Summer"] += 1
            scores["Light Winter"] += 1
        elif depth == "deep":
            scores["Deep Spring"] += 1
            scores["Deep Autumn"] += 1
            scores["Deep Winter"] += 1

        # Pick the season with the highest score
        best_season = max(scores, key=scores.get)
        return best_season
