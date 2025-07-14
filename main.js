// Sticky Navigation
window.addEventListener('scroll', function() {
    const nav = document.getElementById('nav');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    const navDropdown = document.querySelector('.nav-dropdown');
    if (navDropdown) {
        const dropdownMenu = navDropdown.querySelector('.dropdown-menu');
        let hoverTimer;
        
        // Show dropdown on hover
        navDropdown.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimer);
            dropdownMenu.style.display = 'block';
        });
        
        // Hide dropdown when mouse leaves
        navDropdown.addEventListener('mouseleave', function() {
            hoverTimer = setTimeout(function() {
                dropdownMenu.style.display = 'none';
            }, 100); // Small delay to prevent flickering
        });
        
        // Keep dropdown open when hovering over it
        dropdownMenu.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimer);
        });
        
        dropdownMenu.addEventListener('mouseleave', function() {
            dropdownMenu.style.display = 'none';
        });
    }
});