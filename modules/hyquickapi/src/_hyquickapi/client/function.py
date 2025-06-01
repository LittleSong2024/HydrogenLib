from _hycore.better_descriptor import BetterDescriptor, BetterDescriptorInstance

from .template import *


class ApiFunctionInstance(BetterDescriptorInstance):
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

    def __better_init__(self, instance, owner, name):
        self.name = name

    def __call__(self, **kwargs):
        ...


class ApiFunction(BetterDescriptor):
    __better_type__ = ApiFunctionInstance

    base_url: str = None

    def __better_new__(self) -> "BetterDescriptorInstance":
        return ApiFunctionInstance(self.request_template, self.response_template, self)

    def __better_init__(self, name, owner):
        self.serializer = owner.backend.api_serializer
        self.requester = owner.backend.api_requester
        self.processor = owner.backend.api_handlers

    def __init__(self, target_path, request: RequestTemplate, response: ResponseTemplate, method='GET'):
        super().__init__()
        self.target = target_path
        self.method = method
        self.request_template = request
        self.response_template = response
