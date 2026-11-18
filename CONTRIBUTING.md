# Contributing

Thanks for helping with the Homebrew Channel theme. Bug reports, fixes and new
color ideas are all welcome.

## Goals

Every change should keep these true:

- **Close to the original.** The theme should look as much like The Homebrew
  Channel as T3 Code allows.
- **Works on T3 Code stable.** Use the stable selectors listed in T3 Code's theme
  guide. If a rule needs a selector outside that list, say so in its comment,
  because a T3 Code update can rename it.
- **Dark only.** There is no light mode. Do not add light-mode styles.
- **Light on power.** The bubbles animate behind the whole window. Avoid
  `backdrop-filter`, animating anything other than `transform` or `opacity`, and
  larger embedded images. Keep bubble images as WebP at quality 90.
- **Under the size limit.** Each theme's CSS must stay under 50,000 characters.
  The build script stops if it does not.

## Reporting a bug

Open an issue with the bug report form. Include:

- your T3 Code version and operating system,
- which theme you use,
- a screenshot, and the window size if the problem only shows in small or
  large windows.

## Making a change

1. Fork the repository and create a branch from `main`.
2. Edit the files in `src/` or `scripts/`. Do not edit `themes/*.json` by hand,
   except `homebrew-channel-colors.json`.
3. Rebuild the themes:

   ```sh
   python scripts/build-theme.py
   ```

4. Apply the theme and check it in T3 Code:

   ```sh
   t3 theme set ./themes/homebrew-channel.json
   ```

   Check a normal window and a narrow one, with the sidebar open and closed.
   If you changed colors, check a few color variations too.

5. Commit the source changes and the rebuilt `themes/*.json` together.
6. Open a pull request. Add before and after screenshots for any visual change.

[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) explains the project layout, how to
add a color variation and how releases work.

## After a T3 Code update

T3 Code can rename elements between releases. `scripts/check-selectors.js`
checks that the elements the theme styles still exist. Paste it into the
DevTools console in T3 Code (Ctrl+Shift+I, or Cmd+Option+I on macOS). The
comment at the top of the script explains how to read the results.

## Style

- CSS comments explain why a rule exists, not what it does.
- Keep the comments in `src/`. The build script removes them from the theme files.
- Write commit messages in the imperative, such as "Fix sidebar overlay in narrow windows".

## License

This theme builds on The Homebrew Channel's GPL source code, so it is released
under the [GNU General Public License, version 2 or later](LICENSE). By
contributing, you agree that your contributions are licensed under the same terms.

Only use Homebrew Channel material from the
[fail0verflow/hbc](https://github.com/fail0verflow/hbc) repository, and credit it.
Do not add Nintendo assets.
