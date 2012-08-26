insert into colla (id, name, city) values
  (1, "cvg", "Barcelona/Gràcia");

insert into role values
  (1, "crossa"),
  (2, "baix"),
  (3, "contrafort"),
  (4, "vent"),
  (5, "mà"),
  (6, "agulla"), 
  (7, "pinya");

insert into member (name)  values 
  ("crossa1"),
  ("crossa2"),	
  ("baix1"),
  ("baix2"),
  ("contrafort1"),
  ("contrafort2"),
  ("vent1"),
  ("vent2"),
  ("mà1"),
  ("mà2"),
  ("agulla1"), 
  ("agulla2"), 
  ("pinya1"),  
  ("pinya2"),  
  ("pinya3"),  
  ("pinya4"),  
  ("pinya5"),  
  ("pinya6");

insert into member_colla values
  (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1),
  (11,1), (12,1), (13,1), (14,1), (15,1), (16,1), (17,1), (18,1);

insert into member_role values
  (1,1), (2,1), (3,2), (4,2), (5,3), (6,3), (7,4), (8,4), (9,5), (10,5),
  (11,6), (12,6), (13,7), (14,7), (15,7), (16,7), (17,7), (18,7);

insert into castell_type values 
  (1, 1, "p4", "Pilar de 4"),
  (2, 1, "2de8f", "Torre de vuit amb folre");

insert into castell_position (id, castell_type_id, role_id, svg_id, svg_text, x, y) values
  (1, 1, 1, "crossa1", "Crossa 1", 500, -100),
  (2, 1, 1, "crossa2", "Crossa 2", 500, -500),
  (3, 1, 5, "ma1", "Ma 1", 100, 600);