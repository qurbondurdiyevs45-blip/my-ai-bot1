<?php
/**
 * Spectral Cache Inspector
 * A polymorphic, single-file PHP utility to visualize OPcache and System memory.
 * Combines low-level diagnostics with a terminal-inspired web UI.
 */

display_errors(0);
error_reporting(E_ALL);

class SpectralInspector {
    private $startTime;

    public function __construct() {
        $this->startTime = microtime(true);
    }

    public function getSystemStats() {
        $load = function_exists('sys_getloadavg') ? sys_getloadavg() : [0, 0, 0];
        $opcache = function_exists('opcache_get_status') ? opcache_get_status() : null;
        
        return [
            'php_version' => PHP_VERSION,
            'os' => PHP_OS,
            'load' => $load,
            'memory_peak' => memory_get_peak_usage(true),
            'opcache' => $opcache,
            'timestamp' => date('Y-m-d H:i:s')
        ];
    }

    public function render() {
        $data = $this->getSystemStats();
        $jsonStats = json_encode($data);

        echo "<!DOCTYPE html>\n<html lang='en'>\n<head>\n    <meta charset='UTF-8'>\n    <title>Spectral Cache Inspector</title>\n    <style>\n        :root { --bg: #0a0a0f; --accent: #00ffca; --text: #a0a0ff; --dim: #2a2a40; }\n        body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }\n        #canvas-bg { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }\n        .console { padding: 20px; max-width: 1000px; margin: 50px auto; background: rgba(10, 10, 15, 0.8); border: 1px solid var(--accent); box-shadow: 0 0 20px rgba(0, 255, 202, 0.2); }\n        h1 { color: var(--accent); text-transform: uppercase; letter-spacing: 4px; border-bottom: 2px solid var(--accent); padding-bottom: 10px; }\n        .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }\n        .card { border-left: 3px solid var(--text); padding-left: 15px; background: var(--dim); padding: 10px; }\n        .label { font-weight: bold; color: var(--accent); }\n        .pulse { animation: blink 1.5s infinite; }\n        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }\n        .bar-outer { width: 100%; height: 10px; background: #111; margin-top: 8px; border: 1px solid #333; }\n        .bar-inner { height: 100%; background: var(--accent); box-shadow: 0 0 10px var(--accent); transition: width 0.5s ease-in-out; }\n    </style>\n</head>\n<body>\n    <canvas id='canvas-bg'></canvas>\n    <div class='console'>\n        <h1>Spectral Cache Inspector <small style='font-size: 10px;'>v1.0</small></h1>\n        <p class='pulse'>> SCANNING CORE DUMP... OK</p>\n        <div class='stat-grid'>\n            <div class='card'>\n                <div class='label'>OS / ENVIRONMENT</div>\n                <div>{$data['os']} / PHP {$data['php_version']}</div>\n            </div>\n            <div class='card'>\n                <div class='label'>SYSTEM LOAD (1m, 5m, 15m)</div>\n                <div>" . implode(' | ', $data['load']) . "</div>\n            </div>\n            <div class='card'>\n                <div class='label'>PEAK MEMORY CONSUMPTION</div>\n                <div>" . round($data['memory_peak'] / 1024 / 1024, 2) . " MB</div>\n                <div class='bar-outer'><div class='bar-inner' style='width: " . min(100, ($data['memory_peak'] / 1048576) * 5) . "%'></div></div>\n            </div>\n            <div class='card'>\n                <div class='label'>OPCACHE STATUS</div>\n                <div>" . ($data['opcache']['opcache_enabled'] ? 'ACTIVE' : 'DISABLED') . "</div>\n                <div style='font-size: 12px; margin-top: 5px; opacity: 0.7;'>Scripts Cached: " . ($data['opcache']['opcache_statistics']['num_cached_scripts'] ?? 0) . "</div>\n            </div>\n        </div>\n        <pre id='raw-dump' style='margin-top: 30px; border-top: 1px solid var(--dim); padding-top: 15px; font-size: 11px;'>// Initializing Matrix Stream...\n</pre>\n    </div>\n\n    <script>\n        const stats = {$jsonStats};\n        const dump = document.getElementById('raw-dump');\n        let cursor = 0;\n\n        function typeWriter() {\n            const text = JSON.stringify(stats, null, 2);\n            if (cursor < text.length) {\n                dump.innerHTML += text.charAt(cursor);\n                cursor++;\n                setTimeout(typeWriter, 1);\n                if(cursor % 50 === 0) window.scrollTo(0, document.body.scrollHeight);\n            }\n        }\n\n        const canvas = document.getElementById('canvas-bg');\n        const ctx = canvas.getContext('2d');\n        canvas.width = window.innerWidth;\n        canvas.height = window.innerHeight;\n\n        const particles = Array(50).fill().map(() => ({\n            x: Math.random() * canvas.width,\n            y: Math.random() * canvas.height,\n            v: Math.random() * 0.5 + 0.2,\n            size: Math.random() * 2\n        }));\n\n        function animate() {\n            ctx.clearRect(0, 0, canvas.width, canvas.height);\n            ctx.fillStyle = '#00ffca';\n            particles.forEach(p => {\n                p.y -= p.v;\n                if (p.y < 0) p.y = canvas.height;\n                ctx.fillRect(p.x, p.y, p.size, p.size);\n            });\n            requestAnimationFrame(animate);\n        }\n\n        window.onload = () => {\n            animate();\n            setTimeout(typeWriter, 1000);\n        };\n    </script>\n</body>\n</html>";
    }
}

$inspector = new SpectralInspector();
$inspector.render();
?>