import { stitchGlossary } from './glossarydata.js';

const searchInput = document.getElementById("search");
const grid = document.getElementById("glossary-grid");

function buildCards() {
  grid.innerHTML = '';
  stitchGlossary.forEach((s) => {
    const card = document.createElement("div");
    card.className = "stitch-card";
    card.setAttribute("data-name", s.name_us.toLowerCase());
    card.setAttribute("data-tags", s.tags ? s.tags.join(' ').toLowerCase() : '');
    card.setAttribute("data-abbr", s.id.toLowerCase());

    const cardInner = document.createElement("div");
    cardInner.className = "card-inner";

    // FRONT - Full name only
    const cardFront = document.createElement("div");
    cardFront.className = "card-front";
    
    const name = document.createElement("div");
    name.className = "name";
    name.textContent = s.name_us;
    
    const nameLength = s.name_us.length;
    if (nameLength < 15) {
      name.classList.add('name-short');
    } else if (nameLength < 25) {
      name.classList.add('name-medium');
    } else if (nameLength < 35) {
      name.classList.add('name-long');
    } else {
      name.classList.add('name-extra-long');
    }
    
    cardFront.appendChild(name);

    // BACK - Abbreviation + Description + "..."
    const cardBack = document.createElement("div");
    cardBack.className = "card-back";
    
    const abbr = document.createElement("div");
    abbr.className = "abbr";
    abbr.textContent = s.id.toUpperCase();
    
    const description = document.createElement("div");
    description.className = "description";
    description.textContent = s.notes || `UK: ${s.name_uk}`;
    
    const clickMore = document.createElement("div");
    clickMore.className = "click-more";
    clickMore.textContent = "...";
    
    cardBack.appendChild(abbr);
    cardBack.appendChild(description);
    cardBack.appendChild(clickMore);

    cardInner.appendChild(cardFront);
    cardInner.appendChild(cardBack);
    card.appendChild(cardInner);

    // Click handler for enhanced modal
    card.onclick = () => {
      const stitchData = stitchGlossary.find(stitch => stitch.id === s.id);
      
      // Add enhanced data if not already present
      if (!stitchData.difficulty) {
        stitchData.difficulty = stitchData.tags.includes('basic') ? 1 : 
                               stitchData.tags.includes('intermediate') ? 3 : 
                               stitchData.tags.includes('advanced') ? 4 : 2;
        
        stitchData.timeToLearn = stitchData.tags.includes('basic') ? '15-30 minutes' :
                                stitchData.tags.includes('intermediate') ? '30-60 minutes' :
                                stitchData.tags.includes('advanced') ? '1-2 hours' : '30 minutes';
      }
      
      // Open the enhanced modal
      if (window.openEnhancedModal) {
        window.openEnhancedModal(stitchData);
      }
    };

    grid.appendChild(card);
  });
}

function initGlossary() {
    buildCards();

    // Search functionality
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase().trim();
        
        Array.from(grid.children).forEach((card) => {
            const cardName = card.getAttribute("data-name");
            const cardTags = card.getAttribute("data-tags");
            const cardAbbr = card.getAttribute("data-abbr");
            
            const matches = query === "" || 
                           cardName.includes(query) || 
                           cardAbbr.includes(query) || 
                           cardTags.includes(query);
            
            // Remove highlight first
            card.classList.remove('search-highlight');
            
            // Show/hide cards
            card.style.display = matches ? "" : "none";
            
            // Add highlight if there's a query and it matches
            if (query !== "" && matches) {
                card.classList.add('search-highlight');
            }
        });
    });

    // ESC key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && window.closeEnhancedModal) {
            window.closeEnhancedModal();
        }
    });
}

// Initialize when DOM is ready
if (document.readyState !== "loading") {
    initGlossary();
} else {
    document.addEventListener("DOMContentLoaded", initGlossary);
}

// Sticky navigation
window.addEventListener('scroll', function() {
    const nav = document.getElementById('nav');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});