create table colla (
  id   	     int   not null auto_increment,
  name 	     varchar(255) not null,
  city 	     varchar(255) not null,
  cap 	     varchar(255) default null,
  phone1     varchar(50)  default null,
  phone2     varchar(50)  default null,      
  email      varchar(50)  default null,
  web 	     varchar(255) default null,
  primary key (id)
) engine=InnoDB default character set utf8;

create table role (
  id   	     int	not null auto_increment,
  name 	     varchar(100) not null,
  primary key (id)
) engine=InnoDB default character set utf8;

create table member (
  id   	     int	not null auto_increment,
  name 	     varchar(100) not null,
  total_height      float(3,2) default 0,
  shoulder_height   float(3,2) default 0,
  hip_height        float(3,2) default 0,
  stretched_height  float(3,2) default 0,
  weight            float(3,2) default 0,
  primary key (id)
) engine=InnoDB default character set utf8;

create table member_colla (
  member_id  int  not null,
  colla_id   int  not null,
  foreign key (member_id) references member(id),
  foreign key (colla_id) references colla(id)
) engine=InnoDB default character set utf8;

create table member_role (
  member_id  int  not null,
  role_id   int  not null,
  foreign key (member_id) references member(id),
  foreign key (role_id) references role(id)
) engine=InnoDB default character set utf8;

create table castell_type (
  id   	     int	not null auto_increment,     
  colla_id   int        not null,
  name 	     varchar(10) not null,
  description varchar(255) default null,
  primary key (id),
  foreign key (colla_id) references colla(id)
) engine=InnoDB default character set utf8;

create table position (
  id   	     int	not null auto_increment,     
  castell_type_id int 	not null,
  role_id     int 	not null,
  x 	     float(3,2)	not null,
  y 	     float(3,2) not null,
  primary key (id),
  foreign key (castell_type_id) references castell_type (id),
  foreign key (role_id) references role (id)
) engine=InnoDB default character set utf8;

create table executed_castell (
  id   	       int  not null auto_increment,     
  colla_id     int  not null,
  castell_type_id int not null,
  ts 	       timestamp default current_timestamp,
  member_id    int  not null,
  role_id      int  not null,
  position_id  int  not null,
  foreign key (colla_id) references colla(id),
  foreign key (castell_type_id) references castell_type (id),
  foreign key (member_id) references member(id),
  foreign key (role_id) references role (id),
  foreign key (position_id) references position(id)
) engine=InnoDB default character set utf8;