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
  role1   int default null,
  role2   int default null,
  role3   int default null,
  role4   int default null,  
  role5   int default null,
  primary key (id),
  foreign key (role1) references role(id),
  foreign key (role2) references role(id),
  foreign key (role3) references role(id),
  foreign key (role4) references role(id),
  foreign key (role5) references role(id)
) engine=InnoDB default character set utf8;

create table castell (
  id   	     int	not null auto_increment,     
  colla      int        not null,
  name 	     varchar(10) not null,
  description varchar(255) default null,
  primary key (id),
  foreign key (colla) references colla (id)
) engine=InnoDB default character set utf8;

create table position (
  id   	     int	not null auto_increment,     
  castell    int 	not null,
  role 	     int 	not null,
  x 	     float(3,2)	not null,
  y 	     float(3,2) not null,
  primary key (id),
  foreign key (castell) references castell (id),
  foreign key (role) references role (id)
) engine=InnoDB default character set utf8;
