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

insert into casteller (name, total_height, shoulder_height, axle_height, hip_height, stretched_height, shoulder_width, weight, strength)  values 
  ("crossa1", 150, 130, 120, 50, 200, 70, 65, 5),
  ("crossa2", 155, 135, 125, 55, 205, 70, 70, 7),	
  ("baix1", 155, 135, 115, 55, 200, 70, 65, 5),
  ("baix2", 160, 140, 120, 60, 205, 70, 70, 7),
  ("contrafort1", 155, 135, 115, 55, 200, 70, 65, 5),
  ("contrafort2", 160, 140, 120, 60, 205, 70, 70, 7),
  ("vent1", 180, 160, 150, 70, 210, 70, 70, 5),
  ("vent2", 185, 165, 155, 75, 215, 70, 75, 7),
  ("mà1", 190, 170, 160, 80, 220, 70, 80, 5),
  ("mà2", 195, 175, 165, 85, 225, 70, 85, 7),
  ("agulla1", 155, 135, 115, 55, 200, 70, 65, 5),
  ("agulla2", 160, 140, 120, 60, 205, 70, 70, 7), 
  ("pinya1", 150, 130, 120, 50, 200, 70, 65, 2),  
  ("pinya2", 155, 135, 115, 55, 200, 70, 65, 3),  
  ("pinya3", 155, 135, 115, 55, 200, 70, 65, 4),  
  ("pinya4", 180, 160, 150, 70, 210, 70, 70, 5),  
  ("pinya5", 190, 170, 160, 80, 220, 70, 80, 6),  
  ("pinya6", 155, 135, 115, 55, 200, 70, 65, 7);

insert into casteller_colla values
  (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1),
  (11,1), (12,1), (13,1), (14,1), (15,1), (16,1), (17,1), (18,1);

insert into casteller_role values
  (1,1), (2,1), (3,2), (4,2), (5,3), (6,3), (7,4), (8,4), (9,5), (10,5),
  (11,6), (12,6), (13,7), (14,7), (15,7), (16,7), (17,7), (18,7);

insert into castell_type values 
  (1, 1, "p4", "Pilar de 4"),
  (2, 1, "2de8f", "Torre de vuit amb folre");

insert into castell_position (id, castell_type_id, role_id, svg_id, svg_text, x, y) values
  (1, 1, 1, "crossa1", "Crossa 1", 500, -100),
  (2, 1, 1, "crossa2", "Crossa 2", 500, -500),
  (3, 1, 5, "ma1", "Ma 1", 100, 600),
  (4, 1, 7, "pinya1", "Pinya 1", 100, 700),
  (5, 1, 7, "pinya2", "Pinya 2", 100, 800);

insert into castell_relation (id, castell_type_id, relation_type, from_position, to_position, fparam1, fparam2) values
  (1, 1, 1, 1, 2, 10, 0),
  (2, 1, 1, 3, 4, 7, 0),
  (3, 1, 1, 4, 5, 5, 0),
  (4, 1, 2, 2, null, 65, 0);

insert into incompatible_castellers (id, colla_id, mem1_id, mem2_id) values 
  (1, 1, 1, 3);