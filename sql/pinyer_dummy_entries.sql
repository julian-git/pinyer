delete from incompatible_castellers where colla_id=2;
delete from castell_relation where castell_type_id=1000;
delete from castell_position where castell_type_id=1000;
delete from castell_type where id in (1000, 1001);
delete from casteller_role where casteller_id > 1000;
delete from casteller_colla where casteller_id > 1000;
delete from casteller where id > 1000;
delete from colla where id=2;

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
  (1001,'crossa'), (1002,'crossa'), (1003,'baix'), (1004,'baix'), (1005,'contrafort'), (1006,'contrafort'), (1007,'vent'), (1008,'vent'), (1009,'ma'), (1010,'ma'),
  (1011,'agulla'), (1012,'agulla'), (1013,'pinya'), (1014,'pinya'), (1015,'pinya'), (1016,'pinya'), (1017,'pinya'), (1018,'pinya');

insert into castell_type values 
  (1000, 2, "p4", "Pilar de 4"),
  (1001, 2, "2de8f", "Torre de vuit amb folre");

insert into castell_position (id, castell_type_id, role, is_essential, svg_id, svg_text, svg_elem, x, y, rx) values
  (1001, 1000, 'crossa', true, 1001, "Crossa 1", "circle", -50, -40, 30),
  (1002, 1000, 'crossa', true, 1002, "Crossa 2", "circle", -50, 40, 30);

insert into castell_position (id, castell_type_id, role, is_essential, svg_id, svg_text, x, y) values
  (1003, 1000, 'ma', true, 1003, "Ma 1", 0, 100),
  (1004, 1000, 'pinya', true, 1004, "Pinya 1", 0, 150),
  (1005, 1000, 'pinya', false, 1005, "Pinya 2", 0, 200);

insert into castell_relation (id, castell_type_id, relation_type, coeff_list, field_names, pos_list, pos_type_list, sense, rhs) values
  (1001, 1000, 'zero_or_tol', '1_1', 'total_height~total_height', '1001_1002', 'c_c', true, 6),
  (1002, 1000, 'zero_or_tol', '1_1', 'total_height~total_height', '1003_1004', 'm_p', true, 7),
  (1003, 1000, 'zero_or_tol', '1_1', 'total_height~total_height', '1004_1005', 'p_p', true, 5),
  (1004, 1000, 'val_tol', '1', 'weight', '1002', true, 65);

insert into incompatible_castellers (id, colla_id, cast1_id, cast2_id) values 
  (1000, 2, 1016, 1018);