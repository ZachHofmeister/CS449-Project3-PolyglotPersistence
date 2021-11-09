PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS users(
	id INTEGER PRIMARY KEY,
	username TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	bio TEXT
);
INSERT INTO users VALUES(1, 'zachattack', 'zach@gmail.com', 'password', 'cs student csuf');
INSERT INTO users VALUES(2, 'willum', 'will@gmail.com', '12345', 'engineering major');
INSERT INTO users VALUES(3, 'joachim', 'joachim@cox.net', '#iwantmyroommatetomoveout', 'plays some nice keys');

CREATE TABLE IF NOT EXISTS followers (
	id INTEGER PRIMARY KEY,
	follower_id INTEGER NOT NULL REFERENCES users(id),
	following_id INTEGER NOT NULL REFERENCES users(id),

	UNIQUE(follower_id, following_id)
);

INSERT INTO followers(follower_id, following_id) VALUES(1, 2);
INSERT INTO followers(follower_id, following_id) VALUES(1, 3);
INSERT INTO followers(follower_id, following_id) VALUES(2, 1);
INSERT INTO followers(follower_id, following_id) VALUES(2, 3);
INSERT INTO followers(follower_id, following_id) VALUES(3, 2);

CREATE VIEW IF NOT EXISTS following
AS
    SELECT users.username as followername, friends.username as friendname
    FROM users, followers, users AS friends
    WHERE
        users.id = followers.follower_id AND
        followers.following_id = friends.id;

CREATE TABLE IF NOT EXISTS posts (
	id INTEGER PRIMARY KEY,
	username TEXT NOT NULL REFERENCES users(username),
	text TEXT NOT NULL,
	timestamp INTEGER DEFAULT CURRENT_TIMESTAMP,
	repost_url TEXT
);

INSERT INTO posts(username, text) VALUES('zachattack', 'Just finished project 2 for CPSC 449!');
INSERT INTO posts(username, text) VALUES('zachattack', 'Idk what to post but I gotta post something...');
INSERT INTO posts(username, text) VALUES('willum', 'whens the next ludum dare?');
INSERT INTO posts(username, text) VALUES('joachim', 'where the heck is Jose?');

CREATE INDEX IF NOT EXISTS post_timestamp_idx ON posts(timestamp);
