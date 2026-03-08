// Progress tracking system
class CourseProgress {
    constructor() {
        this.totalDays = 5; // Changed to 5 sections
        this.storageKey = 'po_course_progress';
        this.init();
    }

    init() {
        this.loadProgress();
        this.updateUI();
    }

    loadProgress() {
        const saved = localStorage.getItem(this.storageKey);
        this.data = saved ? JSON.parse(saved) : this.getDefaultData();
    }

    getDefaultData() {
        return {
            days: {
                1: { completed: false, checkpoints: {} },
                2: { completed: false, checkpoints: {} },
                3: { completed: false, checkpoints: {} },
                4: { completed: false, checkpoints: {} },
                5: { completed: false, checkpoints: {} }
            },
            lastAccessed: Date.now()
        };
    }

    save() {
        this.data.lastAccessed = Date.now();
        localStorage.setItem(this.storageKey, JSON.stringify(this.data));
        this.updateUI();
    }

    markDayComplete(dayNumber) {
        this.data.days[dayNumber].completed = true;
        this.save();
    }

    markDayIncomplete(dayNumber) {
        this.data.days[dayNumber].completed = false;
        this.save();
    }

    isDayComplete(dayNumber) {
        return this.data.days[dayNumber]?.completed || false;
    }

    markCheckpoint(dayNumber, checkpointId, complete = true) {
        if (!this.data.days[dayNumber].checkpoints) {
            this.data.days[dayNumber].checkpoints = {};
        }
        this.data.days[dayNumber].checkpoints[checkpointId] = complete;
        this.save();
    }

    isCheckpointComplete(dayNumber, checkpointId) {
        return this.data.days[dayNumber]?.checkpoints?.[checkpointId] || false;
    }

    getCompletedCount() {
        return Object.values(this.data.days).filter(d => d.completed).length;
    }

    getProgressPercent() {
        return Math.round((this.getCompletedCount() / this.totalDays) * 100);
    }

    updateUI() {
        // Update overall progress bar
        const progressFill = document.getElementById('overallProgress');
        const progressPercent = document.getElementById('progressPercent');
        const completedDays = document.getElementById('completedDays');

        if (progressFill) {
            progressFill.style.width = this.getProgressPercent() + '%';
        }
        if (progressPercent) {
            progressPercent.textContent = this.getProgressPercent();
        }
        if (completedDays) {
            completedDays.textContent = this.getCompletedCount();
        }

        // Mark completed days in the list
        for (let i = 1; i <= this.totalDays; i++) {
            const dayItem = document.querySelector(`.day-item[data-day="${i}"]`);
            if (dayItem) {
                if (this.isDayComplete(i)) {
                    dayItem.classList.add('completed');
                } else {
                    dayItem.classList.remove('completed');
                }
            }
        }

        // Check for completion celebration
        if (this.getCompletedCount() === this.totalDays) {
            this.celebrateCompletion();
        }
    }

    celebrateCompletion() {
        if (!sessionStorage.getItem('celebrated')) {
            setTimeout(() => {
                alert('🎉 Congratulations! You completed the course!\n\nNow go apply to those jobs and get your first $100!');
                sessionStorage.setItem('celebrated', 'true');
            }, 500);
        }
    }

    reset() {
        if (confirm('Reset all progress? This cannot be undone.')) {
            localStorage.removeItem(this.storageKey);
            this.data = this.getDefaultData();
            this.updateUI();
        }
    }

    export() {
        const data = {
            progress: this.data,
            exported: new Date().toISOString()
        };
        console.log('Course Progress Export:', data);
        return data;
    }
}

// Initialize global progress tracker
const courseProgress = new CourseProgress();

// Expose to window for debugging
window.courseProgress = courseProgress;
window.resetProgress = () => courseProgress.reset();
window.exportProgress = () => console.log(courseProgress.export());