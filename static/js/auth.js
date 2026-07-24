// ─── TruthLens AI — Auth JS ───────────────────────────────────

// Toggle password visibility
const toggle   = document.getElementById('togglePassword');
const password = document.getElementById('password');
if (toggle && password) {
  toggle.addEventListener('click', () => {
    const isHidden = password.type === 'password';
    password.type  = isHidden ? 'text' : 'password';
    toggle.className = isHidden ? 'bx bx-hide' : 'bx bx-show';
  });
}

// Password strength meter (register page only)
const bar      = document.getElementById('strengthBar');
const label    = document.getElementById('strengthLabel');
if (bar && password) {
  password.addEventListener('input', () => {
    let score = 0;
    const v   = password.value;
    if (v.length >= 8)              score++;
    if (/[A-Z]/.test(v))           score++;
    if (/[0-9]/.test(v))           score++;
    if (/[^A-Za-z0-9]/.test(v))   score++;

    bar.style.width      = (score * 25) + '%';
    const colors  = ['#ef4444', '#f97316', '#fbbf24', '#22c55e'];
    const labels  = ['Weak', 'Fair', 'Good', 'Strong'];
    bar.style.background = colors[score - 1] || '#374151';
    if (label) label.textContent = v.length ? labels[score - 1] || '' : '';
  });
}
