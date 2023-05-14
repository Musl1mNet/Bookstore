from rest_framework import renderers

class OwnRenderer(renderers.BaseRenderer):
    media_type = 'text/muslim'
    format = 'muslim'
    def _to_str(self, data):

        if isinstance(data, str):
            return data
        if isinstance(data, (int, float)):
            return str(data)
        from collections import OrderedDict
        if isinstance(data, (dict, OrderedDict)):
            result = "->"
            for k, v in data.items():
                result += f"{k}:" + self._to_str(v) + ';'
            result += "<-"
            return result
        if isinstance(data, list):
            result = "=>"
            for row in data:
                result += self._to_str(row) + ",\n"
            result += "<="
            return result
        return "None"
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return self._to_str(data)