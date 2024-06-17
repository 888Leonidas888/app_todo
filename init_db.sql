create database todo_db;
use todo_db;
create table table_todo(id int auto_increment primary key,
                        title varchar(255) not null,
                        description text not null,
                        status boolean not null);