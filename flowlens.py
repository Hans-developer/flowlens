import sys
import webbrowser
import os
import time
import functools
import asyncio
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class FunctionStats:
    calls: int
    total_time: float
    @property
    def average_time(self) -> float:
        return self.total_time / self.calls if self.calls > 0 else 0.0

class FlowLens:
    def __init__(self):
        self.steps = []
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.indent_level = 0
        self.registry = {}

    def track_stats(self, func):
        _stats = {"calls": 0, "total_time": 0.0}
        self.registry[func.__name__] = _stats
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try: return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                _stats["total_time"] += duration
                _stats["calls"] += 1
                if self.steps and self.steps[-1]['func'] == func.__name__:
                    self.steps[-1]['ms'] = round(duration * 1000, 4)
        return wrapper

    def _tracer(self, frame, event, arg):
        filename = frame.f_code.co_filename
        if not filename.startswith(self.base_dir) or "flowlens.py" in filename:
            return self._tracer
        
        func_name = frame.f_code.co_name
        if func_name in ["auditoria", "menu", "<module>", "input", "wrapper"]: return self._tracer

        if event == 'call':
            # Lógica solicitada: Identificar si es impresión o cálculo
            es_print = any(x in func_name.lower() for x in ["print", "mostrar", "display", "output"])
            comentario = "📢 MOSTRAR DATOS (Salida)" if es_print else "⚙️ TRABAJO INTERNO / CÁLCULO"
            
            self.steps.append({
                "tipo": "INICIO", "func": func_name, "linea": frame.f_lineno,
                "data": {k: v for k, v in frame.f_locals.items()}, "nivel": self.indent_level,
                "accion": comentario
            })
            self.indent_level += 1
        elif event == 'return':
            self.indent_level -= 1
            self.steps.append({
                "tipo": "FIN", "func": func_name, "linea": frame.f_lineno,
                "data": arg, "nivel": self.indent_level, "ms": 0
            })
        return self._tracer

    def start(self):
        self.steps = []
        sys.settrace(self._tracer)

    def stop(self):
        sys.settrace(None)
        self._render()

    def _render(self):
        bloques = ""
        for i, paso in enumerate(self.steps):
            es_in = paso['tipo'] == "INICIO"
            color = "#58a6ff" if es_in else "#7ee787"
            margen = paso['nivel'] * 45
            
            # Encabezado de estado según el tipo de trabajo
            estado_texto = paso.get('accion', '') if es_in else "🏁 PROCESO COMPLETADO"
            meta_label = "📥 Argumentos recibidos" if es_in else "📤 Datos generados"
            tiempo_html = f"<span class='perf'>⏱️ {paso.get('ms', 0)}ms</span>" if not es_in else ""

            bloques += f"""
            <div class="trace-box" style="margin-left:{margen}px; border-left: 3px solid {color}">
                <div class="action-label">{estado_texto}</div>
                <div class="node">
                    <div class="node-header">
                        <span class="tag" style="background:{color}">{paso['tipo']}</span>
                        <strong>{paso['func']}</strong> {tiempo_html}
                    </div>
                    <div class="node-body">
                        <small>Línea {paso['linea']} | {meta_label}:</small><br>
                        <code>{paso['data']}</code>
                    </div>
                </div>
            </div>"""

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ background: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; padding: 50px; }}
                h1 {{ color: #58a6ff; text-align: center; margin-bottom: 40px; border-bottom: 1px solid #30363d; padding-bottom: 20px; }}
                .trace-box {{ position: relative; padding: 10px 0 10px 25px; }}
                .action-label {{ font-size: 11px; color: #8b949e; margin-bottom: 4px; font-weight: bold; text-transform: uppercase; }}
                .node {{ background: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; min-width: 400px; display: inline-block; }}
                .tag {{ font-size: 9px; color: #000; padding: 2px 6px; border-radius: 4px; margin-right: 10px; font-weight: bold; }}
                .perf {{ color: #d29922; font-size: 12px; font-weight: bold; margin-left: 10px; }}
                .node-body {{ margin-top: 10px; font-size: 12px; color: #adbac7; }}
                code {{ color: #ffa657; background: #0d1117; padding: 2px 4px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <h1>FlowLens Audit Timeline</h1>
            <div class="timeline">{bloques}</div>
        </body>
        </html>"""
        
        with open("flowlens_report.html", "w", encoding="utf-8") as f: f.write(html)
        webbrowser.open("file://" + os.path.abspath("flowlens_report.html"))

lens = FlowLens()