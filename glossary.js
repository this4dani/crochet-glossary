import { stitchGlossary } from './glossarydata.js';

const searchInput = document.getElementById("search");
const grid = document.getElementById("glossary-grid");
const popup = document.getElementById("popup");
const popupTitle = document.getElementById("popup-title");
const popupDesc = document.getElementById("popup-description");
const popupUK = document.getElementById("popup-uk");
const popupTags = document.getElementById("popup-tags");

function buildCards() {
  grid.innerHTML = '';
  stitchGlossary.forEach((s) => {
    const card = document.createElement("div");
    card.className = "stitch-card";
    card.setAttribute("data-name", s.name_us);
    card.setAttribute("data-tags", s.tags ? s.tags.join(' ') : '');

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

    card.onclick = () => {
      popupTitle.textContent = s.name_us;
      popupUK.textContent = `UK: ${s.name_uk}`;
      popupDesc.textContent = s.notes || "No description available.";
      
      popupTags.innerHTML = '';
      if (s.tags && s.tags.length > 0) {
        s.tags.forEach(tag => {
          const tagEl = document.createElement('span');
          tagEl.className = 'tag';
          tagEl.textContent = tag;
          popupTags.appendChild(tagEl);
        });
      }
      
      popup.classList.add("active");
    };

    grid.appendChild(card);
  });
}

function initGlossary() {
    buildCards();

    // Search with enhanced highlighting
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase().trim();
        
        // Remove all existing highlights and search-matched class
        document.querySelectorAll('.stitch-card').forEach(card => {
            card.classList.remove('search-matched');
            const existingFrame = card.querySelector('.search-highlight-frame');
            if (existingFrame) {
                existingFrame.remove();
            }
        });
        
        if (query === "") return;
        
        Array.from(grid.children).forEach((card) => {
            const name = card.getAttribute("data-name");
            const tags = card.getAttribute("data-tags");
            const abbr = card.getAttribute("data-abbr");
            
            const matches = name.includes(query) || 
                           abbr.includes(query) || 
                           tags.includes(query);
            
            if (matches) {
                // Add search-matched class for enhanced hover
                card.classList.add('search-matched');
                
                // Create bold highlight frame
                const frame = document.createElement('div');
                frame.className = 'search-highlight-frame';
                card.appendChild(frame);
            }
        });
    });

    // Popup close handlers
    document.querySelector(".popup-close").onclick = () => closePopup();
    popup.onclick = (e) => {
        if (e.target === popup) closePopup();
    };

    // ESC key to close popup
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closePopup();
        }
    });
}

// Global functions
window.toggleTips = function() {
    const tipsContent = document.getElementById('tips-content');
    const toggle = document.querySelector('.tips-toggle');
    
    if (tipsContent.classList.contains('show')) {
        tipsContent.classList.remove('show');
        toggle.innerHTML = 'Tips & Tricks ▼';
    } else {
        tipsContent.classList.add('show');
        toggle.innerHTML = 'Tips & Tricks ▲';
    }
};

window.closePopup = function() {
    popup.classList.remove("active");
};

// Close tips when clicking outside
document.addEventListener('click', function(e) {
    const tipsToggle = document.querySelector('.tips-toggle');
    const tipsContent = document.getElementById('tips-content');
    if (tipsToggle && !tipsToggle.contains(e.target)) {
        tipsContent.classList.remove('show');
        tipsToggle.innerHTML = 'Tips & Tricks ▼';
    }
});

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