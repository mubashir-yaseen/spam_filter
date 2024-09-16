CREATE DATABASE phishsheild;
use phishsheild;

CREATE TABLE hashtable(
	hashes VARCHAR(5000)
);

CREATE TABLE urltable(
	urls VARCHAR(500)
);

CREATE TABLE euser(
	id INT IDENTITY(1,1) PRIMARY KEY,
	email VARCHAR(500),
	rep INT
);

SELECT * from hashtable;
SELECT * from urltable;