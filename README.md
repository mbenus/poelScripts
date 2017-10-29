# poelScripts
Python scripts to copy data from redis to mysql


# mysql
CREATE DATABASE poel DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE miners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(96) not null,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE minerhistory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    minerId INT not null,
    hashes BIGINT not null,
    lastshare BIGINT not null,
    balance DOUBLE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (minerId) REFERENCES miners(id)
);
