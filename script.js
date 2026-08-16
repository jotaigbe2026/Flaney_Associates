/* Homepage behaviour.
 *
 * Email validation, the Formsubmit bridge and the gated PDF modal live in
 * lead-capture.js, which every page loads first — blog article pages need the
 * same gate and don't load this file.
 */

// ===== NAVBAR =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});

document.addEventListener('click', (e) => {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('active');
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const href = this.getAttribute('href');

        // The logo is href="#", and querySelector('#') is a syntax error, so
        // this threw on every logo click and the click did nothing at all —
        // preventDefault had already run. A bare hash means "back to the top".
        if (!href || href === '#') {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            return;
        }

        const target = document.querySelector(href);
        if (target) {
            const offset = 80;
            const top = target.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        }
    });
});


// ===== SCHEDULED POSTS =====
// Future-dated cards in the "latest from the blog" strip stay hidden until
// their publication date. See hideScheduledCards() in lead-capture.js.
hideScheduledCards();


// ===== CONTACT FORM SUBMISSION =====
const form = document.getElementById('contactForm');
if (form) {
    // Set the _next redirect to current page
    const nextInput = form.querySelector('input[name="_next"]');
    if (nextInput) nextInput.value = window.location.href;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validate email first
        const emailInput = document.getElementById('contactEmail');
        const emailResult = validateEmail(emailInput.value);
        if (!emailResult.valid) {
            emailInput.focus();
            const fb = document.getElementById('contactEmailFeedback');
            fb.classList.remove('valid');
            fb.classList.add('invalid');
            fb.textContent = emailResult.message || 'Please enter a valid email';
            return;
        }

        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        btn.textContent = 'Sending...';
        btn.disabled = true;

        const formData = {
            name: form.querySelector('[name="name"]').value.trim(),
            email: emailInput.value.trim(),
            company: form.querySelector('[name="company"]').value.trim(),
            service: form.querySelector('[name="service"]').value,
            message: form.querySelector('[name="message"]').value.trim()
        };

        sendToFormsubmit(formData, 'New Consultation Request — Flaney Associates')
            .then(res => {
                if (res.ok) {
                    btn.textContent = 'Request Sent!';
                    btn.style.background = '#22c55e';
                    form.reset();
                    // Clear validation states
                    emailInput.classList.remove('email-valid', 'email-invalid');
                    document.getElementById('contactEmailFeedback').textContent = '';
                } else {
                    btn.textContent = 'Error — Try Again';
                    btn.style.background = '#ef4444';
                }
            })
            .catch(() => {
                btn.textContent = 'Error — Try Again';
                btn.style.background = '#ef4444';
            })
            .finally(() => {
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 3000);
            });
    });

    attachEmailValidation('contactEmail', 'contactEmailFeedback');
}


// ===== SCROLL ANIMATIONS =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.service-card, .expertise-card, .industry-card, .testimonial-card, .process-step, .blog-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
