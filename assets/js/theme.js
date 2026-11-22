(() => {
    "use strict";
    const root = document.documentElement;
    const body = document.body;
    const modes = ["auto", "light", "dark"];
    const labels = { auto: "Follow system", light: "Light", dark: "Dark" };
    const valid = (value) => modes.includes(value);
    const configured = body.dataset.theme;
    let mode = valid(configured) ? configured : "auto";
    try {
        const saved = localStorage.getItem("theme");
        if (valid(saved)) mode = saved;
    } catch {
        // Storage can be unavailable in restricted browsers.
    }

    let button;
    const nextMode = () => modes[(modes.indexOf(mode) + 1) % modes.length];
    function render() {
        // With neither class set, the theme's media queries follow the system live.
        root.classList.toggle("light", mode === "light");
        root.classList.toggle("dark", mode === "dark");
        root.style.colorScheme = mode === "auto" ? "light dark" : mode;
        if (button) {
            const icon = document.getElementById(`theme-icon-${mode}`)?.content.cloneNode(true);
            if (icon) {
                icon.querySelector("svg")?.setAttribute("aria-hidden", "true");
                button.replaceChildren(icon);
            } else {
                button.textContent = labels[mode];
            }
            const label = `Theme: ${labels[mode]}. Switch to ${labels[nextMode()]}.`;
            button.title = label;
            button.setAttribute("aria-label", label);
        }
    }

    render();
    requestAnimationFrame(() => body.classList.remove("notransition"));
    document.addEventListener("DOMContentLoaded", () => {
        const control = document.getElementById("mode");
        if (control) {
            button = document.createElement("button");
            button.type = "button";
            button.id = "mode";
            control.replaceWith(button);
            button.addEventListener("click", () => {
                mode = nextMode();
                try {
                    localStorage.setItem("theme", mode);
                } catch {
                    // The choice still applies until the page is reloaded.
                }
                render();
            });
            render();
        }
        const menu = document.getElementById("menu-trigger");
        menu?.addEventListener("change", () => {
            document.querySelector(".wrapper")?.classList.toggle("blurry", menu.checked);
        });
    });
})();
