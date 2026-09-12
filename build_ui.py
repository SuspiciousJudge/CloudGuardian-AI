import os
import textwrap

html_content = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CloudGuardian Edge</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    :root {
      --bg: #070d10; --panel: #111a1f; --panel-border: rgba(255,255,255,0.08); 
      --panel-hover: #162228;
      --text: #e2e8f0; --muted: #94a3b8; 
      --green: #10b981; --green-bg: rgba(16, 185, 129, 0.15);
      --red: #ef4444; --red-bg: rgba(239, 68, 68, 0.15);
      --orange: #f59e0b; --orange-bg: rgba(245, 158, 11, 0.15);
      --blue: #3b82f6; --blue-bg: rgba(59, 130, 246, 0.15);
      --purple: #8b5cf6;
      --font: 'Inter', sans-serif;
    }
    * { box-sizing: border-box; }
    body { background: var(--bg); color: var(--text); font-family: var(--font); margin: 0; line-height: 1.5; font-size: 14px; overflow-x: hidden; }
    h1, h2, h3, h4 { margin: 0; font-weight: 600; }
    
    /* Layout */
    .app-container { display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }
    .sidebar { background: #0a1114; border-right: 1px solid var(--panel-border); display: flex; flex-direction: column; }
    .main-content { padding: 32px; max-width: 1600px; margin: 0 auto; width: 100%; display: flex; flex-direction: column; height: 100vh; overflow-y: auto;}
    
    /* Sidebar */
    .brand { padding: 24px; border-bottom: 1px solid var(--panel-border); }
    .brand h2 { font-size: 18px; font-weight: 800; background: linear-gradient(90deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .brand p { font-size: 12px; color: var(--muted); margin: 4px 0 0 0; }
    .nav-links { padding: 16px 8px; flex: 1; }
    .nav-item { padding: 12px 16px; margin-bottom: 4px; border-radius: 8px; cursor: pointer; color: var(--muted); transition: all 0.2s; font-weight: 600; display: flex; justify-content: space-between; align-items: center;}
    .nav-item:hover { background: var(--panel-hover); color: var(--text); }
    .nav-item.active { background: var(--panel-hover); color: var(--text); border-left: 3px solid var(--blue); }
    .nav-item .badge-count { background: var(--panel-border); padding: 2px 6px; border-radius: 4px; font-size: 11px; }
    
    /* Header & Controls */
    .header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px; }
    .page-title h1 { font-size: 28px; font-weight: 800; margin-bottom: 8px; }
    .status-bar { display: flex; gap: 12px; font-size: 12px; }
    .status-badge { background: rgba(0,0,0,0.3); border: 1px solid var(--panel-border); padding: 6px 12px; border-radius: 100px; display: flex; align-items: center; gap: 8px; font-weight: 600; }
    
    /* Blinking dot */
    .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    .dot.live { background: var(--green); box-shadow: 0 0 8px var(--green); animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    
    /* Buttons */
    .btn { background: var(--panel); border: 1px solid var(--panel-border); color: var(--text); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; }
    .btn:hover { background: var(--panel-hover); border-color: rgba(255,255,255,0.2); }
    .btn.primary { background: var(--blue); border-color: var(--blue); color: #fff; }
    .btn.primary:hover { background: #2563eb; }
    .btn.danger { background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.4); color: var(--red); }
    .btn.danger:hover { background: rgba(239, 68, 68, 0.2); }
    
    /* Demo Controls Bar */
    .demo-bar { background: linear-gradient(90deg, rgba(17,26,31,1) 0%, rgba(20,35,46,1) 100%); border: 1px solid var(--blue-bg); padding: 16px; border-radius: 12px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }
    .demo-info { line-height: 1.4; }
    .demo-controls { display: flex; gap: 12px; }
    .demo-controls select { background: #000; border: 1px solid var(--panel-border); color: #fff; padding: 8px; border-radius: 6px; outline: none; }
    
    /* Cards & Panels */
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .card { background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px; padding: 20px; transition: transform 0.2s; }
    .card:hover { border-color: rgba(255,255,255,0.15); }
    .card-label { color: var(--muted); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
    .card-value { font-size: 32px; font-weight: 800; display: flex; align-items: baseline; gap: 8px;}
    .card-trend { font-size: 14px; font-weight: 600; padding: 4px 8px; border-radius: 4px; }
    .card-trend.up { background: var(--red-bg); color: var(--red); }
    .card-trend.success { background: var(--green-bg); color: var(--green); }
    
    .panel { background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px; overflow: hidden; margin-bottom: 24px; }
    .panel-header { padding: 16px 20px; border-bottom: 1px solid var(--panel-border); display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2);}
    .panel-body { padding: 20px; }
    
    /* Tables */
    table { width: 100%; border-collapse: collapse; text-align: left; }
    th { color: var(--muted); font-size: 12px; font-weight: 600; text-transform: uppercase; padding: 12px 16px; border-bottom: 1px solid var(--panel-border); }
    td { padding: 16px; border-bottom: 1px solid var(--panel-border); font-size: 14px; }
    tr:last-child td { border-bottom: none; }
    tr { transition: background 0.15s; }
    tr:hover { background: rgba(255,255,255,0.02); }
    
    /* Badges */
    .badge { padding: 4px 10px; border-radius: 100px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid transparent; }
    .badge.HEALTHY { background: var(--green-bg); color: var(--green); border-color: rgba(16, 185, 129, 0.3); }
    .badge.CRITICAL { background: var(--red-bg); color: var(--red); border-color: rgba(239, 68, 68, 0.3); box-shadow: 0 0 10px rgba(239, 68, 68, 0.2); animation: pulse-red 2s infinite;}
    .badge.HIGH { background: var(--orange-bg); color: var(--orange); border-color: rgba(245, 158, 11, 0.3); }
    .badge.DEGRADED { background: var(--orange-bg); color: var(--orange); }
    .badge.INVESTIGATING { background: var(--blue-bg); color: var(--blue); }
    .badge.MITIGATED { background: var(--purple); color: #fff; opacity: 0.8; }
    .badge.RESOLVED { background: var(--green-bg); color: var(--green); }
    .badge.INFO { background: rgba(255,255,255,0.1); color: var(--muted); }
    .badge.WARN { background: var(--orange-bg); color: var(--orange); }
    .badge.ERROR { background: var(--red-bg); color: var(--red); }
    
    @keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }

    /* Views */
    .view-section { display: none; animation: fadeIn 0.3s ease-out; }
    .view-section.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
    
    /* Live Charts Area */
    .charts-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
    .mini-chart { background: rgba(0,0,0,0.2); border: 1px solid var(--panel-border); border-radius: 8px; padding: 12px; }
    .mini-chart-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
    .mini-chart-bars { display: flex; align-items: flex-end; height: 60px; gap: 2px; }
    .bar { flex: 1; background: var(--blue); opacity: 0.6; min-width: 3px; border-radius: 2px 2px 0 0; transition: height 0.3s ease; }
    .bar:last-child { opacity: 1; background: var(--green); }
    .bar.warn { background: var(--orange) !important; }
    .bar.crit { background: var(--red) !important; }

    /* Multi-line Live Logs */
    .log-stream { background: #000; font-family: 'Consolas', monospace; font-size: 13px; padding: 16px; border-radius: 8px; height: 350px; overflow-y: auto; border: 1px solid var(--panel-border); }
    .log-line { margin: 4px 0; display: flex; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }
    .log-time { color: var(--muted); white-space: nowrap; }
    .log-svc { color: #facc15; min-width: 150px; }
    .log-msg { color: #e2e8f0; word-break: break-all;}
    .log-line.error .log-msg { color: var(--red); }
    .log-line.warn .log-msg { color: var(--orange); }

    /* Incident Detail Split */
    .incident-split { display: grid; grid-template-columns: 3fr 2fr; gap: 24px; }
    
    /* Code / Markdown block */
    .md-block { background: rgba(0,0,0,0.3); padding: 16px; border-radius: 8px; font-family: monospace; color: var(--green); white-space: pre-wrap; line-height: 1.6;}
    
    /* Root Cause Analysis view */
    .rca-box { border-left: 4px solid var(--purple); padding: 16px 20px; background: rgba(139, 92, 246, 0.05); margin: 16px 0; border-radius: 0 8px 8px 0; }
    .rca-title { color: var(--purple); font-weight: 800; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px; }

    /* Timeline */
    .timeline { list-style: none; padding: 0; margin: 0; position: relative; }
    .timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: var(--panel-border); }
    .timeline li { position: relative; padding-left: 24px; margin-bottom: 16px; }
    .timeline li::before { content: ''; position: absolute; left: 3px; top: 4px; width: 10px; height: 10px; background: var(--panel); border: 2px solid var(--blue); border-radius: 50%; }
    .timeline li:last-child { margin-bottom: 0; }
    .timeline li:last-child::before { border-color: var(--green); background: var(--green); box-shadow: 0 0 10px var(--green); }
    .time-time { font-size: 11px; color: var(--muted); margin-bottom: 2px; }

  </style>
</head>
<body>

<div class="app-container">
  <aside class="sidebar">
    <div class="brand">
      <h2>CloudGuardian Edge</h2>
      <p>Detect. Diagnose. Respond.</p>
    </div>
    <div class="nav-links">
      <div class="nav-item active" data-view="overview">Overview</div>
      <div class="nav-item" data-view="incidents">Incidents <span class="badge-count" id="nav-inc-count">0</span></div>
      <div class="nav-item" data-view="services">Services</div>
      <div class="nav-item" data-view="logs">Live Logs</div>
      <div class="nav-item" data-view="model">Model Performance</div>
      <div class="nav-item" data-view="docs">Architecture</div>
    </div>
  </aside>

  <main class="main-content">
    
    <div class="demo-bar" id="demo-bar">
      <div class="demo-info">
        <strong><span class="dot live"></span> LIVE SIMULATION ENGINE</strong><br>
        <span style="color:var(--muted); font-size:12px;">Local Demo Mode • Qualcomm Snapdragon AI Lab Challenge</span>
      </div>
      <div class="demo-controls">
        <select id="scenario-selector">
          <option value="database_pool">Database Connection Pool Exhaustion</option>
          <option value="payment_latency">Payment API Latency Spike</option>
          <option value="auth_failures">Authentication Failure Spike</option>
          <option value="memory_leak">Memory Leak</option>
          <option value="crash_loop">Container Crash Loop</option>
          <option value="cpu_saturation">CPU Saturation</option>
          <option value="cache_failure">Redis/Cache Failure</option>
          <option value="network_timeout">Network Timeout Cascade</option>
        </select>
        <button class="btn primary" id="btn-start-incident">Start Incident</button>
        <button class="btn" id="btn-reset">Reset Environment</button>
      </div>
    </div>

    <header class="header">
      <div class="page-title">
        <h1 id="page-title-text">System Overview</h1>
        <div class="status-bar">
          <div class="status-badge"><span class="dot live"></span> <span id="status-text">OPERATIONAL</span></div>
          <div class="status-badge" style="background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3); color: var(--green);">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            PRIVACY FIRST · LOCAL AI
          </div>
        </div>
      </div>
    </header>

    <!-- OVERVIEW VIEW -->
    <div id="view-overview" class="view-section active">
      <div class="grid-4" id="overview-cards">
        <!-- Rendered via JS -->
      </div>
      
      <div class="panel">
        <div class="panel-header">
          <h3>Live Telemetry Feed</h3>
          <span class="badge INFO">Updated <span id="last-update-time">just now</span></span>
        </div>
        <div class="panel-body charts-grid" id="main-charts">
          <!-- Rendered via JS -->
        </div>
      </div>

      <div class="incident-split">
        <div class="panel">
          <div class="panel-header">
            <h3>Recent Incidents</h3>
            <button class="btn" onclick="switchView('incidents')">View All</button>
          </div>
          <div class="panel-body" style="padding:0;">
            <table id="recent-incidents-table">
               <!-- Rendered via JS -->
            </table>
          </div>
        </div>
        
        <div class="panel">
          <div class="panel-header">
            <h3>System Logs</h3>
          </div>
          <div class="panel-body">
            <div class="log-stream" id="mini-log-stream">
               <!-- Rendered via JS -->
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- INCIDENTS VIEW -->
    <div id="view-incidents" class="view-section">
      <div class="panel" id="incident-list-panel">
        <div class="panel-header">
          <h3>Incident History</h3>
        </div>
        <div class="panel-body" style="padding:0;">
          <table id="all-incidents-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Severity</th>
                <th>Title</th>
                <th>Affected Service</th>
                <th>Status</th>
                <th>AI Confidence</th>
                <th>Detected</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

      <!-- Detail View (Hidden by default, shown when incident clicked) -->
      <div id="incident-detail-panel" style="display:none;">
        <button class="btn" style="margin-bottom: 16px;" onclick="closeIncidentDetail()">← Back to Incidents</button>
        
        <div class="panel" style="border-color: rgba(239, 68, 68, 0.4);">
          <div class="panel-header" style="background: rgba(239, 68, 68, 0.05);">
            <h2 id="det-title" style="color:var(--text);">Title</h2>
            <div style="display:flex; gap: 8px;">
               <span id="det-sev" class="badge"></span>
               <span id="det-status" class="badge"></span>
            </div>
          </div>
          <div class="panel-body incident-split">
            
            <!-- Left col: Analysis & Remediation -->
            <div>
              <h3>AI Root Cause Analysis</h3>
              <div id="det-ai-content">
                 <button class="btn primary" id="btn-run-ai" style="margin-top: 16px; padding: 12px 24px; font-size: 16px; width: 100%;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:bottom; margin-right:8px;"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                    Run Local AI Analysis
                 </button>
              </div>

              <div id="det-remediation" style="margin-top: 32px; display:none;">
                 <h3>Recommended Remediation</h3>
                 <div id="det-rem-list" style="margin-top: 16px; display:flex; flex-direction:column; gap:12px;"></div>
                 <button class="btn primary" id="btn-execute-rem" style="margin-top: 16px; width:100%; background: var(--orange); border-color: var(--orange);">
                    Execute Simulated Remediation
                 </button>
              </div>
            </div>

            <!-- Right col: Information -->
            <div>
               <div style="background: #000; padding:16px; border-radius:8px; border:1px solid var(--panel-border); margin-bottom: 16px;">
                  <div style="margin-bottom:12px;"><span style="color:var(--muted)">Service:</span> <strong id="det-svc"></strong></div>
                  <div style="margin-bottom:12px;"><span style="color:var(--muted)">Summary:</span> <span id="det-summary"></span></div>
                  <div><span style="color:var(--muted)">Detected:</span> <span id="det-time"></span></div>
               </div>

               <h3>Incident Timeline</h3>
               <div style="background: var(--bg); padding:16px; border-radius:8px; border:1px solid var(--panel-border); margin-top:16px;">
                  <ul class="timeline" id="det-timeline"></ul>
               </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    
    <!-- SERVICES VIEW -->
    <div id="view-services" class="view-section">
      <div class="panel">
        <div class="panel-header">
          <h3>Enterprise Services</h3>
        </div>
        <div class="panel-body" style="padding:0;">
          <table id="services-table">
            <thead>
              <tr>
                <th>Service</th>
                <th>Status</th>
                <th>CPU</th>
                <th>Memory</th>
                <th>Latency</th>
                <th>Error Rate</th>
                <th>Req/Sec</th>
                <th>Uptime</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- LOGS VIEW -->
    <div id="view-logs" class="view-section">
      <div class="panel">
        <div class="panel-header">
          <h3>Live Log Stream</h3>
        </div>
        <div class="panel-body">
           <div class="log-stream" id="full-log-stream" style="height: 600px;"></div>
        </div>
      </div>
    </div>

    <!-- MODEL VIEW -->
    <div id="view-model" class="view-section">
      <div class="panel">
        <div class="panel-header">
          <h3>Local AI Performance Benchmark</h3>
          <button class="btn primary" id="btn-run-bench">Run Benchmark Series</button>
        </div>
        <div class="panel-body">
          <div class="grid-4" id="bench-cards">
            <!-- Rendered by JS -->
          </div>
          
          <div class="incident-split" style="margin-top: 32px;">
            <div class="card" style="box-shadow: inset 0 0 20px rgba(16,185,129,0.05); border-color: rgba(16,185,129,0.2);">
              <h3 style="color:var(--green); margin-bottom: 16px;">CloudGuardian Edge (Local Processing)</h3>
              <p style="margin-bottom: 8px;"><strong>Data Privacy:</strong> Absolute (Data never leaves localhost)</p>
              <p style="margin-bottom: 8px;"><strong>Network Dependency:</strong> None (Works offline)</p>
              <p style="margin-bottom: 8px;"><strong>Inference Cost:</strong> $0.00 / Request</p>
              <p style="margin-bottom: 8px;"><strong>Target Architecture:</strong> Qualcomm Snapdragon AI Engine (NPU)</p>
            </div>
            <div class="card" style="opacity: 0.7;">
              <h3 style="margin-bottom: 16px;">Cloud-based Alternatives</h3>
              <p style="margin-bottom: 8px;"><strong>Data Privacy:</strong> Requires sending sensitive logs over internet</p>
              <p style="margin-bottom: 8px;"><strong>Network Dependency:</strong> Requires highly-available internet</p>
              <p style="margin-bottom: 8px;"><strong>Inference Cost:</strong> Cloud token billing applies</p>
              <p style="margin-bottom: 8px;"><strong>Target Architecture:</strong> Cloud GPU Farms</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- DOCS VIEW -->
    <div id="view-docs" class="view-section">
      <div class="panel">
        <div class="panel-header">
          <h3>Platform Architecture</h3>
        </div>
        <div class="panel-body md-block">
# CloudGuardian Edge
A privacy-preserving, on-device AI incident response platform.

## Key Features
1. Wait-Free Telemetry: Live data ingestion scaling from edge gateways.
2. Anomaly Detection: Deterministic local rules engine flagging anomalies in ms.
3. Edge AI Processing: Zero-telemetry-exfiltration root cause analysis using local models.
4. Auto-Remediation: Autonomous orchestration for self-healing infrastructure.

## Snapdragon Target
Designed to eventually leverage the Qualcomm Snapdragon AI Hub. 
By pulling models natively optimized for Snapdragon NPUs, the edge agent can perform 
LLM-based root-cause-analysis directly on edge nodes with minimal power utilization 
and zero cloud latency.
        </div>
      </div>
    </div>

  </main>
</div>

<script>
// ---------- State ----------
let state = {
  currentView: 'overview',
  simulation: {},
  cards: {},
  services: [],
  incidents: [],
  activity: [],
  logs: [],
  metrics: [],
  history: {}, // serviceId -> metric keys -> arrays of values
  benchmark: null
};

let selectedIncidentId = null;

// ---------- Routing ----------
document.querySelectorAll('.nav-item').forEach(el => {
  el.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
    
    document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
    document.getElementById('view-' + el.dataset.view).classList.add('active');
    
    document.getElementById('page-title-text').innerText = el.innerText.replace(/[0-9]/g, '').trim();
    
    if (el.dataset.view === 'incidents') {
      document.getElementById('incident-list-panel').style.display = 'block';
      document.getElementById('incident-detail-panel').style.display = 'none';
      selectedIncidentId = null;
    }
  });
});

function switchView(viewName) {
  document.querySelector(`.nav-item[data-view="${viewName}"]`).click();
}

function closeIncidentDetail() {
  document.getElementById('incident-list-panel').style.display = 'block';
  document.getElementById('incident-detail-panel').style.display = 'none';
  selectedIncidentId = null;
}

// ---------- UI Renderers ----------
function getBadge(status) {
   let b = status.toUpperCase();
   return `<span class="badge ${b}">${b}</span>`;
}

function processHistory(metrics) {
  // Keep last 40 data points per metric per service
  state.history = {};
  metrics.forEach(m => {
    const sId = m.serviceId;
    if (!state.history[sId]) state.history[sId] = { cpu: [], memory: [], latency: [], errorRate: [], req: [] };
    state.history[sId].cpu.push(m.cpu);
    state.history[sId].memory.push(m.memory);
    state.history[sId].latency.push(m.latency);
    state.history[sId].errorRate.push(m.errorRate);
    state.history[sId].req.push(m.requestsPerSec);
  });
}

function renderMiniBarChart(values, thresholdWarn, thresholdCrit) {
   if (!values || values.length === 0) return '';
   // sample down to 20 bars
   const step = Math.max(1, Math.floor(values.length / 20));
   const sampled = values.filter((_, i) => i % step === 0).slice(-20);
   
   let max = Math.max(...sampled, thresholdCrit * 1.2, 10);
   
   return sampled.map(v => {
      let cls = 'bar';
      if (v >= thresholdCrit) cls += ' crit';
      else if (v >= thresholdWarn) cls += ' warn';
      let h = Math.max(2, (v / max) * 100);
      return `<div class="${cls}" style="height: ${h}%" title="${v}"></div>`;
   }).join('');
}

function renderOverview() {
  // Cards
  document.getElementById('overview-cards').innerHTML = `
    <div class="card">
      <div class="card-label">Healthy Services</div>
      <div class="card-value">${state.cards.healthyServices || 0} <span style="font-size:16px; color:var(--muted); margin-left:auto;">/ ${state.cards.totalServices || 0}</span></div>
    </div>
    <div class="card">
      <div class="card-label">Active Incidents</div>
      <div class="card-value">${state.cards.activeIncidents || 0}</div>
    </div>
    <div class="card">
      <div class="card-label">Critical Incidents</div>
      <div class="card-value" style="color:var(--red);">${state.cards.criticalIncidents || 0}</div>
    </div>
    <div class="card">
      <div class="card-label">System State</div>
      <div class="card-value" style="font-size: 24px; color: ${state.simulation.state === 'HEALTHY' ? 'var(--green)' : 'var(--red)'}">${state.simulation.state}</div>
    </div>
  `;

  document.getElementById('status-text').innerText = state.simulation.state === 'HEALTHY' ? 'OPERATIONAL' : 'DEGRADED / INCIDENT';
  document.getElementById('nav-inc-count').innerText = state.incidents.filter(i => i.status === 'ACTIVE' || i.status === 'INVESTIGATING').length;

  // Charts (using global metrics if available, or aggregating)
  const glob = state.history['global'] || state.history['svc-4'] || { cpu:[], memory:[], latency:[], errorRate:[], req:[] };
  const getLatest = (arr) => arr && arr.length ? arr[arr.length-1] : 0;
  
  document.getElementById('main-charts').innerHTML = `
    <div class="mini-chart">
       <div class="mini-chart-header"><span>CPU Usage</span><strong>${getLatest(glob.cpu)}%</strong></div>
       <div class="mini-chart-bars">${renderMiniBarChart(glob.cpu, 75, 90)}</div>
    </div>
    <div class="mini-chart">
       <div class="mini-chart-header"><span>Memory</span><strong>${getLatest(glob.memory)}%</strong></div>
       <div class="mini-chart-bars">${renderMiniBarChart(glob.memory, 80, 90)}</div>
    </div>
    <div class="mini-chart">
       <div class="mini-chart-header"><span>P99 Latency</span><strong>${getLatest(glob.latency)}ms</strong></div>
       <div class="mini-chart-bars">${renderMiniBarChart(glob.latency, 300, 800)}</div>
    </div>
    <div class="mini-chart">
       <div class="mini-chart-header"><span>Error Rate</span><strong>${getLatest(glob.errorRate)}%</strong></div>
       <div class="mini-chart-bars">${renderMiniBarChart(glob.errorRate, 2, 5)}</div>
    </div>
    <div class="mini-chart">
       <div class="mini-chart-header"><span>Requests/sec</span><strong>${getLatest(glob.req)}</strong></div>
       <div class="mini-chart-bars">${renderMiniBarChart(glob.req, 99999, 99999)}</div>
    </div>
  `;

  // Recent Incidents
  const recentIncs = state.incidents.slice(0, 5);
  document.getElementById('recent-incidents-table').innerHTML = recentIncs.map(i => `
    <tr style="cursor:pointer;" onclick="openIncident('${i.id}')">
      <td>${getBadge(i.severity)}</td>
      <td><strong>${i.title}</strong></td>
      <td style="color:var(--muted);">${i.service}</td>
      <td style="text-align:right;">${getBadge(i.status)}</td>
    </tr>
  `).join('') || `<tr><td colspan="4" style="text-align:center; color:var(--muted)">No incidents recorded.</td></tr>`;

  // Mini Logs
  const logRenderer = l => {
     let c = 'info';
     if (l.level === 'ERROR' || l.level === 'CRITICAL') c = 'error';
     if (l.level === 'WARN') c = 'warn';
     let time = new Date(l.timestamp).toLocaleTimeString();
     return `<div class="log-line ${c}"><span class="log-time">[${time}]</span><span class="log-svc">${l.service}</span><span class="log-msg">${l.message}</span></div>`;
  };
  
  document.getElementById('mini-log-stream').innerHTML = state.logs.slice(-20).map(logRenderer).join('');
  document.getElementById('full-log-stream').innerHTML = state.logs.slice(-100).map(logRenderer).join('');
  
  // Auto scroll logs
  let ml = document.getElementById('mini-log-stream');
  let fl = document.getElementById('full-log-stream');
  ml.scrollTop = ml.scrollHeight;
  fl.scrollTop = fl.scrollHeight;
}

function renderServices() {
  document.getElementById('services-table').querySelector('tbody').innerHTML = state.services.map(s => `
    <tr>
      <td><strong>${s.name}</strong></td>
      <td>${getBadge(s.status)}</td>
      <td>${s.cpu}%</td>
      <td>${s.memory}%</td>
      <td>${s.latency}ms</td>
      <td>${s.errorRate}%</td>
      <td>${s.requestsPerSec}</td>
      <td style="color:var(--muted);">${s.uptime}%</td>
    </tr>
  `).join('');
}

function renderIncidents() {
  document.getElementById('all-incidents-table').querySelector('tbody').innerHTML = state.incidents.map(i => `
    <tr>
      <td style="color:var(--muted); font-family:monospace;">${i.id.split('-')[1] || i.id}</td>
      <td>${getBadge(i.severity)}</td>
      <td><strong>${i.title}</strong></td>
      <td>${i.service}</td>
      <td>${getBadge(i.status)}</td>
      <td>${i.aiConfidence ? i.aiConfidence+'%' : '<span style="color:var(--muted)">Pending</span>'}</td>
      <td style="color:var(--muted);">${new Date(i.detectedAt).toLocaleTimeString()}</td>
      <td><button class="btn" onclick="openIncident('${i.id}')">Inspect</button></td>
    </tr>
  `).join('');
}

function renderBenchmark() {
   if (!state.benchmark || !state.benchmark.runs) {
      document.getElementById('bench-cards').innerHTML = `<div style="grid-column: span 4; color:var(--muted)">Run benchmark to see metrics.</div>`;
      return;
   }
   
   let b = state.benchmark;
   document.getElementById('bench-cards').innerHTML = `
    <div class="card">
      <div class="card-label">Average Latency</div>
      <div class="card-value">${b.averageLatencyMs} <span style="font-size:16px; color:var(--muted); margin-left:8px;">ms</span></div>
    </div>
    <div class="card">
      <div class="card-label">Min Latency</div>
      <div class="card-value">${b.minimumLatencyMs} <span style="font-size:16px; color:var(--muted); margin-left:8px;">ms</span></div>
    </div>
    <div class="card">
      <div class="card-label">Max Latency</div>
      <div class="card-value">${b.maximumLatencyMs} <span style="font-size:16px; color:var(--muted); margin-left:8px;">ms</span></div>
    </div>
    <div class="card">
      <div class="card-label">Throughput</div>
      <div class="card-value">${b.throughputPerSecond} <span style="font-size:16px; color:var(--muted); margin-left:8px;">req/s</span></div>
    </div>
   `;
}

// ---------- Actions & Modals ----------
async function openIncident(id) {
  selectedIncidentId = id;
  document.getElementById('incident-list-panel').style.display = 'none';
  document.getElementById('incident-detail-panel').style.display = 'block';
  
  if (state.currentView !== 'incidents') switchView('incidents');
  
  // Fetch detailed incident sync
  try {
     const res = await fetch(`/api/incidents/${id}`);
     const inc = await res.json();
     
     document.getElementById('det-title').innerText = inc.title;
     document.getElementById('det-sev').innerHTML = getBadge(inc.severity);
     document.getElementById('det-status').innerHTML = getBadge(inc.status);
     document.getElementById('det-svc').innerText = inc.service;
     document.getElementById('det-summary').innerText = inc.summary;
     document.getElementById('det-time').innerText = new Date(inc.detectedAt).toLocaleString();
     
     document.getElementById('det-timeline').innerHTML = (inc.timeline || []).map(t => {
        let parts = t.split(' ');
        let time = parts[0].includes('T') ? new Date(parts[0]).toLocaleTimeString() : parts[0];
        let msg = parts.slice(1).join(' ');
        if (!msg) { msg = time; time = ''; }
        return `<li><div class="time-time">${time}</div><div>${msg}</div></li>`;
     }).join('');

     const aiContainer = document.getElementById('det-ai-content');
     const remContainer = document.getElementById('det-remediation');
     
     // Render AI Box if analyzed
     if (inc.analysis) {
        aiContainer.innerHTML = `
           <div class="rca-box">
              <div class="rca-title">Root Cause Identified</div>
              <p style="font-size:16px; font-weight:600; margin-bottom:12px;">${inc.analysis.rootCause}</p>
              
              <div class="rca-title" style="margin-top:16px;">Telemetry Evidence (Confidence: ${inc.analysis.confidence}%)</div>
              <ul style="margin:8px 0 0 -5px;">
                 ${inc.analysis.evidence.map(e => `<li>${e}</li>`).join('')}
              </ul>
           </div>
        `;
        
        remContainer.style.display = 'block';
        document.getElementById('det-rem-list').innerHTML = (inc.remediations || []).map(r => `
           <div style="background:rgba(255,255,255,0.05); padding:12px; border:1px solid var(--panel-border); border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
              <div>
                 <strong>${r.action}</strong>
                 <div style="font-size:12px; color:var(--muted); margin-top:4px;">Risk: ${r.risk} | Impact: ${r.expectedImpact}</div>
              </div>
              ${getBadge(r.status)}
           </div>
        `).join('');
        
     } else {
        aiContainer.innerHTML = `
           <button class="btn primary" id="btn-run-ai" style="margin-top: 16px; padding: 12px 24px; font-size: 16px; width: 100%;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:bottom; margin-right:8px;"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              Run Local AI Analysis
           </button>
        `;
        remContainer.style.display = 'none';
        
        document.getElementById('btn-run-ai').onclick = async () => {
           document.getElementById('btn-run-ai').innerText = 'Analyzing local telemetry...';
           await fetch(`/api/incidents/${id}/analyze`, {method: 'POST'});
           openIncident(id); // reload
        };
     }
     
     // Rem execution
     if (inc.remediations && inc.remediations.length > 0) {
        document.getElementById('btn-execute-rem').onclick = async () => {
           document.getElementById('btn-execute-rem').innerText = 'Executing Remediation...';
           await fetch(`/api/remediations/${inc.remediations[0].id}/execute`, {method: 'POST'});
           // Wait a second and close, simulation handles the rest via tick
           setTimeout(() => {
               closeIncidentDetail();
           }, 1500);
        };
     }
     
  } catch (e) {
     console.error(e);
  }
}

// ---------- API Bindings ----------
document.getElementById('btn-start-incident').onclick = async () => {
  const sc = document.getElementById('scenario-selector').value;
  await fetch('/api/simulation/start', {
     method: 'POST', 
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({scenario: sc})
  });
};

document.getElementById('btn-reset').onclick = async () => {
  await fetch('/api/demo/reset', {method: 'POST'});
  closeIncidentDetail();
};

document.getElementById('btn-run-bench').onclick = async () => {
  const btn = document.getElementById('btn-run-bench');
  btn.innerText = 'Running Inference Benchmark...';
  try {
     const res = await fetch('/api/model/benchmark', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({runs: 12})
     });
     state.benchmark = await res.json();
     renderBenchmark();
  } finally {
     btn.innerText = 'Run Benchmark Series';
  }
};

// ---------- SSE Connection ----------
function connectSSE() {
  const src = new EventSource('/api/stream');
  src.onmessage = (e) => {
     try {
        const data = JSON.parse(e.data);
        
        // Update State
        state.simulation = data.simulation || {};
        state.cards = data.cards || {};
        state.services = data.services || [];
        state.incidents = data.incidents || [];
        state.activity = data.activity || [];
        if (data.logs_recent) { // append new logs
           let seen = new Set(state.logs.map(l=>l.id));
           data.logs_recent.forEach(l => {
              if(!seen.has(l.id)) state.logs.push(l);
           });
           if (state.logs.length > 200) state.logs = state.logs.slice(-200);
        }
        if (data.metrics) processHistory(data.metrics);
        if (data.perf) state.benchmark = data.perf;
        
        // Re-render components
        renderOverview();
        renderServices();
        renderIncidents();
        
        // Details view auto-updates via active polling not needed, but we can update status
        if (selectedIncidentId) {
           let updated = state.incidents.find(i => i.id === selectedIncidentId);
           if (updated) {
              document.getElementById('det-status').innerHTML = getBadge(updated.status);
           }
        }

     } catch(err) {
        console.error("SSE Parse block:", err);
     }
  };
  src.onerror = () => {
     console.error("SSE Lost connection.");
  };
}

// Startup
connectSSE();

</script>
</body>
</html>"""

with open("app/ui/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html successfully with {len(html_content)} bytes.")
