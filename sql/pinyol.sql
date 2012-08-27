/**
 *  General information about the colla
 */
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

/**
 *  The different roles in a castell: crosses, mans, vents, ...
 */
create table role (
  id   	     int	not null auto_increment,
  name 	     varchar(100) not null,
  primary key (id)
) engine=InnoDB default character set utf8;

/**
 *   Some information about the members of a colla, 
 *   especially their physical characteristics
 */
create table member (
  id   	     int	not null auto_increment,
  name 	     varchar(100) not null,
  total_height      float(10,2) default 0,
  shoulder_height   float(10,2) default 0,
  hip_height        float(10,2) default 0,
  stretched_height  float(10,2) default 0,
  weight            float(10,2) default 0,
  primary key (id)
) engine=InnoDB default character set utf8;

/** 
 *   The collas that a certain member belongs to
 */
create table member_colla (
  member_id  int  not null,
  colla_id   int  not null,
  foreign key (member_id) references member(id),
  foreign key (colla_id) references colla(id)
) engine=InnoDB default character set utf8;

/**
 *  The roles that a certain member can fulfill in a castell
 */
create table member_role (
  member_id  int  not null,
  role_id   int  not null,
  foreign key (member_id) references member(id),
  foreign key (role_id) references role(id)
) engine=InnoDB default character set utf8;

/** 
 *  The different types of castell that each colla does: p4, 2de8f, ...
 */
create table castell_type (
  id   	     int	not null auto_increment,     
  colla_id   int        not null,
  name 	     varchar(10) not null,
  description varchar(255) default null,
  primary key (id),
  foreign key (colla_id) references colla(id)
) engine=InnoDB default character set utf8;

/** 
 *  The data for displaying the positions in each type of castell
 */ 
create table castell_position (
  id   	     int	not null auto_increment,     
  castell_type_id int 	not null,
  role_id     int 	not null,
  svg_id     varchar(20) not null,
  svg_text   varchar(20) not null,
  x 	     float(10,2) not null,
  y 	     float(10,2) not null,
  w 	     float(10,2) default null,
  h 	     float(10,2) default null,
  rx 	     float(10,2) default null,
  ry 	     float(10,2) default null,
  primary key (id),
  foreign key (castell_type_id) references castell_type (id),
  foreign key (role_id) references role (id)
) engine=InnoDB default character set utf8;

/**
 *  The data for establishing relations between two positions in a given castell
 */
create table castell_relation (
  id   	       int  not null auto_increment,
  castell_type_id int 	not null,
  from_position int not null,
  to_position   int default null,
  weight 	float(10,4) default 0,
  primary key (id),
  foreign key (castell_type_id) references castell_type (id),
  foreign key (from_position) references castell_position (id),
  foreign key (to_position) references castell_position (id)
) engine=InnoDB default character set utf8;

/**
 *  Which castells has a colla executed, and with which result?
 */ 
create table executed_castell (
  id   	       int  not null auto_increment,
  colla_id     int  not null,
  castell_type_id int not null,
  execution_date  timestamp default current_timestamp,
  result       varchar(20) default null,
  comment      varchar(255) default null,
  primary key (id),
  foreign key (colla_id) references colla(id),
  foreign key (castell_type_id) references castell_type (id)
) engine=InnoDB default character set utf8;

/** 
 *  What has each member done in each executed castell, 
 *  and what was his strength that day?
 */
create table executed_castell_position (
  id   	       int  not null auto_increment,
  executed_castell_id int not null,
  member_id    int  not null,
  role_id      int  not null,
  position_id  int  not null,
  strength     int default 5,
  primary key (id),
  foreign key (executed_castell_id) references executed_castell(id),
  foreign key (member_id) references member(id),
  foreign key (role_id) references role (id),
  foreign key (position_id) references castell_position (id)
) engine=InnoDB default character set utf8;
