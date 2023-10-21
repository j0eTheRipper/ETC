CREATE TABLE "users" (
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"role"	TEXT NOT NULL DEFAULT 'student',
	PRIMARY KEY("username")
);

CREATE TABLE "subjects" (
	"subject"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("subject")
);

CREATE TABLE "tutors" (
	"name"	TEXT NOT NULL UNIQUE,
	"subject"	TEXT NOT NULL,
	FOREIGN KEY("subject") REFERENCES "subjects"("subject"),
	FOREIGN KEY("name") REFERENCES "users"("username")
);

CREATE TABLE "classes" (
	"class-id"	INTEGER NOT NULL UNIQUE,
	"subject"	TEXT NOT NULL,
	"tutor"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	FOREIGN KEY("subject") REFERENCES "subjects"("subject"),
	PRIMARY KEY("class-id" AUTOINCREMENT),
	FOREIGN KEY("tutor") REFERENCES "tutors"("name")
);

CREATE TABLE "students" (
	"name"	TEXT NOT NULL UNIQUE,
	"subjects"	BLOB NOT NULL,
	"ID"	TEXT NOT NULL UNIQUE,
	"fees"	INTEGER,
	FOREIGN KEY("name") REFERENCES "users"("username"),
	PRIMARY KEY("ID")
);