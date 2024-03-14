PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE iframe (id integer not null,title varchar(200),url varchar(500),idLogin integer not null,primary key(id),foreign key (idLogin) references login(id));
INSERT INTO iframe VALUES(1,'Rock','https://www.youtube.com/embed/Vco19mCx1qw?si=9Lf3ZIf--69XAGIY',1);
CREATE TABLE login (id integer not null,username varchar(50),password varchar(50),primary key(id));
INSERT INTO login VALUES(1,'oscar','123');
COMMIT;
