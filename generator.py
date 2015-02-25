# #!/usr/bin/python
# # -*- coding: utf-8 -*-
import yaml

class Generator(object):
	__create_table = "CREATE TABLE \"{table}\" (\n\
	{table}_id serial,\n" + '{fields}' + \
			',\n    PRIMARY KEY ({table}_id)' + '\n);\n'
	__time_table = 'ALTER TABLE {table} ADD COLUMN {table}_{function} timestamp;\n\
ALTER TABLE {table} ALTER COLUMN {table}_{function} SET NOT NULL;\n\
ALTER TABLE {table} ALTER COLUMN {table}_{function} SET DEFAULT now();\n'
	__trigger = 'CREATE OR REPLACE FUNCTION {table}_timestamp_update()\n\
RETURNS TRIGGER AS $$\n\
BEGIN\n\
	NEW.{table}_updated = now();\n\
	RETURN NEW;\n\
END;\n\
$$ language \'plpgsql\';\n\
CREATE TRIGGER \"tr_{table}_updated\" BEFORE UPDATE ON \"{table}\" \
FOR EACH ROW EXECUTE PROCEDURE {table}_timestamp_update();\n'

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
				fields_elements = '{}_{} {} NOT NULL'.format(table_name_low, key, value)
				fields_list.append(fields_elements)
				fields_join = '    ' + ',\n    '.join(fields_list)
				new_table = self.__create_table.format(table = table_name_low, fields = fields_join)
			tables.append(new_table)

		return '\n'.join(tables) + '\n'

	def timestamps(self):
		timestamp_and_trigger = list()

		for elem in self.load:
			table_name = elem
			table_name_low = elem.lower()

			timestamp_created = self.__time_table.format(table = table_name_low, function = 'created')
			timestamp_updated = self.__time_table.format(table = table_name_low, function = 'updated')

			trigger = self.__trigger.format(table = table_name_low)
			timestamp_and_trigger.append(timestamp_created+'\n'+timestamp_updated+'\n'+trigger)

		return '\n'.join(timestamp_and_trigger)

if __name__ == "__main__":
    generator = Generator('file.yml')

    fields = generator.fields()
    timestamps = generator.timestamps()
    generator.save('schema.sql', fields+timestamps)
 