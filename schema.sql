create table user_account (
    id SERIAL PRIMARY KEY,
    username varchar(50),
    password varchar(200),
    firstname varchar(30),
    middlename varchar(30),
    lastname varchar(30),
    email varchar(50),
    is_active boolean,
    is_validated boolean,
    last_login timestamp
);