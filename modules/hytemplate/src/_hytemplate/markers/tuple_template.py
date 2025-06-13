from ..basic_methods import *


class TupleTemplateMarker(AbstractMarker):
    """
    Tuple template marker
    """

    def __init__(self, *markers):
        self._markers = markers

    def generate(self, context: GenerationContext):
        return tuple(
            generate(marker, context, parent=self) for marker in self._markers
        )

    def restore(self, context: RestorationContext):
        return tuple(
            restore(marker, value, context, parent=self) for marker, value in zip(self._markers, context.value)
        )
