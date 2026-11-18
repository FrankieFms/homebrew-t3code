// Checks that T3 Code still has the elements the Homebrew Channel theme styles.
//
// Run it after a T3 Code update:
//   1. In T3 Code, open DevTools with Ctrl+Shift+I (Cmd+Option+I on macOS).
//   2. Open the Console tab, paste this whole file and press Enter.
//
// Some elements only exist in certain states. Before running, open a thread,
// open the right panel, and if you can, have a question prompt or banner
// showing above the chat box. A "not found" row whose "Needs" state was not on
// screen is not a problem; run the script again with that state showing.
//
// "Non-stable" rows use selectors outside T3 Code's stable theme list, so an
// update can rename them. If one is not found while its state is showing,
// the matching rule in src/hbc-theme.css needs a new selector.

(() => {
  const checks = [
    // Not on T3 Code's stable list.
    ["Non-stable", "Selected thread row", '[data-thread-item] [data-sidebar-row][aria-current="page"]', "A thread open"],
    ["Non-stable", "Left resize edge", '[data-slot="sidebar-rail"]', "Sidebar open"],
    ["Non-stable", "Right resize edge", '[data-workspace-area="panel"] [role="separator"] > span', "Right panel open"],
    ["Non-stable", "New-thread fill", "[data-timeline-loading]", "New thread screen, or a thread loading"],
    ["Non-stable", "Chat box banner", "[data-composer-banner-stack]", "A banner above the chat box"],
    ["Non-stable", "Question prompt", "[data-pending-user-input-toggle]", "A question prompt above the chat box"],
    ["Non-stable", "Compact chip", '[data-chat-composer-form] button[aria-label^="Compact "]', "A thread with the Compact chip shown"],
    // On T3 Code's stable list: these should always be found in their state.
    ["Stable", "Sidebar", '[data-slot="sidebar-inner"]', "Sidebar open"],
    ["Stable", "Thread row", "[data-thread-item]", "Any thread in the sidebar"],
    ["Stable", "Chat area", '[data-workspace-area="conversation"]', "A thread open"],
    ["Stable", "Chat box", '[data-slot="composer-host"]', "A thread open"],
    ["Stable", "Button", '[data-slot="button"]', "Always"],
  ];

  const rows = checks.map(([kind, name, selector, needs]) => {
    let count;
    try {
      count = document.querySelectorAll(selector).length;
    } catch {
      count = -1;
    }
    return {
      Result: count > 0 ? "✅ found" : count === 0 ? "❌ not found" : "⚠️ bad selector",
      Kind: kind,
      Element: name,
      Count: Math.max(count, 0),
      Needs: needs,
      Selector: selector,
    };
  });

  const themeId = document.documentElement.getAttribute("data-theme-id") || "(none)";
  console.log(`Homebrew Channel selector check. Active theme: ${themeId}`);
  console.table(rows);

  const missing = rows.filter((row) => !row.Result.startsWith("✅"));
  console.log(
    missing.length
      ? `${missing.length} not found. Check that each one's "Needs" state was on screen, then run again.`
      : "All found.",
  );

  // Put a plain-text copy on the clipboard, ready to paste into a chat.
  // copy() is a DevTools console helper, so it only exists when the script
  // is pasted into the Console.
  const text = [
    `Homebrew Channel selector check. Active theme: ${themeId}`,
    ...rows.map((row) => `${row.Result} | ${row.Kind} | ${row.Element} (${row.Count}) | needs: ${row.Needs}`),
  ].join("\n");
  if (typeof copy === "function") {
    copy(text);
    console.log("Results copied to the clipboard.");
  } else {
    console.log(text);
  }
})();
