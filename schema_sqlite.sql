create table user_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    firstname TEXT,
    middlename TEXT,
    lastname TEXT,
    email TEXT,
    is_active BOOLEAN,
    is_validated BOOLEAN,
    is_anonymous BOOLEAN
);