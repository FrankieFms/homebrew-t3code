"""Make the compressed backgrounds that build-theme.py embeds.

Needs Pillow (pip install pillow). Run it only when the source image or a
color variation changes; the WebP files it writes are committed.

    python scripts/make-backgrounds.py
"""

from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SOURCE = ASSETS / "source" / "background_wide.png"
OUTPUT_DIR = ASSETS / "generated"
QUALITY = 85

# The source water is hue 199 degrees. Each variation shifts the hue and can
# scale saturation and brightness.
VARIATIONS = {
    "background_wide.webp": {"hue": 199, "saturation": 1.0, "value": 1.0},
    "background_wide_pink.webp": {"hue": 330, "saturation": 0.55, "value": 1.0},
    "background_wide_red.webp": {"hue": 356, "saturation": 1.0, "value": 0.8},
    # Yellow and green are bright hues, so they are darkened for readable text.
    # Grey is greyscale, darkened to a charcoal like the black HBC banner.
    "background_wide_yellow.webp": {"hue": 66, "saturation": 1.0, "value": 0.85},
    "background_wide_green.webp": {"hue": 120, "saturation": 1.0, "value": 0.75},
    "background_wide_purple.webp": {"hue": 260, "saturation": 1.0, "value": 1.0},
    "background_wide_orange.webp": {"hue": 27, "saturation": 1.0, "value": 0.85},
    "background_wide_grey.webp": {"hue": 199, "saturation": 0.0, "value": 0.45},
    "background_wide_teal.webp": {"hue": 172, "saturation": 1.0, "value": 0.85},
    "background_wide_gold.webp": {"hue": 45, "saturation": 1.0, "value": 0.75},
    "background_wide_magenta.webp": {"hue": 300, "saturation": 1.0, "value": 0.9},
    "background_wide_indigo.webp": {"hue": 235, "saturation": 1.0, "value": 1.0},
}
SOURCE_HUE = 199


def recolor(image: Image.Image, hue: float, saturation: float, value: float) -> Image.Image:
    shift = round((hue - SOURCE_HUE) % 360 * 255 / 360)
    h, s, v = image.convert("HSV").split()
    h = h.point(lambda x: (x + shift) % 256)
    s = s.point(lambda x: min(255, round(x * saturation)))
    v = v.point(lambda x: min(255, round(x * value)))
    return Image.merge("HSV", (h, s, v)).convert("RGB")


# The bubble art (hue 201, close to the water) is tinted per color variation
# here, so themes need no per-frame CSS filter on the four full-screen bubble
# layers. Keys are theme ids without the "homebrew-channel-" prefix.
BUBBLE_SOURCE = ASSETS / "source" / "bubbles"
BUBBLE_OUTPUT = OUTPUT_DIR / "bubbles"
BUBBLE_TINTS = {
    "pink": (330, 0.8), "red": (356, 1.0), "yellow": (64, 1.0), "green": (120, 1.0),
    "purple": (260, 1.0), "orange": (27, 1.0), "grey": (199, 0.0), "teal": (172, 1.0),
    "gold": (45, 1.0), "magenta": (300, 1.0), "indigo": (235, 1.0),
}


def tint_bubble(image: Image.Image, hue: float, saturation: float) -> Image.Image:
    """Recolor RGBA bubble art, keeping its alpha."""
    tinted = recolor(image.convert("RGB"), hue, saturation, 1.0).convert("RGBA")
    tinted.putalpha(image.getchannel("A"))
    return tinted


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    for name, settings in VARIATIONS.items():
        output = OUTPUT_DIR / name
        recolor(source, **settings).save(output, "WEBP", quality=QUALITY, method=6)
        print(f"Wrote {output.name}: {output.stat().st_size} bytes.")
    BUBBLE_OUTPUT.mkdir(exist_ok=True)
    for theme, (hue, saturation) in BUBBLE_TINTS.items():
        for n in (1, 2, 3):
            source = Image.open(BUBBLE_SOURCE / f"bubble{n}.png").convert("RGBA")
            output = BUBBLE_OUTPUT / f"{theme}-{n}.png"
            tint_bubble(source, hue, saturation).save(output, optimize=True)
        print(f"Wrote bubbles/{theme}-1..3.png.")


if __name__ == "__main__":
    main()
