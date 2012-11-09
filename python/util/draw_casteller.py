#from local_config import floor_level
from db_interaction import get_db
#from xml_to_svg import printAttr

svg = ''

def draw_casteller(xml_id, xml_text, _class, \
                       shoulder_height, shoulder_width, axle_height, hip_height):
    return draw_casteller_as_rect(xml_id, xml_text, _class, \
                                      shoulder_height, shoulder_width, axle_height, hip_height)

def draw_casteller_as_rect(xml_id, xml_text, _class, \
                       shoulder_height, shoulder_width, axle_height, hip_height):
    floor_level = -60
    svg  = ''.join(['<rect id="', xml_id, '_body" class="', _class,  '" ', \
                       'width="', str(shoulder_width), '" ', \
                       'height="', str(shoulder_height - hip_height), '" ', \
                       'x="', str(round(-shoulder_width/2, 2)), '" ',
                       'y="', str(round(floor_level + hip_height, 2)), '"/>'])
    svg += ''.join(['<rect id="', xml_id, '_left_leg" class="', _class, '" ', \
                       'width="', str(round(shoulder_width/2.5, 2)), '" ', \
                       'height="', str(hip_height), '" ', \
                       'x="', str(round(-shoulder_width/2, 2)), '" ', \
                       'y="', str(round(floor_level, 2)), '"/>'])
    svg += ''.join(['<rect id="', xml_id, '_right_leg" class="', _class, '" ', \
                       'width="', str(round(shoulder_width/2.5, 2)), '" ', \
                       'height="', str(hip_height), '" ', \
                       'x="', str(round(shoulder_width/2 - shoulder_width/2.5, 2)), '" ', \
                       'y="', str(round(floor_level, 2)), '"/>'])
    return svg


def draw_castellers_to_db(colla_id_name):
    db = get_db()
    c = db.cursor()
    c.execute("""
select id, nickname, shoulder_height, shoulder_width, axle_height, hip_height
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id_name = %s""", colla_id_name)
    svg_arr = []
    castellers = c.fetchall()
    
    for (id, nickname, shoulder_height, shoulder_width, axle_height, hip_height) in castellers:
        svg = draw_casteller('cast_' + str(id), nickname, '${_class_' + str(id) + '}', \
                                  shoulder_height, shoulder_width, axle_height, hip_height)
        c.execute("update casteller set svg_rep=%s where id=%s", (svg, int(id),))
        svg_arr.append(svg)
    db.commit()
    return ''.join(svg_arr)

if __name__ == "__main__":
    draw_castellers_to_db('cvg')

                                  
