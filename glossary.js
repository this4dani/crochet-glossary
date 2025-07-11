// DANI'S Interactive Crochet Glossary - Professional glossary interface
console.log("🔧 Glossary script loading...");

let stitchGlossary = [];

// Load glossary data from API
async function loadGlossaryData() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json');
        const data = await response.json();
        stitchGlossary = data.data;
        console.log(`✅ Loaded ${stitchGlossary.length} terms from API`);
        
        initializeGlossary();
    } catch (error) {
        console.error('❌ Error loading glossary:', error);
        showErrorMessage();
    }
}

// Display error message if API fails
function showErrorMessage() {
    const grid = document.getElementById("glossary-grid");
    if (grid) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: #666;">
                <p>Unable to load glossary data. Please try refreshing the page.</p>
            </div>
        `;
    }
}

// Tips Toggle Manager - handles auto-open behavior and manual toggle controls
class TipsToggleManager {
    constructor() {
        this.tipsContent = document.getElementById('tips-content');
        this.tipsButton = document.querySelector('.tips-toggle');
        this.autoOpenTriggered = false;
        this.manuallyToggled = false;
        this.autoCloseTimer = null;
        
        this.initEventListeners();
        this.setupScrollTrigger();
    }

    initEventListeners() {
        if (this.tipsButton) {
            this.tipsButton.addEventListener('click', () => this.handleManualToggle());
        }
    }

    setupScrollTrigger() {
        window.addEventListener('scroll', () => this.handleScrollTrigger());
    }

    handleScrollTrigger() {
        if (this.manuallyToggled || this.autoOpenTriggered) return;

        const glossarySection = document.getElementById('glossary-grid');
        if (!glossarySection) return;

        const rect = glossarySection.getBoundingClientRect();
        const isVisible = rect.top <= window.innerHeight * 0.8;

        if (isVisible) {
            this.autoOpen();
        }
    }

    autoOpen() {
        if (!this.tipsContent) return;
        
        this.tipsContent.classList.add('show');
        this.autoOpenTriggered = true;
        
        this.autoCloseTimer = setTimeout(() => {
            if (!this.manuallyToggled) {
                this.tipsContent.classList.remove('show');
            }
        }, 30000);
    }

    handleManualToggle() {
        if (!this.tipsContent) return;
        
        this.manuallyToggled = true;
        
        if (this.autoCloseTimer) {
            clearTimeout(this.autoCloseTimer);
            this.autoCloseTimer = null;
        }
        
        this.tipsContent.classList.toggle('show');
    }
}

// Build and display glossary cards
function buildCards() {
    const grid = document.getElementById("glossary-grid");
    if (!grid) return;

    grid.innerHTML = '';

    stitchGlossary.forEach((stitch) => {
        const card = document.createElement("div");
        card.className = "stitch-card";
        card.setAttribute("data-name", stitch.name_us.toLowerCase());
        card.setAttribute("data-abbr", stitch.id.toLowerCase());
        card.setAttribute("data-tags", stitch.tags ? stitch.tags.join(' ').toLowerCase() : '');

        card.innerHTML = `
            <div class="card-front">
                <div class="name">${stitch.name_us}</div>
            </div>
            <div class="card-back">
                <div class="abbr">${stitch.id}</div>
            </div>
        `;

        card.addEventListener('click', () => openStitchModal(stitch));
        grid.appendChild(card);
    });
}

// Open detailed modal for a stitch
function openStitchModal(stitch) {
    const modal = document.getElementById("popup");
    const title = document.getElementById("popup-title");
    const ukName = document.getElementById("popup-uk");
    const description = document.getElementById("popup-description");
    const tags = document.getElementById("popup-tags");

    if (!modal) return;

    if (title) title.textContent = stitch.name_us;
    if (ukName) ukName.textContent = `UK: ${stitch.name_uk || stitch.name_us}`;
    if (description) description.textContent = stitch.description || stitch.notes || "No description available.";
    if (tags && stitch.tags) {
        tags.innerHTML = stitch.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
    }

    modal.style.display = "block";
    document.body.style.overflow = "hidden";
}

// Close modal
function closePopup() {
    const modal = document.getElementById("popup");
    if (modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById("search");
    const grid = document.getElementById("glossary-grid");
    
    if (!searchInput || !grid) return;

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        
        Array.from(grid.children).forEach((card) => {
            const name = card.getAttribute("data-name") || '';
            const abbr = card.getAttribute("data-abbr") || '';
            const tags = card.getAttribute("data-tags") || '';
            
            const matches = query === "" || 
                           name.includes(query) || 
                           abbr.includes(query) || 
                           tags.includes(query);
            
            card.classList.remove('search-highlight');
            card.style.display = matches ? "" : "none";
            
            if (query !== "" && matches) {
                card.classList.add('search-highlight');
            }
        });
    });
}

// Sticky navigation handler
function initializeNavigation() {
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('nav');
        if (nav) {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        }
    });
}

// Modal event handlers
function initializeModalHandlers() {
    // Close modal on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closePopup();
        }
    });

    // Close modal on background click
    const modal = document.getElementById("popup");
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closePopup();
            }
        });
    }

    // Close button
    const closeBtn = document.querySelector(".popup-close");
    if (closeBtn) {
        closeBtn.addEventListener('click', closePopup);
    }
}

// Initialize all glossary functionality
function initializeGlossary() {
    buildCards();
    initializeSearch();
    initializeNavigation();
    initializeModalHandlers();
    
    // Initialize tips manager
    if (document.getElementById('tips-content')) {
        new TipsToggleManager();
    }
    
    console.log("✅ DANI's Glossary initialized successfully");
}

// Make closePopup globally available for HTML onclick handlers
window.closePopup = closePopup;

// Load data when DOM is ready
document.addEventListener('DOMContentLoaded', loadGlossaryData);