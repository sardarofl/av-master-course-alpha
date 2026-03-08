// AV Master Course - Complete Navigation System

// Section definitions
var sections = {
    stage1: {title: "Audio Systems", subtitle: "Stage 1: Point to Point Audio", prev: null, next: "stage2"},
    stage2: {title: "Audio Systems", subtitle: "Stage 2: Amplifier Chain", prev: "stage1", next: "stage3"},
    stage3: {title: "Audio Systems", subtitle: "Stage 3: Basic Mixing", prev: "stage2", next: "stage4"},
    stage4: {title: "Audio Systems", subtitle: "Stage 4: Zone Distribution", prev: "stage3", next: "stage5"},
    stage5: {title: "Audio Systems", subtitle: "Stage 5: Matrix Switching", prev: "stage4", next: "stage6"},
    stage6: {title: "Audio Systems", subtitle: "Stage 6: DSP Processing", prev: "stage5", next: "stage7"},
    stage7: {title: "Audio Systems", subtitle: "Stage 7: Network Audio (Dante)", prev: "stage6", next: "stage8"},
    stage8: {title: "Audio Systems", subtitle: "Stage 8: Hybrid Systems", prev: "stage7", next: "stage9"},
    stage9: {title: "Audio Systems", subtitle: "Stage 9: Large Venue Capstone", prev: "stage8", next: "module1"},
    module1: {title: "Video Systems", subtitle: "Module 1: Signal Basics", prev: "stage9", next: "module2"},
    module2: {title: "Video Systems", subtitle: "Module 2: Extension & Cables", prev: "module1", next: "module3"},
    module3: {title: "Video Systems", subtitle: "Module 3: Distribution & Switching", prev: "module2", next: "module4"},
    module4: {title: "Video Systems", subtitle: "Module 4: True Matrix Switching", prev: "module3", next: "module5"},
    module5: {title: "Video Systems", subtitle: "Module 5: Resolution & Scaling", prev: "module4", next: "module6"},
    module6: {title: "Video Systems", subtitle: "Module 6: Video Wall Basics", prev: "module5", next: "module7"},
    module7: {title: "Video Systems", subtitle: "Module 7: LED Processing Flow", prev: "module6", next: "module8"},
    module8: {title: "Video Systems", subtitle: "Module 8: Video Over IP & Multicast", prev: "module7", next: "module9"},
    module9: {title: "Video Systems", subtitle: "Module 9: Control Systems", prev: "module8", next: "module10"},
    module10: {title: "Video Systems", subtitle: "Module 10: System Design", prev: "module9", next: "led1"},
    led1: {title: "LED Displays", subtitle: "Section 1: Digital Signage Applications", prev: "module10", next: "led2"},
    led2: {title: "LED Displays", subtitle: "Section 2: Hospitality & Venues", prev: "led1", next: "led3"},
    led3: {title: "LED Displays", subtitle: "Section 3: Interactive Displays", prev: "led2", next: "led4"},
    led4: {title: "LED Displays", subtitle: "Section 4: Conference Rooms", prev: "led3", next: "led5"},
    led5: {title: "LED Displays", subtitle: "Section 5: Rental & Staging", prev: "led4", next: "led6"},
    led6: {title: "LED Displays", subtitle: "Section 6: Transparent & Creative LED", prev: "led5", next: "led7"},
    led7: {title: "LED Displays", subtitle: "Section 7: Package Technology Overview", prev: "led6", next: "led8"},
    led8: {title: "LED Displays", subtitle: "Section 8: SMD LED Technology", prev: "led7", next: "led9"},
    led9: {title: "LED Displays", subtitle: "Section 9: DIP LED Technology", prev: "led8", next: "led10"},
    led10: {title: "LED Displays", subtitle: "Section 10: COB LED Technology", prev: "led9", next: "led11"},
    led11: {title: "LED Displays", subtitle: "Section 11: GOB LED Technology", prev: "led10", next: "led12"},
    led12: {title: "LED Displays", subtitle: "Section 12: Pixel Pitch & Viewing Distance", prev: "led11", next: "led13"},
    led13: {title: "LED Displays", subtitle: "Section 13: Application Decision Matrix", prev: "led12", next: "cross1"},
    cross1: {title: "Integration", subtitle: "Audio-Video Integration Strategies", prev: "led13", next: "cross2"},
    cross2: {title: "Integration", subtitle: "Video-LED Integration", prev: "cross1", next: "cross3"},
    cross3: {title: "Integration", subtitle: "Control Systems Overview", prev: "cross2", next: "career"},
    career: {title: "Integration", subtitle: "Career Paths & Next Steps", prev: "cross3", next: null}
};

// Section content
var sectionContent = {
    stage1: "<div class='section-header'><h2>Stage 1: Basic Point to Point Audio</h2><p>Laptop/Microphone Active Speaker</p></div><div class='intro-box'><h3>Welcome to Audio Systems!</h3><p>The simplest audio system possible: a source, a cable, and a speaker. Understanding this foundation is critical for everything that follows.</p></div><h2>Audio Levels</h2><div class='concept-grid'><div class='concept-card'><h3>Mic Level (-60 to -40 dBu)</h3><p>The weakest audio signal from microphones. Needs significant amplification.</p></div><div class='concept-card'><h3>Line Level (+4 dBu pro / -10 dBV consumer)</h3><p>The standard operating level for most audio equipment.</p></div><div class='concept-card'><h3>Balanced vs Unbalanced</h3><p>Balanced (XLR) rejects noise. Unbalanced (TS/RCA) for shorter runs.</p></div></div><h2>Key Takeaways</h2><ul><li>Mic level needs pre-amp; Line level is standard</li><li>Balanced cables for long runs</li><li>Active speakers have built-in amplifiers</li></ul>",
    
    stage2: "<div class='section-header'><h2>Stage 2: Passive Chain with Amplifier</h2><p>Microphone Amplifier Passive Speaker</p></div><div class='intro-box'><h3>Why Do We Need Amplifiers?</h3><p>Passive speakers have no built-in amplification. They need an external amplifier to drive them.</p></div><h2>Key Concepts</h2><div class='concept-grid'><div class='concept-card'><h3>Impedance (Ohms)</h3><p>Common values: 4, 8, 16 ohms. Match amp to speaker impedance.</p></div><div class='concept-card'><h3>Power Ratings</h3><p>RMS = continuous power. Amp should be 1.5-2x speaker RMS.</p></div></div><h2>Key Takeaways</h2><ul><li>Never connect speakers below amps rated minimum load</li><li>Amp should be 1.5-2x speaker RMS for clean headroom</li><li>Series adds ohms; Parallel: 1/(1/a+1/b)</li></ul>",
    
    stage3: "<div class='section-header'><h2>Stage 3: Basic Mixing</h2><p>Multiple Sources Mixer Speaker</p></div><div class='intro-box'><h3>Combining Multiple Sources</h3><p>A mixer combines multiple audio signals with level control and EQ.</p></div><h2>Channel Strip</h2><div class='concept-grid'><div class='concept-card'><h3>Gain/Trim</h3><p>Sets input sensitivity. Boost mic level to line level.</p></div><div class='concept-card'><h3>EQ (HF, MF, LF)</h3><p>Tone shaping for each channel.</p></div><div class='concept-card'><h3>Fader</h3><p>Volume control (0dB unity, -inf to +10dB).</p></div></div><h2>Key Takeaways</h2><ul><li>Channel: Input Gain EQ Aux Fader Bus</li><li>Set each stage for optimal level</li><li>Leave 12-18dB headroom below clipping</li></ul>"
};

var currentSectionId = 'stage1';

function loadSection(sectionId) {
    var section = sections[sectionId];
    if (!section) {
        console.error('Section not found:', sectionId);
        return;
    }

    currentSectionId = sectionId;
    
    // Update active nav link
    var links = document.querySelectorAll('.nav-link');
    for (var i = 0; i < links.length; i++) {
        links[i].classList.remove('active');
    }
    var activeLink = document.querySelector('a[href="#' + sectionId + '"]');
    if (activeLink) activeLink.classList.add('active');

    // Update content
    var contentArea = document.getElementById('contentArea');
    var content = sectionContent[sectionId] || '<h2>' + section.subtitle + '</h2><p>Content coming soon...</p>';
    contentArea.innerHTML = content;

    // Update header
    document.getElementById('sectionTitle').textContent = section.title;
    document.getElementById('sectionSubtitle').textContent = section.subtitle;

    // Update navigation buttons
    updateNavButtons(section);
    updateProgress(sectionId);
    
    // Scroll to top
    document.querySelector('.content').scrollTop = 0;

    // Update URL hash
    window.location.hash = sectionId;
}

function navigateSection(direction) {
    var currentSection = sections[currentSectionId];
    if (!currentSection) return;
    
    var targetSection = null;
    
    if (direction === -1 && currentSection.prev) {
        targetSection = currentSection.prev;
    } else if (direction === 1 && currentSection.next) {
        targetSection = currentSection.next;
    }
    
    if (targetSection) {
        loadSection(targetSection);
    }
}

function updateNavButtons(section) {
    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    
    if (section.prev) {
        prevBtn.style.opacity = '1';
        prevBtn.style.cursor = 'pointer';
    } else {
        prevBtn.style.opacity = '0.3';
        prevBtn.style.cursor = 'not-allowed';
    }
    
    if (section.next) {
        nextBtn.style.opacity = '1';
        nextBtn.style.cursor = 'pointer';
    } else {
        nextBtn.style.opacity = '0.3';
        nextBtn.style.cursor = 'not-allowed';
    }
    
    var allSections = Object.keys(sections);
    var currentIndex = allSections.indexOf(currentSectionId);
    document.getElementById('sectionIndicator').textContent = 'Section ' + (currentIndex + 1) + ' of ' + allSections.length;
}

function updateProgress(sectionId) {
    var allSections = Object.keys(sections);
    var currentIndex = allSections.indexOf(sectionId);
    var progress = ((currentIndex + 1) / allSections.length) * 100;

    var masterProgress = document.getElementById('masterProgress');
    var progressText = document.getElementById('progressText');
    
    if (masterProgress) masterProgress.style.width = progress + '%';
    if (progressText) progressText.textContent = (currentIndex + 1) + ' of ' + allSections.length + ' sections completed';
}

function toggleCategory(categoryName) {
    var categoryList = document.getElementById('cat-' + categoryName);
    var toggleIcon = event.target.closest('.category-title').querySelector('.toggle');
    
    if (categoryList.style.display === 'none') {
        categoryList.style.display = 'block';
        toggleIcon.textContent = '▼';
    } else {
        categoryList.style.display = 'none';
        toggleIcon.textContent = '▶';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    var initialSection = window.location.hash.substring(1);
    if (!initialSection || !sections[initialSection]) {
        initialSection = 'stage1';
    }
    loadSection(initialSection);
});
