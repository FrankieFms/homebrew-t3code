"""Make the compressed backgrounds that build-theme.py embeds.

Needs Pillow (pip install pillow). Run it only when the source image or a
color variation changes; the WebP files it writes are committed.

    python make-backgrounds.py
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
SOURCE = ASSETS / "background_wide.png"
QUALITY = 85

# The source water is hue 199 degrees. Each variation shifts the hue and can
# scale saturation and brightness.
VARIATIONS = {
    "background_wide.webp": {"hue": 199, "saturation": 1.0, "value": 1.0},
    "background_wide_pink.webp": {"hue": 330, "saturation": 0.55, "value": 1.0},
    "background_wide_red.webp": {"hue": 356, "saturation": 1.0, "value": 0.8},
}
SOURCE_HUE = 199


def recolor(image: Image.Image, hue: float, saturation: float, value: float) -> Image.Image:
    shift = round((hue - SOURCE_HUE) % 360 * 255 / 360)
    h, s, v = image.convert("HSV").split()
    h = h.point(lambda x: (x + shift) % 256)
    s = s.point(lambda x: min(255, round(x * saturation)))
    v = v.point(lambda x: min(255, round(x * value)))
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    for name, settings in VARIATIONS.items():
        output = ASSETS / name
        recolor(source, **settings).save(output, "WEBP", quality=QUALITY, method=6)
        print(f"Wrote {output.name}: {output.stat().st_size} bytes.")


if __name__ == "__main__":
    main()
