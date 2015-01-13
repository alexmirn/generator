CREATE TABLE "article" (
    article_id serial,
    article_title text NOT NULL,
    article_text  text NOT NULL,
    article_created timestamp NOT NULL DEFAULT now(),
    article_updated timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (article_id)
);

CREATE TABLE "category" (
    category_id serial,
    category_title text NOT NULL,
    category_created timestamp NOT NULL DEFAULT now(),
    category_updated timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (category_id)
);

CREATE OR REPLACE FUNCTION article_timestamp_update()
RETURNS TRIGGER AS $$
BEGIN
	NEW.article_updated = now();
	RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER "tr_article_updated" BEFORE UPDATE ON "article" FOR EACH ROW EXECUTE PROCEDURE article_timestamp_update();

CREATE OR REPLACE FUNCTION category_timestamp_update()
RETURNS TRIGGER AS $$
BEGIN
	NEW.category_updated = now();
	RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER "tr_category_updated" BEFORE UPDATE ON "category" FOR EACH ROW EXECUTE PROCEDURE category_timestamp_update();

INSERT INTO article (article_title, article_text) VALUES
('3 WORLD WAR', 'вторая мировая'),
('4 WORLD WAR', 'IN 2050 4 WORLD WAR COULD BEGIN')
;

UPDATE article
SET article_title = 'other war'
WHERE
article_id = 1;