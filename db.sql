create table boards if not exists (
    id varchar(30) not null PRIMARY KEY,
    name varchar(55) not null,
    desc varchar(255) null,
    closed boolean not null,
    dateClosed TIMESTAMP null,
    url VARCHAR(255) not null
);

create table members if not exists (
    idBoard varchar(30) not null FOREIGN key REFERENCES boards(id),
    id varchar(30) not null,
    fullName VARCHAR(180) not null,
    username VARCHAR(180) not null,
    constraint members_pk PRIMARY KEY (idBoard, id)
);

create table lists if not exists (
    idBoard varchar(30) not null FOREIGN key REFERENCES boards(id),
    id varchar(30) not null PRIMARY KEY,
    name varchar(55) not null,
    closed boolean not null,
    constraint members_pk PRIMARY KEY (idBoard, id)
); 

create table cards if not exists (
    idList varchar(30) not null FOREIGN key REFERENCES boards(id),
    id varchar(30) not null,
    name VARCHAR(255) not null,
    desc text null,
    due TIMESTAMP null,
    closed boolean,
    dateLastActivity TIMESTAMP,
    labels string,
    url VARCHAR(255) not null,
    constraint members_pk PRIMARY KEY (idList, id)
);

create table comments if not exists (
    id varchar(30) not null PRIMARY KEY,
    idCard varchar(30) not null FOREIGN key REFERENCES boards(id),
    idMemberCreator varchar(30) not null FOREIGN key REFERENCES members(id),
    text text NOT null,
    date TIMESTAMP not null
);
