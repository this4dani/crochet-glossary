// DANI'S Interactive Crochet Glossary - Complete functionality
import { stitchGlossary } from './glossarydata.js';

// Tips Toggle Manager - auto-open on scroll, auto-close timing, manual control
class TipsToggleManager {
    constructor() {
        this.tipsContent = document.getElementById('tips-content');
        this.tipsButton = document.getElementById('tips-toggle');
        this.autoCloseTimer = null;
        this.isManuallyControlled = false;
        this.hasAutoOpened = false;
        
        this.init();
    }
    
    init() {
        if (!this.tipsContent || !this.tipsButton) {
            console.warn('Tips elements not found');
            return;
        }
        
        this.setupScrollListener();
        this.setupClickListeners();
        this.setupOutsideClickListener();
    }
    
    // Auto-opens tips when glossary grid becomes visible
    setupScrollListener() {
        const glossaryGrid = document.getElementById('glossary-grid');
        if (!glossaryGrid) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.hasAutoOpened && !this.isManuallyControlled) {
                    this.autoOpen();
                }
            });
        }, { threshold: 0.3 });
        
        observer.observe(glossaryGrid);
    }
    
    // Auto-opens with 30-second timer
    autoOpen() {
        this.hasAutoOpened = true;
        this.openTips();
        
        this.autoCloseTimer = setTimeout(() => {
            if (!this.isManuallyControlled) {
                this.closeTips();
            }
        }, 30000);
    }
    
    // Manual button control
    setupClickListeners() {
        this.tipsButton.addEventListener('click', (e) => {
            e.stopPropagation();
            this.isManuallyControlled = true;
            this.clearAutoTimer();
            this.toggleTips();
        });
    }
    
    // Auto-close on outside interaction
    setupOutsideClickListener() {
        document.addEventListener('click', (e) => {
            if (!this.tipsButton.contains(e.target) && 
                !this.tipsContent.contains(e.target) && 
                !this.isManuallyControlled) {
                this.closeTips();
            }
        });
        
        let scrollTimer;
        window.addEventListener('scroll', () => {
            if (this.hasAutoOpened && !this.isManuallyControlled) {
                clearTimeout(scrollTimer);
                scrollTimer = setTimeout(() => {
                    this.closeTips();
                }, 500);
            }
        });
    }
    
    openTips() {
        this.tipsContent.classList.add('show');
        this.tipsButton.innerHTML = '💡 Tips & Tricks ▲';
    }
    
    closeTips() {
        this.tipsContent.classList.remove('show');
        this.tipsButton.innerHTML = '💡 Tips & Tricks ▼';
        this.clearAutoTimer();
    }
    
    toggleTips() {
        if (this.tipsContent.classList.contains('show')) {
            this.closeTips();
        } else {
            this.openTips();
        }
    }
    
    clearAutoTimer() {
        if (this.autoCloseTimer) {
            clearTimeout(this.autoCloseTimer);
            this.autoCloseTimer = null;
        }
    }
}

// Glossary Cards Manager - card creation, flip animations, search
class GlossaryCardsManager {
    constructor() {
        this.grid = document.getElementById('glossary-grid');
        this.searchInput = document.getElementById('search');
        
        this.init();
    }
    
    init() {
        if (!this.grid) {
            console.warn('Glossary grid not found');
            return;
        }
        
        this.buildCards();
        this.setupSearch();
    }
    
    /**
     * Creates all glossary cards from data
     */
    buildCards() {
        this.grid.innerHTML = '';
        
        stitchGlossary.forEach((term) => {
            const card = this.createCard(term);
            this.grid.appendChild(card);
        });
    }
    
    /**
     * Creates individual card with flip functionality
     */
    createCard(term) {
        const card = document.createElement('div');
        card.className = 'stitch-card';
        card.setAttribute('data-name', term.name_us.toLowerCase());
        card.setAttribute('data-abbr', (term.id || '').toLowerCase());
        card.setAttribute('data-tags', term.tags ? term.tags.join(' ').toLowerCase() : '');
        
        // Determine back side content
        let backContent = '';
        if (term.id) {
            backContent = term.id.toUpperCase();
        } else if (term.name_uk && term.name_uk !== term.name_us) {
            backContent = `UK: ${term.name_uk}`;
        } else if (term.notes) {
            backContent = term.notes.substring(0, 50) + '...';
        } else {
            backContent = 'See Details';
        }
        
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <div class="name">${term.name_us}</div>
                </div>
                <div class="card-back">
                    <div class="abbr">${term.id ? term.id.toUpperCase() : ''}</div>
                    <div class="description">${term.notes || 'UK: ' + term.name_uk}</div>
                </div>
            </div>
        `;
        
        // Add click handler for popup
        card.addEventListener('click', () => {
            window.popupManager.openPopup(term);
        });
        
        return card;
    }
    
    /**
     * Search functionality with highlighting
     */
    setupSearch() {
        if (!this.searchInput) return;
        
        this.searchInput.addEventListener('input', () => {
            const query = this.searchInput.value.toLowerCase().trim();
            
            Array.from(this.grid.children).forEach((card) => {
                const name = card.getAttribute('data-name');
                const abbr = card.getAttribute('data-abbr');
                const tags = card.getAttribute('data-tags');
                
                const matches = query === '' || 
                               name.includes(query) || 
                               abbr.includes(query) || 
                               tags.includes(query);
                
                card.style.display = matches ? '' : 'none';
                
                if (query !== '' && matches) {
                    card.classList.add('search-highlight');
                } else {
                    card.classList.remove('search-highlight');
                }
            });
        });
    }
}

/**
 * Tabbed Popup Manager
 * Handles modal display, tab switching, and content population
 */
class TabbedPopupManager {
    constructor() {
        this.modal = document.getElementById('enhanced-modal');
        this.currentTerm = null;
        
        this.init();
    }
    
    init() {
        if (!this.modal) {
            console.warn('Enhanced modal not found');
            return;
        }
        
        this.setupEventListeners();
    }
    
    /**
     * Modal event listeners
     */
    setupEventListeners() {
        // Close button
        const closeButton = this.modal.querySelector('.close-button');
        if (closeButton) {
            closeButton.addEventListener('click', () => this.closePopup());
        }
        
        // Click outside to close
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closePopup();
            }
        });
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.closePopup();
            }
        });
        
        // Tab switching
        const tabButtons = this.modal.querySelectorAll('.tab-button');
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tabName = e.target.textContent.toLowerCase().replace(/[^a-z]/g, '');
                this.switchTab(tabName);
            });
        });
    }
    
    /**
     * Opens popup with term data
     */
    openPopup(term) {
        this.currentTerm = term;
        this.populateContent(term);
        this.modal.classList.add('active');
    }
    
    /**
     * Closes popup
     */
    closePopup() {
        this.modal.classList.remove('active');
        this.currentTerm = null;
    }
    
    /**
     * Populates modal content with term data
     */
    populateContent(term) {
        // Header
        const titleElement = document.getElementById('modal-stitch-name');
        const abbrElement = document.getElementById('modal-abbr');
        if (titleElement) titleElement.textContent = term.name_us;
        if (abbrElement) abbrElement.textContent = term.id ? term.id.toUpperCase() : '';
        
        // Overview tab content
        const usNameElement = document.getElementById('modal-us-name');
        const ukNameElement = document.getElementById('modal-uk-name');
        const symbolElement = document.getElementById('modal-symbol');
        const descriptionElement = document.getElementById('modal-description');
        
        if (usNameElement) usNameElement.textContent = term.name_us;
        if (ukNameElement) ukNameElement.textContent = term.name_uk || 'Same as US';
        if (symbolElement) symbolElement.textContent = term.id ? term.id.toUpperCase() : '-';
        if (descriptionElement) {
            descriptionElement.textContent = term.notes || 'Comprehensive information coming soon!';
        }
        
        // Set difficulty stars (placeholder)
        this.setDifficultyStars(term.difficulty || 1);
        
        // Reset to Overview tab
        this.switchTab('overview');
    }
    
    /**
     * Sets difficulty star display
     */
    setDifficultyStars(difficulty) {
        const difficultyContainer = document.getElementById('modal-difficulty');
        if (!difficultyContainer) return;
        
        const stars = difficultyContainer.querySelectorAll('.star');
        stars.forEach((star, index) => {
            if (index < difficulty) {
                star.classList.remove('empty');
            } else {
                star.classList.add('empty');
            }
        });
    }
    
    /**
     * Switches between tabs
     */
    switchTab(tabName) {
        // Hide all panels
        const panels = this.modal.querySelectorAll('.tab-panel');
        panels.forEach(panel => {
            panel.style.display = 'none';
            panel.classList.remove('active');
        });
        
        // Deactivate all buttons
        const buttons = this.modal.querySelectorAll('.tab-button');
        buttons.forEach(btn => {
            btn.classList.remove('active');
            btn.style.color = 'var(--clr-primary-dark)';
        });
        
        // Show selected panel
        const targetPanel = document.getElementById(tabName + '-panel');
        if (targetPanel) {
            targetPanel.style.display = 'block';
            targetPanel.classList.add('active');
        }
        
        // Activate selected button
        const targetButton = Array.from(buttons).find(btn => 
            btn.textContent.toLowerCase().includes(tabName)
        );
        if (targetButton) {
            targetButton.classList.add('active');
            targetButton.style.color = 'var(--clr-fuchsia)';
        }
    }
}

/**
 * Navigation Scroll Behavior
 * Handles sticky navigation state
 */
class NavigationManager {
    constructor() {
        this.nav = document.getElementById('nav');
        this.init();
    }
    
    init() {
        if (!this.nav) return;
        
        let navigationTicking = false;
        
        const updateNavigationState = () => {
            const scrollY = window.scrollY;
            
            if (scrollY > 40) {
                this.nav.classList.add('scrolled');
            } else {
                this.nav.classList.remove('scrolled');
            }
            navigationTicking = false;
        };
        
        const requestNavigationTick = () => {
            if (!navigationTicking) {
                requestAnimationFrame(updateNavigationState);
                navigationTicking = true;
            }
        };
        
        window.addEventListener('scroll', requestNavigationTick, { passive: true });
    }
}

/**
 * Main Glossary Application
 * Initializes all managers
 */
class GlossaryApp {
    constructor() {
        this.init();
    }
    
    init() {
        // Initialize all managers
        window.tipsManager = new TipsToggleManager();
        window.cardsManager = new GlossaryCardsManager();
        window.popupManager = new TabbedPopupManager();
        window.navigationManager = new NavigationManager();
        
        console.log('DANI\'S Glossary initialized successfully');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.glossaryApp = new GlossaryApp();
});

// Global functions for compatibility
window.toggleTips = function() {
    if (window.tipsManager) {
        window.tipsManager.isManuallyControlled = true;
        window.tipsManager.toggleTips();
    }
};

window.closeModal = function() {
    if (window.popupManager) {
        window.popupManager.closePopup();
    }
};

window.switchTab = function(tabName) {
    if (window.popupManager) {
        window.popupManager.switchTab(tabName);
    }
};