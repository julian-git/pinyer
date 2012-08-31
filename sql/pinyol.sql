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
create table casteller (
  id   	     int	not null auto_increment,
  name 	     varchar(100) not null,
  total_height      float(10,2) default 170,
  shoulder_height   float(10,2) default 150,
  axle_height       float(10,2) default 140,
  hip_height        float(10,2) default 60,
  stretched_height  float(10,2) default 220,
  shoulder_width    float(10,2) default 70,
  circumference     float(10,2) default 100,
  weight            float(10,2) default 60,
  strength 	    float(10,2) default 5,
  primary key (id)
) engine=InnoDB default character set utf8;

/** 
 *   The collas that a certain casteller belongs to
 */
create table casteller_colla (
  casteller_id  int  not null,
  colla_id   int  not null,
  foreign key (casteller_id) references casteller(id),
  foreign key (colla_id) references colla(id)
) engine=InnoDB default character set utf8;

/**
 *  The roles that a certain casteller can fulfill in a castell
 */
create table casteller_role (
  casteller_id  int  not null,
  role_id   int  not null,
  foreign key (casteller_id) references casteller(id),
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
  is_essential bool     not null default true,
  svg_id     varchar(20) not null,
  svg_text   varchar(20) not null,
  svg_elem   varchar(20) not null default 'rect',
  x 	     float(10,2) not null,
  y 	     float(10,2) not null,
  w 	     float(10,2) default 120,
  h 	     float(10,2) default 40,
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
  relation_type int not null,
  field_name    varchar(20) not null,
  from_pos_id int default null,
  to_pos_id   int default null,
  fparam1 	float(10,4) default 0,
  fparam2 	float(10,4) default 0,
  iparam1 	int default 0,
  iparam2 	int default 0,
  primary key (id),
  foreign key (castell_type_id) references castell_type (id),
  foreign key (from_pos_id) references castell_position (id),
  foreign key (to_pos_id) references castell_position (id)
) engine=InnoDB default character set utf8;

/** 
 *  Which castellers dont get along and have to be separated?
 */ 
create table incompatible_castellers (
  id   	   int  not null auto_increment,
  colla_id int not null,
  cast1_id  int not null,
  cast2_id  int not null,
  primary key (id),
  foreign key (colla_id) references colla(id),
  foreign key (cast1_id) references casteller(id),         
  foreign key (cast2_id) references casteller(id)
) engine=InnoDB default character set utf8;

/**
 *  Which castells has a colla executed, and with which result?
 */ 
create table executed_castell (
  id   	       int  not null auto_increment,
  colla_id     int  not null,
  castell_type_id int not null,
  execution_date  timestamp default current_timestamp,
  result       varchar(20) default 'descarregat',
  comment      varchar(255) default null,
  primary key (id),
  foreign key (colla_id) references colla(id),
  foreign key (castell_type_id) references castell_type (id)
) engine=InnoDB default character set utf8;

/** 
 *  What has each casteller done in each executed castell, 
 *  and what was his strength that day?
 */
create table executed_castell_position (
  id   	       int  not null auto_increment,
  executed_castell_id int not null,
  casteller_id    int  not null,
  role_id      int  not null,
  position_id  int  not null,
  current_strength     int default 5,
  primary key (id),
  foreign key (executed_castell_id) references executed_castell(id),
  foreign key (casteller_id) references casteller(id),
  foreign key (role_id) references role (id),
  foreign key (position_id) references castell_position (id)
) engine=InnoDB default character set utf8;
