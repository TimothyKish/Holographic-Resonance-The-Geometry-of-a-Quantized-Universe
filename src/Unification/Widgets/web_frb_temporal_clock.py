<script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>

<div style="font-family: Arial, sans-serif; border: 1px solid #ccc; padding: 20px; border-radius: 8px; background-color: #f9f9f9;">
    <h3 id="frb-title" style="color: #00c8ff; text-align: center; margin-bottom: 5px; text-shadow: 1px 1px 2px #aaa;">Lattice Scale: Quantum Update Rate</h3>
    <p style="text-align: center; font-size: 14px; color: #555; margin-bottom: 20px;">Zoom out to observe the scale-invariance of the 16.35 vacuum metronome.</p>
    
    <div id="frb-plot" style="width: 100%; height: 400px;"></div>
    
    <div style="margin-top: 20px; text-align: center;">
        <label for="zoomSlider" style="font-weight: bold; font-size: 16px;">Temporal Zoom Level</label><br>
        <input type="range" id="zoomSlider" min="0" max="4" step="0.1" value="0" style="width: 80%; margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; width: 80%; margin: 0 auto; font-size: 12px; color: #666;">
            <span>Micro (ms)</span>
            <span>Seconds</span>
            <span>Minutes</span>
            <span>Hours</span>
            <span>Macro (Days)</span>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 25px; font-size: 10px; color: #888;">
        Copyright &copy; 2026 Sovereign KishLattice 16pi Initiative
    </div>
</div>

<script>
    // --- LATTICE CONSTANTS ---
    const PI = Math.PI;
    const HARMONIC_BASE = 16.35;

    // Generate time array (0 to 50 units)
    let timeUnits = [];
    for (let t = 0; t <= 50; t += 0.1) { timeUnits.push(t); }

    // --- PHYSICS FUNCTION ---
    // The geometry is constant; only our human perspective of "time" changes.
    function getMetronomeWave() {
        return timeUnits.map(t => Math.abs(Math.sin((t / HARMONIC_BASE) * PI)));
    }

    // --- INITIALIZE PLOT ---
    let waveData = getMetronomeWave();
    
    // Nodes where the "tick" happens (troughs of the abs-sine wave)
    let tickNodesX = [16.35, 32.70, 49.05];
    let tickNodesY = [0, 0, 0];

    let traceWave = {
        x: timeUnits, y: waveData,
        type: 'scatter', mode: 'lines',
        name: 'Vacuum Metronome',
        line: {color: '#00c8ff', width: 4}
    };

    let traceTicks = {
        x: tickNodesX, y: tickNodesY,
        type: 'scatter', mode: 'markers',
        name: 'Harmonic Node (Tick)',
        marker: {color: 'black', size: 10}
    };

    let layout = {
        margin: { t: 10, r: 20, b: 40, l: 50 },
        xaxis: { title: 'Time in Milliseconds (ms)' },
        yaxis: { title: 'Lattice Amplitude', range: [-0.1, 1.2], showticklabels: false },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
        annotations: [{
            x: 16.35, y: 0.15,
            xref: 'x', yref: 'y',
            text: '16.35 ms',
            showarrow: false, font: {color: 'black', weight: 'bold', size: 14}
        }]
    };

    Plotly.newPlot('frb-plot', [traceWave, traceTicks], layout, {responsive: true});

    // --- SLIDER INTERACTIVITY ---
    document.getElementById('zoomSlider').addEventListener('input', function(e) {
        let zoom = parseFloat(e.target.value);
        
        let unit = "";
        let domain = "";
        let waveColor = "";

        if (zoom < 1.0) {
            unit = "Milliseconds (ms)"; domain = "Quantum Update Rate"; waveColor = "#00c8ff";
        } else if (zoom < 2.0) {
            unit = "Seconds (s)"; domain = "Acoustic / Mechanical"; waveColor = "#0044ff";
        } else if (zoom < 3.0) {
            unit = "Minutes (m)"; domain = "Planetary Atmospheric"; waveColor = "#8800ff";
        } else if (zoom < 4.0) {
            unit = "Hours (h)"; domain = "Stellar Core Dynamics"; waveColor = "#ff8800";
        } else {
            unit = "Days (d)"; domain = "MACRO-LOCK: FRB 180916"; waveColor = "#ff0000";
        }

        let titleEl = document.getElementById('frb-title');
        titleEl.innerText = "Lattice Scale: " + domain;
        titleEl.style.color = waveColor;

        // Update Plotly layout and styling (Wave shape DOES NOT change)
        let updateLayout = {
            'xaxis.title': 'Time in ' + unit,
            'annotations[0].text': '16.35 ' + unit.split(' ')[0]
        };
        
        let updateStyle = { 'line.color': [waveColor, 'black'] };

        Plotly.update('frb-plot', updateStyle, updateLayout);
    });
</script>