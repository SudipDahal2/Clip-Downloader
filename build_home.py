import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, "templates", "home.html")

new_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SonicSnap</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg-dark: #0f1c24;
      --bg-card: #13222a;
      --bg-input: #081015;
      --cyan: #2ce5ff;
      --cyan-glow: rgba(44, 229, 255, 0.4);
      --text-main: #ffffff;
      --text-muted: #88a2b5;
      --border: #283b48;
      --green: #2ecc71;
      --red: #e74c3c;
      --amber: #f1c40f;
    }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      /* Grid pattern background */
      background-image: 
        linear-gradient(rgba(40, 59, 72, 0.3) 1px, transparent 1px),
        linear-gradient(90deg, rgba(40, 59, 72, 0.3) 1px, transparent 1px);
      background-size: 40px 40px;
    }
    
    .page { max-width: 900px; margin: 0 auto; padding: 32px 24px 80px; }
    
    /* ── Header ─────────────────────────────────────────── */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 80px;
    }
    .logo-area { display: flex; align-items: center; gap: 10px; text-decoration: none; color: white;}
    .logo-icon {
      width: 32px; height: 32px; border-radius: 50%;
      background: var(--cyan); display: flex; align-items: center; justify-content: center;
      color: #000; font-weight: bold; font-size: 18px;
    }
    .logo-text { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.5px; }
    
    .nav-links {
      display: flex; gap: 32px; font-size: 0.9rem; font-weight: 500; color: var(--text-main);
    }
    .nav-links a { text-decoration: none; color: inherit; transition: color 0.2s; }
    .nav-links a:hover { color: var(--cyan); }
    
    .header-actions { display: flex; align-items: center; gap: 16px; }
    .btn-icon {
      width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--border);
      background: rgba(255,255,255,0.05); color: var(--text-main); cursor: pointer;
      display: flex; align-items: center; justify-content: center; transition: all 0.2s;
    }
    .btn-icon:hover { background: rgba(255,255,255,0.1); }
    .btn-pro {
      background: var(--cyan); color: #000; font-weight: 600; font-size: 0.9rem;
      padding: 8px 20px; border-radius: 99px; text-decoration: none; border: none;
      box-shadow: 0 0 15px var(--cyan-glow); transition: all 0.2s; cursor: pointer;
    }
    .btn-pro:hover { box-shadow: 0 0 25px var(--cyan-glow); transform: translateY(-1px); }

    @media (max-width: 768px) {
      .nav-links { display: none; }
    }

    /* ── Hero ─────────────────────────────────────────── */
    .hero { text-align: center; margin-bottom: 40px; }
    .hero h1 {
      font-family: 'Space Grotesk', sans-serif; font-size: clamp(2.5rem, 6vw, 4rem);
      font-weight: 700; margin-bottom: 16px; letter-spacing: -1px;
    }
    .hero h1 span { color: var(--cyan); }
    .hero p {
      color: var(--text-muted); font-size: 1rem; max-width: 500px; margin: 0 auto; line-height: 1.6;
    }

    /* ── Main Panel ─────────────────────────────────────────── */
    .panel {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 32px;
      margin-bottom: 60px;
      box-shadow: 0 0 40px rgba(0,0,0,0.5);
    }
    
    .mode-toggle {
      background: var(--bg-input);
      border-radius: 99px; display: inline-flex; margin-bottom: 32px; padding: 4px;
      border: 1px solid var(--border);
    }
    .mode-pill {
      padding: 8px 24px; border-radius: 99px; font-size: 0.85rem; font-weight: 500;
      color: var(--text-muted); background: transparent; border: none; cursor: pointer;
      transition: all 0.2s;
    }
    .mode-pill.active { background: var(--cyan); color: #000; box-shadow: 0 0 10px var(--cyan-glow); }

    .input-group { margin-bottom: 24px; }
    .input-wrapper {
      position: relative; display: flex; align-items: center;
    }
    .input-wrapper svg {
      position: absolute; left: 16px; color: var(--cyan); width: 18px; height: 18px;
    }
    .input-field {
      width: 100%; background: var(--bg-input); border: 1px solid var(--border);
      border-radius: 12px; color: var(--text-main); font-family: 'Inter', sans-serif;
      font-size: 0.95rem; padding: 14px 14px 14px 44px; outline: none; transition: all 0.2s;
    }
    .input-field:focus { border-color: var(--cyan); box-shadow: 0 0 0 1px var(--cyan); }
    
    .format-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
    .select-wrapper { display: flex; flex-direction: column; gap: 8px; }
    .select-label { font-size: 0.75rem; text-transform: uppercase; font-weight: 600; color: var(--cyan); letter-spacing: 1px; }
    .select-field {
      width: 100%; background: var(--bg-input); border: 1px solid var(--border);
      border-radius: 12px; color: var(--text-main); font-family: 'Inter', sans-serif;
      font-size: 0.95rem; padding: 14px; outline: none; cursor: pointer;
      appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%232ce5ff' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
      background-repeat: no-repeat; background-position: right 16px center;
    }
    .select-field:focus { border-color: var(--cyan); }

    .btn-go {
      width: 100%; padding: 18px; background: var(--cyan); color: #000;
      font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.1rem;
      border: none; border-radius: 12px; cursor: pointer; transition: all 0.2s;
      box-shadow: 0 4px 20px var(--cyan-glow); letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 8px;
    }
    .btn-go:hover { box-shadow: 0 8px 30px var(--cyan-glow); transform: translateY(-2px); }
    .btn-go:active { transform: translateY(0); }
    .btn-go:disabled { opacity: 0.5; cursor: not-allowed; box-shadow: none; transform: none; }

    /* Bulk inputs */
    .link-rows { display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px; }
    .link-row { display: flex; gap: 8px; align-items: center; }
    .link-row input { padding-left: 14px; }
    .btn-remove { 
      background: var(--bg-input); border: 1px solid var(--border); color: var(--text-muted); 
      width: 44px; height: 44px; border-radius: 12px; cursor: pointer; transition: 0.2s; flex-shrink: 0;
    }
    .btn-remove:hover { border-color: var(--red); color: var(--red); }
    .btn-add-link {
      background: transparent; border: 1px dashed var(--border); color: var(--text-muted); padding: 10px; width: 100%; border-radius: 12px; cursor: pointer; transition: 0.2s;
    }
    .btn-add-link:hover { border-color: var(--cyan); color: var(--cyan); }

    /* ── Live Downloads Status Cards ───────────────────────── */
    .section-head {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;
    }
    .section-head h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; display: flex; align-items: center; gap: 8px; }
    .section-head svg { color: var(--cyan); width: 20px; }
    .clear-link { font-size: 0.85rem; color: var(--cyan); text-decoration: none; font-weight: 500; }
    .clear-link:hover { text-decoration: underline; }

    .card {
      background: transparent; border: 1px solid var(--border); border-radius: 16px;
      padding: 16px; margin-bottom: 12px; display: grid; grid-template-columns: 48px 1fr auto; gap: 16px; align-items: center;
      transition: background 0.2s;
    }
    .card:hover { background: rgba(255,255,255,0.02); }
    .card-thumb-ph {
      width: 48px; height: 48px; border-radius: 12px; background: rgba(44, 229, 255, 0.1);
      display: flex; align-items: center; justify-content: center; color: var(--cyan);
    }
    .card-thumb { width: 48px; height: 48px; border-radius: 12px; object-fit: cover; }
    .card-title { font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .card-meta { font-size: 0.7rem; color: var(--text-muted); display:flex; gap: 6px; align-items:center;}
    
    .badge {
      font-size: 0.65rem; font-weight: 600; padding: 4px 10px; border-radius: 99px; border: 1px solid currentColor; letter-spacing: 0.5px;
    }
    .badge-completed { color: var(--green); background: rgba(46, 204, 113, 0.1); }
    .badge-processing, .badge-downloading { color: var(--cyan); background: rgba(44, 229, 255, 0.1); box-shadow: 0 0 8px var(--cyan-glow); }
    .badge-failed, .badge-error { color: var(--red); background: rgba(231, 76, 60, 0.1); }
    .badge-queued { color: var(--text-muted); }

    .action-group { display: flex; align-items: center; gap: 12px; }
    .btn-act-icon { background: transparent; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; transition: 0.2s; }
    .btn-act-icon:hover { color: var(--text-main); }
    
    .prog-track { margin-top: 8px; width: 100%; height: 4px; background: var(--bg-input); border-radius: 2px; overflow: hidden; }
    .prog-fill { height: 100%; background: var(--cyan); width: 0%; transition: width 0.3s; box-shadow: 0 0 8px var(--cyan); }
    
    .empty { text-align: center; padding: 40px; color: var(--text-muted); font-size: 0.9rem; }
    
    /* Footer */
    .footer { display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: var(--text-muted); padding-top: 40px; border-top: 1px solid var(--border); margin-top: 60px; }
    .footer-links { display: flex; gap: 24px; }
    .footer-links a { color: inherit; text-decoration: none; font-weight: 500; letter-spacing: 0.5px; }
    .footer-links a:hover { color: var(--text-main); }
  </style>
</head>
<body>
  <div class="page">

    <!-- Header -->
    <header class="header">
      <a href="{% url 'home' %}" class="logo-area">
        <div class="logo-icon">⚡</div>
        <div class="logo-text">SONICSNAP</div>
      </a>
      <div class="nav-links">
        <a href="#">Converter</a>
        <a href="#">Playlist</a>
        <a href="#">Cloud Sync</a>
      </div>
      <div class="header-actions">
        <button class="btn-icon">⚙</button>
        <button class="btn-pro">Go Pro</button>
      </div>
    </header>

    <!-- Hero -->
    <div class="hero">
      <h1>The <span>Future</span> of Extraction</h1>
      <p>High-fidelity media processing powered by SonicSnap's advanced neural architecture.</p>
    </div>

    <!-- Main Form Panel -->
    <div class="panel" style="display:flex; flex-direction:column; align-items:center;">
      
      <form id="dlForm" style="width: 100%;">
        {% csrf_token %}
        <textarea name="url" id="id_url" style="display:none;"></textarea>
        <input name="mode" id="id_mode" type="hidden" value="single">

        <div style="text-align: center;">
          <div class="mode-toggle">
            <button type="button" class="mode-pill active" id="pill-single" onclick="setMode('single')">Single</button>
            <button type="button" class="mode-pill" id="pill-bulk" onclick="setMode('bulk')">Batch</button>
          </div>
        </div>

        <!-- Single URL input -->
        <div id="single-section" class="input-group">
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
            <input type="url" id="single-url" class="input-field" placeholder="Paste your media URL (YouTube, SoundCloud, Spotify)...">
          </div>
        </div>

        <!-- Bulk input section -->
        <div id="bulk-section" style="display:none;" class="input-group">
          <div class="link-rows" id="link-rows"></div>
          <button type="button" class="btn-add-link" onclick="addLinkRow()">Add another link...</button>
        </div>

        <div class="format-row">
          <div class="select-wrapper">
            <label class="select-label" for="id_file_format">Format</label>
            <select name="file_format" id="id_file_format" class="select-field" onchange="updateQualityOptions()">
              <option value="mp4">MP4 Video (H.264)</option>
              <option value="mp3">MP3 Audio</option>
            </select>
          </div>
          <div class="select-wrapper">
            <label class="select-label" for="id_quality">Quality</label>
            <select name="quality" id="id_quality" class="select-field">
              <!-- JS fills this -->
            </select>
          </div>
        </div>

        <button class="btn-go" id="dlBtn" type="submit">
          INITIATE DOWNLOAD
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        </button>
      </form>
    </div>

    <!-- Live Downloads Tracking -->
    <div id="dlSection" style="display:none; margin-bottom:40px;">
      <div class="section-head">
        <h2>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          Active Tasks (<span id="dlCount">0</span>)
        </h2>
      </div>
      <div id="dlList"></div>
    </div>

    <!-- Recent Activity Section (Server Rendered) -->
    <div>
      <div class="section-head">
        <h2>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>
          Recent Activity
        </h2>
        <a href="{% url 'history' %}" class="clear-link">View Full History</a>
      </div>
      <div>
        {% for item in recent_activity %}
        <div class="card">
          {% if item.thumbnail %}
            <img src="{{ item.thumbnail }}" class="card-thumb" alt="Thumb">
          {% else %}
            <div class="card-thumb-ph">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
            </div>
          {% endif %}
          <div>
            <div class="card-title">{{ item.title }}</div>
            <div class="card-meta">
              <span>{{ item.file_format|upper }} • {% if item.quality != 'default' %}{% if item.file_format == 'mp3' %}{{ item.quality }}kbps{% else %}{{ item.quality }}p{% endif %} • {% endif %}{{ item.created_at|date:"M j" }}</span>
            </div>
          </div>
          <div class="action-group">
            <span class="badge badge-{{ item.status }}">{{ item.status|upper }}</span>
          </div>
        </div>
        {% empty %}
        <div class="empty">No recent activity found.</div>
        {% endfor %}
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px; vertical-align:-2px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        © 2024 SonicSnap Labs. End-to-End Encrypted Transfers.
      </div>
      <div class="footer-links">
        <a href="#">PRIVACY PROTOCOL</a>
        <a href="#">TERMS OF SERVICE</a>
        <a href="#">API ACCESS</a>
      </div>
    </footer>

  </div>

  <script>
    const TERMINAL = new Set(["done", "completed", "cancelled", "error"]);
    const tasks = {};
    let pollTimer = null;
    
    // ── Dynamic Quality Dropdown ────────────────────────────
    function updateQualityOptions() {
      const formatSelect = document.getElementById('id_file_format');
      const qualitySelect = document.getElementById('id_quality');
      if (!formatSelect || !qualitySelect) return;
      qualitySelect.innerHTML = '';
      
      const mp4Options = [
        { value: '2160', text: '4K Ultra HD' },
        { value: '1080', text: '1080p FHD' },
        { value: '720', text: '720p HD' },
        { value: '480', text: '480p SD' }
      ];

      const mp3Options = [
        { value: '320', text: 'Lossless (320kbps)' },
        { value: '256', text: 'High (256kbps)' },
        { value: '192', text: 'Normal (192kbps)' },
        { value: '128', text: 'Low (128kbps)' }
      ];
      
      const options = formatSelect.value === 'mp3' ? mp3Options : mp4Options;
      
      options.forEach(opt => {
        const optionElement = document.createElement('option');
        optionElement.value = opt.value;
        optionElement.textContent = opt.text;
        qualitySelect.appendChild(optionElement);
      });
      // Try to select Normal/1080p by default based on type
      qualitySelect.value = formatSelect.value === 'mp3' ? '320' : '1080';
    }
    
    // Initialize standard options based on default selection 
    document.addEventListener("DOMContentLoaded", () => {
        const formatSelect = document.getElementById('id_file_format');
        if(formatSelect) {
            formatSelect.value = 'mp4'; // Default to mp4 as in design reference
        }
        updateQualityOptions();
    });

    // ── Mode Toggle ─────────────────────────────────────────
    function setMode(mode) {
      document.getElementById("id_mode").value = mode;
      const isBulk = mode === "bulk";
      document.getElementById("single-section").style.display = isBulk ? "none" : "block";
      document.getElementById("bulk-section").style.display = isBulk ? "block" : "none";
      document.getElementById("pill-single").classList.toggle("active", !isBulk);
      document.getElementById("pill-bulk").classList.toggle("active", isBulk);
      if (isBulk && document.querySelectorAll(".link-row").length === 0) {
        addLinkRow(); addLinkRow(); addLinkRow();  // seed with 3 rows
      }
    }

    // ── Bulk link rows ──────────────────────────────────────
    function addLinkRow() {
      const rows = document.getElementById("link-rows");
      const idx = rows.children.length + 1;
      const row = document.createElement("div");
      row.className = "link-row";
      row.innerHTML = `
      <input type="url" class="input-field" placeholder="Media URL ${idx}..." autocomplete="off">
      <button type="button" class="btn-remove" title="Remove" onclick="removeLinkRow(this)">✕</button>`;
      rows.appendChild(row);
      refreshRemoveBtns();
    }

    function removeLinkRow(btn) {
      btn.closest(".link-row").remove();
      refreshRemoveBtns();
    }

    function refreshRemoveBtns() {
      const btns = document.querySelectorAll(".link-row .btn-remove");
      btns.forEach((b, i) => b.style.visibility = (btns.length === 1 && i === 0) ? "hidden" : "visible");
    }

    // ── Form Submit ────────────────────────────────────────────────
    document.getElementById("dlForm").addEventListener("submit", async e => {
      e.preventDefault();
      const btn = document.getElementById("dlBtn");
      const mode = document.getElementById("id_mode").value;

      // Populate the hidden textarea before POSTing
      if (mode === "bulk") {
        const filled = [...document.querySelectorAll(".link-row input[type='url']")]
          .map(i => i.value.trim()).filter(Boolean);
        if (!filled.length) { alert("Please add at least one link."); return; }
        document.getElementById("id_url").value = filled.join("\n");
      } else {
        const v = document.getElementById("single-url").value.trim();
        if (!v) { alert("Please paste a URL."); return; }
        document.getElementById("id_url").value = v;
      }

      btn.disabled = true;
      btn.innerHTML = "PROCESSING...";

      try {
        const res = await fetch("/start/", { method: "POST", body: new FormData(e.target) });
        const data = await res.json();

        if (data.tasks?.length) {
          data.tasks.forEach(id => spawnCard(id, { status: "downloading", percent: "0%", title: "Fetching Media...", thumbnail: "", speed: "", eta: "" }));
          document.getElementById("dlSection").style.display = "block";
          startPolling();
        }
      } catch (err) { console.error(err); }
      finally { 
        btn.disabled = false; 
        btn.innerHTML = `INITIATE DOWNLOAD <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>`; 
      }
    });

    // ── Spawn card once ──────────────────────────────────────
    function spawnCard(id, t) {
      if (tasks[id]) return;

      const list = document.getElementById("dlList");
      const card = document.createElement("div");
      card.className = "card";
      card.id = `c-${id}`;
      card.innerHTML = `
      <div class="card-thumb-ph" id="th-${id}">
         <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
      </div>
      <div>
        <div class="card-title" id="ti-${id}">Fetching Media...</div>
        <div class="card-meta">
          <span id="pc-${id}">0%</span> • <span id="sp-${id}">Evaluating</span>
        </div>
        <div class="prog-track"><div class="prog-fill" id="pf-${id}"></div></div>
      </div>
      <div class="action-group">
        <span class="badge badge-downloading" id="bd-${id}">PROCESSING</span>
        <button class="btn-act-icon" onclick="doPause('${id}')" id="btn-pause-${id}">⏸</button>
        <button class="btn-act-icon" onclick="doCancel('${id}')">✕</button>
      </div>`;

      // Prepend so newest is on top
      list.prepend(card);
      tasks[id] = { done: false };
      patchCard(id, t);
      refreshCount();
    }

    // ── Patch only changed nodes ─────────────────────────────
    function patchCard(id, t) {
      const pct = parseFloat(t.percent) || 0;
      const status = (t.status || "queued").toLowerCase();
      const done = TERMINAL.has(status);
      tasks[id].done = done;

      // Title
      const ti = document.getElementById(`ti-${id}`);
      if (ti && t.title && !["Loading…", "Unknown"].includes(t.title))
        ti.textContent = t.title;

      // Thumbnail
      const th = document.getElementById(`th-${id}`);
      if (th && t.thumbnail && th.tagName !== "IMG") {
        const img = document.createElement("img");
        img.className = "card-thumb";
        img.id = `th-${id}`;
        img.src = t.thumbnail;
        img.alt = "";
        th.replaceWith(img);
      }

      // Bar
      const pf = document.getElementById(`pf-${id}`);
      if (pf) {
        pf.style.width = pct + "%";
        if (status === "done" || status === "completed") {
            pf.style.background = "var(--green)";
            pf.style.boxShadow = "0 0 8px var(--green)";
        } else if (status === "error" || status === "cancelled") {
            pf.style.background = "var(--red)";
            pf.style.boxShadow = "none";
        }
      }

      // Badge
      const bd = document.getElementById(`bd-${id}`);
      if (bd) { 
        bd.textContent = status === 'done' ? 'COMPLETED' : status.toUpperCase(); 
        bd.className = `badge badge-${status}`; 
      }

      // Speed
      const sp = document.getElementById(`sp-${id}`);
      if (sp) sp.textContent = [t.speed, t.eta ? "ETA " + t.eta : ""].filter(Boolean).join(" · ") || "Processing";

      // Pct
      const pc = document.getElementById(`pc-${id}`);
      if (pc) pc.textContent = pct.toFixed(0) + "%";

      // Actions container
      const btnPause = document.getElementById(`btn-pause-${id}`);
      if (btnPause) {
        if (done) {
           btnPause.style.display = 'none';
        } else {
           btnPause.textContent = status === "paused" ? "▶" : "⏸";
        }
      }
      
      const acGrp = document.getElementById(`c-${id}`).querySelector('.action-group');
      if (done && (status === "done" || status === "completed")) {
          // Add download link if not exists
          if (!acGrp.querySelector('a')) {
              const dlAnchor = document.createElement('a');
              dlAnchor.href = `/serve/${id}/`;
              dlAnchor.className = "btn-act-icon";
              dlAnchor.download = true;
              dlAnchor.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>';
              // Replace the X button with Download button
              const xBtn = acGrp.querySelector('button[onclick^="doCancel"]');
              if(xBtn) xBtn.replaceWith(dlAnchor);
          }
      }
    }

    function refreshCount() {
      const ids = Object.keys(tasks);
      document.getElementById("dlCount").textContent = ids.length;
    }

    // ── Polling ──────────────────────────────────────────────
    function startPolling() {
      if (pollTimer) return;
      pollTimer = setInterval(async () => {
        try {
          const data = await (await fetch("/tasks/")).json();
          Object.entries(data).forEach(([id, t]) => {
            if (!tasks[id]) { spawnCard(id, t); }
            else { patchCard(id, t); }
          });
          if (Object.keys(tasks).length && Object.values(tasks).every(t => t.done)) {
            clearInterval(pollTimer); pollTimer = null;
          }
        } catch (e) { console.error(e); }
      }, 1000);
    }

    // ── Controls ─────────────────────────────────────────────
    async function doCancel(id) {
      await fetch(`/cancel/${id}/`);
      patchCard(id, { status: "cancelled", percent: "100%", title: "", thumbnail: "", speed: "", eta: "" });
      if (Object.values(tasks).every(t => t.done)) { clearInterval(pollTimer); pollTimer = null; }
    }

    async function doPause(id) {
      await fetch(`/pause/${id}/`);
      const cur = document.getElementById(`bd-${id}`)?.textContent?.toLowerCase() || "";
      patchCard(id, { status: cur === "paused" ? "downloading" : "paused", percent: document.getElementById(`pc-${id}`)?.textContent || "0%", title: "", thumbnail: "", speed: "", eta: "" });
    }
  </script>
</body>
</html>
"""

with open(template_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Successfully overwrote home.html with the new SonicSnap design!")
