from _hycore.better_descriptor import Descriptor, DescriptorInstance

from .template import *


class ApiFunctionInstance(DescriptorInstance):
    def __init__(self, request_template: RequestTemplate, response_template: ResponseTemplate,
                 parent: "ApiFunction" = None):
        super().__init__()
        self.parent = parent

        self.request_template = request_template
        self.response_template = response_template

        self.method = parent.method
        self.target = parent.target

        self.backend = parent.backend

        self.url = parent.base_url + self.target

    def __dspt_init__(self, instance, owner, name):
        self.name = name

    def __call__(self, **kwargs):
        ...


class ApiFunction(Descriptor):
    __better_type__ = ApiFunctionInstance

    base_url: str = None

    def __dspt_new__(self) -> "DescriptorInstance":
        return ApiFunctionInstance(self.request_template, self.response_template, self)

    def __dspt_init__(self, name, owner):
        self.serializer = owner.backends.api_serializer
        self.requester = owner.backends.api_requester
        self.processor = owner.backends.api_handlers

    def __init__(self, target_path, request: RequestTemplate, response: ResponseTemplate, method='GET'):
        super().__init__()
        self.target = target_path
        self.method = method
        self.request_template = request
        self.response_template = response
