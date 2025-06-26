import { stitchGlossary } from "./glossarydata.js";

const searchInput = document.getElementById("search");
const grid = document.getElementById("glossary-grid");
const popup = document.getElementById("popup");
const popupTitle = document.getElementById("popupTitle");
const popupDesc = document.getElementById("popupDescription");
const popupClose = document.getElementById("popupClose");

const safeSymbol = (sym) => (/^[a-zA-Z_]/.test(sym) ? sym : `sym_${sym}`);

function buildCards() {
  stitchGlossary.forEach((s) => {
    const card = document.createElement("div");
    card.className = "stitch-card";
    card.setAttribute("data-name", s.name_us);

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", 40);
    svg.setAttribute("height", 40);
    const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use.setAttribute("href", `#${safeSymbol(s.symbol)}`);
    svg.appendChild(use);

    const abbr = document.createElement("span");
    abbr.className = "abbr";
    abbr.textContent = s.id;

    const full = document.createElement("span");
    full.className = "fullword";
    full.textContent = s.name_us;

    card.append(svg, abbr, full);

    card.onclick = () => {
      popupTitle.textContent = s.name_us;
      popupDesc.textContent = s.notes || "";
      popup.classList.add("active");
    };

    grid.appendChild(card);
  });
}

function initGlossary() {
  buildCards();

  // live search
  searchInput.addEventListener("input", () => {
    const v = searchInput.value.toLowerCase();
    Array.from(grid.children).forEach((c) => {
      const name = c.getAttribute("data-name").toLowerCase();
      const abbr = c.querySelector(".abbr").textContent.toLowerCase();
      c.style.display = name.includes(v) || abbr.includes(v) ? "" : "none";
    });
  });

  // popup close
  popupClose.onclick = () => popup.classList.remove("active");
  popup.onclick = (e) => {
    if (e.target === popup) popup.classList.remove("active");
  };
}

document.readyState !== "loading"
  ? initGlossary()
  : document.addEventListener("DOMContentLoaded", initGlossary);
