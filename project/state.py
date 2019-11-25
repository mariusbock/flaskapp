from project import db


class State:
    table_name = ""
    number_of_entries = 0

    def __init__(self, table_name):
        self.table_name = table_name

    def count_entries_in_table(self):
        script = "select count(id) from :table_name"
        count = db.engine.execute(script, table_name=self.table_name).fetchAll()
        return count.scalar()

    #this two functions are called when number of entries from the tables differ
    def delete_old_entries_from_table(self):
        #TODO function which deletes the old entries from table
        return 0
    def add_new_entries_to_table(self):
        #TODO function which insert new entries from xdata
        return 0

    def print_state(self):
        print("The number of entries from table:" + self.table_name + " is: " + self.count_entries_in_table())
