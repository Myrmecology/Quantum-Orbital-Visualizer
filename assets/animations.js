// =========================================
// Quantum Orbital Visualizer - Animations
// JavaScript for enhanced UI effects
// =========================================

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('⚛️ Quantum Orbital Visualizer - Animations Loaded');
    
    // Initialize animations
    initParticleBackground();
    initScrollEffects();
    initButtonEffects();
    initThemeTransitions();
});

// =========================================
// PARTICLE BACKGROUND EFFECT
// =========================================

function initParticleBackground() {
    // Create canvas for particle effect
    const canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.3';
    
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Particle array
    const particles = [];
    const particleCount = 50;
    
    // Particle class
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.radius = Math.random() * 2 + 1;
            this.color = '#4CC9F0';
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            
            // Wrap around edges
            if (this.x < 0) this.x = canvas.width;
            if (this.x > canvas.width) this.x = 0;
            if (this.y < 0) this.y = canvas.height;
            if (this.y > canvas.height) this.y = 0;
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
            
            // Glow effect
            ctx.shadowBlur = 10;
            ctx.shadowColor = this.color;
        }
    }
    
    // Create particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }
    
    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        
        // Draw connections
        particles.forEach((p1, i) => {
            particles.slice(i + 1).forEach(p2 => {
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(76, 201, 240, ${1 - distance / 150})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // Resize handler
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// =========================================
// SCROLL EFFECTS
// =========================================

function initScrollEffects() {
    const cards = document.querySelectorAll('.card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.5s ease-out';
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => observer.observe(card));
}

// =========================================
// BUTTON EFFECTS
// =========================================

function initButtonEffects() {
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(76, 201, 240, 0.5)';
            ripple.style.animation = 'ripple-effect 0.6s ease-out';
            
            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple-effect {
            from {
                transform: scale(0);
                opacity: 1;
            }
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// =========================================
// THEME TRANSITIONS
// =========================================

function initThemeTransitions() {
    // Smooth theme transitions
    const root = document.documentElement;
    
    // Watch for theme changes
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.attributeName === 'data-theme') {
                document.body.style.transition = 'background-color 0.5s ease, color 0.5s ease';
            }
        });
    });
    
    observer.observe(root, { attributes: true });
}

// =========================================
// ORBITAL ROTATION ANIMATION
// =========================================

function animateOrbitalRotation(plotElement) {
    if (!plotElement) return;
    
    let angle = 0;
    const rotationSpeed = 0.5;
    
    function rotate() {
        angle += rotationSpeed;
        
        // Update camera rotation (if plotly plot exists)
        if (plotElement.layout && plotElement.layout.scene) {
            Plotly.relayout(plotElement, {
                'scene.camera.eye': {
                    x: 1.5 * Math.cos(angle * Math.PI / 180),
                    y: 1.5 * Math.sin(angle * Math.PI / 180),
                    z: 1.5
                }
            });
        }
        
        requestAnimationFrame(rotate);
    }
    
    // Uncomment to enable auto-rotation
    // rotate();
}

// =========================================
// LOADING ANIMATION
// =========================================

function showLoadingAnimation(message = 'Calculating quantum states...') {
    const loader = document.createElement('div');
    loader.id = 'quantum-loader';
    loader.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(10, 14, 39, 0.95);
        padding: 30px 50px;
        border-radius: 10px;
        border: 2px solid #4CC9F0;
        box-shadow: 0 0 20px rgba(76, 201, 240, 0.5);
        z-index: 9999;
        text-align: center;
    `;
    
    loader.innerHTML = `
        <div style="color: #4CC9F0; font-size: 18px; margin-bottom: 15px;">
            ${message}
        </div>
        <div class="spinner" style="
            border: 4px solid rgba(76, 201, 240, 0.3);
            border-top: 4px solid #4CC9F0;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        "></div>
    `;
    
    document.body.appendChild(loader);
    
    // Add spin animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    return loader;
}

function hideLoadingAnimation() {
    const loader = document.getElementById('quantum-loader');
    if (loader) {
        loader.remove();
    }
}

// =========================================
// QUANTUM NUMBER VALIDATION EFFECTS
// =========================================

function highlightInvalidInput(inputElement) {
    inputElement.style.animation = 'shake 0.5s';
    inputElement.style.borderColor = '#FF0000';
    
    setTimeout(() => {
        inputElement.style.borderColor = '#4CC9F0';
    }, 1000);
    
    // Add shake animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);
}

// =========================================
// SUCCESS NOTIFICATION
// =========================================

function showSuccessNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4CC9F0, #7209B7);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(76, 201, 240, 0.5);
        z-index: 10000;
        animation: slideIn 0.3s ease-out, fadeOut 0.3s ease-out 2.7s;
        font-weight: 600;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Add animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes fadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    setTimeout(() => notification.remove(), 3000);
}

// =========================================
// EXPORT FUNCTIONS FOR DASH CALLBACKS
// =========================================

window.quantumAnimations = {
    showLoading: showLoadingAnimation,
    hideLoading: hideLoadingAnimation,
    showSuccess: showSuccessNotification,
    highlightInvalid: highlightInvalidInput,
    animateRotation: animateOrbitalRotation
};

console.log('✨ Quantum animations initialized successfully!');