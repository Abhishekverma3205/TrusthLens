// ─── TruthLens AI — Dashboard JS ──────────────────────────────

let trendChart = null;
let pieChart   = null;

// ─── Load All Data ────────────────────────────────────────────
async function loadDashboard() {
  try {
    const [dashRes, metricRes] = await Promise.all([
      fetch('/dashboard-data'),
      fetch('/metrics')
    ]);
    const dash    = await dashRes.json();
    const metrics = await metricRes.json();

    if (dash.success) {
      const s = dash.statistics;
      animateCount('statTotal', s.total);
      animateCount('statReal',  s.real);
      animateCount('statFake',  s.fake);

      renderTrendChart(s.daily || []);
      renderPieChart(s.real, s.fake);
      renderHistory(dash.history || []);
    }

    if (metrics.accuracy) {
      document.getElementById('accuracyMetric').textContent  = metrics.accuracy  + '%';
      document.getElementById('precisionMetric').textContent = metrics.precision + '%';
      document.getElementById('recallMetric').textContent    = metrics.recall    + '%';
      document.getElementById('f1Metric').textContent        = metrics.f1_score  + '%';
    }

  } catch (e) { console.error('Dashboard load error:', e); }
}

// ─── Animated Counter ─────────────────────────────────────────
function animateCount(id, target) {
  const el  = document.getElementById(id);
  if (!el) return;
  let start = 0;
  const inc = Math.max(1, Math.ceil(target / 60));
  const t   = setInterval(() => {
    start = Math.min(start + inc, target);
    el.textContent = start.toLocaleString();
    if (start >= target) clearInterval(t);
  }, 20);
}

// ─── Trend Chart ──────────────────────────────────────────────
function renderTrendChart(daily) {
  const ctx = document.getElementById('trendChart');
  if (!ctx) return;

  // Build last 7 days labels
  const labels = [], counts = [];
  for (let i = 6; i >= 0; i--) {
    const d   = new Date();
    d.setDate(d.getDate() - i);
    const key = d.toISOString().split('T')[0];
    labels.push(d.toLocaleDateString('en', { weekday: 'short', month: 'short', day: 'numeric' }));
    const found = daily.find(r => r.day === key);
    counts.push(found ? found.cnt : 0);
  }

  if (trendChart) trendChart.destroy();
  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Predictions',
        data: counts,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99,102,241,.15)',
        fill: true,
        tension: .4,
        pointRadius: 5,
        pointHoverRadius: 8,
        pointBackgroundColor: '#6366f1'
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: '#fff' } } },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,.05)' } },
        y: { beginAtZero: true, ticks: { color: '#94a3b8', stepSize: 1 }, grid: { color: 'rgba(255,255,255,.05)' } }
      }
    }
  });
}

// ─── Pie Chart ────────────────────────────────────────────────
function renderPieChart(real, fake) {
  const ctx = document.getElementById('pieChart');
  if (!ctx) return;
  if (pieChart) pieChart.destroy();
  pieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Real News', 'Fake News'],
      datasets: [{
        data: [real || 0, fake || 0],
        backgroundColor: ['#22c55e', '#ef4444'],
        borderWidth: 0
      }]
    },
    options: {
      cutout: '72%',
      plugins: { legend: { display: false }, tooltip: { callbacks: {
        label: ctx => ` ${ctx.label}: ${ctx.raw}`
      }}}
    }
  });
}

// ─── History Table ────────────────────────────────────────────
function renderHistory(history) {
  const tbody = document.getElementById('historyBody');
  if (!tbody) return;
  if (!history.length) {
    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:var(--sub);padding:24px;">No predictions yet — <a href="/detector">analyze your first article</a>.</td></tr>';
    return;
  }
  tbody.innerHTML = '';
  history.forEach(row => {
    const tr     = document.createElement('tr');
    const isFake = row.prediction === 'FAKE NEWS';
    tr.innerHTML = `
      <td style="font-size:13px;white-space:nowrap;">${row.created_at.split('.')[0]}</td>
      <td style="font-size:13px;color:var(--sub);">${row.preview}...</td>
      <td><span style="color:${isFake ? '#ef4444' : '#22c55e'};font-weight:600;">${row.prediction}</span></td>
      <td>${parseFloat(row.confidence).toFixed(1)}%</td>`;
    tbody.appendChild(tr);
  });
}

// ─── Live Clock ───────────────────────────────────────────────
function updateClock() {
  const now = new Date();
  const cl  = document.getElementById('liveClock');
  const dt  = document.getElementById('liveDate');
  if (cl) cl.textContent = now.toLocaleTimeString();
  if (dt) dt.textContent = now.toLocaleDateString('en', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
}
setInterval(updateClock, 1000);
updateClock();

// ─── AI Status Pulse ──────────────────────────────────────────
const statusEl = document.getElementById('aiStatus');
const statuses = ['● Online', '● Processing', '● Ready', '● Optimized'];
let si = 0;
setInterval(() => {
  si = (si + 1) % statuses.length;
  if (statusEl) statusEl.textContent = statuses[si];
}, 4000);

// ─── Live Activity Feed ───────────────────────────────────────
const activities = [
  '✅ Real News Detected', '❌ Fake News Caught', '🧠 ML Model Active',
  '📈 Confidence Scored', '📰 Article Processed', '🔍 NLP Analysis Complete',
  '⚡ Prediction Generated', '🧠 Keywords Extracted'
];
const feed = document.getElementById('activityFeed');
function addActivity() {
  if (!feed) return;
  const li   = document.createElement('li');
  li.textContent = activities[Math.floor(Math.random() * activities.length)];
  feed.prepend(li);
  while (feed.children.length > 8) feed.removeChild(feed.lastChild);
}
setInterval(addActivity, 3500);

// ─── Boot ─────────────────────────────────────────────────────
loadDashboard();

console.log('TruthLens AI Dashboard — Ready');
