function updatePicker(picker, value) {
  const input = picker.querySelector('input[type="hidden"]');
  if (!input) return;

  const selected = picker.querySelector(
    `.priority-option[data-value="${value}"]`,
  );

  if (!selected) return;

  input.value = value;

  picker.querySelectorAll(".priority-option").forEach((button) => {
    const active = button === selected;

    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

export function resetPicker(pickerId) {
  const input = document.getElementById(pickerId);
  const picker = input?.closest(".priority-picker");

  if (picker) updatePicker(picker, "");
}

export function initPriorityPickers() {
  document.querySelectorAll(".priority-picker").forEach((picker) => {
    const input = picker.querySelector('input[type="hidden"]');
    if (input) updatePicker(picker, input.value);
  });

  document.addEventListener("click", (event) => {
    const button = event.target.closest(".priority-option[data-picker]");
    if (!button) return;

    const input = document.getElementById(button.dataset.picker);
    const picker = input?.closest(".priority-picker");

    if (picker) updatePicker(picker, button.dataset.value);
  });
}
