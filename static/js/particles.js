class Particle {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.reset();
    }

    reset() {
        this.x = Math.random() * this.canvas.width;
        this.y = Math.random() * this.canvas.height;
        this.size = Math.random() * 5 + 1;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = Math.random() * 3 - 1.5;
        this.color = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 100) + 155}, 255, ${Math.random() * 0.5 + 0.2})`;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > this.canvas.width) this.x = 0;
        else if (this.x < 0) this.x = this.canvas.width;
        if (this.y > this.canvas.height) this.y = 0;
        else if (this.y < 0) this.y = this.canvas.height;
    }

    draw() {
        this.ctx.fillStyle = this.color;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        this.ctx.fill();
    }
}

class ParticleSystem {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.numberOfParticles = 100;
        this.init();
    }

    init() {
        this.canvas.className = 'particles-container';
        document.body.appendChild(this.canvas);
        this.resize();
        window.addEventListener('resize', () => this.resize());

        // Create particles
        for (let i = 0; i < this.numberOfParticles; i++) {
            this.particles.push(new Particle(this.canvas));
        }

        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw particles
        for (let particle of this.particles) {
            particle.update();
            particle.draw();

            // Draw connections
            for (let otherParticle of this.particles) {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(100, 149, 237, ${0.1 * (1 - distance / 100)})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(otherParticle.x, otherParticle.y);
                    this.ctx.stroke();
                }
            }
        }

        requestAnimationFrame(() => this.animate());
    }
}

// Initialize particle system when page loads
document.addEventListener('DOMContentLoaded', () => {
    new ParticleSystem();
});