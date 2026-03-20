// Navbar scroll effect
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

// Close mobile nav on link click
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});

// Close mobile nav on outside click
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

// Form submission (main contact form)
const form = document.getElementById('contactForm');
if (form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        btn.textContent = 'Sending...';
        btn.disabled = true;

        // Simulate form submission (replace with actual endpoint)
        setTimeout(() => {
            btn.textContent = 'Message Sent!';
            btn.style.background = '#22c55e';
            form.reset();
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.disabled = false;
            }, 3000);
        }, 1000);
    });
}

// ===== GATED PDF DOWNLOAD SYSTEM =====
const downloadModal = document.getElementById('downloadModal');
const downloadForm = document.getElementById('downloadForm');
const modalClose = document.getElementById('modalClose');
const dlArticleInput = document.getElementById('dlArticle');
let pendingPdfUrl = '';
let pendingPdfTitle = '';

// Check if user already provided their info (stored in localStorage)
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
    } catch (e) {
        // localStorage not available — no problem, modal will show again next time
    }
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

    // Pre-fill if we have stored lead data
    const stored = getStoredLead();
    if (stored) {
        document.getElementById('dlName').value = stored.name || '';
        document.getElementById('dlEmail').value = stored.email || '';
        document.getElementById('dlCompany').value = stored.company || '';
    }

    // Reset form to input view (in case it was showing success)
    resetModalToForm();

    downloadModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Focus the first empty field
    setTimeout(() => {
        const nameField = document.getElementById('dlName');
        const emailField = document.getElementById('dlEmail');
        if (!nameField.value) {
            nameField.focus();
        } else if (!emailField.value) {
            emailField.focus();
        }
    }, 100);
}

function closeModal() {
    downloadModal.classList.remove('active');
    document.body.style.overflow = '';
    pendingPdfUrl = '';
    pendingPdfTitle = '';
}

function resetModalToForm() {
    const card = document.querySelector('.modal-card');
    // Remove success state if present
    const successEl = card.querySelector('.modal-success');
    if (successEl) {
        successEl.remove();
    }
    // Show form elements
    card.querySelector('.modal-icon').style.display = '';
    card.querySelector('h3').style.display = '';
    card.querySelector('.modal-subtitle').style.display = '';
    downloadForm.style.display = '';
}

function showSuccess() {
    const card = document.querySelector('.modal-card');
    // Hide form elements
    card.querySelector('.modal-icon').style.display = 'none';
    card.querySelector('h3').style.display = 'none';
    card.querySelector('.modal-subtitle').style.display = 'none';
    downloadForm.style.display = 'none';

    // Insert success message
    const successDiv = document.createElement('div');
    successDiv.className = 'modal-success';
    successDiv.innerHTML = `
        <div class="success-icon">&#10004;</div>
        <h3>Download Starting!</h3>
        <p>Your article is downloading now.<br>We'll also send a copy to your email.</p>
    `;
    card.insertBefore(successDiv, card.querySelector('.modal-close').nextSibling || null);
    card.appendChild(successDiv);
}

// Click handler for all gated download buttons
document.querySelectorAll('.gated-download').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const pdfUrl = btn.getAttribute('data-pdf');
        const pdfTitle = btn.getAttribute('data-title');

        // If user already submitted their info previously, still show a quick
        // pre-filled modal — keeps the conversion path consistent and reminds
        // them we value the relationship. But auto-download after brief delay.
        const stored = getStoredLead();
        if (stored && stored.name && stored.email) {
            // Returning lead — skip the modal, download directly
            triggerDownload(pdfUrl);
            return;
        }

        // New visitor — show the lead capture modal
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

// Form submission — capture lead then download
downloadForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('dlName').value.trim();
    const email = document.getElementById('dlEmail').value.trim();
    const company = document.getElementById('dlCompany').value.trim();

    if (!name || !email) return;

    const btn = downloadForm.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Processing...';
    btn.disabled = true;

    // Store the lead
    storeLead(name, email, company);

    // Simulate sending lead data to backend (replace with real endpoint)
    // In production, you would POST to Formspree, Zapier, or your CRM here.
    setTimeout(() => {
        // Show success state
        showSuccess();

        // Trigger the actual PDF download
        triggerDownload(pendingPdfUrl);

        // Auto-close modal after a moment
        setTimeout(() => {
            closeModal();
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2500);
    }, 800);
});


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

// Apply animation to cards
document.querySelectorAll('.service-card, .expertise-card, .industry-card, .testimonial-card, .process-step, .blog-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
