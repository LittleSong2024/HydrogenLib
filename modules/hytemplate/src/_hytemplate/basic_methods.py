from .abstract import AbstractMarker
from .context import GenerationContext, RestorationContext


def generate(maybe_marker, context: GenerationContext, **kwargs):
    if not isinstance(maybe_marker, AbstractMarker):
        return maybe_marker

    kwargs['current'] = kwargs.get('current', context.current)

    new_context = GenerationContext.new(context, **kwargs)

    return maybe_marker.generate(new_context)


def restore(maybe_marker, value, context, **kwargs):
    if not isinstance(maybe_marker, AbstractMarker):
        return value

    new_context = RestorationContext.new(context, **kwargs, value=value)

    return maybe_marker.restore(new_context)
