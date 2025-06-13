from ..abstract import AbstractMarker
from ..basic_methods import generate, restore
from ..context import GenerationContext, RestorationContext


def process_template(template: dict):
    for k in template.keys():
        value = template[k]
        if isinstance(value, dict):
            template[k] = DictTemplateMarker(value)

    return template


class DictTemplateMarker(AbstractMarker):
    def __init__(self, dct):
        self._template = process_template(dct)

    def generate(self, context: GenerationContext):
        target = {}
        for key, maybe_marker in self._template.items():
            target[key] = generate(maybe_marker, context, parent=self)

        return target

    def restore(self, context: RestorationContext):
        value: dict = context.value
        for key, maybe_marker in self._template.items():
            value[key] = restore(maybe_marker, value[key], context, parent=self)
