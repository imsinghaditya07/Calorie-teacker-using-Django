/* CalorieTrack — Main JS */

// ── Theme Toggle ──────────────────────────────────────────────────────────────
(function () {
  const KEY = 'ct-theme';
  const html = document.documentElement;

  // Apply saved preference (also done inline in <head> to avoid FOUC)
  const saved = localStorage.getItem(KEY);
  if (saved) html.setAttribute('data-theme', saved);

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(KEY, theme);
  }

  function toggle() {
    const current = html.getAttribute('data-theme');
    setTheme(current === 'light' ? 'dark' : 'light');
  }

  // Wire up both buttons (sidebar + mobile topbar)
  ['themeToggle', 'themeToggleMobile'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', toggle);
  });
})();



// ── Sidebar toggle (mobile) ───────────────────────────────────────────────────
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const toggleBtn = document.getElementById('sidebarToggle');

if (toggleBtn) {
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
  });
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  });
}

// ── Auto-dismiss alerts ───────────────────────────────────────────────────────
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-8px)';
    setTimeout(() => alert.remove(), 500);
  }, 4000);
});

// ── SVG gradient for progress ring ───────────────────────────────────────────
(function () {
  const svg = document.querySelector('.progress-ring');
  if (!svg) return;
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.innerHTML = `
    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0ea5e9"/>
    </linearGradient>`;
  svg.insertBefore(defs, svg.firstChild);

  // Animate ring in
  const fill = svg.querySelector('.ring-fill');
  if (fill) {
    const pct = parseInt(fill.getAttribute('data-pct') || 0);
    const circumference = 314.16;
    fill.style.strokeDashoffset = circumference;
    requestAnimationFrame(() => {
      fill.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)';
      fill.style.strokeDashoffset = circumference - (circumference * pct / 100);
    });
  }
})();

// ── Macro bar animations ──────────────────────────────────────────────────────
document.querySelectorAll('.macro-bar-fill').forEach(bar => {
  const w = bar.style.width;
  bar.style.width = '0';
  setTimeout(() => { bar.style.width = w; }, 300);
});

// ── Date input — set today if empty ──────────────────────────────────────────
document.querySelectorAll('input[type=date]').forEach(el => {
  if (!el.value) {
    const d = new Date();
    el.value = d.toISOString().split('T')[0];
  }
});
