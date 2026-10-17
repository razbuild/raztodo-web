const THEME_KEY = "theme";

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);

  const button = document.getElementById("theme-toggle");
  if (button) {
    const icon = button.querySelector(".theme-icon");

    if (icon) {
      icon.src =
        theme === "dark"
          ? "/static/img/dark.svg"
          : "/static/img/light.svg";
    }
  }
}


function toggleTheme() {
  const current =
    document.documentElement.getAttribute("data-theme") || "dark";

  const next = current === "dark" ? "light" : "dark";

  const button = document.getElementById("theme-toggle");
  const root = document.documentElement;

  if (button) {
    const rect = button.getBoundingClientRect();

    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;

    const radius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y)
    );

    root.style.setProperty("--theme-x", `${x}px`);
    root.style.setProperty("--theme-y", `${y}px`);
    root.style.setProperty("--theme-radius", `${radius}px`);
  }

  const update = () => {
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  };

  if (document.startViewTransition) {
    document.startViewTransition(update);
  } else {
    update();
  }
}

export function initTheme() {
  const savedTheme = localStorage.getItem(THEME_KEY) || "dark";
  applyTheme(savedTheme);

  document
    .getElementById("theme-toggle")
    ?.addEventListener("click", toggleTheme);
}
