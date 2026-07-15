/**
 * Theme palette helpers for ThemeConfig admin.
 * Syncs: color input <-> hex input <-> preview <-> swatches.
 */
(function () {
  "use strict";

  function normalizeHex(v) {
    if (!v) return "";
    let s = String(v).trim();
    if (!s) return "";
    if (s[0] !== "#") s = "#" + s;
    // Expand short #rgb to #rrggbb
    if (s.length === 4) {
      s = "#" + s[1] + s[1] + s[2] + s[2] + s[3] + s[3];
    }
    return s;
  }

  function isValidHex(v) {
    return /^#[0-9a-fA-F]{6}$/.test(v);
  }

  function setValue(root, hex) {
    const picker = root.querySelector(".admin-color-picker");
    const hexInput = root.querySelector("input.admin-color-hex");
    const previewSwatch = root.querySelector(".admin-color-preview-swatch");
    const previewHex = root.querySelector(".admin-color-preview-hex");
    const preview = root.querySelector(".admin-color-preview");

    if (!picker || !hexInput) return;

    const norm = normalizeHex(hex);
    if (!isValidHex(norm)) return;

    picker.value = norm;
    hexInput.value = norm;

    if (previewSwatch) previewSwatch.style.background = norm;
    if (previewHex) previewHex.textContent = norm;
    if (preview) preview.title = norm;
  }

  function initField(root) {
    const picker = root.querySelector(".admin-color-picker");
    const hexInput = root.querySelector("input.admin-color-hex");
    if (!picker || !hexInput) return;

    // Initialize preview from current value
    const initial = normalizeHex(hexInput.value) || picker.value;
    if (isValidHex(initial)) setValue(root, initial);

    picker.addEventListener("input", function () {
      setValue(root, picker.value);
    });

    hexInput.addEventListener("input", function () {
      const v = normalizeHex(hexInput.value);
      // don't force-update until hex is valid
      if (isValidHex(v)) setValue(root, v);
    });

    root.querySelectorAll(".admin-color-swatch").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const c = btn.getAttribute("data-color");
        if (c) setValue(root, c);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-color-field]").forEach(initField);
  });
})();

