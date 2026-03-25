// ===== EMAIL VALIDATION =====
const DISPOSABLE_DOMAINS = [
    'mailinator.com','guerrillamail.com','tempmail.com','throwaway.email',
    'yopmail.com','sharklasers.com','guerrillamailblock.com','grr.la',
    'dispostable.com','trashmail.com','10minutemail.com','temp-mail.org',
    'fakeinbox.com','mailnesia.com','maildrop.cc','discard.email',
    'tmpmail.net','tmpmail.org','boun.cr','mt2015.com','tmail.ws',
    'mohmal.com','getnada.com','emailondeck.com','33mail.com',
    'guerrillamail.info','guerrillamail.net','spam4.me','trash-mail.com',
    'mytemp.email','tempail.com','tempr.email','burnermail.io'
];

function validateEmail(email) {
    const trimmed = email.trim().toLowerCase();
    if (!trimmed) return { valid: false, message: '' };

    // Basic format check
    const formatRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    if (!formatRegex.test(trimmed)) {
        return { valid: false, message: 'Please enter a valid email address' };
    }

    // Must have a real TLD (at least 2 chars after last dot)
    const parts = trimmed.split('@');
    if (parts.length !== 2) return { valid: false, message: 'Please enter a valid email address' };
    const domain = parts[1];
    const tld = domain.split('.').pop();
    if (!tld || tld.length < 2) {
        return { valid: false, message: 'Please enter a valid email domain' };
    }

    // Block disposable email providers
    if (DISPOSABLE_DOMAINS.includes(domain)) {
        return { valid: false, message: 'Please use a permanent email address (no disposable emails)' };
    }

    return { valid: true, message: 'Email looks good' };
}

function attachEmailValidation(inputId, feedbackId) {
    const input = document.getElementById(inputId);
    const feedback = document.getElementById(feedbackId);
    if (!input || !feedback) return;

    let timeout;
    input.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const result = validateEmail(input.value);
            input.classList.remove('email-valid', 'email-invalid');
            feedback.classList.remove('valid', 'invalid');

            if (!input.value.trim()) {
                feedback.textContent = '';
                return;
            }

            if (result.valid) {
                input.classList.add('email-valid');
                feedback.classList.add('valid');
                feedback.textContent = result.message;
            } else {
                input.classList.add('email-invalid');
                feedback.classList.add('invalid');
                feedback.textContent = result.message;
            }
        }, 400);
    });

    // Also validate on blur immediately
    input.addEventListener('blur', () => {
        clearTimeout(timeout);
        if (!input.value.trim()) return;
        const result = validateEmail(input.value);
        input.classList.remove('email-valid', 'email-invalid');
        feedback.classList.remove('valid', 'invalid');
        if (result.valid) {
            input.classList.add('email-valid');
            feedback.classList.add('valid');
            feedback.textContent = result.message;
        } else {
            input.classList.add('email-invalid');
            feedback.classList.add('invalid');
            feedback.textContent = result.message;
        }
    });
}

// ===== SEND LEAD TO FORMSUBMIT (sends email to info@otaigbeconsultancy.com) =====
function sendToFormsubmit(data, subject) {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('email', data.email);
    if (data.company) formData.append('company', data.company);
    if (data.service) formData.append('service', data.service);
    if (data.message) formData.append('message', data.message);
    if (data.article) formData.append('article_downloaded', data.article);
    formData.append('_subject', subject);
    formData.append('_captcha', 'false');
    formData.append('_template', 'table');

    return fetch('https://formsubmit.co/ajax/info@otaigbeconsultancy.com', {
        method: 'POST',
        body: formData
    });
}


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
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offset = 80;
            const top = target.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        }
    });
});


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

        sendToFormsubmit(formData, 'New Consultation Request — Otaigbe Consultancy')
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
}


// ===== GATED PDF DOWNLOAD SYSTEM =====
const downloadModal = document.getElementById('downloadModal');
const downloadForm = document.getElementById('downloadForm');
const modalClose = document.getElementById('modalClose');
const dlArticleInput = document.getElementById('dlArticle');
let pendingPdfUrl = '';
let pendingPdfTitle = '';

function getStoredLead() {
    try {
        const data = localStorage.getItem('otaigbe_lead');
        return data ? JSON.parse(data) : null;
    } catch (e) {
        return null;
    }
}

function storeLead(name, email, company) {
    try {
        localStorage.setItem('otaigbe_lead', JSON.stringify({ name, email, company, ts: Date.now() }));
    } catch (e) {}
}

function triggerDownload(url) {
    const a = document.createElement('a');
    a.href = url;
    a.download = '';
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function openModal(pdfUrl, pdfTitle) {
    pendingPdfUrl = pdfUrl;
    pendingPdfTitle = pdfTitle;
    dlArticleInput.value = pdfTitle;

    const stored = getStoredLead();
    if (stored) {
        document.getElementById('dlName').value = stored.name || '';
        document.getElementById('dlEmail').value = stored.email || '';
        document.getElementById('dlCompany').value = stored.company || '';
    }

    resetModalToForm();
    downloadModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    setTimeout(() => {
        const nameField = document.getElementById('dlName');
        const emailField = document.getElementById('dlEmail');
        if (!nameField.value) nameField.focus();
        else if (!emailField.value) emailField.focus();
    }, 100);
}

function closeModal() {
    downloadModal.classList.remove('active');
    document.body.style.overflow = '';
    pendingPdfUrl = '';
    pendingPdfTitle = '';
    // Clear validation states
    const dlEmail = document.getElementById('dlEmail');
    dlEmail.classList.remove('email-valid', 'email-invalid');
    document.getElementById('dlEmailFeedback').textContent = '';
}

function resetModalToForm() {
    const card = document.querySelector('.modal-card');
    const successEl = card.querySelector('.modal-success');
    if (successEl) successEl.remove();
    card.querySelector('.modal-icon').style.display = '';
    card.querySelector('h3').style.display = '';
    card.querySelector('.modal-subtitle').style.display = '';
    downloadForm.style.display = '';
}

function showSuccess() {
    const card = document.querySelector('.modal-card');
    card.querySelector('.modal-icon').style.display = 'none';
    card.querySelector('h3').style.display = 'none';
    card.querySelector('.modal-subtitle').style.display = 'none';
    downloadForm.style.display = 'none';

    const successDiv = document.createElement('div');
    successDiv.className = 'modal-success';
    successDiv.innerHTML = `
        <div class="success-icon">&#10004;</div>
        <h3>Download Starting!</h3>
        <p>Your article is downloading now.<br>We'll also send a copy to your email.</p>
    `;
    card.appendChild(successDiv);
}

// Click handler for gated download buttons
document.querySelectorAll('.gated-download').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const pdfUrl = btn.getAttribute('data-pdf');
        const pdfTitle = btn.getAttribute('data-title');

        const stored = getStoredLead();
        if (stored && stored.name && stored.email) {
            triggerDownload(pdfUrl);
            return;
        }

        openModal(pdfUrl, pdfTitle);
    });
});

// Close modal handlers
modalClose.addEventListener('click', closeModal);
downloadModal.addEventListener('click', (e) => {
    if (e.target === downloadModal) closeModal();
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && downloadModal.classList.contains('active')) {
        closeModal();
    }
});

// Download form submission — validate, capture lead, send email, then download
downloadForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('dlName').value.trim();
    const email = document.getElementById('dlEmail').value.trim();
    const company = document.getElementById('dlCompany').value.trim();

    if (!name || !email) return;

    // Validate email
    const emailResult = validateEmail(email);
    if (!emailResult.valid) {
        document.getElementById('dlEmail').focus();
        const fb = document.getElementById('dlEmailFeedback');
        fb.classList.remove('valid');
        fb.classList.add('invalid');
        fb.textContent = emailResult.message || 'Please enter a valid email';
        return;
    }

    const btn = downloadForm.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Processing...';
    btn.disabled = true;

    // Store the lead locally
    storeLead(name, email, company);

    // Send lead to your email via Formsubmit
    sendToFormsubmit(
        { name, email, company, article: pendingPdfTitle },
        'PDF Download Lead: ' + pendingPdfTitle + ' — Otaigbe Consultancy'
    )
    .then(() => {
        showSuccess();
        triggerDownload(pendingPdfUrl);
        setTimeout(() => {
            closeModal();
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2500);
    })
    .catch(() => {
        // Even if email sending fails, still allow the download
        showSuccess();
        triggerDownload(pendingPdfUrl);
        setTimeout(() => {
            closeModal();
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2500);
    });
});


// ===== INIT EMAIL VALIDATION ON BOTH FORMS =====
attachEmailValidation('contactEmail', 'contactEmailFeedback');
attachEmailValidation('dlEmail', 'dlEmailFeedback');


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
