/**
 * PARALLAX EFFECTS - Específico para Home
 * Efeito parallax para elementos geométricos
 */

(function() {
    'use strict';
    
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hexPattern = document.querySelector('.hex-pattern');
        const diagonalLines = document.querySelector('.diagonal-lines');
        
        if (hexPattern) {
            hexPattern.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
        
        if (diagonalLines) {
            diagonalLines.style.transform = `translateY(${scrolled * 0.2}px) rotate(-15deg)`;
        }
    });
})();
