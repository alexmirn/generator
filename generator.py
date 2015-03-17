# #!/usr/bin/python
# # -*- coding: utf-8 -*-

import yaml
from queries import PostgreSQL

class Generator(object):

    def __init__(self, file_name, sql_type):
        self.file_name = file_name
        self.load = self.load()
        self.create_table = sql_type.create_table
        self.time_table = sql_type.time_table
        self.trigger = sql_type.trigger

    def load(self):
        with open(self.file_name) as schema:
            stream = schema.read()
            return yaml.load(stream)

    def save(self, file_name, statements):
        with open(file_name, 'wb') as _file:
            _file.write(statements)

    def fields(self):
        tables = set()

        for elem in self.load:
            table_name = elem
            table_name_low = elem.lower()
            fields_list = list()

            for field_name, field_type in self.load[table_name]['fields'].iteritems():
                fields_elements = '{}_{} {} NOT NULL'.format(table_name_low, field_name, field_type)
                fields_list.append(fields_elements)
                fields_join = ',\n    '.join(fields_list)
                new_table = self.create_table.format(table = table_name_low, fields = fields_join)
            tables.add('{}\n'.format(new_table))

        tables = sorted(tables)
        return '\n'.join(tables)

    def alter_table(self):
        alter_tables = set()

        for elem in self.load:
            table_name_low = elem.lower()

            timestamp_created = self.time_table.format(table = table_name_low, function = 'created')
            timestamp_updated = self.time_table.format(table = table_name_low, function = 'updated')

            alter_tables.add('{}\n\n{}\n'.format(timestamp_created, timestamp_updated))

        alter_tables = sorted(alter_tables)
        print alter_tables
        return '\n'.join(alter_tables)

    def triggers(self):
        trigger_set = set()

        for elem in self.load:
            table_name = elem
            table_name_low = elem.lower()

            trigger_elem = self.trigger.format(table = table_name_low)
            trigger_set.add('{}\n'.format(trigger_elem))
        
        trigger_set = sorted(trigger_set)
        return '\n'.join(trigger_set)

if __name__ == "__main__":
    # sql_type = PostgreSQL()
    generator = Generator('file.yml', PostgreSQL())

    fields = generator.fields()
    alter_table = generator.alter_table()
    trigger1 = generator.triggers()
    generator.save('schema.sql', '{}\n{}\n{}'.format(fields, alter_table, trigger1))
