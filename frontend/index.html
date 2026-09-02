<!doctype html>
<html lang="ur">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Multi-Asset Signal Robot</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0b1020;color:#eef2ff;font-family:Arial,sans-serif}
.wrap{max-width:900px;margin:auto;padding:14px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:#9eabc7;font-size:13px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:1fr;gap:12px}
.card{background:#121a2d;border:1px solid #263452;border-radius:16px;padding:14px}
.symbol{font-size:15px;font-weight:800;color:#cdd9f5}
.label{font-size:11px;color:#9eabc7;margin-bottom:6px}
.price{font-size:24px;font-weight:800;margin:6px 0}
.badge{display:inline-block;padding:6px 12px;border-radius:10px;font-weight:800;font-size:13px}
.wait{background:#4a3b12;color:#ffd86b}
.buy{background:#103e2b;color:#63e6a4}
.sell{background:#4a1820;color:#ff8996}
.error{background:#2a2a2a;color:#aaa}
.meta{font-size:11px;color:#7c8bab;margin-top:8px}
.chart{height:180px;overflow:hidden;border-radius:10px;margin-top:10px;background:#0d1425}
.chart iframe{width:100%;height:100%;border:0}
button{width:100%;border:0;border-radius:12px;padding:13px;background:#1e2b47;color:white;font-size:15px;font-weight:700;margin-top:14px}
.note{font-size:12px;line-height:1.5;color:#9eabc7;margin-top:14px;background:#121a2d;border:1px solid #263452;border-radius:16px;padding:14px}
.cfg{font-size:11px;color:#7c8bab;margin-bottom:10px}
.cfg input{background:#0d1425;border:1px solid #263452;color:#eef2ff;border-radius:8px;padding:6px 8px;width:100%;margin-top:4px}
</style>
</head>
<body>
<div class="wrap">
  <h1>🤖 Multi-Asset Signal Robot</h1>
  <div class="sub">Gold • Silver • BTC • SOL — 5 Minute Chart — Live</div>

  <div class="cfg">
    Backend API URL:
    <input id="apiUrl" placeholder="https://your-backend.onrender.com" />
  </div>

  <div class="grid" id="grid">
    <div class="card"><div class="label">GOLD (XAU/USD)</div><div class="price">Loading...</div></div>
    <div class="card"><div class="label">SILVER (XAG/USD)</div><div class="price">Loading...</div></div>
    <div class="card"><div class="label">BTC/USDT</div><div class="price">Loading...</div></div>
    <div class="card"><div class="label">SOL/USDT</div><div class="price">Loading...</div></div>
  </div>

  <button onclick="loadSignals()">🔄 Refresh Now</button>

  <div class="note">
    <b>اہم:</b> یہ signals ایک simple EMA9/EMA21 crossover + RSI filter پر مبنی ہیں (reference/analysis کے لیے)۔
    یہ خود کسی broker پر trade نہیں لگاتا۔ ہمیشہ اپنی risk management کے ساتھ manually confirm کر کے trade کریں۔
  </div>
</div>

<script>
const ORDER = ["GOLD", "SILVER", "BTC", "SOL"];
const TV_SYMBOLS = {
  GOLD: "OANDA:XAUUSD",
  SILVER: "OANDA:XAGUSD",
  BTC: "BINANCE:BTCUSDT",
  SOL: "BINANCE:SOLUSDT",
};

function getApiBase() {
  const saved = localStorage.getItem('signalRobotApiUrl');
  const input = document.getElementById('apiUrl');
  if (saved && !input.value) input.value = saved;
  return (input.value || saved || '').replace(/\/$/, '');
}

document.getElementById('apiUrl').addEventListener('change', (e) => {
  localStorage.setItem('signalRobotApiUrl', e.target.value.trim());
  loadSignals();
});

function badgeClass(signal) {
  if (signal === 'BUY') return 'buy';
  if (signal === 'SELL') return 'sell';
  if (signal === 'ERROR') return 'error';
  return 'wait';
}

async function loadSignals() {
  const base = getApiBase();
  const grid = document.getElementById('grid');
  if (!base) {
    grid.innerHTML = '<div class="card"><div class="label">SETUP NEEDED</div><div class="sub">Upar apna backend API URL daalein</div></div>';
    return;
  }
  const chartsBuilt = grid.dataset.built === 'true';
  if (!chartsBuilt) {
    grid.innerHTML = '';
    ORDER.forEach((key) => {
      const tvSymbol = TV_SYMBOLS[key];
      grid.insertAdjacentHTML('beforeend', `
        <div class="card">
          <div class="symbol">${key}</div>
          <div class="price" id="price-${key}">Loading...</div>
          <span class="badge wait" id="badge-${key}">...</span>
          <div class="meta" id="meta-${key}"></div>
          <div class="chart">
            <iframe
              src="https://www.tradingview.com/widgetembed/?frameElementId=tv_${key}&symbol=${encodeURIComponent(tvSymbol)}&interval=5&hidesidetoolbar=1&symboledit=0&saveimage=0&toolbarbg=0b1020&studies=%5B%5D&theme=dark&style=1&timezone=Etc%2FUTC&hidelegend=0&hidevolume=1"
              allowtransparency="true" scrolling="no" allowfullscreen>
            </iframe>
          </div>
        </div>
      `);
    });
    grid.dataset.built = 'true';
  }

  try {
    const r = await fetch(base + '/api/signals', { cache: 'no-store' });
    const json = await r.json();
    ORDER.forEach((key) => {
      const d = json.data[key];
      const priceText = d.price !== null ? '$' + d.price.toLocaleString(undefined, {maximumFractionDigits: 4}) : '--';
      const rsiText = d.rsi !== null ? 'RSI ' + d.rsi : '';
      const priceEl = document.getElementById('price-' + key);
      const badgeEl = document.getElementById('badge-' + key);
      const metaEl = document.getElementById('meta-' + key);
      if (priceEl) priceEl.textContent = priceText;
      if (badgeEl) {
        badgeEl.textContent = d.signal;
        badgeEl.className = 'badge ' + badgeClass(d.signal);
      }
      if (metaEl) metaEl.textContent = `${rsiText} • ${d.status}`;
    });
  } catch (e) {
    grid.innerHTML = '<div class="card"><div class="label">CONNECTION ERROR</div><div class="sub">Backend URL check karein</div></div>';
  }
}

loadSignals();
setInterval(loadSignals, 30000);
</script>
</body>
</html>
