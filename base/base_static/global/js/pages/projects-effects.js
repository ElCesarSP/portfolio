/**
 * PROJECT CARDS - Específico para Página de Projetos
 * Efeitos de hover nos cards de projetos
 */

(function() {
    'use strict'

    const projectCards = document.querySelectorAll('.project-card-tech')

    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function(){
            this.style.transform = 'translateY(-10px)';
        });

        card.addEventListener('mouseleave',function(){
            this.style.transform = 'translateY(0)';
        });
    });
})();