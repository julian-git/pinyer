from build_ip import find_pinya
from html_common import *
from db_interaction import get_db, get_positions, get_castell

def fill_in(pd, svg, svgclass, min_x, max_x, min_y, max_y, name=''):
    if pd['svg_elem'] == 'rect':
        svg = svg + \
            svg_rect.substitute(_svg_id=pd['svg_id'], _svg_text=pd['svg_text'], \
                                    _class=svgclass, _name=name, _angle=pd['angle'], \
                                    _x=pd['x'], _y=pd['y'], \
                                    _rx=pd['x'], _ry=pd['y'], _rw=pd['w'], _rh=pd['h'])
        min_x = min(min_x, pd['x']); max_x = max(max_x, pd['x']+pd['w'])
        min_y = min(min_y, pd['y']); max_y = max(max_y, pd['y']+pd['h'])
    elif pd['svg_elem'] == 'circle':
        svg = svg + \
            svg_circle.substitute(_svg_id=pd['svg_id'], _class=svgclass, \
                                      _name=name, \
                                      _x=pd['x'], _y=pd['y'], _rx=pd['rx'])
        min_x = min(min_x, pd['x']-pd['rx']); max_x = max(max_x, pd['x']+pd['rx'])
        min_y = min(min_y, pd['y']-pd['rx']); max_y = max(max_y, pd['y']+pd['rx'])
    return [svg, min_x, max_x, min_y, max_y]

def center_image(min_x, max_x, min_y, max_y):
    min_x = min_x - 500; max_x = max_x + 500; # center the image a little
    min_y = min_y - 10 # and put a little margin on top
    return [min_x, max_x, min_y, max_y]


def editable_castell_plan(position_data, castell_data):
    svg = ''
    svgclass = 'design'
    [min_x, max_x, min_y, max_y] = [1000000, -1000000, 1000000, -1000000]
    for pos, pd in position_data.iteritems():
        [svg, min_x, max_x, min_y, max_y] = \
            fill_in(pd, svg, svgclass, min_x, max_x, min_y, max_y, pd['role_name'])
    [min_x, max_x, min_y, max_y] = center_image(min_x, max_x, min_y, max_y)
    return \
        head.substitute(_title=castell_data['name']) + \
        body.substitute(_name=castell_data['name'], \
                            _desc=castell_data['description']) + \
        script + \
        svg_head.substitute(_vx=str(min_x), _vy=str(min_y), _vw=str(max_x-min_x), _vh=str(max_y-min_y)) + \
        svg + \
        "</svg>" + "</html>"


def solution_as_svg(solution, position_data, prescribed):
    svg = ''
    [min_x, max_x, min_y, max_y] = [1000000, -1000000, 1000000, -1000000]
    for pos, casteller in solution.iteritems():
        pd = position_data[pos]
        [cast_id, name] = casteller
        if cast_id in prescribed:
            svgclass = "prescribed"
        else:
            svgclass = "calculated"
        [svg, min_x, max_x, min_y, max_y] = \
            fill_in(pd, svg, svgclass, min_x, max_x, min_y, max_y, pd['role_name'])
    [min_x, max_x, min_y, max_y] = center_image(min_x, max_x, min_y, max_y)
    return svg_head.substitute(_vx=min_x, _vy=min_y, _vw=max_x-min_x, _vh=max_y-min_y) + \
        svg + "</svg>" + "</html>"

if __name__ == "__main__":
    prescribed = dict([(9, 0), (17, 5)])
    position_data = dict()
    castell_type_id = 1
#    solution = find_pinya(prescribed, position_data)
    f = open("../tests/index.html", 'w')
#    f.write(solution_as_svg(solution, position_data, prescribed))
    db = get_db()
    position_data = get_positions(db, castell_type_id)
    castell_data = get_castell(db, castell_type_id)
    f.write(editable_castell_plan(position_data, castell_data))
