class FilterManager:
    def __init__(self, filters: list = None):
        self.filters = filters or []

    def add_filters(self, *filters):
        self.filters.extend(filters)

    def remove_filters(self, *filters):
        for filter in filters:
            self.filters.remove(filter)

    def filter(self, data):
        return all(filter(data) for filter in self.filters)
