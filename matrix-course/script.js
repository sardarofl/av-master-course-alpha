// Matrix Video Course - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const navLinks = document.querySelectorAll('.nav-link');
    const modules = document.querySelectorAll('.module');
    const progressBar = document.getElementById('progressBar');
    
    // Total modules
    const totalModules = modules.length;
    
    // Load saved progress
    const savedProgress = localStorage.getItem('matrixCourseProgress');
    let currentModule = savedProgress ? parseInt(savedProgress) : 1;
    
    // Initialize
    showModule(currentModule);
    updateProgress();
    
    // Navigation click handlers
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const moduleNum = parseInt(this.dataset.module);
            showModule(moduleNum);
        });
    });
    
    // Show module function
    function showModule(moduleNum) {
        // Hide all modules
        modules.forEach(module => {
            module.classList.remove('active');
        });
        
        // Remove active class from nav links
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Show target module
        const targetModule = document.getElementById('module' + moduleNum);
        if (targetModule) {
            targetModule.classList.add('active');
        }
        
        // Add active class to nav link
        const targetLink = document.querySelector(`.nav-link[data-module="${moduleNum}"]`);
        if (targetLink) {
            targetLink.classList.add('active');
        }
        
        // Save progress
        localStorage.setItem('matrixCourseProgress', moduleNum);
        
        // Update progress bar
        updateProgress();
        
        // Scroll to top
        window.scrollTo(0, 0);
    }
    
    // Update progress bar
    function updateProgress() {
        const progress = (currentModule / totalModules) * 100;
        if (progressBar) progressBar.style.width = progress + '%';
        const pct = document.getElementById('progressPct');
        if (pct) pct.textContent = Math.round(progress) + '%';
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            // Previous module
            if (currentModule > 1) {
                showModule(currentModule - 1);
            }
        } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
            // Next module
            if (e.key === ' ') e.preventDefault(); // Prevent scrolling on space
            if (currentModule < totalModules) {
                showModule(currentModule + 1);
            }
        }
    });
    
    // Add smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe concept cards and other elements
    document.querySelectorAll('.concept-card, .comparison-card, .warning-box').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
    
    console.log('Matrix Video Course loaded successfully');
    console.log(`Total modules: ${totalModules}`);
});
