import json

from ..abstract import AbstractSerializer


class Json(AbstractSerializer):
    object_hook = None
    default = None
    
    def dump(self, fp, *args, **kwargs):
        return json.dump(
            fp,
            *args,
            **{'default': self.default, **kwargs}
        )

    def load(self, fp, *args, **kwargs):
        return json.load(
            fp,
            *args,
            **{'object_hook': self.object_hook, **kwargs}
        )
    