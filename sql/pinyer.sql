/**
 *  General information about the colla
 */
create table colla (
  id_name    varchar(30)   not null,
  name 	     varchar(255) not null,
  city 	     varchar(255) not null,
  cap 	     varchar(255) default null,
  phone1     varchar(50)  default null,
  phone2     varchar(50)  default null,      
  email      varchar(50)  default null,
  web 	     varchar(255) default null,
  primary key (id_name)
) engine=InnoDB default character set utf8;


/**
 *  The different roles in a castell: crosses, mans, vents, ...
 */
create table role (
  name 	     varchar(30) not null,
  primary key (name)
) engine=InnoDB default character set utf8;


/**
 *   Some information about the members of a colla, 
 *   especially their physical characteristics
 */
create table casteller (
  id   	     	    int	not null auto_increment,
  nickname     	    varchar(30) not null,
  first_name  	    varchar(100) default '',
  last_name  	    varchar(100) default '',
  picture_path 	    varchar(150) default '',
  total_height      float(10,2) default 170,
  shoulder_height   float(10,2) default 150,
  axle_height       float(10,2) default 140,
  hip_height        float(10,2) default 60,
  stretched_height  float(10,2) default 220,
  shoulder_width    float(10,2) default 70,
  circumference     float(10,2) default 100,
  weight            float(10,2) default 60,
  strength 	    float(10,2) default 5,
  svg_rep           varchar(1000) default '',
  alt_text          varchar(1000) default '',
  is_present 	    bool default true,
  last_revision     timestamp default current_timestamp,
  primary key (id),
  key(nickname),
  key(is_present)
) engine=InnoDB default character set utf8;


/**
 *  When has a casteller become available/unavailable for making castells?
 */
create table casteller_availability (
  id   	     int	not null auto_increment,
  casteller_id int  not null,
  available  bool   not null,
  ts        timestamp default current_timestamp,
  primary key (id),
  foreign key (casteller_id) references casteller (id),
  key (ts)
) engine=InnoDB default character set utf8;


/** 
 *   The collas that a certain casteller belongs to
 */
create table casteller_colla (
  casteller_id  int  not null,
  colla_id_name   varchar(30)  not null,
  foreign key (casteller_id) references casteller(id),
  foreign key (colla_id_name) references colla(id_name)
) engine=InnoDB default character set utf8;

/**
  *  The roles that a certain casteller can fulfill in a castell
  */
 create table casteller_role (
   casteller_id  int  not null,
   role   varchar(30)  not null,
   foreign key (casteller_id) references casteller(id),
   foreign key (role) references role(name)
) engine=InnoDB default character set utf8;


/** 
 *  The different types of castell that each colla does: p4, 2de8f, ...
 */
create table castell_type (
  id_name 	     varchar(100) not null,     
  colla_id_name   varchar(30)        not null,
  name        varchar(100),
  description varchar(255) default null,
  primary key (id_name),
  foreign key (colla_id_name) references colla(id_name)
) engine=InnoDB default character set utf8;


/** 
 *  Which castellers don't get along and have to be separated?
 */ 
create table incompatible_castellers (
  id   	   int  not null auto_increment,
  colla_id_name varchar(30) not null,
  cast1_id  int not null,
  cast2_id  int not null,
  primary key (id),
  foreign key (colla_id_name) references colla(id_name),
  foreign key (cast1_id) references casteller(id),         
  foreign key (cast2_id) references casteller(id)
) engine=InnoDB default character set utf8;


/**
 *  Which castells has a colla executed, and with which result?
 */ 
create table executed_castell (
  id   	        int  not null auto_increment,
  colla_id_name varchar(30)  not null,
  castell_name varchar(100) not null,
  execution_date  timestamp default current_timestamp,
  result       varchar(30) default 'descarregat',
  comment      varchar(255) default null,
  primary key (id),
  foreign key (colla_id_name) references colla(id_name),
  foreign key (castell_name) references castell_type (id_name)
) engine=InnoDB default character set utf8;


/** 
 *  What has each casteller done in each executed castell, 
 *  and what was his strength that day?
 */
create table executed_castell_position (
  id   	       int  not null auto_increment,
  executed_castell_id int not null,
  casteller_id    int  not null,
  role      varchar(30)  not null,
  position_id  int  not null,
  current_strength     int default 5,
  primary key (id),
  foreign key (executed_castell_id) references executed_castell(id),
  foreign key (casteller_id) references casteller(id),
  foreign key (role) references role (name)
) engine=InnoDB default character set utf8;
