/**
 * theme.js — Light / Dark mode toggle with localStorage persistence.
 * Injected early (in <head>) via an inline snippet to avoid flash of wrong theme.
 * This module re-applies and wires up the toggle buttons once the DOM is ready.
 */
(function () {
    const KEY = 'ct-theme';
    const html = document.documentElement;

    function setTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem(KEY, theme);

        // Update icon on all toggle buttons
        document.querySelectorAll('.theme-toggle i').forEach(icon => {
            icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        });
    }

    function toggle() {
        const current = html.getAttribute('data-theme') || 'dark';
        setTheme(current === 'light' ? 'dark' : 'light');
    }

    // Apply saved preference (also done inline in <head> to prevent FOUC)
    const saved = localStorage.getItem(KEY);
    if (saved) setTheme(saved);

    // Wire up all toggle buttons once DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        ['themeToggle', 'themeToggleMobile'].forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.addEventListener('click', toggle);
        });
        // Set correct icon on load
        const current = html.getAttribute('data-theme') || 'dark';
        document.querySelectorAll('.theme-toggle i').forEach(icon => {
            icon.className = current === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        });
    });
})();
