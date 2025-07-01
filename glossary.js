import { stitchGlossary } from './glossarydata.js';

const searchInput = document.getElementById("search");
const grid = document.getElementById("glossary-grid");
const popup = document.getElementById("popup");
const popupTitle = document.getElementById("popup-title");
const popupDesc = document.getElementById("popup-description");
const popupUK = document.getElementById("popup-uk");
const popupTags = document.getElementById("popup-tags");
const popupClose = document.querySelector(".popup-close");

const safeSymbol = (sym) => (/^[a-zA-Z_]/.test(sym) ? sym : `sym_${sym}`);

function buildCards() {
  grid.innerHTML = '';
  stitchGlossary.forEach((s) => {
    const card = document.createElement("div");
    card.className = "stitch-card";
    card.setAttribute("data-name", s.name_us);
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

  // FIXED SEARCH WITH HIGHLIGHTING
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase().trim();
    
    Array.from(grid.children).forEach((card) => {
      const name = card.getAttribute("data-name").toLowerCase();
      const tags = card.getAttribute("data-tags").toLowerCase();
      const abbr = card.querySelector(".abbr").textContent.toLowerCase();
      
      const matches = name.includes(query) || 
                     abbr.includes(query) || 
                     tags.includes(query);
      
      // Remove existing highlight first
      card.classList.remove("search-highlight");
      
      // Add highlight if query exists and matches
      if (query !== "" && matches) {
        card.classList.add("search-highlight");
      }
    });
  });

  // Popup close
  popupClose.onclick = () => popup.classList.remove("active");
  popup.onclick = (e) => {
    if (e.target === popup) popup.classList.remove("active");
  };

  // Tips toggle - FIXED
  window.toggleTips = function() {
    const tipsContent = document.getElementById('tips-content');
    tipsContent.classList.toggle('show');
  };

  // Close tips when clicking outside - FIXED
  document.addEventListener('click', function(e) {
    const tipsToggle = document.querySelector('.tips-toggle');
    const tipsContent = document.getElementById('tips-content');
    if (tipsToggle && !tipsToggle.contains(e.target)) {
      tipsContent.classList.remove('show');
    }
  });

  // ESC key to close popup
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      popup.classList.remove('active');
    }
  });
}

document.readyState !== "loading"
  ? initGlossary()
  : document.addEventListener("DOMContentLoaded", initGlossary);