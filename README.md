# Homebrew Channel theme for T3 Code

A T3 Code theme inspired by the channel menu of The Homebrew Channel on the Nintendo Wii.
Bubbles rise behind the chat, panels are frosted glass, and messages sit in rounded channel tiles.

## Themes

All themes are in the `themes/` folder.

| Theme file | Theme id | Look |
| --- | --- | --- |
| `homebrew-channel.json` | `homebrew-channel` | Main theme. Dark mode uses the Homebrew Channel underwater background. Light mode is a soft white menu look. |
| `homebrew-channel-no-bg.json` | `homebrew-channel-no-bg` | Backup of the main theme with no background image. Dark mode uses a navy gradient. |
| `homebrew-channel-pink.json` | `homebrew-channel-pink` | Dark only. Light pink water, pink bubbles and accents. |
| `homebrew-channel-red.json` | `homebrew-channel-red` | Dark only. Red water, red bubbles and accents. |
| `homebrew-channel-yellow.json` | `homebrew-channel-yellow` | Dark only. Lime-yellow water, bubbles and accents. |
| `homebrew-channel-green.json` | `homebrew-channel-green` | Dark only. Green water, bubbles and accents. |
| `homebrew-channel-purple.json` | `homebrew-channel-purple` | Dark only. Purple water, bubbles and accents. |
| `homebrew-channel-orange.json` | `homebrew-channel-orange` | Dark only. Orange water, bubbles and accents. |
| `homebrew-channel-grey.json` | `homebrew-channel-grey` | Dark only. Charcoal water, grey bubbles and white accents. |
| `homebrew-channel-teal.json` | `homebrew-channel-teal` | Dark only. Teal water, bubbles and accents. |
| `homebrew-channel-gold.json` | `homebrew-channel-gold` | Dark only. Gold water, bubbles and accents. |
| `homebrew-channel-magenta.json` | `homebrew-channel-magenta` | Dark only. Magenta water, bubbles and accents. |
| `homebrew-channel-indigo.json` | `homebrew-channel-indigo` | Dark only. Indigo water, bubbles and accents. |

`themes/homebrew-channel-colors.json` is a colors-only version with no CSS: a dark, deep navy look with Wii-blue accents.

Set T3 Code to dark mode for the color variations. They have no light palette.

## Requirements

- The `t3` CLI. T3 Code installs it at `~/.t3/bin/t3` (`t3.cmd` on Windows).

Check that your build supports themes:

```sh
t3 theme --help
```

If the command shows `set`, `clear` and `show`, your build supports themes.

## Install

1. Clone or download this repository.
2. Open a terminal in the repository folder.
3. Publish a theme and make it the active theme. For example, the main theme:

   ```sh
   t3 theme set ./themes/homebrew-channel.json
   ```

   T3 Code publishes the file under its file name as the theme id, here `homebrew-channel`.
   Connected T3 Code windows switch to it.

4. Check that the theme is active:

   ```sh
   t3 theme show
   ```

   The output should show `Environment theme: "homebrew-channel"`.

The published copy lives in `~/.t3/userdata/themes/`. After the first publish,
you can switch between published themes by id:

```sh
t3 theme set homebrew-channel-pink
```

### Install by copying the file

You can also copy a theme file into `~/.t3/userdata/themes/` yourself.
T3 Code watches that folder and lists the theme. Then pick it in T3 Code,
or run `t3 theme set <theme id>`.

## Customize

```
themes/              Ready-to-use theme files. Built by scripts/build-theme.py,
                     except homebrew-channel-colors.json, which is edited by hand.
src/
  hbc-bubbles.css    A pure-CSS version of the rising background bubbles.
  hbc-theme.css      The Homebrew Channel styling for T3 Code's layout.
scripts/
  build-theme.py     Holds the palettes and the list of themes. Merges them with
                     the CSS and backgrounds into themes/.
  make-backgrounds.py  Makes the recolored WebP backgrounds. Needs Pillow.
archive/             Unreleased experiments, such as the rainbow theme.
                     Built by scripts/build-theme.py. Not supported.
assets/
  source/            The original Homebrew Channel backgrounds.
  generated/         The compressed WebP backgrounds the themes embed.
```

The dark palette of the main theme comes from `themes/homebrew-channel-colors.json`.
The pink and red palettes are tinted from it.

After editing a CSS file or a palette, rebuild the themes and apply one:

```sh
python scripts/build-theme.py
t3 theme set ./themes/homebrew-channel.json
```

To add a color variation, add a background entry in `scripts/make-backgrounds.py`
and a theme entry in `THEMES` in `scripts/build-theme.py`. Then run both scripts:

```sh
pip install pillow
python scripts/make-backgrounds.py
python scripts/build-theme.py
```

Each theme's CSS can be at most 50,000 characters. The build script stops if one is longer.

## Uninstall

Remove the theme from the environment:

```sh
t3 theme clear
```

Connected clients keep the theme they already have until you pick another
theme. To remove the published copies as well, delete the theme files from
`~/.t3/userdata/themes/`.

## Limits

- Color values must be hex (`#rgb` or `#rrggbb`).
- The `css` field holds at most 50,000 characters. Images must be embedded as `data:` URLs.
- CSS cannot reach the terminal text, the file tree or diff internals. Those use the color roles.
