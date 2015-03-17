# __all__ = ['create_table', 'time_table', 'trigger']
# __all__ = [PostgreSQL()]

class PostgreSQL(object):
	def __init__(self):
		self.create_table = '''CREATE TABLE "{table}" (
	{table}_id serial,
	{fields},
	PRIMARY KEY ({table}_id)
);'''

		self.time_table = '''ALTER TABLE {table} ADD COLUMN {table}_{function} timestamp;
ALTER TABLE {table} ALTER COLUMN {table}_{function} SET NOT NULL;
ALTER TABLE {table} ALTER COLUMN {table}_{function} SET DEFAULT now();'''

		self.trigger = '''CREATE OR REPLACE FUNCTION {table}_timestamp_update()
RETURNS TRIGGER AS $$
BEGIN
	NEW.{table}_updated = now();
	RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER "tr_{table}_updated" BEFORE UPDATE ON "{table}" 
FOR EACH ROW EXECUTE PROCEDURE {table}_timestamp_update();'''




# create_table = '''CREATE TABLE "{table}" (
# 	{table}_id serial,
# 	{fields},
# 	PRIMARY KEY ({table}_id)
# );'''

# time_table = '''ALTER TABLE {table} ADD COLUMN {table}_{function} timestamp;
# ALTER TABLE {table} ALTER COLUMN {table}_{function} SET NOT NULL;
# ALTER TABLE {table} ALTER COLUMN {table}_{function} SET DEFAULT now();'''

# trigger = '''CREATE OR REPLACE FUNCTION {table}_timestamp_update()
# RETURNS TRIGGER AS $$
# BEGIN
# 	NEW.{table}_updated = now();
# 	RETURN NEW;
# END;
# $$ language 'plpgsql';
# CREATE TRIGGER "tr_{table}_updated" BEFORE UPDATE ON "{table}" 
# FOR EACH ROW EXECUTE PROCEDURE {table}_timestamp_update();'''
