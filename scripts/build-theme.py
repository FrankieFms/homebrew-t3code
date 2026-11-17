"""Build the Homebrew Channel themes for T3 Code.

Each entry in THEMES becomes one theme file in themes/. A theme merges its
palettes, its background image, hbc-bubbles.css and hbc-theme.css. Run it
after editing a CSS file or a palette, then apply a theme:

    python scripts/build-theme.py
    t3 theme set ./themes/homebrew-channel.json
"""

import base64
import colorsys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "themes"
CSS_FILES = [ROOT / "src" / "hbc-bubbles.css", ROOT / "src" / "hbc-theme.css"]
BACKGROUNDS = ROOT / "assets" / "generated"
CSS_MAX_LENGTH = 50_000

# Light: the Homebrew Channel menu. White tiles, grey-blue chrome, Wii blue.
LIGHT = {
    "canvas": "#f1f5f8",
    "chrome": "#e6edf3",
    "toolbar": "#e6edf3",
    "toolbarForeground": "#2b3640",
    "toolbarBorder": "#ccd9e3",
    "toolbarControl": "#ffffff",
    "toolbarControlForeground": "#2b3640",
    "toolbarControlHover": "#dcebf5",
    "surface": "#ffffff",
    "surfaceRaised": "#ffffff",
    "surfaceOverlay": "#ffffff",
    "text": "#2b3640",
    "textMuted": "#5f6f7d",
    "border": "#c9d6e1",
    "input": "#ffffff",
    "focus": "#34beed",
    "accent": "#0b7fbd",
    "accentForeground": "#ffffff",
    "secondary": "#e3eef6",
    "secondaryForeground": "#2b3640",
    "muted": "#e9f0f5",
    "mutedForeground": "#5f6f7d",
    "placeholder": "#7d8c99",
    "secondaryLabel": "#5f6f7d",
    "iconMuted": "#7d8c99",
    "error": "#d93a3a",
    "errorForeground": "#b42323",
    "errorSurface": "#fde8e8",
    "warning": "#e08a00",
    "warningForeground": "#9a5d00",
    "warningSurface": "#fff3dc",
    "update": "#0b7fbd",
    "updateForeground": "#0a6ea4",
    "updateSurface": "#ddf0fb",
    "accentSurface": "#dcf0fb",
    "accentSurfaceForeground": "#1f4a63",
    "messageSurface": "#ffffff",
    "messageForeground": "#2b3640",
    "messageAction": "#0b7fbd",
    "messageActionForeground": "#ffffff",
    "messageActionHover": "#096da3",
    "codeBackground": "#f3f7fa",
    "codeForeground": "#2b3640",
    "sidebar": "#e2ebf2",
    "sidebarForeground": "#2b3640",
    "sidebarMutedForeground": "#5f6f7d",
    "sidebarControlSurface": "#ffffff",
    "sidebarRowHover": "#d5e5f0",
    "sidebarRowActive": "#c6e3f5",
    "sidebarRowSelected": "#d0e8f7",
    "sidebarBorder": "#ccd9e3",
    "searchMatchBackground": "#bfe6f8",
    "searchMatchForeground": "#1f2a33",
    "searchMatchActiveBackground": "#34beed",
    "searchMatchActiveForeground": "#06202e",
    "terminalBackground": "#f7fafc",
    "terminalForeground": "#2b3640",
    "terminalCursor": "#0b7fbd",
    "terminalSelection": "#bfe3f5",
    "terminalScrollbar": "#c9d6e1",
    "terminalScrollbarHover": "#a9bccb",
}

# Dark: the same palette as the colors-only theme.
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


def variation(id_: str, name: str, palette: dict, accent: str, bubbles: str, hue: float,
              saturation: float = 1.0) -> dict:
    """A dark-only color variation with its own background and tinted bubbles."""
    return {
        "id": f"homebrew-channel-{id_}",
        "name": f"Homebrew Channel {name}",
        "appearance": "dark",
        "dark": palette,
        "background": f"background_wide_{id_}.webp",
        "css": f":root {{\n  --hbc-accent: {accent};\n  --hbc-bubble-filter: {bubbles};\n}}\n\n"
        + tinted_glass(hue, saturation),
    }


THEMES = [
    {
        "id": "homebrew-channel",
        "name": "Homebrew Channel",
        "appearance": "light",
        "light": LIGHT,
        "dark": DARK,
        "background": "background_wide.webp",
    },
    {
        # Backup: the navy gradient from before the background image.
        "id": "homebrew-channel-no-bg",
        "name": "Homebrew Channel (No Background)",
        "appearance": "light",
        "light": LIGHT,
        "dark": DARK,
        "background": None,
        "css": f".dark {{\n  --hbc-backdrop: {NAVY_BACKDROP};\n}}",
    },
    {
        "id": "homebrew-channel-pink",
        "name": "Homebrew Channel Pink",
        "appearance": "dark",
        "dark": PINK,
        "background": "background_wide_pink.webp",
        "css": ":root {\n  --hbc-accent: #ff9ecf;\n  --hbc-bubble-filter: hue-rotate(130deg) saturate(0.8);\n}\n\n"
        + glass("36, 13, 26", "52, 19, 38", "#5a2442"),
    },
    {
        "id": "homebrew-channel-red",
        "name": "Homebrew Channel Red",
        "appearance": "dark",
        "dark": RED,
        "background": "background_wide_red.webp",
        "css": ":root {\n  --hbc-accent: #ff4d5a;\n  --hbc-bubble-filter: hue-rotate(157deg);\n}\n\n"
        + glass("36, 10, 12", "50, 14, 18", "#5a2026"),
    },
    # Bubble art is hue 199; hue-rotate moves it to each channel color.
    variation("yellow", "Yellow", YELLOW, "#d4e600", "hue-rotate(225deg)", 64),
    variation("green", "Green", GREEN, "#2ed82b", "hue-rotate(281deg)", 120),
    variation("purple", "Purple", PURPLE, "#9b6dff", "hue-rotate(61deg)", 260),
    variation("orange", "Orange", ORANGE, "#f4790f", "hue-rotate(188deg)", 27),
    variation("grey", "Grey", GREY, "#e6e6e6", "grayscale(1)", 0, 0.0),
    variation("teal", "Teal", TEAL, "#2ee6c8", "hue-rotate(333deg)", 172),
    variation("gold", "Gold", GOLD, "#ffc233", "hue-rotate(206deg)", 45),
    variation("magenta", "Magenta", MAGENTA, "#e55cff", "hue-rotate(101deg)", 300),
    variation("indigo", "Indigo", INDIGO, "#6d7dff", "hue-rotate(36deg)", 235),
]


def background_css(name: str) -> str:
    """Embed a background as a data: URL, since themes cannot load files."""
    data = base64.b64encode((BACKGROUNDS / name).read_bytes()).decode("ascii")
    return f':root {{\n  --hbc-background-image: url("data:image/webp;base64,{data}");\n}}'


def build(spec: dict) -> dict:
    parts = []
    if spec["background"]:
        parts.append(background_css(spec["background"]))
    parts += [path.read_text("utf-8").strip() for path in CSS_FILES]
    if spec.get("css"):
        parts.append(spec["css"])
    css = "\n\n".join(parts) + "\n"
    if len(css) > CSS_MAX_LENGTH:
        raise SystemExit(f"{spec['id']}: CSS is {len(css)} characters; T3 Code allows {CSS_MAX_LENGTH}.")

    main_palette = spec["light"] if spec["appearance"] == "light" else spec["dark"]
    theme = {
        "version": 1,
        "name": spec["name"],
        "appearance": spec["appearance"],
        "canvas": main_palette["canvas"],
        "accent": main_palette["accent"],
        "colors": main_palette,
    }
    if spec["appearance"] == "light":
        theme["variants"] = {"dark": spec["dark"]}
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
