// ─── TruthLens AI — Landing Page JS ──────────────────────────

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
  });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  nav.style.background = window.scrollY > 50
    ? 'rgba(8,17,31,.92)'
    : 'rgba(255,255,255,.05)';
});

// Counter animation (IntersectionObserver)
const counters = document.querySelectorAll('.counter');
const obs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el     = entry.target;
    const target = parseFloat(el.dataset.target);
    const isFloat = String(target).includes('.');
    let current  = 0;
    const inc    = target / 80;
    const t      = setInterval(() => {
      current = Math.min(current + inc, target);
      el.textContent = isFloat ? current.toFixed(1) : Math.floor(current).toLocaleString();
      if (current >= target) clearInterval(t);
    }, 16);
    obs.unobserve(el);
  });
}, { threshold: 0.4 });
counters.forEach(c => obs.observe(c));

// Fade-in on scroll
const fadeEls = document.querySelectorAll('.feature-card, .workflow-card, .why-card, .stat-card');
const fadeObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });
fadeEls.forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity .5s ease, transform .5s ease';
  fadeObs.observe(el);
});
