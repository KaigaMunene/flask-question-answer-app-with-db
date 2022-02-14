DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS answers;

CREATE TABLE questions (
    id Text PRIMARY KEY,
    title Text NOT NULL,
    question Text NOT NULL
);

CREATE TABLE answers(
    id Text PRIMARY KEY,
    answer NOT NULL,
    question_id TEXT NOT NULL,
    FOREIGN KEY(question_id)
        REFERENCES questions (id)
);