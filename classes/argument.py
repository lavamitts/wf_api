import classes.functions as f


class Argument:
    def __init__(self, argument, value):
        self.argument = argument
        self.value = f.to_bool(value)
        self.parse_argument()

    def parse_argument(self):
        self.measure_type_id = self.argument[9:12]
        self.document_code = self.argument[-4:]
        del self.argument
        a = 1

    def api_response(self):
        r = {
            "measure_type_id": self.measure_type_id,
            "document_code": self.document_code,
            "value": self.value
        }
        return r
