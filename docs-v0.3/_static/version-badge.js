document.addEventListener("DOMContentLoaded", function () {
  function applyLatestBadgeText() {
    var latestTokenPattern = /\|\s*Latest\b/;
    var titleNodes = document.querySelectorAll(".sy-head .sy-head-links a > span, .sy-head .sy-head-links button > span");

    titleNodes.forEach(function (titleNode) {
      var container = titleNode.parentElement;
      if (!container || container.querySelector(".version-latest-badge")) {
        return;
      }

      var text = (titleNode.textContent || "").trim();
      if (!latestTokenPattern.test(text)) {
        return;
      }

      var label = text.replace(/\s*\|\s*Latest\b\s*/, " ").trim();
      if (!label) {
        return;
      }

      titleNode.textContent = label;
      titleNode.classList.add("version-label");

      var badgeSpan = document.createElement("span");
      badgeSpan.className = "version-latest-badge";
      badgeSpan.textContent = "Latest";

      if (container.querySelector("small")) {
        // Keep title and summary stacked; badge sits to the right, vertically centered.
        container.classList.add("has-latest-badge");
        container.appendChild(badgeSpan);
      } else {
        titleNode.appendChild(document.createTextNode(" "));
        titleNode.appendChild(badgeSpan);
      }
    });
  }

  applyLatestBadgeText();

  // Re-apply when nav DOM mutates (e.g., dropdown nodes are toggled/updated).
  var head = document.querySelector(".sy-head");
  if (head) {
    var observer = new MutationObserver(function () {
      applyLatestBadgeText();
    });
    observer.observe(head, { childList: true, subtree: true });
  }
});
