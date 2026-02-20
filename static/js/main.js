/**
 * main.js — Global UI helpers: alerts, progress ring animation, date inputs.
 */
document.addEventListener('DOMContentLoaded', () => {

    // ── Auto-dismiss alert messages ──────────────────────────────────────────────
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // ── SVG progress ring animation ───────────────────────────────────────────────
    const svg = document.querySelector('.progress-ring');
    if (svg) {
        const fill = svg.querySelector('.ring-fill, .tf-ring-fill');
        if (fill) {
            const pct = parseInt(fill.getAttribute('data-pct') || '0', 10);
            const circumference = 314.16;
            fill.style.strokeDashoffset = String(circumference);
            requestAnimationFrame(() => {
                fill.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)';
                fill.style.strokeDashoffset = String(circumference - (circumference * pct / 100));
            });
        }
    }

    // ── Macro / stat bar entrance animations ─────────────────────────────────────
    document.querySelectorAll('.macro-bar-fill, .tf-bar-fill').forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => { bar.style.width = targetWidth; }, 200);
    });

    // ── Date inputs — default to today if empty ───────────────────────────────────
    document.querySelectorAll('input[type="date"]').forEach(el => {
        if (!el.value) {
            el.value = new Date().toISOString().split('T')[0];
        }
    });

});
