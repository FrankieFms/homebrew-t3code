# Homebrew Channel theme for T3 Code

A T3 Code theme inspired by the channel menu of The Homebrew Channel on the Nintendo Wii.

## Files

| File | What it is |
| --- | --- |
| `homebrew-channel-colors.json` | The colors-only theme. Light mode is the main look: a pale icy blue background, white panels and Wii-blue accents. Dark mode is a deep navy version. |
| `hbc-bubbles.css` | A pure-CSS version of the rising background bubbles. T3 Code themes cannot load CSS yet, so this file is not used by the theme. |

## Requirements

- T3 Code **Nightly**. Custom themes (`t3 theme`) are not in the stable release yet.
- The `t3` CLI. T3 Code installs it at `~/.t3/bin/t3` (`t3.cmd` on Windows).

Check that your build supports themes:

```sh
t3 theme --help
```

If the command shows `set`, `clear` and `show`, your build supports themes.

## Install

1. Clone or download this repository.
2. Open a terminal in the repository folder.
3. Publish the theme and make it the active theme:

   ```sh
   t3 theme set ./homebrew-channel-colors.json
   ```

   T3 Code publishes the file as the theme id `homebrew-channel-colors`.
   Connected T3 Code windows switch to it.

4. Check that the theme is active:

   ```sh
   t3 theme show
   ```

   The output should show `Environment theme: "homebrew-channel-colors"`.

The published copy lives in `~/.t3/userdata/themes/homebrew-channel-colors.json`.
After that first publish, you can switch back to it by id:

```sh
t3 theme set homebrew-channel-colors
```

### Install by copying the file

You can also copy `homebrew-channel-colors.json` into `~/.t3/userdata/themes/`
yourself. T3 Code watches that folder and lists the theme. Then pick it in
T3 Code, or run `t3 theme set homebrew-channel-colors`.

## Light and dark mode

The file sets `"appearance": "light"`. The dark palette is under `variants.dark`.
T3 Code picks the variant that matches your appearance setting.

## Update after editing

Run the install command again. It replaces the published copy:

```sh
t3 theme set ./homebrew-channel-colors.json
```

## Uninstall

Remove the theme from the environment:

```sh
t3 theme clear
```

Connected clients keep the theme they already have until you pick another
theme. To remove the published copy as well, delete
`~/.t3/userdata/themes/homebrew-channel-colors.json`.

## Limits

- A theme file holds colors only. Values must be hex (`#rgb` or `#rrggbb`).
- A theme file can be at most 32768 bytes.
- Theme files cannot load CSS, images or animations. The bubbles and the
  Homebrew Channel background will come in a later version, once T3 Code
  supports them.
