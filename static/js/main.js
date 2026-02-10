// Main JavaScript for Metamorphosis Workshop

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initAnimations();
    initStatsCounter();
    initVideoPlayer();
    initContactForm();
    initScrollAnimations();
    initParallaxEffect();
});

// Navbar Scroll Effect
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const adminLoginBtn = document.querySelector('.admin-login-btn');
    
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/admin/login';
        });
    }

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Counter Animation for Stats
function initStatsCounter() {
    const counters = document.querySelectorAll('.stat-value');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.textContent.replace('+', '').replace('%', ''));
                const isPercentage = counter.textContent.includes('%');
                const isPlus = counter.textContent.includes('+');
                
                animateCounter(counter, target, isPercentage, isPlus);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target, isPercentage, isPlus) {
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        if (isPercentage) {
            element.textContent = Math.round(current) + '%';
        } else if (isPlus) {
            element.textContent = Math.round(current) + '+';
        } else {
            element.textContent = Math.round(current);
        }
    }, 20);
}

// Video Player Modal
function initVideoPlayer() {
    const videoCards = document.querySelectorAll('.video-card');
    
    videoCards.forEach(card => {
        card.addEventListener('click', function() {
            const videoSrc = this.dataset.videoSrc;
            const videoTitle = this.dataset.videoTitle;
            
            showVideoModal(videoSrc, videoTitle);
        });
    });
}

function showVideoModal(src, title) {
    const modalHTML = `
        <div class="video-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; display: flex; align-items: center; justify-content: center;">
            <div style="position: relative; width: 90%; max-width: 800px;">
                <button class="close-video" style="position: absolute; top: -40px; right: 0; background: none; border: none; color: white; font-size: 2rem; cursor: pointer;">×</button>
                <h3 style="color: white; margin-bottom: 1rem;">${title}</h3>
                <video controls autoplay style="width: 100%; border-radius: 10px;">
                    <source src="${src}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    `;
    
    const modal = document.createElement('div');
    modal.innerHTML = modalHTML;
    document.body.appendChild(modal);
    
    // Close modal
    modal.querySelector('.close-video').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

// Contact Form Validation
function initContactForm() {
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simple validation
            const name = this.querySelector('#name').value;
            const email = this.querySelector('#email').value;
            const phone = this.querySelector('#phone').value;
            
            if (!name || !email || !phone) {
                showAlert('Please fill all required fields', 'error');
                return;
            }
            
            // If validation passes, submit form
            this.submit();
        });
    }
}

// Scroll Animations
function initScrollAnimations() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animateElements.forEach(element => observer.observe(element));
}

// Parallax Effect
function initParallaxEffect() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const rate = element.dataset.rate || 0.5;
            const movement = scrolled * rate;
            element.style.transform = `translateY(${movement}px)`;
        });
    });
}

// Alert System
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease;
    `;
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    document.body.removeChild(alertDiv);
                }
            }, 300);
        }
    }, 5000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }
    
    .animate-on-scroll.animated {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);