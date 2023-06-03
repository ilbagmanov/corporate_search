CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    file_data bytea
);

CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE word_documents (
    id SERIAL PRIMARY KEY,
    word_id INT REFERENCES words(id),
    document_id INT REFERENCES documents(id)
);

