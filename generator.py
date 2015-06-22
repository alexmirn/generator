# !/usr/bin/python
# -*- coding: utf-8 -*-

import yaml

CREATE_TABLE = """CREATE TABLE "{table}" (
    "{table}_id" SERIAL PRIMARY KEY,
    {columns},
    "{table}_created" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),
    "{table}_updated" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)
);
"""
CREATED = '"{table}_created" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)'
UPDATED = '"{table}_updated" INTEGER NOT NULL DEFAULT 0'
FOREIGN_KEY = """ALTER TABLE "{table}" ADD "{target}_id" INTEGER NOT NULL,
    ADD CONSTRAINT "fk_{table}_{target}_id" FOREIGN KEY ("{target}_id") REFERENCES "{target}" ("{target}_id");
"""
MANY_MANY_FOREIGN_KEY = """ALTER TABLE {table_save} ADD CONSTRAINT "fk_{table}_{target}_id" 
FOREIGN KEY ("{target}_id") REFERENCES "{target}" ("{target}_id");
"""
UNION_TABLE = """CREATE TABLE "{left_table}__{right_table}" (
    "{left_table}_id" INTEGER NOT NULL,
    "{right_table}_id" INTEGER NOT NULL,
    PRIMARY KEY ("{left_table}_id", "{right_table}_id"),
);
"""
TRIGGER = """CREATE OR REPLACE FUNCTION update_{table}_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.{table}_updated = cast(extract(epoch from now()) as integer);
   RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER "tr_{table}_updated" BEFORE UPDATE ON "{table}" FOR EACH ROW EXECUTE PROCEDURE update_{table}_timestamp();
"""

class Generator(object):
    def __init__(self):
        self._alters   = set()
        self._tables   = set()
        self._triggers = set()

    def __build_tables(self):
        for table_name in self.__schema:
            table_name_low = table_name.lower()
            fields = self.__build_columns(self.__schema[table_name], table_name_low)

            fields_join = ',\n    '.join(fields)
            new_table = CREATE_TABLE.format(table = table_name_low, columns = fields_join)
            self._tables.add(new_table)
        
    def __build_columns(self, entity, table_name_low):
        fields = []
        for field_name, field_type in entity['fields'].iteritems():
            fields_elements = '"{}_{}" {} NOT NULL'.format(table_name_low, field_name, field_type)
            fields.append(fields_elements)
        return fields

    def __build_relations(self):
        table_subtable_relation = self.__create_table_subtable_relation()

        start_index = 0
        for left_table in table_subtable_relation:
            self.__choose_relation(table_subtable_relation, left_table, start_index)
            start_index += 1

    def __create_table_subtable_relation(self):
        table_subtable_relation = []
        for table in self.__schema:
            for sub_table, relation in self.__schema[table]['relations'].iteritems():
                table_subtable_relation.append({'table' : table.lower(), 'subtable' : sub_table.lower(), 'relation': relation})
        return table_subtable_relation

    def __choose_relation(self, table_subtable_relation, left_table, start_index):
        for right_table in table_subtable_relation[start_index:len(table_subtable_relation)]:
                if left_table['table'] == right_table['subtable'] and right_table['table'] == left_table['subtable']:
                    if (left_table['relation'] == 'one' and right_table['relation'] == 'many'):
                        self.__build_many_to_one(left_table['table'], left_table['subtable'])    
                    elif (left_table['relation'] == 'many' and right_table['relation'] == 'one'):
                        self.__build_many_to_one(left_table['subtable'], left_table['table'])
                    elif (left_table['relation'] == 'many' and right_table['relation'] == 'many'):
                        self.__build_many_to_many(left_table['table'], left_table['subtable'])

    def __build_many_to_one(self, child_entity, parent_entity):
        new_alter = FOREIGN_KEY.format(table = child_entity, target = parent_entity)
        self._alters.add(new_alter)

    def __build_many_to_many(self, left_entity, right_entity):
        table = UNION_TABLE.format(left_table=left_entity, right_table=right_entity)
        self._tables.add(table)

        union_table_name = '{left_table}__{right_table}'.format(left_table=left_entity, right_table=right_entity)
        right_table_alter = MANY_MANY_FOREIGN_KEY.format(table=left_entity, target=right_entity, table_save=union_table_name)
        self._alters.add(right_table_alter) 
        left_table_alter = MANY_MANY_FOREIGN_KEY.format(table=right_entity, target=left_entity, table_save=union_table_name) 
        self._alters.add(left_table_alter)

        trigger = TRIGGER.format(table = union_table_name)
        self._triggers.add(trigger)

    def __build_triggers(self):
        for table_name in self.__schema:
            table_name_low = table_name.lower()

            trigger = TRIGGER.format(table = table_name_low)
            self._triggers.add(trigger)

    def build_ddl(self, filename):
        with open(filename) as f:
            self.__schema = yaml.load(f)

        self.__build_tables()
        self.__build_relations()
        self.__build_triggers()

    def clear(self):
        self._tables.clear()
        self._alters.clear()
        self._triggers.clear()

    def dump(self, filename):
        with open(filename, 'w') as out:
            out.write('\n'.join(self._tables))
            out.write('\n')
            out.write('\n'.join(self._alters))
            out.write('\n')
            out.write('\n'.join(self._triggers))


if __name__ == "__main__":
    g = Generator()

    g.build_ddl('schema.yaml')
    g.dump('schema1.sql')

    g.clear()

    # g.build_ddl('another.yaml')
    # g.dump('another.sql')













# # !/usr/bin/python
# # -*- coding: utf-8 -*-

# import yaml

# CREATE_TABLE = """CREATE TABLE "{table}" (
#     "{table}_id" SERIAL PRIMARY KEY,
#     {columns},
#     "{table}_created" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),
#     "{table}_updated" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)
# );
# """
# CREATED = '"{table}_created" INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)'
# UPDATED = '"{table}_updated" INTEGER NOT NULL DEFAULT 0'
# FOREIGN_KEY = """ALTER TABLE "{table}" ADD "{target}_id" INTEGER NOT NULL,
#     ADD CONSTRAINT "fk_{table}_{target}_id" FOREIGN KEY ("{target}_id") REFERENCES "{target}" ("{target}_id");
# """
# MANY_MANY_FOREIGN_KEY = """ALTER TABLE {table_save} ADD CONSTRAINT "fk_{table}_{target}_id" 
# FOREIGN KEY ("{target}_id") REFERENCES "{target}" ("{target}_id");
# """
# UNION_TABLE = """CREATE TABLE "{left_table}__{right_table}" (
#     "{left_table}_id" INTEGER NOT NULL,
#     "{right_table}_id" INTEGER NOT NULL,
#     PRIMARY KEY ("{left_table}_id", "{right_table}_id")
# );
# """
# TRIGGER = """CREATE OR REPLACE FUNCTION update_{table}_timestamp()
# RETURNS TRIGGER AS $$
# BEGIN
#    NEW.{table}_updated = cast(extract(epoch from now()) as integer);
#    RETURN NEW;
# END;
# $$ language 'plpgsql';
# CREATE TRIGGER "tr_{table}_updated" BEFORE UPDATE ON "{table}" FOR EACH ROW EXECUTE PROCEDURE update_{table}_timestamp();
# """

# class Generator(object):
#     def __init__(self):
#         self._alters   = set()
#         self._tables   = set()
#         self._triggers = set()

#     def __build_tables(self):
#         for table_name in self.__schema:
#             table_name_low = table_name.lower()
#             fields = self.__build_columns(self.__schema[table_name], table_name_low)

#             fields_join = ',\n    '.join(fields)
#             new_table = CREATE_TABLE.format(table = table_name_low, columns = fields_join)
#             self._tables.add(new_table)
        
#     def __build_columns(self, entity, table_name_low):
#         fields = []
#         for field_name, field_type in entity['fields'].iteritems():
#             fields_elements = '"{}_{}" {} NOT NULL'.format(table_name_low, field_name, field_type)
#             fields.append(fields_elements)
#         return fields

#     def __build_relations(self):
#         table_subtable_relation = self.__create_table_subtable_relation()

#         start_index = 0
#         for left_table in table_subtable_relation:
#             self.__choose_relation(table_subtable_relation, left_table, start_index)
#             start_index += 1

#     def __create_table_subtable_relation(self):
#         table_subtable_relation = []
#         for table in self.__schema:
#             for sub_table, relation in self.__schema[table]['relations'].iteritems():
#                 table_subtable_relation.append({'table' : table.lower(), 'subtable' : sub_table.lower(), 'relation': relation})
#         return table_subtable_relation

#     def __choose_relation(self, table_subtable_relation, left_table, start_index):
#         for right_table in table_subtable_relation[start_index:len(table_subtable_relation)]:
#                 if left_table['table'] == right_table['subtable'] and right_table['table'] == left_table['subtable']:
#                     if (left_table['relation'] == 'one' and right_table['relation'] == 'many'):
#                         self.__build_many_to_one(left_table['table'], left_table['subtable'])    
#                     elif (left_table['relation'] == 'many' and right_table['relation'] == 'one'):
#                         self.__build_many_to_one(left_table['subtable'], left_table['table'])
#                     elif (left_table['relation'] == 'many' and right_table['relation'] == 'many'):
#                         self.__build_many_to_many(left_table['table'], left_table['subtable'])

#     def __build_many_to_one(self, child_entity, parent_entity):
#         new_alter = FOREIGN_KEY.format(table = child_entity, target = parent_entity)
#         self._alters.add(new_alter)

#     def __build_many_to_many(self, left_entity, right_entity):
#         table = UNION_TABLE.format(left_table=left_entity, right_table=right_entity)
#         self._tables.add(table)

#         union_table_name = '{left_table}__{right_table}'.format(left_table=left_entity, right_table=right_entity)
#         right_table_alter = MANY_MANY_FOREIGN_KEY.format(table=left_entity, target=right_entity, table_save=union_table_name)
#         self._alters.add(right_table_alter) 
#         left_table_alter = MANY_MANY_FOREIGN_KEY.format(table=right_entity, target=left_entity, table_save=union_table_name) 
#         self._alters.add(left_table_alter)

#         trigger = TRIGGER.format(table = union_table_name)
#         self._triggers.add(trigger)

#     def __build_triggers(self):
#         for table_name in self.__schema:
#             table_name_low = table_name.lower()

#             trigger = TRIGGER.format(table = table_name_low)
#             self._triggers.add(trigger)

#     def build_ddl(self, filename):
#         with open(filename) as f:
#             self.__schema = yaml.load(f)

#         self.__build_tables()
#         self.__build_relations()
#         self.__build_triggers()

#     def clear(self):
#         self._tables.clear()
#         self._alters.clear()
#         self._triggers.clear()

#     def dump(self, filename):
#         with open(filename, 'w') as out:
#             out.write('\n'.join(self._tables))
#             out.write('\n')
#             out.write('\n'.join(self._alters))
#             out.write('\n')
#             out.write('\n'.join(self._triggers))


# if __name__ == "__main__":
#     g = Generator()

#     g.build_ddl('schema.yaml')
#     g.dump('schema1.sql')

#     g.clear()

#     # g.build_ddl('another.yaml')
#     # g.dump('another.sql')
