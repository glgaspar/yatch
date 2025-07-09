
create table if not exists boards (
    id varchar(30) not null PRIMARY KEY,
    name varchar(55) not null,
    desc varchar(255) null,
    closed boolean not null,
    dateClosed TIMESTAMP null,
    url VARCHAR(255) not null
);

create table if not exists members (
    idBoard varchar(30) not null REFERENCES boards(id) on update cascade on delete cascade,
    id varchar(30) not null,
    fullName VARCHAR(180) not null,
    username VARCHAR(180) not null,
    PRIMARY KEY (idBoard, id)
);

create table if not exists lists (
    idBoard varchar(30) not null REFERENCES boards(id) on update cascade on delete cascade,
    id varchar(30) not null,
    name varchar(55) not null,
    closed boolean not null,
    PRIMARY KEY (idBoard, id)
); 

create table if not exists cards (
    idList varchar(30) not null REFERENCES boards(id) on update cascade on delete cascade,
    id varchar(30) not null,
    name VARCHAR(255) not null,
    desc text null,
    due TIMESTAMP null,
    closed boolean,
    dateLastActivity TIMESTAMP,
    labels string,
    url VARCHAR(255) not null,
    PRIMARY KEY (idList, id)
);

create table if not exists comments (
    id varchar(30) not null PRIMARY KEY,
    idCard varchar(30) not null REFERENCES boards(id) on update cascade on delete cascade,
    idMemberCreator varchar(30) not null REFERENCES members(id) on update cascade on delete cascade,
    text text NOT null,
    date TIMESTAMP not null
);
