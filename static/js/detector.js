// ─── TruthLens AI — Detector JS ───────────────────────────────

const analyzeBtn     = document.getElementById('analyzeBtn');
const clearBtn       = document.getElementById('clearBtn');
const newsText       = document.getElementById('newsText');
const predictionEl   = document.getElementById('prediction');
const predictionIcon = document.getElementById('predictionIcon');
const confidenceBar  = document.getElementById('confidenceBar');
const confidenceVal  = document.getElementById('confidenceValue');
const loading        = document.getElementById('loading');
const explainList    = document.getElementById('explanationList');
const historyBody    = document.getElementById('historyBody');
const downloadBtn    = document.getElementById('downloadReport');
const wordCounter    = document.getElementById('wordCounter');

let latestResult = null;

// ─── Word Counter ─────────────────────────────────────────────
newsText.addEventListener('input', () => {
  const words = newsText.value.trim().split(/\s+/).filter(Boolean).length;
  const chars = newsText.value.length;
  wordCounter.textContent = `Words: ${words} | Characters: ${chars}`;
});

// ─── Analyze ──────────────────────────────────────────────────
analyzeBtn.addEventListener('click', async () => {
  const text = newsText.value.trim();
  if (text.length < 20) {
    showToast('⚠️ Please enter a longer article (at least 20 characters).', 'warning');
    return;
  }

  loading.classList.add('show');
  analyzeBtn.disabled = true;

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ news: text })
    });

    const data = await res.json();
    loading.classList.remove('show');
    analyzeBtn.disabled = false;

    if (!data.success) {
      showToast(data.message || 'Error — please try again.', 'danger');
      if (data.message && data.message.toLowerCase().includes('login')) {
        setTimeout(() => { window.location.href = '/login'; }, 1500);
      }
      return;
    }

    renderResult(data, text);

  } catch (err) {
    loading.classList.remove('show');
    analyzeBtn.disabled = false;
    showToast('❌ Server error — please try again.', 'danger');
    console.error(err);
  }
});

// ─── Render Result ────────────────────────────────────────────
function renderResult(data, text) {
  const isFake = data.prediction === 'FAKE NEWS';

  // Verdict
  predictionEl.textContent = data.prediction;
  predictionEl.style.color = isFake ? '#ef4444' : '#22c55e';
  predictionIcon.textContent = isFake ? '❌' : '✅';
  predictionIcon.style.background = isFake
    ? 'linear-gradient(135deg,#ef4444,#dc2626)'
    : 'linear-gradient(135deg,#22c55e,#16a34a)';

  // Confidence bar animate
  confidenceBar.style.width = '0%';
  confidenceVal.textContent = '0%';
  confidenceBar.style.background = isFake
    ? 'linear-gradient(90deg,#ef4444,#dc2626)'
    : 'linear-gradient(90deg,#22c55e,#06b6d4)';

  let current = 0;
  const target = parseFloat(data.confidence);
  const step = target / 60;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    confidenceBar.style.width = current + '%';
    confidenceVal.textContent = current.toFixed(1) + '%';
    if (current >= target) clearInterval(timer);
  }, 16);

  // Explainability
  explainList.innerHTML = '';
  if (data.explanation && data.explanation.length) {
    data.explanation.forEach((item, i) => {
      const li = document.createElement('li');
      const barWidth = Math.round((item.score / data.explanation[0].score) * 100);
      li.innerHTML = `
        <div class="kw-left">
          <span class="kw-rank">#${i + 1}</span>
          <strong class="kw-word">${item.word}</strong>
        </div>
        <div class="kw-right">
          <div class="kw-bar-wrap">
            <div class="kw-bar" style="width:${barWidth}%;background:${isFake ? '#ef4444' : '#22c55e'}"></div>
          </div>
          <span class="kw-score">${item.score.toFixed(4)}</span>
        </div>`;
      explainList.appendChild(li);
    });
  } else {
    explainList.innerHTML = '<li style="color:var(--sub);padding:16px 0;">No keyword data available.</li>';
  }

  // Save for download & history
  latestResult = {
    news: text,
    prediction: data.prediction,
    confidence: data.confidence,
    explanation: data.explanation || []
  };

  downloadBtn.disabled = false;

  // Add to session history table
  addHistoryRow(data, text);

  showToast(`${isFake ? '❌' : '✅'} ${data.prediction} — ${data.confidence.toFixed(1)}% confidence`, isFake ? 'danger' : 'success');
}

// ─── History Table ────────────────────────────────────────────
function addHistoryRow(data, text) {
  if (historyBody.querySelector('td[colspan]')) historyBody.innerHTML = '';
  const tr = document.createElement('tr');
  const isFake = data.prediction === 'FAKE NEWS';
  const preview = text.length > 60 ? text.substring(0, 60) + '...' : text;
  const now = new Date();
  tr.innerHTML = `
    <td style="font-size:13px;white-space:nowrap;">${now.toLocaleDateString()} ${now.toLocaleTimeString()}</td>
    <td style="font-size:13px;color:var(--sub);">${preview}</td>
    <td><span style="color:${isFake ? '#ef4444' : '#22c55e'};font-weight:600;">${data.prediction}</span></td>
    <td>${data.confidence.toFixed(1)}%</td>`;
  historyBody.prepend(tr);
}

// Load DB history on page load
async function loadHistory() {
  try {
    const res  = await fetch('/dashboard-data');
    const data = await res.json();
    if (!data.success || !data.history || !data.history.length) return;
    historyBody.innerHTML = '';
    data.history.forEach(row => {
      const tr = document.createElement('tr');
      const isFake = row.prediction === 'FAKE NEWS';
      tr.innerHTML = `
        <td style="font-size:13px;white-space:nowrap;">${row.created_at.split('.')[0]}</td>
        <td style="font-size:13px;color:var(--sub);">${row.preview}...</td>
        <td><span style="color:${isFake ? '#ef4444' : '#22c55e'};font-weight:600;">${row.prediction}</span></td>
        <td>${parseFloat(row.confidence).toFixed(1)}%</td>`;
      historyBody.appendChild(tr);
    });
  } catch (e) { /* silent */ }
}
loadHistory();

// ─── Clear ────────────────────────────────────────────────────
clearBtn.addEventListener('click', () => {
  newsText.value = '';
  predictionEl.textContent = 'Waiting...';
  predictionEl.style.color = 'white';
  predictionIcon.textContent = '🤖';
  predictionIcon.style.background = 'linear-gradient(135deg,#6366f1,#06b6d4)';
  confidenceBar.style.width = '0%';
  confidenceVal.textContent = '0%';
  explainList.innerHTML = '<li style="color:var(--sub);padding:16px 0;">Run a prediction to see keyword analysis here.</li>';
  wordCounter.textContent = 'Words: 0 | Characters: 0';
  downloadBtn.disabled = true;
  latestResult = null;
});

// ─── PDF Download ─────────────────────────────────────────────
downloadBtn.addEventListener('click', async () => {
  if (!latestResult) return;
  try {
    downloadBtn.textContent = '⏳ Generating...';
    downloadBtn.disabled = true;
    const res  = await fetch('/download-report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(latestResult)
    });
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = 'TruthLens_Report.pdf';
    a.click();
    URL.revokeObjectURL(url);
    downloadBtn.textContent = '📄 Download PDF Report';
    downloadBtn.disabled = false;
  } catch (e) {
    downloadBtn.textContent = '📄 Download PDF Report';
    downloadBtn.disabled = false;
    showToast('PDF generation failed.', 'danger');
  }
});

// ─── Toast ────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const t = document.createElement('div');
  t.className = `alert alert-${type}`;
  t.style.cssText = 'position:fixed;top:80px;right:20px;z-index:9999;min-width:280px;border-radius:14px;animation:fadeUp .3s;';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}
