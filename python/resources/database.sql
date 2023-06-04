create table documents
(
    id         serial
        primary key,
    title      varchar(100),
    file_data  bytea,
    word_count integer default 0 not null
);

create table words
(
    id   serial
        primary key,
    word varchar(50) not null
        unique
);

create table word_documents
(
    id          serial
        primary key,
    word_id     integer
        references words,
    document_id integer
        references documents,
    count       integer not null
);

