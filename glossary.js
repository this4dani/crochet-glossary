// DANI'S Interactive Crochet Glossary - Safe API Version
let stitchGlossary = [];

async function loadGlossaryData() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json');
        const data = await response.json();
        stitchGlossary = data.data;
        console.log(`✅ Loaded ${stitchGlossary.length} terms from API`);
        initGlossary();
    } catch (error) {
        console.error('❌ Error loading glossary:', error);
        const grid = document.getElementById('glossary-grid');
        if (grid) {
            grid.innerHTML = '<p>Unable to load glossary data. Please refresh the page.</p>';
        }
    }
}

function buildCards() {
    const grid = document.getElementById("glossary-grid");
    if (!grid) return;
    
    grid.innerHTML = "";
    
    stitchGlossary.forEach((stitch) => {
        const card = document.createElement("div");
        card.className = "stitch-card";
        card.setAttribute("data-name", stitch.name_us.toLowerCase());
        card.setAttribute("data-abbr", stitch.id.toLowerCase());
        card.setAttribute("data-tags", stitch.tags ? stitch.tags.join(' ') : '');

        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <div class="name">${stitch.name_us}</div>
                </div>
                <div class="card-back">
                    <div class="abbr">${stitch.id.toUpperCase()}</div>
                    <div class="description">${stitch.notes || ''}</div>
                </div>
            </div>
        `;

        card.onclick = () => openPopup(stitch);
        grid.appendChild(card);
    });
}

function openPopup(stitch) {
    const popup = document.getElementById("popup");
    const popupTitle = document.getElementById("popup-title");
    const popupUK = document.getElementById("popup-uk");
    const popupDesc = document.getElementById("popup-desc");
    const popupTags = document.getElementById("popup-tags");
    
    if (!popup) return;
    
    if (popupTitle) popupTitle.textContent = stitch.name_us;
    if (popupUK) popupUK.textContent = `UK: ${stitch.name_uk}`;
    if (popupDesc) popupDesc.textContent = stitch.notes || "No description available.";
    
    if (popupTags) {
        popupTags.innerHTML = '';
        if (stitch.tags && stitch.tags.length > 0) {
            stitch.tags.forEach(tag => {
                const tagEl = document.createElement('span');
                tagEl.className = 'tag';
                tagEl.textContent = tag;
                popupTags.appendChild(tagEl);
            });
        }
    }
    
    popup.classList.add("active");
}

function closePopup() {
    const popup = document.getElementById("popup");
    if (popup) popup.classList.remove("active");
}

function initGlossary() {
    buildCards();
    
    // Search functionality
    const searchInput = document.getElementById("search");
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase().trim();
            const grid = document.getElementById("glossary-grid");
            if (!grid) return;
            
            Array.from(grid.children).forEach((card) => {
                const name = card.getAttribute("data-name") || "";
                const tags = card.getAttribute("data-tags") || "";
                const abbr = card.getAttribute("data-abbr") || "";
                
                const matches = name.includes(query) || 
                               abbr.includes(query) || 
                               tags.includes(query);
                
                card.classList.remove("search-highlight");
                if (query !== "" && matches) {
                    card.classList.add("search-highlight");
                }
            });
        });
    }
    
    // Tips toggle
    const tipsToggle = document.getElementById("tips-toggle");
    if (tipsToggle) {
        tipsToggle.onclick = () => {
            const tipsContent = document.getElementById('tips-content');
            if (tipsContent) {
                tipsContent.classList.toggle('show');
            }
        };
    }
    
    // Popup close handlers
    const popupClose = document.querySelector(".popup-close");
    const popup = document.getElementById("popup");
    
    if (popupClose) {
        popupClose.onclick = closePopup;
    }
    
    if (popup) {
        popup.onclick = (e) => {
            if (e.target === popup) closePopup();
        };
    }
    
    // ESC key handler
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closePopup();
    });
}

// Make functions globally available
window.closePopup = closePopup;

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadGlossaryData);
