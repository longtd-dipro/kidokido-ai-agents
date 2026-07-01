// Render ```mermaid fenced code blocks client-side.
// MkDocs (theme readthedocs, no mkdocs-material) outputs fenced code as
// <pre><code class="language-mermaid">...</code></pre> — convert those into
// <div class="mermaid">...</div> and let mermaid.js render them.
document.addEventListener("DOMContentLoaded", function () {
  if (!window.mermaid) return;
  mermaid.initialize({ startOnLoad: false, theme: "default" });
  var blocks = document.querySelectorAll("pre code.language-mermaid");
  blocks.forEach(function (block) {
    var pre = block.parentElement;
    var container = document.createElement("div");
    container.className = "mermaid";
    container.textContent = block.textContent;
    pre.replaceWith(container);
  });
  mermaid.run();
});
