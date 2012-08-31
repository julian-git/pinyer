maximize
7.0 c10p3 + 2.0 c13p4 + 2.0 c13p5 + 3.0 c14p4 + 3.0 c14p5 + 4.0 c15p4 + 4.0 c15p5 + 5.0 c16p4 + 5.0 c16p5 + 6.0 c17p4 + 6.0 c17p5 + 7.0 c18p4 + 7.0 c18p5 + 5.0 c1p1 + 5.0 c1p2 + 7.0 c2p1 + 7.0 c2p2 + 5.0 c9p3
subject to
pos1: c1p1 + c2p1 = 1
pos2: c1p2 + c2p2 = 1
pos3: c9p3 + c10p3 = 1
pos4: c13p4 + c14p4 + c15p4 + c16p4 + c17p4 + c18p4 = 1
pos5: c13p5 + c14p5 + c15p5 + c16p5 + c17p5 + c18p5 <= 1
cas1: c1p1 + c1p2 <= 1
cas2: c2p1 + c2p2 <= 1
cas9: c9p3 = 0
cas10: c10p3 <= 1
cas13: c13p4 + c13p5 <= 1
cas14: c14p4 + c14p5 <= 1
cas15: c15p4 + c15p5 <= 1
cas16: c16p4 + c16p5 <= 1
cas17: c17p4 = 0
cas17: c17p5 = 1
cas18: c18p4 + c18p5 <= 1
total_height_1_2: 150.0 c1p1 + 155.0 c2p1 - 150.0 c1p2 - 155.0 c2p2 >= 0
total_height_1_2: 150.0 c1p1 + 155.0 c2p1 - 150.0 c1p2 - 155.0 c2p2 <= 10.0
total_height_3_4: 185.0 c9p3 + 190.0 c10p3 - 150.0 c13p4 - 155.0 c14p4 - 155.0 c15p4 - 180.0 c16p4 - 185.0 c17p4 - 190.0 c18p4 >= 0
total_height_3_4: 185.0 c9p3 + 190.0 c10p3 - 150.0 c13p4 - 155.0 c14p4 - 155.0 c15p4 - 180.0 c16p4 - 185.0 c17p4 - 190.0 c18p4 <= 7.0
total_height_4_5: 150.0 c13p4 + 155.0 c14p4 + 155.0 c15p4 + 180.0 c16p4 + 185.0 c17p4 + 190.0 c18p4 - 150.0 c13p5 - 155.0 c14p5 - 155.0 c15p5 - 180.0 c16p5 - 185.0 c17p5 - 190.0 c18p5 >= 0
total_height_4_5: 150.0 c13p4 + 155.0 c14p4 + 155.0 c15p4 + 180.0 c16p4 + 185.0 c17p4 + 190.0 c18p4 - 150.0 c13p5 - 155.0 c14p5 - 155.0 c15p5 - 180.0 c16p5 - 185.0 c17p5 - 190.0 c18p5 <= 5.0
weight_2: 65.0 c1p2 + 70.0 c2p2 >= 65.0
binary
c10p3 c13p4 c13p5 c14p4 c14p5 c15p4 c15p5 c16p4 c16p5 c17p4 c17p5 c18p4 c18p5 c1p1 c1p2 c2p1 c2p2 c9p3 