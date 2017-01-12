drop table if exists persons;
create table persons(
	id integer primary key autoincrement,
	name text not null,
	address text not null,
	skills text not null
);
