// LED Displays Course - Interactive JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    loadStage(1);
    updateProgress();
});

// Navigation initialization
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const stageNum = parseInt(this.dataset.stage);
            loadStage(stageNum);
        });
    });
}

// Load specific stage
function loadStage(stageNum) {
    // Hide all stages
    const stages = document.querySelectorAll('.stage');
    stages.forEach(stage => stage.classList.remove('active'));
    
    // Show selected stage
    const targetStage = document.getElementById(`section${stageNum}`);
    if (targetStage) {
        targetStage.classList.add('active');
        
        // Update navigation active state
        updateNavActive(stageNum);
        
        // Update progress bar
        updateProgress();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Store current stage in localStorage
        localStorage.setItem('currentStage', stageNum);
    }
}

// Update navigation active state
function updateNavActive(stageNum) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (parseInt(link.dataset.stage) === stageNum) {
            link.classList.add('active');
        }
    });
}

// Update progress bar
function updateProgress() {
    const completedStages = getCompletedStages();
    const progress = (completedStages.length / 13) * 100;
    const progressBar = document.getElementById('progressBar');
    if (progressBar) progressBar.style.width = `${progress}%`;
    const pct = document.getElementById('progressPct');
    if (pct) pct.textContent = Math.round(progress) + '%';
}

// Get completed stages from localStorage
function getCompletedStages() {
    const completed = localStorage.getItem('completedStages');
    return completed ? JSON.parse(completed) : [];
}

// Mark stage as completed
function markStageComplete(stageNum) {
    let completed = getCompletedStages();
    if (!completed.includes(stageNum)) {
        completed.push(stageNum);
        localStorage.setItem('completedStages', JSON.stringify(completed));
        updateProgress();
    }
}

// Navigate to specific stage (called from buttons)
function navigateStage(stageNum) {
    // Mark current stage as completed before moving
    const currentStage = getCurrentStage();
    markStageComplete(currentStage);
    
    // Load new stage
    loadStage(stageNum);
}

// Get current stage
function getCurrentStage() {
    const currentStage = localStorage.getItem('currentStage');
    return currentStage ? parseInt(currentStage) : 1;
}

// Reset progress (for testing)
function resetProgress() {
    if (confirm('Are you sure you want to reset your progress?')) {
        localStorage.removeItem('completedStages');
        localStorage.removeItem('currentStage');
        updateProgress();
        loadStage(1);
    }
}

// Load saved state on page load
window.addEventListener('load', function() {
    const savedStage = getCurrentStage();
    loadStage(savedStage);
});

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    const currentStage = getCurrentStage();
    
    // Left arrow - previous stage
    if (e.key === 'ArrowLeft' && currentStage > 1) {
        navigateStage(currentStage - 1);
    }
    
    // Right arrow - next stage
    if (e.key === 'ArrowRight' && currentStage < 13) {
        navigateStage(currentStage + 1);
    }
});

// Track time spent on each stage (analytics)
let stageStartTime = Date.now();

function trackStageTime() {
    const currentStage = getCurrentStage();
    const timeSpent = Math.floor((Date.now() - stageStartTime) / 1000);
    
    // Store in localStorage
    let stageTimes = localStorage.getItem('stageTimes');
    stageTimes = stageTimes ? JSON.parse(stageTimes) : {};
    stageTimes[`stage${currentStage}`] = (stageTimes[`stage${currentStage}`] || 0) + timeSpent;
    localStorage.setItem('stageTimes', JSON.stringify(stageTimes));
    
    // Reset timer
    stageStartTime = Date.now();
}

// Track time when leaving page or changing stage
window.addEventListener('beforeunload', trackStageTime);

// Print friendly function
function printStage() {
    window.print();
}

// Export progress as JSON
function exportProgress() {
    const progress = {
        currentStage: getCurrentStage(),
        completedStages: getCompletedStages(),
        stageTimes: JSON.parse(localStorage.getItem('stageTimes') || '{}'),
        exportDate: new Date().toISOString()
    };
    
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(progress, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "audio-course-progress.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
}

// Add smooth scrolling to all internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Highlight code blocks (if any)
function highlightCode() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        block.classList.add('highlighted');
    });
}

// Initialize tooltips (if needed)
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
            tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Check for saved theme preference
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
}

// Toggle dark theme (optional feature)
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// Search functionality (basic)
function searchContent(query) {
    const stages = document.querySelectorAll('.stage');
    const results = [];
    
    stages.forEach((stage, index) => {
        const content = stage.textContent.toLowerCase();
        if (content.includes(query.toLowerCase())) {
            results.push({
                stage: index + 1,
                preview: getPreview(stage, query)
            });
        }
    });
    
    return results;
}

function getPreview(stage, query) {
    const content = stage.textContent;
    const index = content.toLowerCase().indexOf(query.toLowerCase());
    if (index === -1) return '';
    
    const start = Math.max(0, index - 50);
    const end = Math.min(content.length, index + query.length + 50);
    return '...' + content.substring(start, end) + '...';
}

// Initialize everything on load
window.addEventListener('load', function() {
    loadTheme();
    highlightCode();
    initTooltips();
    
    console.log('LED Displays Course loaded successfully!');
    console.log('Current stage:', getCurrentStage());
    console.log('Completed stages:', getCompletedStages());
});

// Helper function to get URL parameters
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Check if specific stage requested via URL
const requestedStage = getUrlParameter('stage');
if (requestedStage) {
    const stageNum = parseInt(requestedStage);
    if (stageNum >= 1 && stageNum <= 13) {
        loadStage(stageNum);
    }
}

// Add Easter egg for course completion
function checkCompletion() {
    const completed = getCompletedStages();
    if (completed.length === 13) {
        setTimeout(() => {
            alert('🎉 Congratulations! You\'ve completed the entire LED Displays Course! You\'re now ready to design and specify professional LED display systems!');
        }, 500);
    }
}

// Run completion check periodically
setInterval(checkCompletion, 5000);
