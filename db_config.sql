create database astraldb;
\connect astraldb

create table astraldb_projects (
	id SERIAL PRIMARY KEY,
	name varchar(255) unique,
	description text,
	author_team varchar(255),
	authors_list varchar(255)[],
	project_links_array JSONB
);

create table astraldb_tdl (
	id BIGSERIAL PRIMARY KEY,
	name text,
	state smallint
);

create table astraldb_users (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) not null,
	nickname VARCHAR(255) not null,
	passwd text not null,
	description text,
	joined_at TIMESTAMP default CURRENT_TIMESTAMP
);

create table astraldb_projectusers (
	id BIGSERIAL primary key,
	user_id INTEGER references astraldb_users(id),
	projects_id integer references astraldb_projects(id)
);
