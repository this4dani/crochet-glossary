// DANI'S Interactive Crochet Glossary - API Version
let stitchGlossary = [];

// Load data from API
async function loadGlossaryData() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/terms.json');
        const data = await response.json();
        stitchGlossary = data.data; // Extract the data array
        console.log(`✅ Loaded ${stitchGlossary.length} terms from API`);
        initGlossary(); // Initialize after data loads
    } catch (error) {
        console.error('❌ Error loading glossary:', error);
        document.getElementById('glossary-grid').innerHTML = '<p>Unable to load glossary data. Please refresh the page.</p>';
    }
}

// Your existing working functions (keep exactly as they are)
const grid = document.getElementById("glossary-grid");
const searchInput = document.getElementById("search");
const popup = document.getElementById("popup");
const popupClose = document.querySelector(".popup-close");
const popupTitle = document.getElementById("popup-title");
const popupUK = document.getElementById("popup-uk");
const popupDesc = document.getElementById("popup-desc");
const popupTags = document.getElementById("popup-tags");

function buildCards() {
  grid.innerHTML = "";
  
  stitchGlossary.forEach((s) => {
    const card = document.createElement("div");
    card.className = "stitch-card";
    card.setAttribute("data-name", s.name_us.toLowerCase());
    card.setAttribute("data-abbr", s.id.toLowerCase());
    card.setAttribute("data-tags", s.tags ? s.tags.join(' ') : '');

    const abbr = document.createElement("div");
    abbr.className = "abbr";
    abbr.textContent = s.id.toUpperCase();

    const full = document.createElement("div");
    full.className = "name";
    full.textContent = s.name_us;

    card.append(abbr, full);

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

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase().trim();
    
    Array.from(grid.children).forEach((card) => {
      const name = card.getAttribute("data-name").toLowerCase();
      const tags = card.getAttribute("data-tags").toLowerCase();
      const abbr = card.querySelector(".abbr").textContent.toLowerCase();
      
      const matches = name.includes(query) || 
                     abbr.includes(query) || 
                     tags.includes(query);
      
      card.classList.remove("search-highlight");
      
      if (query !== "" && matches) {
        card.classList.add("search-highlight");
      }
    });
  });

  popupClose.onclick = () => popup.classList.remove("active");
  popup.onclick = (e) => {
    if (e.target === popup) popup.classList.remove("active");
  };

  window.toggleTips = function() {
    const tipsContent = document.getElementById('tips-content');
    tipsContent.classList.toggle('show');
  };

  document.addEventListener('click', function(e) {
    const tipsToggle = document.querySelector('.tips-toggle');
    const tipsContent = document.getElementById('tips-content');
    if (tipsToggle && !tipsToggle.contains(e.target)) {
      tipsContent.classList.remove('show');
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      popup.classList.remove('active');
    }
  });
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadGlossaryData);
