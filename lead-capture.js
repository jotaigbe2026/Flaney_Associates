/* Shared lead capture: email validation, the Formsubmit bridge, and the gated
 * PDF modal.
 *
 * Loaded by the homepage (alongside script.js) and by every blog article page
 * (alongside blog/blog.js). It used to live inside script.js, but blog pages
 * don't load script.js, and blog posts now carry their own gated download — one
 * copy beats two that drift. Everything is null-guarded so a page without the
 * modal, or without any .gated-download button, is a no-op.
 */

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

function applyEmailState(input, feedback, result) {
    input.classList.remove('email-valid', 'email-invalid');
    feedback.classList.remove('valid', 'invalid');
    if (result.valid) {
        input.classList.add('email-valid');
        feedback.classList.add('valid');
    } else {
        input.classList.add('email-invalid');
        feedback.classList.add('invalid');
    }
    feedback.textContent = result.message;
}

function attachEmailValidation(inputId, feedbackId) {
    const input = document.getElementById(inputId);
    const feedback = document.getElementById(feedbackId);
    if (!input || !feedback) return;

    let timeout;
    input.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            if (!input.value.trim()) {
                input.classList.remove('email-valid', 'email-invalid');
                feedback.classList.remove('valid', 'invalid');
                feedback.textContent = '';
                return;
            }
            applyEmailState(input, feedback, validateEmail(input.value));
        }, 400);
    });

    // Also validate on blur immediately
    input.addEventListener('blur', () => {
        clearTimeout(timeout);
        if (!input.value.trim()) return;
        applyEmailState(input, feedback, validateEmail(input.value));
    });
}

// ===== SEND LEAD TO FORMSUBMIT (sends email to info@flaneyassociates.com) =====
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

    return fetch('https://formsubmit.co/ajax/info@flaneyassociates.com', {
        method: 'POST',
        body: formData
    });
}

function getStoredLead() {
    try {
        const data = localStorage.getItem('flaney_lead');
        return data ? JSON.parse(data) : null;
    } catch (e) {
        return null;
    }
}

function storeLead(name, email, company) {
    try {
        localStorage.setItem('flaney_lead', JSON.stringify({ name, email, company, ts: Date.now() }));
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

// ===== GATED PDF DOWNLOAD SYSTEM =====
(function () {
    const downloadModal = document.getElementById('downloadModal');
    const downloadForm = document.getElementById('downloadForm');
    const modalClose = document.getElementById('modalClose');
    const dlArticleInput = document.getElementById('dlArticle');
    if (!downloadModal || !downloadForm) return;

    let pendingPdfUrl = '';
    let pendingPdfTitle = '';

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
        const card = downloadModal.querySelector('.modal-card');
        const successEl = card.querySelector('.modal-success');
        if (successEl) successEl.remove();
        card.querySelector('.modal-icon').style.display = '';
        card.querySelector('h3').style.display = '';
        card.querySelector('.modal-subtitle').style.display = '';
        downloadForm.style.display = '';
    }

    function showSuccess() {
        const card = downloadModal.querySelector('.modal-card');
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
    if (modalClose) modalClose.addEventListener('click', closeModal);
    downloadModal.addEventListener('click', (e) => {
        if (e.target === downloadModal) closeModal();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && downloadModal.classList.contains('active')) {
            closeModal();
        }
    });

    // Download form submission — validate, capture lead, send email, then download
    downloadForm.addEventListener('submit', function (e) {
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

        const finish = () => {
            showSuccess();
            triggerDownload(pendingPdfUrl);
            setTimeout(() => {
                closeModal();
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 2500);
        };

        // Send lead to your email via Formsubmit. A failure there must not cost
        // the reader their download — they gave us their details either way.
        sendToFormsubmit(
            { name, email, company, article: pendingPdfTitle },
            'PDF Download Lead: ' + pendingPdfTitle + ' — Flaney Associates'
        ).then(finish).catch(finish);
    });

    attachEmailValidation('dlEmail', 'dlEmailFeedback');
})();


/* ===== SCHEDULED POSTS =====
 * Cards carry data-publish="YYYY-MM-DD". A post dated ahead is generated and
 * committed like any other, but stays out of the listings until its morning,
 * at which point the next visitor's page load reveals it — no rebuild, no
 * deploy. Runs on the homepage strip and the blog archive alike.
 */
function hideScheduledCards(root) {
    const today = new Date();
    const todayKey = [today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, '0'),
        String(today.getDate()).padStart(2, '0')].join('-');

    let hidden = 0;
    (root || document).querySelectorAll('[data-publish]').forEach(card => {
        if (!card.classList.contains('post-card')) return;
        if (card.dataset.publish > todayKey) {
            card.dataset.scheduled = 'true';
            card.hidden = true;
            hidden++;
        }
    });
    return hidden;
}
