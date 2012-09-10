insert into colla (id, name, city) values
  (2, "test_colla", "Barcelona/Gràcia");

insert into casteller (id, nickname, total_height, shoulder_height, axle_height, hip_height, stretched_height, shoulder_width, weight, strength)  values 
  (1001, "crossa1", 150, 130, 120, 50, 200, 70, 65, 5),
  (1002, "crossa2", 155, 135, 125, 55, 205, 70, 70, 7),	
  (1003, "baix1", 155, 135, 115, 55, 200, 70, 65, 5),
  (1004, "baix2", 160, 140, 120, 60, 205, 70, 70, 7),
  (1005, "contrafort1", 155, 135, 115, 55, 200, 70, 65, 5),
  (1006, "contrafort2", 160, 140, 120, 60, 205, 70, 70, 7),
  (1007, "vent1", 180, 160, 150, 70, 210, 70, 70, 5),
  (1008, "vent2", 185, 165, 155, 75, 215, 70, 75, 7),
  (1009, "ma1", 185, 170, 160, 80, 220, 70, 80, 5),
  (1010, 'ma2', 190, 175, 165, 85, 225, 70, 85, 7),
  (1011, "agulla1", 155, 135, 115, 55, 200, 70, 65, 5),
  (1012, "agulla2", 160, 140, 120, 60, 205, 70, 70, 7), 
  (1013, "pinya1", 150, 130, 120, 50, 200, 70, 65, 2),  
  (1014, "pinya2", 155, 135, 115, 55, 200, 70, 65, 3),  
  (1015, "pinya3", 155, 135, 115, 55, 200, 70, 65, 4),  
  (1016, "pinya4", 180, 160, 150, 70, 210, 70, 70, 5),  
  (1017, "pinya5", 185, 170, 160, 80, 220, 70, 80, 6),  
  (1018, "pinya6", 190, 135, 115, 55, 200, 70, 65, 7);

insert into casteller_colla values
  (1001,2), (1002,2), (1003,2), (1004,2), (1005,2), (1006,2), (1007,2), (1008,2), (1009,2), (1010,2),
  (1011,2), (1012,2), (1013,2), (1014,2), (1015,2), (1016,2), (1017,2), (1018,2);

insert into casteller_role values
  (1001,2), (1002,2), (1003,3), (1004,3), (1005,4), (1006,4), (1007,5), (1008,5), (1009,6), (1010,6),
  (1011,7), (1012,7), (1013,1), (1014,1), (1015,1), (1016,1), (1017,1), (1018,1);

insert into castell_type values 
  (1000, 2, "p4", "Pilar de 4"),
  (1001, 2, "2de8f", "Torre de vuit amb folre");

insert into castell_position (id, castell_type_id, role_id, is_essential, svg_id, svg_text, svg_elem, x, y, rx) values
  (1001, 1000, 2, true, "crossa1", "Crossa 1", "circle", -50, -40, 30),
  (1002, 1000, 2, true, "crossa2", "Crossa 2", "circle", -50, 40, 30);

insert into castell_position (id, castell_type_id, role_id, is_essential, svg_id, svg_text, x, y) values
  (1003, 1000, 6, true, "ma1", "Ma 1", 0, 100),
  (1004, 1000, 1, true, "pinya1", "Pinya 1", 0, 150),
  (1005, 1000, 1, false, "pinya2", "Pinya 2", 0, 200);

insert into castell_relation (id, castell_type_id, relation_type, field_name, from_pos_id, to_pos_id, fparam1, fparam2) values
  (1001, 1000, 1, 'total_height', 1001, 1002, 10, 0),
  (1002, 1000, 1, 'total_height', 1003, 1004, 7, 0),
  (1003, 1000, 1, 'total_height', 1004, 1005, 5, 0),
  (1004, 1000, 2, 'weight', 1002, null, 65, 0);

insert into incompatible_castellers (id, colla_id, cast1_id, cast2_id) values 
  (1000, 2, 1016, 1018);