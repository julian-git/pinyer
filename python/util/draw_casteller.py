#from local_config import floor_level
from db_interaction import get_db
#from xml_to_svg import printAttr

svg = ''

def draw_casteller(xml_id, _class, shoulder_height, shoulder_width, axle_height, hip_height):
    return draw_casteller_as_rect(xml_id, _class, \
                                      shoulder_height, shoulder_width, axle_height, hip_height)

def draw_casteller_as_rect(xml_id, _class, \
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
    cursor = db.cursor()
    where_str = """
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id_name = %s"""

    extreme_vals = dict()
    for field in ('shoulder_height', 'shoulder_width', 'axle_height', 'hip_height'):
        cursor.execute('select min(' + field + '), max(' + field + ') ' + where_str, colla_id_name)
        [[min_val, max_val]] = cursor.fetchall()
        extreme_vals[field] = [min_val, max_val]

    field_str = 'id, nickname, shoulder_height, shoulder_width, axle_height, hip_height'
    cursor.execute('select ' + field_str + where_str, colla_id_name)
    castellers = cursor.fetchall()
    svg_arr = []
    shdiff = 1.1 * (extreme_vals['shoulder_height'][1] - extreme_vals['shoulder_height'][0])
    swdiff = 1.1 * (extreme_vals['shoulder_width'][1] - extreme_vals['shoulder_width'][0])
    for (id, nickname, shoulder_height, shoulder_width, axle_height, hip_height) in castellers:
        sh = round(shoulder_height - shdiff, 2)
        ah = round(axle_height - shdiff, 2)
        hh = round(hip_height * sh / shoulder_height, 2)
        sw = round(shoulder_width - swdiff, 2)
        svg = draw_casteller('cast_' + str(id), '${_class_' + str(id) + '}', \
                                 sh, sw, ah, hh)
        fields = dict(zip(field_str.split(', '), \
                         (id, nickname, shoulder_height, shoulder_width, axle_height, hip_height)))
        cursor.execute("update casteller set svg_rep=%s, alt_text=%s where id=%s", \
                           (svg, alt_text(fields), int(id),))
        svg_arr.append(svg)

    db.commit()
    return ''.join(svg_arr)

def alt_text(fields):
    a = []
    for (field, value) in fields.iteritems():
        a.append(field + '=' + str(value))
    return ',&#10;'.join(a)  # line break

if __name__ == "__main__":
    draw_castellers_to_db('cvg')

                                  
