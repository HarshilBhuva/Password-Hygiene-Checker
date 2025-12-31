document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('passwordInput');
    const togglePassword = document.getElementById('togglePassword');
    const checkBtn = document.getElementById('checkBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultsSection = document.getElementById('resultsSection');

    // Toggle password visibility
    togglePassword.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.querySelector('i').classList.toggle('fa-eye');
        this.querySelector('i').classList.toggle('fa-eye-slash');
    });

    // Check on button click
    checkBtn.addEventListener('click', function (e) {
        e.preventDefault();
        triggerCheck();
    });

    // Check on Enter key
    passwordInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            triggerCheck();
        }
    });

    function triggerCheck() {
        const password = passwordInput.value;
        if (!password) {
            // Could add a shake animation here
            passwordInput.parentElement.style.borderColor = 'var(--neon-red)';
            setTimeout(() => {
                passwordInput.parentElement.style.borderColor = '';
            }, 500);
            return;
        }
        checkPassword(password);
    }

    async function checkPassword(password) {
        loadingOverlay.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/check', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: password })
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.error);

            updateUI(data);
            loadingOverlay.classList.add('hidden');
            resultsSection.classList.remove('hidden');

        } catch (err) {
            console.error('Check failed:', err);
            loadingOverlay.classList.add('hidden');
            alert('An error occurred while checking the password.');
        }
    }

    function updateUI(data) {
        // Update Score Ring
        const score = data.risk_score;
        const scoreRingFill = document.getElementById('scoreRingFill');
        const riskScore = document.getElementById('riskScore');
        const riskLevel = document.getElementById('riskLevel');
        const strengthBarFill = document.querySelector('.bar-fill');

        // Set Score Number directly (no animation)
        riskScore.textContent = score;

        // Update Ring Arc (339.292 is full circumference)
        const circumference = 339.292;
        const offset = circumference - (circumference * score) / 100;
        scoreRingFill.style.strokeDashoffset = offset;
        scoreRingFill.style.stroke = data.risk_color;

        // Update Text & Bar
        riskLevel.textContent = data.risk_level;
        riskLevel.style.color = data.risk_color;

        strengthBarFill.style.width = `${score}%`;
        strengthBarFill.style.backgroundColor = data.risk_color;
        strengthBarFill.style.boxShadow = `0 0 15px ${data.risk_color}`;



        // Update Checks Grid
        const checksGrid = document.getElementById('checksGrid');
        checksGrid.innerHTML = '';

        const icons = {
            'Length': 'fa-ruler-horizontal',
            'Uppercase': 'fa-font',
            'Lowercase': 'fa-font',
            'Digits': 'fa-hashtag',
            'Special Characters': 'fa-asterisk',
            'Common Password': 'fa-shield-virus',
            'No Repetition': 'fa-clone'
        };

        data.checks.forEach(check => {
            const div = document.createElement('div');
            div.className = `check-item ${check.passed ? 'passed' : 'failed'}`;
            div.innerHTML = `
                <i class="fas ${icons[check.name] || 'fa-check-circle'} check-icon"></i>
                <div class="check-info">
                    <span class="check-name">${check.name}</span>
                    <span class="check-status">${check.passed ? 'PASSED' : 'FAILED'}</span>
                </div>
            `;
            checksGrid.appendChild(div);
        });

        // Update Issues & Recommendations
        updateList('issuesList', data.issues, 'fa-exclamation-triangle', 'issue');
        updateList('recommendationsList', data.recommendations, 'fa-lightbulb', 'recommendation');

        // Update Badges
        document.getElementById('issueCountBadge').textContent = data.issue_count;
    }

    function updateList(elementId, items, iconClass, itemType) {
        const container = document.getElementById(elementId);
        container.innerHTML = '';

        if (!items || items.length === 0) {
            container.innerHTML = `
                <div class="insight-item" style="background: rgba(255,255,255,0.03); border-left: 3px solid var(--neon-green);">
                    <i class="fas fa-check-circle" style="color: var(--neon-green)"></i> 
                    <span>No ${itemType}s found. Good job!</span>
                </div>`;
            return;
        }

        items.forEach(item => {
            const div = document.createElement('div');
            div.className = `insight-item ${itemType}`;
            div.innerHTML = `<i class="fas ${iconClass}"></i> <span>${item}</span>`;
            container.appendChild(div);
        });
    }

    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active to clicked
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');

            if (tabId === 'issues') {
                document.getElementById('issuesList').classList.add('active');
            } else {
                document.getElementById('recommendationsList').classList.add('active');
            }
        });
    });
});
