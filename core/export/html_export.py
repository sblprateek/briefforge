"""
BriefForge HTML Exporter
Renders print-ready, professional agency brief HTML documents using Jinja2.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from core.generation.brief_schema import BriefDocument


class HTMLExporter:
    """Renders HTML presentation with print stylesheets and clickable traceability."""

    def __init__(self):
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def export(self, brief: BriefDocument) -> str:
        template = self.env.get_template("brief_print.html")
        return template.render(brief=brief)

    def save(self, brief: BriefDocument, output_path: str):
        content = self.export(brief)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
