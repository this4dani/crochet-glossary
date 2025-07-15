// DANI'S Crochet Glossary - Simple Clean Implementation
console.log('Loading DANI\'s Crochet Glossary...');

class SimpleGlossary {
    constructor() {
        this.terms = [];
        this.filteredTerms = [];
        this.currentFilter = 'all';
        this.searchQuery = '';
        
        // Your API endpoint
        this.apiEndpoint = 'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json';
        
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
            
            const response = await fetch(this.apiEndpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.terms = data.data || data.terms || data || [];
            
            console.log(`Loaded ${this.terms.length} terms`);
            
            this.hideElement('loading-message');
            this.updateStats();
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError();
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
        const tags = term.tags || [];
        const name = (term.name_us || '').toLowerCase();
        
        const categoryMap = {
            'basic': ['basic', 'single', 'double', 'chain', 'slip'],
            'advanced': ['advanced', 'cable', 'bobble', 'cluster'],
            'techniques': ['technique', 'method', 'join', 'seam']
        };
        
        const keywords = categoryMap[this.currentFilter] || [];
        
        return tags.some(tag => keywords.includes(tag.toLowerCase())) ||
               keywords.some(keyword => name.includes(keyword));
    }

    matchesSearch(term) {
        const searchFields = [
            term.name_us || '',
            term.name_uk || '',
            term.abbreviation || '',
            term.description || '',
            term.notes || ''
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
        
        grid.innerHTML = termsToShow.map(term => this.createTermHTML(term)).join('');
    }

    createTermHTML(term) {
        const usName = term.name_us || term.name || 'Unknown';
        const ukName = term.name_uk || usName;
        const abbrev = term.abbreviation || term.symbol || '';
        const description = term.description || term.notes || 'No description available';
        
        return `
            <div class="term-item">
                <div class="term-title">${this.escapeHTML(usName)}</div>
                ${abbrev ? `<div class="term-abbrev">${this.escapeHTML(abbrev)}</div>` : ''}
                <div class="term-desc">${this.escapeHTML(description)}</div>
                <div class="term-translations">
                    <div class="translation-row">
                        <strong>US:</strong> <span>${this.escapeHTML(usName)}</span>
                    </div>
                    <div class="translation-row">
                        <strong>UK:</strong> <span>${this.escapeHTML(ukName)}</span>
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
            countElement.textContent = 'Error';
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
