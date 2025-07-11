cat > glossary.js << 'EOF'
// DANI'S Interactive Crochet Glossary - Fixed Version
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
    
    stitchGlossary.forEach(function(stitch) {
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

        card.onclick = function() {
            console.log("Card clicked:", stitch.name_us);
            openModal(stitch);
        };
        
        grid.appendChild(card);
    });
}

function openModal(stitch) {
    const modal = document.getElementById("enhanced-modal");
    if (!modal) {
        console.log("Modal not found!");
        return;
    }
    
    const modalName = document.getElementById("modal-stitch-name");
    const modalAbbr = document.getElementById("modal-abbr");
    const modalUsName = document.getElementById("modal-us-name");
    const modalUkName = document.getElementById("modal-uk-name");
    const modalDesc = document.getElementById("modal-description");
    
    if (modalName) modalName.textContent = stitch.name_us;
    if (modalAbbr) modalAbbr.textContent = stitch.id.toUpperCase();
    if (modalUsName) modalUsName.textContent = stitch.name_us;
    if (modalUkName) modalUkName.textContent = stitch.name_uk;
    if (modalDesc) modalDesc.textContent = stitch.notes || "No description available.";
    
    console.log("Opening modal for:", stitch.name_us);
    modal.classList.add("active");
}

function closeModal() {
    const modal = document.getElementById("enhanced-modal");
    if (modal) {
        console.log("Closing modal");
        modal.classList.remove("active");
    }
}

function initGlossary() {
    console.log("🔧 Starting initGlossary...");
    buildCards();
    
    // Search functionality
    const searchInput = document.getElementById("search");
    if (searchInput) {
        searchInput.addEventListener("input", function() {
            const query = searchInput.value.toLowerCase().trim();
            const grid = document.getElementById("glossary-grid");
            if (!grid) return;
            
            Array.from(grid.children).forEach(function(card) {
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
        console.log("✅ Search initialized");
    }
    
    // Tips toggle - using working syntax
    const tipsToggle = document.getElementById("tips-toggle");
    if (tipsToggle) {
        tipsToggle.onclick = function() {
            console.log("🎯 Tips clicked!");
            const tipsContent = document.getElementById('tips-content');
            if (tipsContent) {
                tipsContent.classList.toggle('show');
                console.log("Tips toggled, show class:", tipsContent.classList.contains('show'));
            }
        };
        console.log("✅ Tips toggle initialized");
    }
    
    // ESC key handler
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
    
    console.log("✅ initGlossary completed!");
}

// Make functions globally available
window.closeModal = closeModal;

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadGlossaryData);
EOF