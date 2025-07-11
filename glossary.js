// DANI'S Interactive Crochet Glossary - HTML-Matched Version
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

        // Match your HTML structure exactly
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

        card.onclick = () => openModal(stitch);
        grid.appendChild(card);
    });
}

function openModal(stitch) {
    // Use your actual modal ID: enhanced-modal
    const modal = document.getElementById("enhanced-modal");
    const modalName = document.getElementById("modal-stitch-name");
    const modalAbbr = document.getElementById("modal-abbr");
    const modalUsName = document.getElementById("modal-us-name");
    const modalUkName = document.getElementById("modal-uk-name");
    const modalDesc = document.getElementById("modal-description");
    
    if (!modal) return;
    
    if (modalName) modalName.textContent = stitch.name_us;
    if (modalAbbr) modalAbbr.textContent = stitch.id.toUpperCase();
    if (modalUsName) modalUsName.textContent = stitch.name_us;
    if (modalUkName) modalUkName.textContent = stitch.name_uk;
    if (modalDesc) modalDesc.textContent = stitch.notes || "No description available.";
    
    modal.classList.add("active");
}

function closeModal() {
    const modal = document.getElementById("enhanced-modal");
    if (modal) modal.classList.remove("active");
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
    
    // Tips toggle - using your actual HTML
    const tipsToggle = document.getElementById("tips-toggle");
    if (tipsToggle) {
        tipsToggle.onclick = () => {
            const tipsContent = document.getElementById('tips-content');
            if (tipsContent) {
                tipsContent.classList.toggle('show');
            }
        };
    }
    
    // Modal close handlers - using your actual close function in HTML
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
}

// Make functions globally available
window.closeModal = closeModal;

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadGlossaryData);
