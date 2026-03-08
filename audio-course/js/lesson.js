// Shared lesson page functionality

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Add copy buttons to all code blocks that don't have them
    document.querySelectorAll('.code-block pre').forEach(pre => {
        if (!pre.nextElementSibling || !pre.nextElementSibling.classList.contains('copy-btn')) {
            const btn = document.createElement('button');
            btn.className = 'copy-btn';
            btn.textContent = 'Copy';
            btn.onclick = function() {
                navigator.clipboard.writeText(pre.textContent).then(() => {
                    btn.textContent = 'Copied!';
                    setTimeout(() => btn.textContent = 'Copy', 2000);
                });
            };
            pre.parentElement.appendChild(btn);
        }
    });

    // Progress persistence
    saveScrollPosition();
    restoreScrollPosition();
});

function saveScrollPosition() {
    window.addEventListener('beforeunload', () => {
        const path = window.location.pathname;
        sessionStorage.setItem(`scroll_${path}`, window.scrollY);
    });
}

function restoreScrollPosition() {
    const path = window.location.pathname;
    const savedScroll = sessionStorage.getItem(`scroll_${path}`);
    if (savedScroll) {
        window.scrollTo(0, parseInt(savedScroll));
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K: Toggle sidebar (if on mobile/collapsed view)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('collapsed');
        }
    }
});