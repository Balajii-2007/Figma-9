/**
 * main.js — Sports Event Registration
 * Client-side enhancements (validation feedback, UX polish).
 */

"use strict";

// ── Input live validation ──────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {

  // Clear error styling on input
  document.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", () => {
      input.classList.remove("error");
      const errEl = input.closest(".field")?.querySelector(".field-error");
      if (errEl) errEl.textContent = "";
    });
  });

  // Auto-dismiss flash messages after 4 s
  document.querySelectorAll(".flash").forEach(el => {
    setTimeout(() => {
      el.style.transition = "opacity .4s";
      el.style.opacity    = "0";
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  // Highlight event card on click (loading feedback)
  document.querySelectorAll(".event-card:not(:disabled)").forEach(card => {
    card.addEventListener("click", function () {
      this.style.borderColor  = "var(--orange)";
      this.style.background   = "#fff7ed";
      this.style.pointerEvents = "none";

      // Spinner inside icon
      const icon = this.querySelector(".event-icon");
      if (icon) {
        const prev = icon.textContent;
        icon.textContent = "⏳";
        setTimeout(() => { icon.textContent = prev; }, 3000);
      }
    });
  });

  // Email format hint
  const emailInput = document.getElementById("email");
  if (emailInput) {
    emailInput.addEventListener("blur", () => {
      const val = emailInput.value.trim();
      const field = emailInput.closest(".field");
      if (!field) return;
      let hint = field.querySelector(".field-hint");
      if (val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
        if (!hint) {
          hint = document.createElement("span");
          hint.className = "field-error field-hint";
          field.appendChild(hint);
        }
        hint.textContent = "Please enter a valid email address.";
        emailInput.classList.add("error");
      } else if (hint) {
        hint.textContent = "";
        emailInput.classList.remove("error");
      }
    });
  }
});
