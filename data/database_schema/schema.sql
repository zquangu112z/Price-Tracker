drop table if exists product;

drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null,
  user_type integer default 0
);

create table product (
  id integer primary key autoincrement,
  author_id integer not null,
  url_product text not null,
  submited_price text not null,
  desired_price text not null,
  submit_time integer,
  price_path  text,
  isdone integer default 0
);

/* isdone:
  0: following (default)
  1: done
  2: stop following
*/

/* user_type:
  0: normal (default), is limited about the number of following products, e.g: 5
  1: vip
*/