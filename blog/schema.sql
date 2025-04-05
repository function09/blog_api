DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS blog_posts;
DROP TABLE IF EXISTS blog_content;

CREATE TABLE user(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT UNIQUE NOT NULL, 
		password TEXT NOT NULL
);

CREATE TABLE blog_posts(
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			user_id INTEGER NOT NULL,
			created_at TEXT NOT NULL,
			blog_title TEXT NOT NULL,
			synopsis TEXT NOT NULL,
			FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE blog_content(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			blog_post_id INTEGER NOT NULL,
			blog_post TEXT NOT NULL,
			FOREIGN KEY (blog_post_id) REFERENCES blog_posts(id) 
);

