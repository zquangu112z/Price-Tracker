drop table if exists product;
create table product (
  id integer primary key autoincrement,
  url_product text not null,
  current_price text not null,
  desired_price text not null,
  email text not null
);
