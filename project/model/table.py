class Table:
    type = ""
    fields = []

    def __init__(self, type, fields):
        self.fields = fields
        self.type = type

    def show(self):
        print("Table : " + type + "contains the following fields: "+ "\n")
        for fields in object.fields:
            print(fields + ", ")
