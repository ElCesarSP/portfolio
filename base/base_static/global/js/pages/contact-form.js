/**
 * CONTACT FORM - Específico para Página de Contato
 * Validação e animações do formulário de contato
 */

(function() {
    'use strict';
    
    // Form validation and animation
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.style.opacity = '0.7';
                const btnText = submitBtn.querySelector('.btn-text');
                if (btnText) {
                    btnText.textContent = 'ENVIANDO...';
                }
            }
        });
    }
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message-alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
})();
