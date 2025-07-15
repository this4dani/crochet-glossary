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