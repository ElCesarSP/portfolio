/**
 * CAROUSEL FUNCTIONALITY
 * Carrossel automático e responsivo para Projetos, Habilidades e Experiências
 */

class Carousel {
    constructor(container, options = {}) {
        this.container = container;
        this.track = container.querySelector('.carousel-track');
        this.items = Array.from(this.track.children);
        this.prevBtn = container.querySelector('.carousel-prev');
        this.nextBtn = container.querySelector('.carousel-next');
        this.indicatorsContainer = container.querySelector('.carousel-indicators');
        this.autoplayBtn = container.querySelector('.carousel-autoplay');
        
        // Configurações
        this.options = {
            itemsToShow: options.itemsToShow || 3,
            autoplay: options.autoplay !== undefined ? options.autoplay : true,
            autoplayInterval: options.autoplayInterval || 5000,
            loop: options.loop !== undefined ? options.loop : true,
            ...options
        };
        
        this.currentIndex = 0;
        this.autoplayTimer = null;
        this.isAutoplayPaused = false;
        
        // Só inicializa se houver mais de 3 itens
        if (this.items.length > 3) {
            this.init();
        } else {
            // Se 3 ou menos, usa grid normal
            this.track.classList.add('no-carousel');
            // Remove controles se existirem
            if (this.prevBtn) this.prevBtn.style.display = 'none';
            if (this.nextBtn) this.nextBtn.style.display = 'none';
            if (this.indicatorsContainer) this.indicatorsContainer.style.display = 'none';
            if (this.autoplayBtn) this.autoplayBtn.style.display = 'none';
        }
    }
    
    init() {
        this.createIndicators();
        this.attachEventListeners();
        this.updateCarousel();
        
        if (this.options.autoplay) {
            this.startAutoplay();
        }
        
        // Suporte a touch/swipe
        this.addTouchSupport();
        
        // Atualiza ao redimensionar
        window.addEventListener('resize', () => this.handleResize());
    }
    
    createIndicators() {
        if (!this.indicatorsContainer) return;
        
        this.indicatorsContainer.innerHTML = '';
        const totalSlides = Math.ceil(this.items.length / this.getItemsPerView());
        
        for (let i = 0; i < totalSlides; i++) {
            const indicator = document.createElement('div');
            indicator.classList.add('carousel-indicator');
            if (i === 0) indicator.classList.add('active');
            indicator.addEventListener('click', () => this.goToSlide(i));
            this.indicatorsContainer.appendChild(indicator);
        }
    }
    
    attachEventListeners() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        if (this.autoplayBtn) {
            this.autoplayBtn.addEventListener('click', () => this.toggleAutoplay());
        }
        
        // Pausa autoplay ao hover
        this.container.addEventListener('mouseenter', () => {
            if (this.options.autoplay && !this.isAutoplayPaused) {
                this.stopAutoplay();
            }
        });
        
        this.container.addEventListener('mouseleave', () => {
            if (this.options.autoplay && !this.isAutoplayPaused) {
                this.startAutoplay();
            }
        });
    }
    
    getItemsPerView() {
        const width = window.innerWidth;
        if (width <= 768) return 1;
        if (width <= 1024) return 2;
        return this.options.itemsToShow;
    }
    
    updateCarousel() {
        const itemsPerView = this.getItemsPerView();
        const itemWidth = this.items[0].offsetWidth;
        const gap = 30; // Gap entre itens
        const offset = -(this.currentIndex * (itemWidth + gap));
        
        this.track.style.transform = `translateX(${offset}px)`;
        
        // Atualiza indicadores
        this.updateIndicators();
        
        // Atualiza botões
        this.updateButtons();
    }
    
    updateIndicators() {
        if (!this.indicatorsContainer) return;
        
        const indicators = this.indicatorsContainer.querySelectorAll('.carousel-indicator');
        const itemsPerView = this.getItemsPerView();
        const activeIndicator = Math.floor(this.currentIndex / itemsPerView);
        
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === activeIndicator);
        });
    }
    
    updateButtons() {
        if (!this.prevBtn || !this.nextBtn) return;
        
        const itemsPerView = this.getItemsPerView();
        const maxIndex = this.items.length - itemsPerView;
        
        if (this.options.loop) {
            this.prevBtn.disabled = false;
            this.nextBtn.disabled = false;
        } else {
            this.prevBtn.disabled = this.currentIndex === 0;
            this.nextBtn.disabled = this.currentIndex >= maxIndex;
        }
    }
    
    next() {
        const itemsPerView = this.getItemsPerView();
        const maxIndex = this.items.length - itemsPerView;
        
        if (this.currentIndex < maxIndex) {
            this.currentIndex++;
        } else if (this.options.loop) {
            this.currentIndex = 0;
        }
        
        this.updateCarousel();
        this.resetAutoplay();
    }
    
    prev() {
        const itemsPerView = this.getItemsPerView();
        const maxIndex = this.items.length - itemsPerView;
        
        if (this.currentIndex > 0) {
            this.currentIndex--;
        } else if (this.options.loop) {
            this.currentIndex = maxIndex;
        }
        
        this.updateCarousel();
        this.resetAutoplay();
    }
    
    goToSlide(index) {
        const itemsPerView = this.getItemsPerView();
        this.currentIndex = index * itemsPerView;
        this.updateCarousel();
        this.resetAutoplay();
    }
    
    startAutoplay() {
        if (!this.options.autoplay) return;
        
        this.stopAutoplay();
        this.autoplayTimer = setInterval(() => {
            this.next();
        }, this.options.autoplayInterval);
        
        if (this.autoplayBtn) {
            this.autoplayBtn.classList.remove('paused');
            this.autoplayBtn.innerHTML = '<i class="fas fa-pause"></i>';
        }
    }
    
    stopAutoplay() {
        if (this.autoplayTimer) {
            clearInterval(this.autoplayTimer);
            this.autoplayTimer = null;
        }
    }
    
    toggleAutoplay() {
        this.isAutoplayPaused = !this.isAutoplayPaused;
        
        if (this.isAutoplayPaused) {
            this.stopAutoplay();
            if (this.autoplayBtn) {
                this.autoplayBtn.classList.add('paused');
                this.autoplayBtn.innerHTML = '<i class="fas fa-play"></i>';
            }
        } else {
            this.startAutoplay();
        }
    }
    
    resetAutoplay() {
        if (this.options.autoplay && !this.isAutoplayPaused) {
            this.startAutoplay();
        }
    }
    
    addTouchSupport() {
        let startX = 0;
        let currentX = 0;
        let isDragging = false;
        
        this.track.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
            this.stopAutoplay();
        });
        
        this.track.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            currentX = e.touches[0].clientX;
        });
        
        this.track.addEventListener('touchend', () => {
            if (!isDragging) return;
            
            const diff = startX - currentX;
            const threshold = 50;
            
            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    this.next();
                } else {
                    this.prev();
                }
            }
            
            isDragging = false;
            this.resetAutoplay();
        });
        
        // Mouse drag support
        this.track.addEventListener('mousedown', (e) => {
            startX = e.clientX;
            isDragging = true;
            this.track.style.cursor = 'grabbing';
            this.stopAutoplay();
        });
        
        this.track.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            currentX = e.clientX;
        });
        
        this.track.addEventListener('mouseup', () => {
            if (!isDragging) return;
            
            const diff = startX - currentX;
            const threshold = 50;
            
            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    this.next();
                } else {
                    this.prev();
                }
            }
            
            isDragging = false;
            this.track.style.cursor = 'grab';
            this.resetAutoplay();
        });
        
        this.track.addEventListener('mouseleave', () => {
            if (isDragging) {
                isDragging = false;
                this.track.style.cursor = 'grab';
                this.resetAutoplay();
            }
        });
    }
    
    handleResize() {
        // Recalcula ao redimensionar
        this.updateCarousel();
        
        // Recria indicadores se necessário
        const itemsPerView = this.getItemsPerView();
        const totalSlides = Math.ceil(this.items.length / itemsPerView);
        const currentIndicators = this.indicatorsContainer?.querySelectorAll('.carousel-indicator').length || 0;
        
        if (totalSlides !== currentIndicators) {
            this.createIndicators();
        }
    }
    
    destroy() {
        this.stopAutoplay();
        // Remove event listeners se necessário
    }
}

// Inicialização automática ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    // Inicializa carrossel de projetos
    const projectsCarousel = document.querySelector('.projects-carousel');
    if (projectsCarousel) {
        new Carousel(projectsCarousel, {
            itemsToShow: 3,
            autoplay: true,
            autoplayInterval: 5000
        });
    }
    
    // Inicializa carrossel de habilidades
    const skillsCarousel = document.querySelector('.skills-carousel');
    if (skillsCarousel) {
        new Carousel(skillsCarousel, {
            itemsToShow: 3,
            autoplay: true,
            autoplayInterval: 4000
        });
    }
    
    // Inicializa carrossel de experiências
    const experiencesCarousel = document.querySelector('.experiences-carousel');
    if (experiencesCarousel) {
        new Carousel(experiencesCarousel, {
            itemsToShow: 3,
            autoplay: true,
            autoplayInterval: 6000
        });
    }
});
