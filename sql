create database zhihu;
create table topic(id int auto_increment primary key not null,name varchar(20) not null,url varchar(200) not null)

create table artical(id int auto_increment primary key not null,title varchar(255) not null,author varchar(100) not null,topic_id int not null,type varchar(30) not null)

create table special(id int auto_increment primary key not null,content text not null,articleid int not null)
create table question(id int auto_increment primary key not null,question text not null,articalid int not null)

create table answer(id int auto_increment primary key not null,author varchar(30) not null,answer text,ques_id int not null)
