class TypeInterrogation:
    type = ""
    fields = []
    rules = {}

    def __init__(self, type, fields, rules):
        self.rule = rules
        self.fields = fields
        self.type = type
