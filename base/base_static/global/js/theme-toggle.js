/**
 * THEME TOGGLE - Universal
 * Gerencia alternância entre tema claro e escuro
 */

(function() {
    'use strict';
    
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    if (!themeToggle) return;
    
    // Check for saved theme preference or default to 'dark'
    const currentTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', currentTheme);
    
    // Toggle theme
    themeToggle.addEventListener('click', function() {
        const theme = htmlElement.getAttribute('data-theme');
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
})();
