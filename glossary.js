// Remove the old import and load from JSON instead
let stitchGlossary = [];

// Load glossary data from JSON
async function loadGlossaryData() {
    try {
        const response = await fetch('data/glossary/crochet-terms-merged.json');
        const data = await response.json();
        
        // Transform the new format to match the old format
        stitchGlossary = data.terms.map(term => ({
            id: term.id.toLowerCase(),
            name_us: term.names.en_us.full || term.id,
            name_uk: term.names.en_uk.full || term.id,
            symbol: term.symbol.chart || '',
            tags: term.tags || [],
            notes: term.descriptions?.brief || '',
            translations: term.translations || {}
        }));
        
        // Initialize the glossary after data is loaded
        initGlossary();
    } catch (error) {
        console.error('Error loading glossary data:', error);
    }
}

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
        card.setAttribute("data-name", s.name_us.toLowerCase());
        card.setAttribute("data-tags", s.tags ? s.tags.join(' ').toLowerCase() : '');
        card.setAttribute("data-abbr", s.id.toLowerCase());

        const cardInner = document.createElement("div");
        cardInner.className = "card-inner";

        // Card Front
        const cardFront = document.createElement("div");
        cardFront.className = "card-front";
        
        const abbr = document.createElement("div");
        abbr.className = "abbr";
        abbr.textContent = s.id.toUpperCase();
        
        const full = document.createElement("div");
        full.className = "name";
        full.textContent = s.name_us;
        
        cardFront.append(abbr, full);

        // Card Back
        const cardBack = document.createElement("div");
        cardBack.className = "card-back";
        
        const backText = document.createElement("div");
        backText.className = "back-text";
        backText.innerHTML = `
            <div class="uk-name">${s.name_uk}</div>
            ${s.translations.ru ? `<div class="translation">RU: ${s.translations.ru.term}</div>` : ''}
        `;
        
        cardBack.appendChild(backText);

        cardInner.append(cardFront, cardBack);
        card.appendChild(cardInner);

        card.onclick = () => {
            popupTitle.textContent = s.name_us;
            popupUK.textContent = `UK: ${s.name_uk}`;
            popupDesc.textContent = s.notes || "No description available.";
            
            // Show translations if available
            let translationHtml = '';
            if (s.translations) {
                for (const [lang, trans] of Object.entries(s.translations)) {
                    translationHtml += `<div>${lang.toUpperCase()}: ${trans.term}</div>`;
                }
            }
            if (translationHtml) {
                popupDesc.innerHTML += `<div class="translations-section"><h4>Translations:</h4>${translationHtml}</div>`;
            }
            
            // Render tags
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

    // Enhanced search
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase();
        Array.from(grid.children).forEach((c) => {
            const name = c.getAttribute("data-name");
            const tags = c.getAttribute("data-tags");
            const abbr = c.getAttribute("data-abbr");
            
            const matches = name.includes(query) || 
                           abbr.includes(query) || 
                           tags.includes(query);
            
            c.style.display = matches ? "" : "none";
            
            // Add highlight effect to matching cards
            if (matches && query.length > 0) {
                c.classList.add("search-highlight");
            } else {
                c.classList.remove("search-highlight");
            }
        });
    });

    // Tips toggle
    const tipsToggle = document.getElementById("tips-toggle");
    if (tipsToggle) {
        tipsToggle.addEventListener("click", () => {
            const content = document.getElementById("tips-content");
            if (content.style.display === "none") {
                content.style.display = "block";
                tipsToggle.textContent = "💡 Hide Tips & Tricks";
            } else {
                content.style.display = "none";
                tipsToggle.textContent = "💡 Show Tips & Tricks";
            }
        });
    }

    // Popup close
    const popupClose = document.querySelector(".popup-close");
    if (popupClose) {
        popupClose.addEventListener("click", closePopup);
    }
    
    popup.addEventListener("click", (e) => {
        if (e.target === popup) closePopup();
    });

    window.closePopup = () => {
        popup.classList.remove("active");
    };
}

// Start loading data when page loads
document.addEventListener('DOMContentLoaded', loadGlossaryData);