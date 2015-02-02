CREATE TABLE "category" (
			category_id serial,
    category_title varchar(50) NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE "article" (
			article_id serial,
    article_text text NOT NULL,
    article_title varchar(50) NOT NULL,
    PRIMARY KEY (article_id)
);

ALTER TABLE category ADD COLUMN category_created timestamp;
ALTER TABLE category ALTER COLUMN category_created SET NOT NULL;
ALTER TABLE category ALTER COLUMN category_created SET DEFAULT now();

ALTER TABLE category ADD COLUMN category_updated timestamp;
ALTER TABLE category ALTER COLUMN category_updated SET NOT NULL;
ALTER TABLE category ALTER COLUMN category_updated SET DEFAULT now();

CREATE OR REPLACE FUNCTION category_timestamp_update()
RETURNS TRIGGER AS $$
BEGIN
	NEW.category_updated = now();
	RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER "tr_category_updated" BEFORE UPDATE ON "category" FOR EACH ROW EXECUTE PROCEDURE category_timestamp_update();

ALTER TABLE article ADD COLUMN article_created timestamp;
ALTER TABLE article ALTER COLUMN article_created SET NOT NULL;
ALTER TABLE article ALTER COLUMN article_created SET DEFAULT now();

ALTER TABLE article ADD COLUMN article_updated timestamp;
ALTER TABLE article ALTER COLUMN article_updated SET NOT NULL;
ALTER TABLE article ALTER COLUMN article_updated SET DEFAULT now();

CREATE OR REPLACE FUNCTION article_timestamp_update()
RETURNS TRIGGER AS $$
BEGIN
	NEW.article_updated = now();
	RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER "tr_article_updated" BEFORE UPDATE ON "article" FOR EACH ROW EXECUTE PROCEDURE article_timestamp_update();
