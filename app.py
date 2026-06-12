import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION & THEME HOST ---
st.set_page_config(
    page_title="Termodinámica y Plegamiento de Proteínas: Modelo de Gō",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyectar estilos CSS para ocultar completamente la barra lateral, cabeceras,
# pies de página y paddings nativos de Streamlit, logrando un fundido 100% nativo.
st.markdown("""
    <style>
    /* Ocultar barra de menú y herramientas nativas de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    data-testid="stHeader" {display: none;}
    
    /* Forzar al contenedor principal a ocupar todo el ancho sin márgenes */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        background-color: #0b0f19;
    }
    
    iframe {
        border: none !important;
    }
    
    body {
        background-color: #0b0f19;
    }
    </style>
""", unsafe_allow_html=True)

# --- SINGLE PAGE APPLICATION (SPA) TEMPLATE ---
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Plegamiento de Proteínas: Modelo de Gō en Red 3D</title>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* --- ESTILOS DE DISEÑO Y GLASSMORPHISM (DARK THEME) --- */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: #0b0f19;
            color: #f8fafc;
            overflow-x: hidden;
            overflow-y: hidden;
            min-height: 100vh;
            height: auto;
            padding: 16px;
        }

        /* Estilización de Scrollbars */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #334155; }

        .dashboard-wrapper {
            display: flex;
            flex-direction: column;
            gap: 16px;
            max-width: 1600px;
            margin: 0 auto;
            height: 100%;
        }

        .app-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 12px;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .dna-icon {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            padding: 8px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .title-container h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }

        .title-container .subtitle {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 1px;
        }

        .academic-badge {
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.2);
            color: #38bdf8;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 16px;
            flex-grow: 1;
        }

        .sidebar-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        }

        .sidebar-card h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: #f8fafc;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 8px;
        }

        .section-desc { font-size: 0.78rem; color: #94a3b8; line-height: 1.4; }
        .control-group { display: flex; flex-direction: column; gap: 6px; }
        .control-label-row { display: flex; justify-content: space-between; align-items: center; }
        .control-label-row label { font-size: 0.82rem; font-weight: 500; color: #cbd5e1; }
        .slider-badge { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border-radius: 6px; padding: 2px 6px; font-size: 0.78rem; font-family: monospace; font-weight: bold; }
        .control-help { font-size: 0.72rem; color: #64748b; line-height: 1.3; }

        input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; margin: 6px 0; }
        input[type=range]:focus { outline: none; }
        input[type=range]::-webkit-slider-runnable-track { width: 100%; height: 6px; cursor: pointer; background: #1e293b; border-radius: 3px; border: 1px solid rgba(255, 255, 255, 0.05); }
        input[type=range]::-webkit-slider-thumb { height: 16px; width: 16px; border-radius: 50%; background: #38bdf8; cursor: pointer; -webkit-appearance: none; margin-top: -5px; box-shadow: 0 0 8px #38bdf8; transition: transform 0.1s, background-color 0.1s; }
        input[type=range]::-webkit-slider-thumb:hover { transform: scale(1.2); background: #0ea5e9; }

        .state-card { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 14px; margin-top: auto; display: flex; flex-direction: column; gap: 8px; }
        .state-title { font-size: 0.75rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.02em; }
        .state-badge { display: inline-flex; align-items: center; justify-content: center; padding: 6px 12px; border-radius: 8px; font-weight: 600; font-size: 0.8rem; text-align: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); transition: all 0.3s; }
        
        .badge-vitreo { background-color: rgba(239, 68, 68, 0.12); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); box-shadow: 0 0 10px rgba(239, 68, 68, 0.15); animation: pulse-red 2s infinite; }
        .badge-plegando { background-color: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 0 10px rgba(16, 185, 129, 0.15); animation: pulse-green 2s infinite; }
        .badge-desplegado { background-color: rgba(148, 163, 184, 0.12); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }

        @keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
        @keyframes pulse-green { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
        .state-desc { font-size: 0.72rem; color: #cbd5e1; line-height: 1.35; }

        .main-content { display: flex; flex-direction: column; gap: 16px; }
        .panel-card { background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); display: flex; flex-direction: column; }
        .panel-card h3 { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }

        .top-row { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 16px; height: 360px; }
        .cv-panel { height: 100%; }
        .cv-layout { display: flex; gap: 16px; align-items: center; width: 100%; height: 280px; }
        #plotCv { flex: 2.3; height: 100%; }
        .metrics-panel { height: 100%; justify-content: space-between; }
        .metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; flex-grow: 1; margin-bottom: 12px; }
        .metric-box { background: rgba(30, 41, 59, 0.35); border: 1px solid rgba(255, 255, 255, 0.03); border-radius: 10px; padding: 8px 12px; display: flex; flex-direction: column; justify-content: center; }
        .m-label { font-size: 0.65rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 2px; }
        .m-value { font-size: 1.1rem; font-weight: 700; color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.25); font-family: monospace; }

        .btn-group { display: flex; gap: 8px; align-items: center; width: 100%; }
        button, select { padding: 8px 12px; font-size: 0.78rem; font-weight: 600; font-family: 'Inter', sans-serif; border-radius: 8px; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center; gap: 5px; }
        button.btn-primary { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25); flex-grow: 1.3; }
        button.btn-primary:hover { background: linear-gradient(135deg, #3b82f6, #2563eb); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); transform: translateY(-1px); }
        button.btn-secondary { background-color: rgba(30, 41, 59, 0.6); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.08); flex-grow: 1; }
        button.btn-secondary:hover { background-color: rgba(51, 65, 85, 0.8); color: #ffffff; border-color: rgba(255, 255, 255, 0.15); }
        select { background-color: rgba(15, 23, 42, 0.8); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.08); padding-right: 18px; cursor: pointer; }
        select:hover { border-color: rgba(255, 255, 255, 0.15); background-color: rgba(30, 41, 59, 0.8); }

        .simulation-row { display: grid; grid-template-columns: 1fr 1.1fr; gap: 16px; height: 420px; }
        .sim-2d-panel { height: 100%; }
        #plotChain3d { width: 100%; height: 350px; margin-top: 0; }
        .sim-3d-panel { height: 100%; }
        #plot3d { width: 100%; height: 350px; margin-top: 0; }


    </style>
</head>
<body>

    <div class="dashboard-wrapper">
        <header class="app-header">
            <div class="logo-container">
                <div class="dna-icon">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5"><path d="M2 15c6.667-6 13.333 0 20-6"/><path d="M9 22c1.798-1.998 2.518-3.995 2.808-5.993"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.808 5.993"/><path d="m17 6-2.891-1.5"/><path d="m14.464 12.016 1.482 1.483"/><path d="m14 18-3-1.5"/><path d="m7 6 3 1.5"/><path d="m6 12 3 1.5"/><path d="m9.5 17.5-2.5-1.5"/></svg>
                </div>
                <div class="title-container">
                    <h1>Simulador de Paisajes de Energía en el Plegamiento de Proteínas</h1>
                </div>
            </div>
            <div class="academic-badge">TRABAJO DE FIN DE GRADO</div>
        </header>

        <div class="dashboard-grid">
            <aside class="sidebar-card">
                <h2>🎛️ Parámetros Físicos</h2>
                
                <div class="control-group" style="gap: 8px; margin-bottom: 8px;">
                    <button id="btn-demo-fold" class="btn-secondary"
                        style="width: 100%; border: 1px solid #10b981; color: #10b981; font-size: 0.82rem; padding: 9px 12px; background: rgba(16, 185, 129, 0.05); justify-content: center;">
                        ✅ DEMO: Plegamiento (Λ &gt; 1)
                    </button>
                    <button id="btn-demo-glass" class="btn-secondary"
                        style="width: 100%; border: 1px solid #f59e0b; color: #f59e0b; font-size: 0.82rem; padding: 9px 12px; background: rgba(245, 158, 11, 0.05); justify-content: center;">
                        🧊 DEMO: Vidrio de Espín (Λ &lt; 1)
                    </button>
                </div>

                <div class="control-group">
                    <div class="control-label-row">
                        <label for="slider-temp">Temperatura (T)</label>
                        <span id="val-temp" class="slider-badge">1.00</span>
                    </div>
                    <input type="range" id="slider-temp" min="0.1" max="3.0" step="0.05" value="1.0">
                    <span class="control-help">Controla las fluctuaciones térmicas.</span>
                </div>

                <div class="control-group">
                    <div class="control-label-row">
                        <label for="slider-frust">Frustración (Rugosidad)</label>
                        <span id="val-frust" class="slider-badge">0.50 kcal/mol</span>
                    </div>
                    <input type="range" id="slider-frust" min="0.0" max="2.0" step="0.05" value="0.5">
                    <span class="control-help">Controla la rugosidad del paisaje de energía.</span>
                </div>

                <div class="control-group">
                    <div class="control-label-row">
                        <label for="slider-estab">Estabilidad Nativa</label>
                        <span id="val-estab" class="slider-badge">1.50 kcal/mol</span>
                    </div>
                    <input type="range" id="slider-estab" min="0.5" max="3.0" step="0.05" value="1.5">
                    <span class="control-help">Define la profundidad del mínimo de energía global (estado nativo).</span>
                </div>

            </aside>

            <main class="main-content">
                <div class="top-row">
                    <div class="panel-card cv-panel">
                        <h3>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
                            Diagrama de Fases
                        </h3>
                        <div class="cv-layout">
                            <div id="plotCv"></div>
                            <div class="state-card" style="flex: 0.7; margin: 0; min-height: 160px; display: flex; flex-direction: column; justify-content: center; gap: 8px;">
                                <div class="state-title">Fase Actual:</div>
                                <div id="state-badge" class="state-badge badge-plegando">PLEGANDO</div>
                                <p id="state-desc" class="state-desc" style="font-size: 0.76rem; line-height: 1.35;">La temperatura se encuentra en la ventana de plegamiento (T_g &lt; T &lt; T_f).</p>
                            </div>
                        </div>
                    </div>

                    <div class="panel-card metrics-panel">
                        <h3>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                            Métricas en Tiempo Real
                        </h3>
                        
                        <div class="metrics-grid">
                            <div class="metric-box">
                                <span class="m-label">Paso MC</span>
                                <span id="val-steps" class="m-value">0</span>
                            </div>
                            <div class="metric-box">
                                <span class="m-label">Energía (E)</span>
                                <span id="val-energy" class="m-value">0.00 kcal/mol</span>
                            </div>
                            <div class="metric-box">
                                <span class="m-label">Cont. Nativos (Q)</span>
                                <span id="val-q" class="m-value">0.00</span>
                            </div>
                            <div class="metric-box">
                                <span class="m-label">Contactos (Nat / Err)</span>
                                <span id="val-contacts" class="m-value">0 / 0</span>
                            </div>
                        </div>

                        <div class="btn-group">
                            <button id="btn-play" class="btn-primary">▶ Iniciar Simulación</button>
                            <button id="btn-reset-open" class="btn-secondary">🔄 Reset (Línea)</button>
                            <button id="btn-reset-native" class="btn-secondary">🏆 Reset (Cubo Nativo)</button>
                            <select id="sel-speed">
                                <option value="1">Velocidad: 1x</option>
                                <option value="5">Velocidad: 5x</option>
                                <option value="15" selected>Velocidad: 15x</option>
                                <option value="30">Velocidad: 30x</option>
                                <option value="60">Velocidad: 60x</option>
                            </select>
                        </div>
                        <div class="btn-group" style="margin-top: 8px;">
                            <button id="btn-annealing" class="btn-secondary" style="flex-grow: 1; border: 1px solid #38bdf8; color: #38bdf8;">❄️ Simulated Annealing (Recocido Simulado): OFF</button>
                            <button id="btn-export-csv" class="btn-secondary" style="flex-grow: 1; border: 1px solid #a855f7; color: #a855f7;">📊 Exportar Trayectoria (CSV)</button>
                        </div>
                    </div>
                </div>

                <div class="simulation-row">
                    <div class="panel-card sim-2d-panel">
                        <h3>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                            Cadena de Aminoácidos en una Red Cúbica 3D
                        </h3>
                        <div id="plotChain3d"></div>
                    </div>

                    <div class="panel-card sim-3d-panel">
                        <h3>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><path d="m21 16-4 4-4-4"/><path d="M17 20V4"/><path d="m3 8 4-4 4 4"/><path d="M7 4v16"/></svg>
                            Paisaje de Energía y Estado de la Proteína
                        </h3>
                        <div id="plot3d"></div>
                    </div>
                </div>
            </main>
        </div>


    </div>

    <script>
        // --- VARIABLES GLOBALES ---
        let T = 1.0;
        let frustration = 0.5;
        let stability = 1.5;
        const N = 27;

        let isAnnealing = false;
        let dynamicT = 1.0;
        let simulationHistory = [];
        let frameCount = 0;
        let isInteractingPlot3d = false;
        let isInteractingPlotChain = false;

        let layoutChain = {
            margin: { l: 0, r: 0, b: 0, t: 0 },
            scene: {
                xaxis: { visible: false }, yaxis: { visible: false }, zaxis: { visible: false },
                camera: { eye: { x: 1.5, y: 1.5, z: 1.5 } }
            },
            paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
            uirevision: 'constant', showlegend: false
        };

        // Coordenadas del Cubo Nativo Perfecto 3x3x3 serpenteante
        const nativeCoords = [
            [0,0,0], [1,0,0], [2,0,0], [2,1,0], [1,1,0], [0,1,0], [0,2,0], [1,2,0], [2,2,0],
            [2,2,1], [1,2,1], [0,2,1], [0,1,1], [1,1,1], [2,1,1], [2,0,1], [1,0,1], [0,0,1],
            [0,0,2], [1,0,2], [2,0,2], [2,1,2], [1,1,2], [0,1,2], [0,2,2], [1,2,2], [2,2,2]
        ];

        // Función para generar la cadena inicial (Línea recta de N aminoácidos)
        function generateRandomWalk3D() {
            let line = [];
            for (let i = 0; i < N; i++) {
                line.push([i, 0, 0]);
            }
            return line;
        }

        let coords = generateRandomWalk3D();
        let steps = 0;
        let isRunning = false;
        let animationId;
        let theta = 0;
        let smoothQ = 0.0;

        // ELEMENTOS DEL DOM
        const sliderTemp = document.getElementById('slider-temp');
        const sliderFrust = document.getElementById('slider-frust');
        const sliderEstab = document.getElementById('slider-estab');
        const valTemp = document.getElementById('val-temp');
        const valFrust = document.getElementById('val-frust');
        const valEstab = document.getElementById('val-estab');

        const btnPlay = document.getElementById('btn-play');
        const btnResetOpen = document.getElementById('btn-reset-open');
        const btnResetNative = document.getElementById('btn-reset-native');
        const btnAnnealing = document.getElementById('btn-annealing');
        const btnExportCsv = document.getElementById('btn-export-csv');
        const selSpeed = document.getElementById('sel-speed');

        const valSteps = document.getElementById('val-steps');
        const valEnergy = document.getElementById('val-energy');
        const valQ = document.getElementById('val-q');
        const valContacts = document.getElementById('val-contacts');

        // --- CALCULO DE CONTACTOS EN 3D ---
        function getContacts(conformation) {
            let contacts = [];
            for (let i = 0; i < N; i++) {
                for (let j = i + 2; j < N; j++) {
                    let dist = Math.abs(conformation[i][0] - conformation[j][0]) +
                               Math.abs(conformation[i][1] - conformation[j][1]) +
                               Math.abs(conformation[i][2] - conformation[j][2]);
                    if (dist === 1) contacts.push([i, j]);
                }
            }
            return contacts;
        }

        const nativeContactsRef = getContacts(nativeCoords);
        const totalNativeContacts = nativeContactsRef.length;
        
        // Fórmulas teóricas del TFG para Tf (plegamiento) y Tg (vidrio de espín)
        // Tf = dE / dS  donde dE = totalNativeContacts * stability, dS = (N-1) * ln(gamma)
        // Tg = frustration / sqrt(2 * ln(gamma))
        function getTf() {
            const gamma = 4.68; // Número efectivo de conformaciones por residuo en 3D
            const dS = (N - 1) * Math.log(gamma); // Pérdida de entropía al plegarse
            const dE = totalNativeContacts * stability; // Energy gap (brecha de energía)
            return dE / dS;
        }

        function getTg() {
            const gamma = 4.68;
            return frustration / Math.sqrt(2 * Math.log(gamma));
        }

        function checkContacts(conformation) {
            let currentContacts = getContacts(conformation);
            let nativeCount = 0;
            let nonNativeCount = 0;
            let activeNative = [];
            let activeNonNative = [];

            for (let c of currentContacts) {
                let isNative = nativeContactsRef.some(nc => (c[0]===nc[0] && c[1]===nc[1]) || (c[0]===nc[1] && c[1]===nc[0]));
                if (isNative) {
                    nativeCount++;
                    activeNative.push(c);
                } else {
                    nonNativeCount++;
                    activeNonNative.push(c);
                }
            }
            return { nativeCount, nonNativeCount, activeNative, activeNonNative };
        }

        function calcEnergy(conformation) {
            let res = checkContacts(conformation);
            return -res.nativeCount * stability - res.nonNativeCount * frustration;
        }

        function acceptMove(E_old, E_new, temp) {
            if (E_new < E_old) return true;
            if (E_new === E_old) {
                // Aceptación de movimientos neutros escala con T^2 para congelar a bajas temperaturas
                let neutralProb = Math.min(1.0, Math.pow(temp / 0.5, 2));
                return Math.random() < neutralProb;
            }
            return Math.random() < Math.exp(-(E_new - E_old) / temp);
        }

        // --- MOTOR MONTE CARLO 3D CORREGIDO ---
        function attemptMonteCarloMove() {
            let effectiveT = isAnnealing ? dynamicT : T;
            let dirs = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]];

            let rVal = Math.random();
            if (rVal < 0.20) {
                // 1. MOVIMIENTO DE EXTREMOS (End Move - 20% de probabilidad)
                let i = Math.random() < 0.5 ? 0 : N - 1;
                let neighbor = i === 0 ? coords[1] : coords[N - 2];
                let d = dirs[Math.floor(Math.random() * 6)];
                let nX = neighbor[0] + d[0], nY = neighbor[1] + d[1], nZ = neighbor[2] + d[2];

                if (coords.some((c, idx) => idx !== i && c[0]===nX && c[1]===nY && c[2]===nZ)) return false;

                let E_old = calcEnergy(coords);
                let old = [...coords[i]];
                coords[i] = [nX, nY, nZ];
                let E_new = calcEnergy(coords);

                if (acceptMove(E_old, E_new, effectiveT)) return true;
                coords[i] = old;
            } else if (rVal < 0.60) {
                // 2. MOVIMIENTO DE ESQUINA MULTIPLANAR (Corner Move 3D - 40% de probabilidad)
                let i = Math.floor(Math.random() * (N - 2)) + 1;
                let prev = coords[i - 1], next = coords[i + 1];
                let dist2 = Math.abs(prev[0]-next[0]) + Math.abs(prev[1]-next[1]) + Math.abs(prev[2]-next[2]);
                
                if (dist2 === 2) {
                    // En un retículo cúbico simple, para conservar estrictamente la longitud de enlace unitaria
                    // (distancia Manhattan = 1 con ambos vecinos), el único punto de red entero que conserva
                    // los enlaces en 3D es el flip de 180° en el plano de la esquina: P_i' = P_{i-1} + P_{i+1} - P_i.
                    let nX = prev[0] + next[0] - coords[i][0];
                    let nY = prev[1] + next[1] - coords[i][1];
                    let nZ = prev[2] + next[2] - coords[i][2];

                    if (coords.some((c, idx) => idx !== i && c[0]===nX && c[1]===nY && c[2]===nZ)) return false;

                    let E_old = calcEnergy(coords);
                    let old = [...coords[i]];
                    coords[i] = [nX, nY, nZ];
                    let E_new = calcEnergy(coords);

                    if (acceptMove(E_old, E_new, effectiveT)) return true;
                    coords[i] = old;
                }
            } else {
                // 3. MOVIMIENTO DE MANIVELA TRIDIMENSIONAL (Crankshaft Move 3D - 40% de probabilidad)
                let i = Math.floor(Math.random() * (N - 3));
                let p0 = coords[i];
                let p1 = coords[i+1];
                let p2 = coords[i+2];
                let p3 = coords[i+3];

                // Comprobar si forman una estructura en "U" (distancia Manhattan entre i e i+3 debe ser exactamente 1)
                let dist_0_3 = Math.abs(p0[0] - p3[0]) + Math.abs(p0[1] - p3[1]) + Math.abs(p0[2] - p3[2]);
                if (dist_0_3 === 1) {
                    // Encontrar el eje axial que conecta p0 y p3 (difieren en exactamente una coordenada)
                    let c = -1;
                    for (let axis = 0; axis < 3; axis++) {
                        if (p0[axis] !== p3[axis]) {
                            c = axis;
                            break;
                        }
                    }

                    // Determinar los dos ejes perpendiculares al eje axial
                    let a = (c + 1) % 3;
                    let b = (c + 2) % 3;

                    // Coordenadas relativas de p1 en el plano perpendicular al eje axial (relativo a p0)
                    let x_perp = p1[a] - p0[a];
                    let y_perp = p1[b] - p0[b];

                    // Elegir un ángulo aleatorio de rotación: 90, 180 o 270 grados
                    let angleChoice = [90, 180, 270][Math.floor(Math.random() * 3)];
                    let rx_perp = 0, ry_perp = 0;

                    if (angleChoice === 90) {
                        rx_perp = -y_perp;
                        ry_perp = x_perp;
                    } else if (angleChoice === 180) {
                        rx_perp = -x_perp;
                        ry_perp = -y_perp;
                    } else if (angleChoice === 270) {
                        rx_perp = y_perp;
                        ry_perp = -x_perp;
                    }

                    // Nuevas posiciones tridimensionales potenciales para i+1 e i+2
                    let nP1 = [];
                    nP1[c] = p0[c];
                    nP1[a] = p0[a] + rx_perp;
                    nP1[b] = p0[b] + ry_perp;

                    let nP2 = [];
                    nP2[c] = p3[c];
                    nP2[a] = p3[a] + rx_perp;
                    nP2[b] = p3[b] + ry_perp;

                    // Verificar volumen excluido (que nadie más ocupe estas posiciones, excepto i+1 e i+2)
                    let collision1 = coords.some((c_coord, idx) => idx !== (i+1) && idx !== (i+2) && c_coord[0] === nP1[0] && c_coord[1] === nP1[1] && c_coord[2] === nP1[2]);
                    let collision2 = coords.some((c_coord, idx) => idx !== (i+1) && idx !== (i+2) && c_coord[0] === nP2[0] && c_coord[1] === nP2[1] && c_coord[2] === nP2[2]);

                    if (!collision1 && !collision2) {
                        let E_old = calcEnergy(coords);
                        let old1 = [...coords[i+1]];
                        let old2 = [...coords[i+2]];

                        coords[i+1] = nP1;
                        coords[i+2] = nP2;

                        let E_new = calcEnergy(coords);
                        if (acceptMove(E_old, E_new, effectiveT)) {
                            return true;
                        }
                        coords[i+1] = old1;
                        coords[i+2] = old2;
                    }
                }
            }
            return false;
        }

        // --- VISOR DE LA CADENA EN 3D (PLOTLY) ---
        function drawChain3d() {
            let res = checkContacts(coords);
            
            let chainX = coords.map(c => c[0]), chainY = coords.map(c => c[1]), chainZ = coords.map(c => c[2]);
            let colors = coords.map((_, i) => i); // Escala para ver los extremos N -> C

            let traceChain = {
                x: chainX, y: chainY, z: chainZ,
                type: 'scatter3d', mode: 'lines+markers',
                marker: { size: 6, color: colors, colorscale: 'Viridis', opacity: 1 },
                line: { color: '#475569', width: 5 },
                hoverinfo: 'none'
            };

            let data = [traceChain];

            // Dibujar lineas de contactos activos nativos (verdes)
            for (let c of res.activeNative) {
                data.push({
                    x: [coords[c[0]][0], coords[c[1]][0]],
                    y: [coords[c[0]][1], coords[c[1]][1]],
                    z: [coords[c[0]][2], coords[c[1]][2]],
                    type: 'scatter3d', mode: 'lines',
                    line: { color: '#10b981', width: 3, dash: 'dash' },
                    hoverinfo: 'none', showlegend: false
                });
            }

            // Dibujar lineas de contactos erróneos (rojas)
            for (let c of res.activeNonNative) {
                data.push({
                    x: [coords[c[0]][0], coords[c[1]][0]],
                    y: [coords[c[0]][1], coords[c[1]][1]],
                    z: [coords[c[0]][2], coords[c[1]][2]],
                    type: 'scatter3d', mode: 'lines',
                    line: { color: '#f43f5e', width: 3, dash: 'dash' },
                    hoverinfo: 'none', showlegend: false
                });
            }

            Plotly.react('plotChain3d', data, layoutChain, { displayModeBar: true, responsive: true });
        }

        // --- PAISAJE DE WOLYNES 3D CORREGIDO ---
        function calcFunnelZ(x, y) {
            let r = Math.sqrt(x*x + y*y);
            if (r > 1) r = 1;
            
            // La profundidad del embudo disminuye (se aplana) a medida que aumenta la frustración
            let effectiveStability = Math.max(0.1, stability - 0.5 * frustration);
            let depth = -effectiveStability * Math.pow(1 - r, 2) * 8.0;
            
            // La rugosidad aumenta su amplitud y no se desvanece tan rápido cerca del centro (usando r^0.5)
            let rugosidad = frustration * Math.sin(5.5 * Math.PI * x) * Math.cos(5.5 * Math.PI * y) * Math.pow(r, 0.5) * 4.0;
            
            return depth + rugosidad;
        }

        function buildFunnelSurface() {
            const gridRes = 50;
            let X = [], Y = [], Z = [];
            for (let i = 0; i < gridRes; i++) {
                X.push([]); Y.push([]); Z.push([]);
                let r = i / (gridRes - 1);
                for (let j = 0; j < gridRes; j++) {
                    let t = (j / (gridRes - 1)) * 2 * Math.PI;
                    let x = r * Math.cos(t), y = r * Math.sin(t);
                    X[i].push(x); Y[i].push(y); Z[i].push(calcFunnelZ(x, y));
                }
            }
            return {
                z: Z, x: X, y: Y, type: 'surface',
                colorscale: 'Blues', showscale: false, opacity: 0.8,
                lighting: { ambient: 0.65, roughness: 0.4 }, hoverinfo: 'none'
            };
        }

        let traceSurface = buildFunnelSurface();

        let traceBall = {
            x: [1.0], y: [0.0], z: [0.8], type: 'scatter3d', mode: 'markers',
            marker: { size: 9, color: '#ef4444', line: { color: 'white', width: 2 } },
            hoverinfo: 'none'
        };

        let layout3d = {
            margin: { l: 0, r: 0, b: 0, t: 0 },
            scene: {
                xaxis: { visible: false, range: [-1.2, 1.2] },
                yaxis: { visible: false, range: [-1.2, 1.2] },
                zaxis: {
                    title: { text: 'Energía Libre', font: { family: 'Inter', size: 10, color: '#94a3b8' } },
                    range: [-stability * 8.0 - frustration * 2.0 - 3.0, frustration * 2.0 + 3.0],
                    backgroundcolor: 'rgba(15, 23, 42, 0.5)', showbackground: true,
                    gridcolor: '#1e293b', tickfont: { color: '#94a3b8' }
                },
                camera: { eye: { x: 1.45, y: 1.45, z: 0.85 } }
            },
            paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', uirevision: 'constant'
        };

        Plotly.newPlot('plot3d', [traceSurface, traceBall], layout3d, { displayModeBar: true, responsive: true });

        // --- GRAFICA DE CV CALIBRADA ---
        function updateCvChart() {
            const Tf = getTf();
            const Tg = getTg();
            
            let T_range = [], Cv_total = [];
            for (let i = 0; i < 250; i++) {
                let t = 0.01 + (i / 249) * 3.49;
                T_range.push(t);
                let cv_folding = 8.0 * Math.exp(-Math.pow(t - Tf, 2) / 0.12);
                let cv_glass = frustration > 0 ? (3.0 * frustration) * Math.exp(-Math.pow(t - Tg, 2) / 0.05) : 0.0;
                Cv_total.push(cv_folding + cv_glass + 1.0);
            }
            
            let effT = isAnnealing ? dynamicT : T;
            let cv_f_curr = 8.0 * Math.exp(-Math.pow(effT - Tf, 2) / 0.12);
            let cv_g_curr = frustration > 0 ? (3.0 * frustration) * Math.exp(-Math.pow(effT - Tg, 2) / 0.05) : 0.0;
            
            let maxVal = Math.max(...Cv_total);
            
            let traceCurve = { 
                x: T_range, 
                y: Cv_total, 
                mode: 'lines', 
                name: 'Cv (Capacidad Calorífica)', 
                line: { color: '#38bdf8', width: 3 }, 
                fill: 'tozeroy', 
                fillcolor: 'rgba(56, 189, 248, 0.04)',
                showlegend: true
            };
            let traceTf = {
                x: [Tf, Tf],
                y: [0, maxVal * 1.25],
                mode: 'lines',
                name: 'T_f (Plegamiento)',
                line: { color: '#10b981', width: 1.8, dash: 'dot' },
                showlegend: true
            };
            let traceTg = {
                x: [Tg, Tg],
                y: [0, maxVal * 1.25],
                mode: 'lines',
                name: 'T_g (Vítrea)',
                line: { color: '#f59e0b', width: 1.8, dash: 'dot' },
                showlegend: true
            };
            let traceEffT = {
                x: [effT, effT],
                y: [0, maxVal * 1.25],
                mode: 'lines',
                name: 'T actual',
                line: { color: '#ef4444', width: 2.0, dash: 'dash' },
                showlegend: true
            };
            let traceMarker = { 
                x: [effT], 
                y: [cv_f_curr + cv_g_curr + 1.0], 
                mode: 'markers', 
                name: 'Punto Operación',
                marker: { color: '#ef4444', size: 10, line: { color: 'white', width: 2 } },
                showlegend: false 
            };
            
            let layoutCv = {
                margin: { l: 55, r: 15, b: 45, t: 55 }, // Aumentado margen izquierdo e inferior para las etiquetas de los ejes
                xaxis: { 
                    title: { text: 'Temperatura (T)', font: { family: 'Inter', size: 10, color: '#94a3b8' } },
                    range: [0, 3.5], 
                    gridcolor: '#1e293b', 
                    tickfont: { color: '#64748b' }, 
                    zeroline: false 
                },
                yaxis: { 
                    title: { text: 'Capacidad Calorífica (Cv)', font: { family: 'Inter', size: 10, color: '#94a3b8' } },
                    range: [0, maxVal * 1.25], 
                    gridcolor: '#1e293b', 
                    tickfont: { color: '#64748b' }, 
                    zeroline: false 
                },
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
                showlegend: true,
                legend: {
                    orientation: 'h',
                    x: 0,
                    y: 1.45,
                    font: { family: 'Inter', size: 9, color: '#cbd5e1' },
                    bgcolor: 'rgba(15, 23, 42, 0.4)',
                    bordercolor: 'rgba(255, 255, 255, 0.05)',
                    borderwidth: 1
                }
            };
            Plotly.react('plotCv', [traceCurve, traceTf, traceTg, traceEffT, traceMarker], layoutCv, { displayModeBar: false, responsive: true });
        }

        function updateThermalState() {
            const Tf = getTf();
            const Tg = getTg();
            let effT = isAnnealing ? dynamicT : T;

            const badge = document.getElementById('state-badge');
            const desc = document.getElementById('state-desc');

            if (effT < Tg) {
                badge.className = "state-badge badge-vitreo"; badge.innerHTML = "VIDRIO (CONGELADO)";
                desc.innerHTML = `La temperatura actual (T = ${effT.toFixed(2)}) es menor que Tg (${Tg.toFixed(2)}). La cadena está atrapada en un mínimo local`;
            } else if (effT > Tf) {
                badge.className = "state-badge badge-desplegado"; badge.innerHTML = "DESPLEGADO / DESORDENADO";
                desc.innerHTML = `La temperatura (T = ${effT.toFixed(2)}) supera Tf (${Tf.toFixed(2)}). El ruido térmico domina por completo.`;
            } else {
                badge.className = "state-badge badge-plegando"; badge.innerHTML = "PLEGANDO";
                desc.innerHTML = `Ventana de plegamiento (Tg &lt; T &lt; Tf). El paisaje guía suavemente la cadena hacia el estado nativo.`;
            }
        }

        // --- LISTENERS DE PARÁMETROS ---
        sliderTemp.addEventListener('input', function() { T = parseFloat(this.value); valTemp.innerHTML = T.toFixed(2); if(!isAnnealing) { updateCvChart(); updateThermalState(); } });
        sliderFrust.addEventListener('input', function() {
            frustration = parseFloat(this.value);
            valFrust.innerHTML = frustration.toFixed(2) + ' kcal/mol';
            traceSurface = buildFunnelSurface();
            layout3d.scene.zaxis.range = [-stability * 8.0 - frustration * 2.0 - 3.0, frustration * 2.0 + 3.0];
            updateCvChart();
            updateThermalState();
            if (!isRunning) {
                let ballQ = checkContacts(coords).nativeCount / totalNativeContacts;
                let r = 1.0 - ballQ;
                let ballX = r * Math.cos(theta), ballY = r * Math.sin(theta);
                let ballZ = calcFunnelZ(ballX, ballY) + 0.15;
                let updatedBall = {
                    x: [ballX], y: [ballY], z: [ballZ],
                    type: 'scatter3d', mode: 'markers',
                    marker: { size: 9, color: '#ef4444', line: { color: 'white', width: 2 } },
                    hoverinfo: 'none'
                };
                Plotly.react('plot3d', [traceSurface, updatedBall], layout3d, { displayModeBar: true, responsive: true });
            }
        });

        sliderEstab.addEventListener('input', function() {
            stability = parseFloat(this.value);
            valEstab.innerHTML = stability.toFixed(2) + ' kcal/mol';
            traceSurface = buildFunnelSurface();
            layout3d.scene.zaxis.range = [-stability * 8.0 - frustration * 2.0 - 3.0, frustration * 2.0 + 3.0];
            updateCvChart();
            updateThermalState();
            if (!isRunning) {
                let ballQ = checkContacts(coords).nativeCount / totalNativeContacts;
                let r = 1.0 - ballQ;
                let ballX = r * Math.cos(theta), ballY = r * Math.sin(theta);
                let ballZ = calcFunnelZ(ballX, ballY) + 0.15;
                let updatedBall = {
                    x: [ballX], y: [ballY], z: [ballZ],
                    type: 'scatter3d', mode: 'markers',
                    marker: { size: 9, color: '#ef4444', line: { color: 'white', width: 2 } },
                    hoverinfo: 'none'
                };
                Plotly.react('plot3d', [traceSurface, updatedBall], layout3d, { displayModeBar: true, responsive: true });
            }
        });

        // --- METRICAS Y LOGISTICA DE DATOS ---
        function updateMetrics() {
            let res = checkContacts(coords);
            let energy = -res.nativeCount * stability - res.nonNativeCount * frustration;
            let q = res.nativeCount / totalNativeContacts;

            valSteps.innerHTML = steps;
            valEnergy.innerHTML = energy.toFixed(2) + ' kcal/mol';
            valQ.innerHTML = q.toFixed(2);
            valContacts.innerHTML = `${res.nativeCount} <span style="color:#64748b;">/</span> <span style="color:#f43f5e;">${res.nonNativeCount}</span>`;

            return { E: energy, Q: q };
        }

        // --- BUCLE PRINCIPAL DE SIMULACIÓN ---
        function loop() {
            if (!isRunning) return;

            const mcSpeed = parseInt(selSpeed.value) * 15; // 15 propuestas por llamada de velocidad para compensar
            for (let k = 0; k < mcSpeed; k++) {
                let moved = attemptMonteCarloMove();
                if (moved) steps++;
            }

            // Calcular Q antes de actualizar la temperatura
            let q_current = checkContacts(coords).nativeCount / totalNativeContacts;

            if (isAnnealing) {
                // Cálculo dinámico de la zona crítica en función de la estabilidad nativa y frustración
                const Tf = getTf();
                const Tg = getTg();

                if (dynamicT > Tf) {
                    dynamicT *= 0.996;        // Descenso más lento y suave por encima de Tf (0.4% por frame)
                } else if (dynamicT > Tg) {
                    dynamicT *= 0.9988;       // Ventana Crítica: Descenso sumamente gradual y largo para búsqueda conformacional (0.12% por frame)
                                               // Λ>1: amplia ventana, sistema encuentra estado nativo
                                               // Λ<1: ventana ausente, vitrifica casi al instante
                } else {
                    dynamicT *= 0.997;        // Enfriamiento pausado por debajo de Tg (0.3% por frame)
                }
                if (dynamicT < 0.05) dynamicT = 0.05;
                valTemp.innerHTML = dynamicT.toFixed(2) + ' <span style="color:#10b981; font-size:0.75em; font-weight:bold;">(AUTO)</span>';
                updateCvChart();
                updateThermalState();
            }

            let state = updateMetrics();

            // Guardar trayectoria para descargar en CSV
            simulationHistory.push({
                step: steps,
                temp: (isAnnealing ? dynamicT : T).toFixed(3),
                energy: state.E.toFixed(2),
                q: state.Q.toFixed(3)
            });

            // Filtro de paso bajo para suavizar el movimiento de la bolita en el embudo
            smoothQ = smoothQ * 0.90 + state.Q * 0.10;

            // Actualizar posicion de la bola en el embudo usando Q suavizado
            let r = 1.0 - smoothQ;
            let ballX = r * Math.cos(theta), ballY = r * Math.sin(theta);
            let ballZ = calcFunnelZ(ballX, ballY) + 0.15;
            theta += 0.008;

            frameCount++;
            if (frameCount % 6 === 0) {
                if (!isInteractingPlotChain) {
                    drawChain3d();
                }
            }
            
            if (!isInteractingPlot3d) {
                Plotly.restyle('plot3d', {
                    x: [[ballX]],
                    y: [[ballY]],
                    z: [[ballZ]]
                }, [1]);
            }
            animationId = requestAnimationFrame(loop);
        }

        // ── DEMO FUNCTIONS ─────────────────────────────────────────────
        function runDemo(scenario) {
            if (scenario === 'fold') {
                frustration = 0.3;
                stability   = 2.0;
                T           = 1.00; // Ventana óptima de plegamiento (Tg = 0.17 < T < Tf = 1.39)
            } else {
                frustration = 1.5;
                stability   = 1.0;
                T           = 0.30; // Muy por debajo de Tg = 0.85 para congelamiento evidente
            }

            // Sync sliders and labels
            sliderFrust.value = frustration;  valFrust.innerHTML = frustration.toFixed(2) + ' kcal/mol';
            sliderEstab.value = stability;    valEstab.innerHTML = stability.toFixed(2) + ' kcal/mol';
            sliderTemp.value  = T;            valTemp.innerHTML  = T.toFixed(2);

            // Reconstruir la superficie del embudo y actualizar el rango
            traceSurface = buildFunnelSurface();
            layout3d.scene.zaxis.range = [-stability * 8.0 - frustration * 2.0 - 3.0, frustration * 2.0 + 3.0];

            updateCvChart();
            updateThermalState();

            // Redibujar el embudo en Plotly de inmediato si la simulación no está corriendo
            if (!isRunning) {
                let ballQ = checkContacts(coords).nativeCount / totalNativeContacts;
                let r = 1.0 - ballQ;
                let ballX = r * Math.cos(theta), ballY = r * Math.sin(theta);
                let ballZ = calcFunnelZ(ballX, ballY) + 0.15;
                let updatedBall = {
                    x: [ballX], y: [ballY], z: [ballZ],
                    type: 'scatter3d', mode: 'markers',
                    marker: { size: 9, color: '#ef4444', line: { color: 'white', width: 2 } },
                    hoverinfo: 'none'
                };
                Plotly.react('plot3d', [traceSurface, updatedBall], layout3d, { displayModeBar: true, responsive: true });
            }
        }

        // --- LISTENERS DE INTERFAZ ---
        btnPlay.addEventListener('click', function() {
            if (!isRunning) {
                isRunning = true;
                this.innerHTML = "⏸ Pausar Simulación";
                this.style.background = "linear-gradient(135deg, #ef4444, #be123c)";
                animationId = requestAnimationFrame(loop);
            } else {
                isRunning = false;
                this.innerHTML = "▶ Iniciar Simulación";
                this.style.background = "linear-gradient(135deg, #2563eb, #1d4ed8)";
                cancelAnimationFrame(animationId);
            }
        });

        function resetSimulation(type) {
            isRunning = false;
            btnPlay.innerHTML = "▶ Iniciar Simulación";
            btnPlay.style.background = "linear-gradient(135deg, #2563eb, #1d4ed8)";
            cancelAnimationFrame(animationId);
            steps = 0; theta = 0; simulationHistory = [];
            
            if (isAnnealing) {
                isAnnealing = false;
                btnAnnealing.style.background = ""; btnAnnealing.style.color = "#38bdf8"; btnAnnealing.innerHTML = "❄️ Simulated Annealing (Recocido simulado): OFF";
                valTemp.innerHTML = T.toFixed(2);
                updateCvChart();
                updateThermalState();
            }

            if (type === 'open') {
                coords = generateRandomWalk3D();
            } else if (type === 'native') {
                coords = nativeCoords.map(c => [...c]);
            }

            drawChain3d();
            let state = updateMetrics();
            smoothQ = state.Q;
            updateCvChart();
            updateThermalState();

            let r = 1.0 - state.Q;
            let updatedBall = {
                x: [r], y: [0], z: [calcFunnelZ(r, 0) + 0.15],
                type: 'scatter3d', mode: 'markers',
                marker: { size: 9, color: '#ef4444', line: { color: 'white', width: 2 } },
                hoverinfo: 'none'
            };
            Plotly.react('plot3d', [traceSurface, updatedBall], layout3d, { displayModeBar: true, responsive: true });
        }

        btnResetOpen.addEventListener('click', () => resetSimulation('open'));
        btnResetNative.addEventListener('click', () => resetSimulation('native'));

        btnAnnealing.addEventListener('click', function() {
            if (!isAnnealing) {
                isAnnealing = true;
                dynamicT = 2.5; // Golpe térmico inicial para romper nudos
                this.innerHTML = "❄️ Simulated Annealing (Recocido Simulado): ON";
                this.style.background = "linear-gradient(135deg, #10b981, #047857)";
                this.style.color = "white";
            } else {
                isAnnealing = false;
                this.innerHTML = "❄️ Simulated Annealing (Recocido Simulado): OFF";
                this.style.background = ""; this.style.color = "#38bdf8";
                valTemp.innerHTML = T.toFixed(2);
                updateCvChart();
                updateThermalState();
            }
        });

        btnExportCsv.addEventListener('click', function() {
            if (simulationHistory.length === 0) {
                alert("No hay registros en el historial. Inicia la simulación para acumular datos.");
                return;
            }
            let csvContent = "Paso,Temperatura,Energia,Q_Solapamiento\\n";
            simulationHistory.forEach(row => {
                csvContent += `${row.step},${row.temp},${row.energy},${row.q}\\n`;
            });
            
            let blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            let url = URL.createObjectURL(blob);
            let link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "trayectoria_plegamiento_3D.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });

        document.getElementById('btn-demo-fold').addEventListener('click',  () => runDemo('fold'));
        document.getElementById('btn-demo-glass').addEventListener('click', () => runDemo('glass'));

        // --- ARRANQUE INICIAL ---
        drawChain3d();
        let initialMetrics = updateMetrics();
        smoothQ = initialMetrics.Q;
        updateCvChart();
        updateThermalState();

        // --- VINCULACIÓN DE EVENTOS DE ROTACIÓN DE CÁMARA (EVITA RESETS EN CADA FRAME) ---
        document.getElementById('plot3d').on('plotly_relayout', function(eventData) {
            if (eventData) {
                if (eventData['scene.camera']) {
                    layout3d.scene.camera = eventData['scene.camera'];
                } else if (eventData['scene.camera.eye']) {
                    if (!layout3d.scene.camera) layout3d.scene.camera = {};
                    layout3d.scene.camera.eye = eventData['scene.camera.eye'];
                }
            }
        });

        document.getElementById('plotChain3d').on('plotly_relayout', function(eventData) {
            if (eventData) {
                if (eventData['scene.camera']) {
                    layoutChain.scene.camera = eventData['scene.camera'];
                } else if (eventData['scene.camera.eye']) {
                    if (!layoutChain.scene.camera) layoutChain.scene.camera = {};
                    layoutChain.scene.camera.eye = eventData['scene.camera.eye'];
                }
            }
        });

        // --- EVITAR INTERRUPCIONES DE RENDER DURANTE LA ROTACIÓN TÁCTIL/MOUSE DE CÁMARA ---
        const plot3dDiv = document.getElementById('plot3d');
        plot3dDiv.addEventListener('mousedown', function() { isInteractingPlot3d = true; });
        plot3dDiv.addEventListener('touchstart', function() { isInteractingPlot3d = true; }, { passive: true });
        window.addEventListener('mouseup', function() { isInteractingPlot3d = false; });
        window.addEventListener('touchend', function() { isInteractingPlot3d = false; });
        window.addEventListener('touchcancel', function() { isInteractingPlot3d = false; });

        const plotChainDiv = document.getElementById('plotChain3d');
        plotChainDiv.addEventListener('mousedown', function() { isInteractingPlotChain = true; });
        plotChainDiv.addEventListener('touchstart', function() { isInteractingPlotChain = true; }, { passive: true });
        window.addEventListener('mouseup', function() { isInteractingPlotChain = false; });
        window.addEventListener('touchend', function() { isInteractingPlotChain = false; });
        window.addEventListener('touchcancel', function() { isInteractingPlotChain = false; });
    </script>
</body>
</html>
"""

# Renderizar el componente interactivo al 100%
components.html(html_code, height=950, scrolling=False)
