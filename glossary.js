// DANI'S Crochet Glossary - Enhanced with Rich Cards
console.log('Loading DANI\'s Crochet Glossary...');

class SimpleGlossary {
    constructor() {
        this.terms = [];
        this.filteredTerms = [];
        this.currentFilter = 'all';
        this.searchQuery = '';
        
        // Try multiple API endpoints in case one fails
        this.apiEndpoints = [
            'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json',
            'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json',
            'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/data/glossary.json'
        ];
        
        this.currentEndpointIndex = 0;
        this.init();
    }

    async init() {
        this.setupEvents();
        await this.loadData();
        this.render();
    }

    setupEvents() {
        // Search
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value.toLowerCase();
                this.filterAndRender();
            });
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.filterAndRender();
            });
        });

        // Tips toggle
        const tipsToggle = document.getElementById('tips-toggle');
        const tipsContent = document.getElementById('tips-content');
        const tipsArrow = document.getElementById('tips-arrow');
        
        if (tipsToggle) {
            tipsToggle.addEventListener('click', () => {
                const isHidden = tipsContent.classList.contains('hidden');
                
                if (isHidden) {
                    tipsContent.classList.remove('hidden');
                    tipsArrow.textContent = '▲';
                } else {
                    tipsContent.classList.add('hidden');
                    tipsArrow.textContent = '▼';
                }
            });
        }
    }

    async loadData() {
        try {
            console.log('Loading from API...');
            
            const response = await fetch(this.apiEndpoints[this.currentEndpointIndex]);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            // Handle different data structures
            if (data.data && Array.isArray(data.data)) {
                this.terms = data.data;
            } else if (data.terms && Array.isArray(data.terms)) {
                this.terms = data.terms;
            } else if (Array.isArray(data)) {
                this.terms = data;
            } else {
                throw new Error('Invalid data structure');
            }
            
            console.log(`Loaded ${this.terms.length} terms`);
            
            this.hideElement('loading-message');
            this.updateStats();
            
        } catch (error) {
            console.error('Error loading data:', error);
            
            // Try next endpoint if available
            if (this.currentEndpointIndex < this.apiEndpoints.length - 1) {
                this.currentEndpointIndex++;
                console.log(`Trying alternate endpoint: ${this.apiEndpoints[this.currentEndpointIndex]}`);
                await this.loadData();
            } else {
                this.showError();
            }
        }
    }

    filterAndRender() {
        let filtered = [...this.terms];
        
        // Apply category filter
        if (this.currentFilter !== 'all') {
            filtered = filtered.filter(term => this.matchesCategory(term));
        }
        
        // Apply search filter
        if (this.searchQuery) {
            filtered = filtered.filter(term => this.matchesSearch(term));
        }
        
        this.filteredTerms = filtered;
        this.render();
        this.updateStats();
    }

    matchesCategory(term) {
        const difficulty = parseInt(term.difficulty || term.Difficulty || 1);
        const name = (term.name_us || term.Name_US || '').toLowerCase();
        const tags = term.tags || term.Tags || [];
        
        if (this.currentFilter === 'basic') {
            return difficulty <= 2 || name.includes('basic') || name.includes('single') || 
                   name.includes('chain') || name.includes('slip');
        } else if (this.currentFilter === 'advanced') {
            return difficulty >= 4 || name.includes('advanced') || name.includes('cable') || 
                   name.includes('cluster');
        } else if (this.currentFilter === 'techniques') {
            return tags.includes('technique') || name.includes('join') || name.includes('seam') ||
                   name.includes('technique') || name.includes('method');
        }
        
        return true;
    }

    matchesSearch(term) {
        const searchFields = [
            term.name_us || term.Name_US || '',
            term.name_uk || term.Name_UK || '',
            term.abbreviation || term.Abbreviation || '',
            term.id || term.ID || '',
            term.description || term.Description || '',
            term.notes || term.Notes || ''
        ];
        
        return searchFields.some(field => 
            field.toLowerCase().includes(this.searchQuery)
        );
    }

    render() {
        const grid = document.getElementById('terms-grid');
        if (!grid) return;
        
        const termsToShow = this.filteredTerms.length > 0 ? this.filteredTerms : this.terms;
        
        if (termsToShow.length === 0) {
            grid.style.display = 'none';
            this.showElement('no-results');
            return;
        }
        
        this.hideElement('no-results');
        grid.style.display = 'grid';
        
        grid.innerHTML = termsToShow.map(term => this.createCardHTML(term)).join('');
    }

    createCardHTML(term) {
        // Extract data with multiple fallbacks
        const usName = term.name_us || term.Name_US || term.name || 'Unknown Stitch';
        const ukName = term.name_uk || term.Name_UK || usName;
        const abbrev = term.id || term.ID || term.abbreviation || term.Abbreviation || '';
        const symbol = term.symbol || term.Symbol || '•';
        const description = term.description || term.Description || term.notes || 'No description available';
        const difficulty = parseInt(term.difficulty || term.Difficulty || 1);
        
        // Generate stars
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            stars += `<span class="star ${i <= difficulty ? '' : 'empty'}">★</span>`;
        }
        
        return `
            <div class="glossary-card">
                <div class="card-header">
                    <div>
                        <div class="stitch-name">${this.escapeHTML(usName)}</div>
                        ${abbrev ? `<div class="stitch-abbr">${this.escapeHTML(abbrev.toUpperCase())}</div>` : ''}
                    </div>
                    <div class="stitch-symbol">${this.escapeHTML(symbol)}</div>
                </div>
                <div class="card-details">
                    <div class="card-description">${this.escapeHTML(description)}</div>
                    <div class="us-uk-terms">
                        <span><strong>US:</strong> ${this.escapeHTML(usName)}</span>
                        ${usName !== ukName ? `<span><strong>UK:</strong> ${this.escapeHTML(ukName)}</span>` : ''}
                    </div>
                    <div class="difficulty-stars">
                        ${stars}
                    </div>
                </div>
            </div>
        `;
    }

    updateStats() {
        const countElement = document.getElementById('term-count');
        if (countElement) {
            const displayCount = this.filteredTerms.length > 0 ? this.filteredTerms.length : this.terms.length;
            const totalCount = this.terms.length;
            
            if (this.searchQuery || this.currentFilter !== 'all') {
                countElement.textContent = `${displayCount} of ${totalCount}`;
            } else {
                countElement.textContent = totalCount;
            }
        }
    }

    showError() {
        this.hideElement('loading-message');
        this.hideElement('terms-grid');
        this.showElement('error-message');
        
        const countElement = document.getElementById('term-count');
        if (countElement) {
            countElement.textContent = '0';
        }
    }

    showElement(id) {
        const element = document.getElementById(id);
        if (element) element.style.display = 'block';
    }

    hideElement(id) {
        const element = document.getElementById(id);
        if (element) element.style.display = 'none';
    }

    escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new SimpleGlossary());
} else {
    new SimpleGlossary();
}

// REPLACE the previous pagination code with this FIXED version

function setupPagination() {
    console.log('Setting up pagination...');
    
    const cardsPerPage = 9; // 3x3 grid
    let currentPage = 0;
    
    // Wait a bit to ensure cards are rendered
    setTimeout(() => {
        // Get all cards
        const allCards = document.querySelectorAll('.glossary-card');
        console.log(`Found ${allCards.length} cards`);
        
        if (allCards.length === 0) {
            console.error('No cards found!');
            return;
        }
        
        const totalPages = Math.ceil(allCards.length / cardsPerPage);
        
        // Create navigation controls
        const termsContainer = document.querySelector('.terms-container');
        
        // Remove any existing navigation
        const existingNav = document.getElementById('pagination-nav');
        if (existingNav) {
            existingNav.remove();
        }
        
        // Add navigation buttons
        const navDiv = document.createElement('div');
        navDiv.id = 'pagination-nav';
        navDiv.style.cssText = 'text-align: center; margin-top: 20px;';
        navDiv.innerHTML = `
            <button id="prevPage" style="
                background: var(--clr-coral);
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 0 10px;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            ">← Previous</button>
            
            <span id="pageInfo" style="
                color: var(--clr-coral);
                margin: 0 20px;
                font-weight: 600;
            ">Page 1 of ${totalPages}</span>
            
            <button id="nextPage" style="
                background: var(--clr-coral);
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 0 10px;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            ">Next →</button>
        `;
        
        // Insert after the terms container
        termsContainer.parentNode.insertBefore(navDiv, termsContainer.nextSibling);
        
        // Function to show specific page
        function showPage(page) {
            console.log(`Showing page ${page + 1}`);
            
            // First hide ALL cards
            allCards.forEach((card) => {
                card.style.display = 'none';
                card.style.visibility = 'hidden';
                card.style.position = 'absolute';
                card.style.left = '-9999px';
            });
            
            // Then show only the cards for this page
            const startIndex = page * cardsPerPage;
            const endIndex = Math.min(startIndex + cardsPerPage, allCards.length);
            
            console.log(`Showing cards ${startIndex} to ${endIndex - 1}`);
            
            for (let i = startIndex; i < endIndex; i++) {
                if (allCards[i]) {
                    allCards[i].style.display = 'flex';
                    allCards[i].style.visibility = 'visible';
                    allCards[i].style.position = 'relative';
                    allCards[i].style.left = '0';
                }
            }
            
            // Update page info
            document.getElementById('pageInfo').textContent = `Page ${page + 1} of ${totalPages}`;
            
            // Update button states
            const prevBtn = document.getElementById('prevPage');
            const nextBtn = document.getElementById('nextPage');
            
            prevBtn.disabled = page === 0;
            nextBtn.disabled = page === totalPages - 1;
            
            // Style disabled buttons
            if (page === 0) {
                prevBtn.style.opacity = '0.5';
                prevBtn.style.cursor = 'default';
            } else {
                prevBtn.style.opacity = '1';
                prevBtn.style.cursor = 'pointer';
            }
            
            if (page === totalPages - 1) {
                nextBtn.style.opacity = '0.5';
                nextBtn.style.cursor = 'default';
            } else {
                nextBtn.style.opacity = '1';
                nextBtn.style.cursor = 'pointer';
            }
            
            // Update current page
            currentPage = page;
        }
        
        // Add click handlers
        document.getElementById('prevPage').onclick = () => {
            if (currentPage > 0) {
                showPage(currentPage - 1);
            }
        };
        
        document.getElementById('nextPage').onclick = () => {
            if (currentPage < totalPages - 1) {
                showPage(currentPage + 1);
            }
        };
        
        // Show first page
        showPage(0);
        
    }, 500); // Small delay to ensure cards are loaded
}

// Call this after glossary loads
// Try multiple times to ensure it works
setTimeout(() => setupPagination(), 1000);
setTimeout(() => setupPagination(), 2000);
setTimeout(() => setupPagination(), 3000);