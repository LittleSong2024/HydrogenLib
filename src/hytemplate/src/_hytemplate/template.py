from .markers import TemplateMarker


class Template:
    def __init__(self, template):
        self._template = TemplateMarker(template)
        self._attrs = {}

    def fill(self, **kwargs):
        return self._template.generate(self, **kwargs)
