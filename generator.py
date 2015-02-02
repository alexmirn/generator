# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# import sys, os, time, atexit
# import psycopg2
# import pprint
import yaml

class Generator(object):
	def __init__(self, file_name):
		self.file_name = file_name
		self.load = self.load()

	def load(self):
		with open(self.file_name) as schema:
			stream = schema.read()
    		return yaml.load(stream)

	def save(self, file_name, statements):
   	    with open(file_name, 'wb') as file_:
    		file_.write(statements)

	def fields(self):
		tables = list()

		for elem in self.load:
			table_name = elem
			table_name_low = elem.lower()
			fields_list = list()

			for key, value in self.load[table_name]['fields'].iteritems():
				fields_elements = '%s_%s %s NOT NULL' % (table_name_low, key, value)
				fields_list.append(fields_elements)
				fields_join = '    ' + ',\n    '.join(fields_list)
				new_table = "CREATE TABLE \"%s\" (\n\
			%s_id serial,\n" % (table_name_low, table_name_low) + fields_join + \
			',\n    PRIMARY KEY (%s_id)' % (table_name_low) + '\n);\n'
			tables.append(new_table)

		return '\n'.join(tables) + '\n'

	def timestamps(self):
		timestamp_and_trigger = list()

		for elem in self.load:
			table_name = elem
			table_name_low = elem.lower()

			timestamp_created = 'ALTER TABLE %s ADD COLUMN %s_created timestamp;\n\
ALTER TABLE %s ALTER COLUMN %s_created SET NOT NULL;\n\
ALTER TABLE %s ALTER COLUMN %s_created SET DEFAULT now();\n' % (table_name_low, table_name_low, \
	table_name_low, table_name_low, table_name_low, table_name_low)

			timestamp_updated = 'ALTER TABLE %s ADD COLUMN %s_updated timestamp;\n\
ALTER TABLE %s ALTER COLUMN %s_updated SET NOT NULL;\n\
ALTER TABLE %s ALTER COLUMN %s_updated SET DEFAULT now();\n' % (table_name_low, table_name_low, \
	table_name_low, table_name_low, table_name_low, table_name_low)

			trigger = 'CREATE OR REPLACE FUNCTION %s_timestamp_update()\n\
RETURNS TRIGGER AS $$\n\
BEGIN\n\
	NEW.%s_updated = now();\n\
	RETURN NEW;\n\
END;\n\
$$ language \'plpgsql\';\n\
CREATE TRIGGER \"tr_%s_updated\" BEFORE UPDATE ON \"%s\" FOR EACH ROW EXECUTE PROCEDURE %s_timestamp_update();\n' % \
		(table_name_low, table_name_low, table_name_low, table_name_low, table_name_low)

			timestamp_and_trigger.append(timestamp_created+'\n'+timestamp_updated+'\n'+trigger)

		return '\n'.join(timestamp_and_trigger)

if __name__ == "__main__":
    generator = Generator('file.yml')

    fields = generator.fields()
    timestamps = generator.timestamps()
    generator.save('schema.sql', fields+timestamps)
    


















