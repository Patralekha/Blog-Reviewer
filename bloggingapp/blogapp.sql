Table users
CREATE TABLE users(
userid SERIAL PRIMARY KEY,
username VARCHAR NOT NULL,
email VARCHAR NOT NULL,
password VARCHAR NOT NULL
);

Table blogs
CREATE TABLE blogs(
blogid SERIAL PRIMARY KEY,
creatorid INTEGER REFERENCES users(userid),
likeno INTEGER,
dislikeno INTEGER,
commentno INTEGER
);

Table usercomments
CREATE TABLE usercomments(
commentid SERIAL PRIMARY KEY,
userid INTEGER REFERENCES users(userid),
blogid INTEGER REFERENCES blogs(blogid),
comments VARCHAR
);

Table userlikes
CREATE TABLE userlikes(
id SERIAL PRIMARY KEY,
userid INTEGER REFERENCES users(userid),
blogid INTEGER REFERENCES blogs(blogid),
likecount INTEGER,
dislikecount INTEGER
);
