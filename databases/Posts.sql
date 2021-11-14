PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS posts (
	id INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	text TEXT NOT NULL,
	timestamp INTEGER DEFAULT CURRENT_TIMESTAMP,
	repost_url TEXT
);

INSERT INTO posts(username, text) VALUES('zachattack', 'Just finished project 2 for CPSC 449!');
INSERT INTO posts(username, text) VALUES('zachattack', 'Idk what to post but I gotta post something...');
INSERT INTO posts(username, text) VALUES('willum', 'whens the next ludum dare?');
INSERT INTO posts(username, text) VALUES('joachim', 'where the heck is Jose?');

CREATE INDEX IF NOT EXISTS post_timestamp_idx ON posts(timestamp);
