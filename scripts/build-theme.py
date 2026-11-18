"""Build the Homebrew Channel themes for T3 Code.

What it does
    Each entry in THEMES becomes one file, themes/<id>.json, in the format
    `t3 theme set` and T3 Code's Settings > Appearance import read. For each
    theme it joins, in this order:
      1. the background image as a data: URL (--hbc-background-image),
      2. the bubble CSS (CSS_FILES[0]), with its three bubble images swapped
         for the theme's WebP copies,
      3. src/hbc-theme.css, the layout styling shared by every theme,
      4. the theme's own "css" (accent, glass tint and HBC art stops).
    The result is minified and checked against T3 Code's 50,000-character
    limit. The color palette goes in the theme's "colors".

Inputs
    themes/homebrew-channel-colors.json   base palette, edited by hand
    src/*.css                             the CSS, with comments
    assets/generated/                     WebP backgrounds and bubbles,
                                          made by make-backgrounds.py

Outputs
    themes/<id>.json for every entry in THEMES. Never edit these by hand:
    the next build overwrites them. Commit them with the source change.

Run it after editing a CSS file, a palette or THEMES, then apply a theme:

    python scripts/build-theme.py
    t3 theme set ./themes/homebrew-channel.json

Rules that keep the themes working
    - Dark only: every theme sets "appearance": "dark". Do not add light
      palettes or light-mode CSS.
    - Images must be embedded: theme CSS cannot load files, so url() only
      takes data: URLs. That is why the size limit matters.
    - Changing a theme id renames its file. Users who installed the old id
      keep a stale copy, so mention any rename in the release notes.

To add a color variation, see docs/DEVELOPMENT.md.
"""

import base64
import colorsys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "themes"
# hbc-bubbles-fast.css is the GPU-friendly bubbles; hbc-bubbles.css is the
# original per-bubble sway, kept for switching back.
CSS_FILES = [ROOT / "src" / "hbc-bubbles-fast.css", ROOT / "src" / "hbc-theme.css"]
BACKGROUNDS = ROOT / "assets" / "generated"
CSS_MAX_LENGTH = 50_000

# The base dark palette. Every color variation is tinted from it with tint().
DARK = json.loads((OUTPUT_DIR / "homebrew-channel-colors.json").read_text("utf-8"))["colors"]


# Roles that keep their own meaning in every color variation.
FIXED_ROLES = {
    "error", "errorForeground", "errorSurface",
    "warning", "warningForeground", "warningSurface",
}


def tint(palette: dict, hue: float, saturation: float = 1.0) -> dict:
    """Move every color in a palette to one hue, keeping its lightness."""
    result = {}
    for role, color in palette.items():
        if role in FIXED_ROLES:
            result[role] = color
            continue
        r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
        _, lightness, sat = colorsys.rgb_to_hls(r, g, b)
        r, g, b = colorsys.hls_to_rgb(hue / 360, lightness, min(1.0, sat * saturation))
        result[role] = "#" + "".join(f"{round(c * 255):02x}" for c in (r, g, b))
    return result


def accent_roles(accent: str, foreground: str, hover: str, soft: str) -> dict:
    """The accent family: buttons, focus, cursor and the active search match."""
    return {
        "accent": accent,
        "accentForeground": foreground,
        "focus": accent,
        "messageAction": accent,
        "messageActionForeground": foreground,
        "messageActionHover": hover,
        "update": accent,
        "updateForeground": soft,
        "searchMatchActiveBackground": accent,
        "searchMatchActiveForeground": foreground,
        "terminalCursor": accent,
    }


# Each variation's palette: the base palette moved to one hue, plus a
# hand-picked accent family that stays readable on that hue.
PINK = {**tint(DARK, 330, 0.8), **accent_roles("#ff9ecf", "#2e0a1c", "#f387bd", "#ffb8dc")}
RED = {**tint(DARK, 356), **accent_roles("#ff4d5a", "#2a0508", "#e83f4c", "#ff7a84")}

YELLOW = {**tint(DARK, 64), **accent_roles("#d4e600", "#1e2200", "#bfcf00", "#e6f266")}
GREEN = {**tint(DARK, 120), **accent_roles("#2ed82b", "#032103", "#22c01f", "#7deb7b")}
PURPLE = {**tint(DARK, 260), **accent_roles("#9b6dff", "#14062e", "#8a5bf5", "#c2a8ff")}
ORANGE = {**tint(DARK, 27), **accent_roles("#f4790f", "#2a1000", "#dd6606", "#f9a95c")}
GREY = {**tint(DARK, 0, 0.0), **accent_roles("#e6e6e6", "#111111", "#cfcfcf", "#f2f2f2")}
TEAL = {**tint(DARK, 172), **accent_roles("#2ee6c8", "#04221d", "#22cdb1", "#7ff0dd")}
GOLD = {**tint(DARK, 45), **accent_roles("#ffc233", "#2a1d00", "#eaa91a", "#ffd877")}
MAGENTA = {**tint(DARK, 300), **accent_roles("#e55cff", "#26052c", "#d045eb", "#f09bff")}
INDIGO = {**tint(DARK, 235), **accent_roles("#6d7dff", "#0a0f33", "#5a6bf0", "#a3adff")}

NAVY_BACKDROP ="linear-gradient(180deg, #13263a 0%, #0d1824 60%, #08111a 100%)"


def glass(rgb: str, strong_rgb: str, border: str) -> str:
    return (
        f".dark {{\n  --hbc-glass: rgba({rgb}, 0.6);\n"
        f"  --hbc-glass-strong: rgba({strong_rgb}, 0.88);\n"
        f"  --hbc-tile-border: {border};\n}}"
    )


def tinted_glass(hue: float, saturation: float = 1.0) -> str:
    """The navy glass and tile border, moved to one hue."""
    colors = tint({"glass": "#0d1824", "strong": "#132235", "border": "#24405a"}, hue, saturation)
    rgb = {k: ", ".join(str(int(v[i:i + 2], 16)) for i in (1, 3, 5)) for k, v in colors.items()}
    return glass(rgb["glass"], rgb["strong"], colors["border"])


# The steel-blue focus bar and teal dialog stops from the HBC art
# (see the "Homebrew Channel art" section of src/hbc-theme.css).
HBC_ART_STOPS = {
    "f1": "#fbfcfd", "f2": "#c2d7e1", "f3": "#82aec4", "f4": "#57879f",
    "f5": "#184860", "f6": "#416e85", "f7": "#698ea1",
    "p1": "#173645", "p2": "#0a181e", "p3": "#10252f",
}


def art_stops(hue: float, saturation: float = 1.0) -> str:
    """The HBC focus bar and dialog stops, moved to one hue."""
    stops = tint(HBC_ART_STOPS, hue, saturation)
    lines = "".join(f"  --hbc-{k}: {v};\n" for k, v in stops.items())
    return f":root {{\n{lines}}}"


def variation(id_: str, name: str, palette: dict, accent: str, hue: float,
              saturation: float = 1.0) -> dict:
    """A dark-only color variation with its own background and tinted bubbles."""
    return {
        "id": f"homebrew-channel-{id_}",
        "name": f"Homebrew Channel {name}",
        "appearance": "dark",
        "dark": palette,
        "background": f"background_wide_{id_}.webp",
        "bubbles": id_,
        "css": f":root {{\n  --hbc-accent: {accent};\n}}\n\n"
        + tinted_glass(hue, saturation)
        + "\n\n"
        + art_stops(hue, saturation),
    }


THEMES = [
    {
        "id": "homebrew-channel",
        "name": "Homebrew Channel",
        "appearance": "dark",
        "dark": DARK,
        "background": "background_wide.webp",
        "bubbles": "default",
    },
    {
        # Backup: the navy gradient from before the background image.
        "id": "homebrew-channel-no-background",
        "name": "Homebrew Channel (No Background)",
        "appearance": "dark",
        "dark": DARK,
        "background": None,
        "bubbles": "default",
        "css": f".dark {{\n  --hbc-backdrop: {NAVY_BACKDROP};\n}}",
    },
    # Pink and red predate variation() and keep hand-picked glass colors,
    # which read better than the tinted ones. Newer colors use variation().
    {
        "id": "homebrew-channel-pink",
        "name": "Homebrew Channel Pink",
        "appearance": "dark",
        "dark": PINK,
        "background": "background_wide_pink.webp",
        "bubbles": "pink",
        "css": ":root {\n  --hbc-accent: #ff9ecf;\n}\n\n"
        + glass("36, 13, 26", "52, 19, 38", "#5a2442")
        + "\n\n"
        + art_stops(330, 0.8),
    },
    {
        "id": "homebrew-channel-red",
        "name": "Homebrew Channel Red",
        "appearance": "dark",
        "dark": RED,
        "background": "background_wide_red.webp",
        "bubbles": "red",
        "css": ":root {\n  --hbc-accent: #ff4d5a;\n}\n\n"
        + glass("36, 10, 12", "50, 14, 18", "#5a2026")
        + "\n\n"
        + art_stops(356),
    },
    # Bubbles come pre-tinted from make-backgrounds.py (assets/generated/bubbles).
    variation("yellow", "Yellow", YELLOW, "#d4e600", 64),
    variation("green", "Green", GREEN, "#2ed82b", 120),
    variation("purple", "Purple", PURPLE, "#9b6dff", 260),
    variation("orange", "Orange", ORANGE, "#f4790f", 27),
    variation("grey", "Grey", GREY, "#e6e6e6", 0, 0.0),
    variation("teal", "Teal", TEAL, "#2ee6c8", 172),
    variation("gold", "Gold", GOLD, "#ffc233", 45),
    variation("magenta", "Magenta", MAGENTA, "#e55cff", 300),
    variation("indigo", "Indigo", INDIGO, "#6d7dff", 235),
]


# Metadata for theme galleries and other sites that list themes. T3 Code
# ignores these fields but keeps them, so they travel with the file.
# "version" is not used here: T3 Code reads it as the theme format version.
REPOSITORY = "https://github.com/FrankieFms/homebrew-t3code"
PREVIEWS = "https://raw.githubusercontent.com/FrankieFms/homebrew-t3code/main/assets/previews"
META = {
    "author": "FrankieFms",
    "homepage": REPOSITORY,
    "license": "GPL-2.0-or-later",
}
TAGS = ["dark", "homebrew-channel", "wii", "animated", "retro"]

# Keyed by theme id without the "homebrew-channel" prefix: "" is the main theme.
# Each value is (description, preview image name in assets/previews/).
DESCRIPTIONS = {
    "": ("A T3 Code theme inspired by The Homebrew Channel on the Wii: its underwater "
         "background, rising bubbles and Wii-blue accents.", "homebrew-default"),
    "no-background": ("A plain navy gradient in place of the underwater image. "
                      "The bubbles stay.", "homebrew-no-bg"),
    "pink": ("Light pink water, pink bubbles and accents.", "homebrew-pink"),
    "red": ("Red water, red bubbles and accents.", "homebrew-red"),
    "orange": ("Orange water, bubbles and accents.", "homebrew-orange"),
    "gold": ("Gold water, bubbles and accents.", "homebrew-gold"),
    "yellow": ("Lime-yellow water, bubbles and accents.", "homebrew-yellow"),
    "green": ("Green water, bubbles and accents.", "homebrew-green"),
    "teal": ("Teal water, bubbles and accents.", "homebrew-teal"),
    "indigo": ("Indigo water, bubbles and accents.", "homebrew-indigo"),
    "purple": ("Purple water, bubbles and accents.", "homebrew-purple"),
    "magenta": ("Magenta water, bubbles and accents.", "homebrew-magenta"),
    "grey": ("Charcoal water, grey bubbles and white accents.", "homebrew-grey"),
}


def metadata(theme_id: str) -> dict:
    key = theme_id.removeprefix("homebrew-channel").removeprefix("-")
    if key not in DESCRIPTIONS:
        raise SystemExit(f"{theme_id}: add a description to DESCRIPTIONS.")
    description, preview = DESCRIPTIONS[key]
    if key:
        description += " A variation of the Homebrew Channel theme for T3 Code."
    return {
        "description": description,
        **META,
        "preview": f"{PREVIEWS}/{preview}.png",
        "tags": TAGS + ([key] if key and key != "no-background" else []),
    }


def background_css(name: str) -> str:
    """Embed a background as a data: URL, since themes cannot load files."""
    data = base64.b64encode((BACKGROUNDS / name).read_bytes()).decode("ascii")
    return f':root {{\n  --hbc-background-image: url("data:image/webp;base64,{data}");\n}}'


def minify(css: str) -> str:
    """Strip comments and spacing from the built CSS only.

    The files in src/ keep their comments; only the copy inside each theme
    is shrunk, to stay under T3 Code's 50,000-character limit. Spaces
    inside values such as calc(1px - 2px) and descendant selectors stay.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def tinted_bubbles(css: str, theme: str) -> str:
    """Swap the three embedded bubble PNGs for a theme's WebP copies, made by
    make-backgrounds.py: tinted for a color variation, so no per-frame CSS
    hue-rotate filter is needed, and about a third the size, which makes
    T3 Code's per-frame restyle of the bubble layers cheaper."""
    def swap(match: re.Match) -> str:
        data = (BACKGROUNDS / "bubbles" / f"{theme}-{match.group(1)}.webp").read_bytes()
        encoded = base64.b64encode(data).decode("ascii")
        return f'--bubble-{match.group(1)}: url("data:image/webp;base64,{encoded}")'

    css, count = re.subn(r'--bubble-(\d):\s*url\("data:image/png;base64,[A-Za-z0-9+/=]+"\)', swap, css)
    if count != 3:
        raise SystemExit(f"{theme}: expected 3 bubble images in {CSS_FILES[0].name}, found {count}.")
    return css


def build(spec: dict) -> dict:
    parts = []
    if spec["background"]:
        parts.append(background_css(spec["background"]))
    bubbles, theme_css = (path.read_text("utf-8").strip() for path in CSS_FILES)
    if spec.get("bubbles"):
        bubbles = tinted_bubbles(bubbles, spec["bubbles"])
    parts += [bubbles, theme_css]
    if spec.get("css"):
        parts.append(spec["css"])
    css = minify("\n".join(parts))
    if len(css) > CSS_MAX_LENGTH:
        raise SystemExit(f"{spec['id']}: CSS is {len(css)} characters; T3 Code allows {CSS_MAX_LENGTH}.")

    main_palette = spec["dark"]
    theme = {
        "version": 1,
        "name": spec["name"],
        **metadata(spec["id"]),
        "appearance": spec["appearance"],
        "canvas": main_palette["canvas"],
        "accent": main_palette["accent"],
        "colors": main_palette,
    }
    theme["css"] = css
    return theme


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    for spec in THEMES:
        theme = build(spec)
        output = OUTPUT_DIR / f"{spec['id']}.json"
        output.write_text(json.dumps(theme, indent=2) + "\n", "utf-8", newline="\n")
        print(f"Wrote themes/{output.name}: {len(theme['css'])} characters of CSS.")


if __name__ == "__main__":
    main()
