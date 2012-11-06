delete from incompatible_castellers where colla_id_name='test_colla';
delete from castell_type where colla_id_name = 'test_colla';
delete from casteller_role where casteller_id > 1000;
delete from casteller_colla where casteller_id > 1000;
delete from casteller where id > 1000;
delete from colla where id_name='test_colla';

insert into colla (id_name, name, city) values
  ('test_colla', 'Test colla', 'Barcelona/Gràcia');

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
  (1001, 'test_colla'), (1002, 'test_colla'), (1003, 'test_colla'),
  (1004, 'test_colla'), (1005, 'test_colla'), (1006, 'test_colla'),
  (1007, 'test_colla'), (1008, 'test_colla'), (1009, 'test_colla'),
  (1010, 'test_colla'), (1011, 'test_colla'), (1012, 'test_colla'),
  (1013, 'test_colla'), (1014, 'test_colla'), (1015, 'test_colla'),
  (1016, 'test_colla'), (1017, 'test_colla'), (1018, 'test_colla');

insert into casteller_role values
  (1001,'crossa'), (1002,'crossa'), (1003,'baix'), (1004,'baix'), (1005,'contrafort'), (1006,'contrafort'), (1007,'vent'), (1008,'vent'), (1009,'ma'), (1010,'ma'),
  (1011,'agulla'), (1012,'agulla'), (1013,'pinya'), (1014,'pinya'), (1015,'pinya'), (1016,'pinya'), (1017,'pinya'), (1018,'pinya');

insert into castell_type values 
  (1000, 'test_colla', "p4", "Pilar de 4"),
  (1001, 'test_colla', "2de8f", "Torre de vuit amb folre");

insert into incompatible_castellers (id, colla_id_name, cast1_id, cast2_id) values 
  (1000, 'test_colla', 1016, 1018);