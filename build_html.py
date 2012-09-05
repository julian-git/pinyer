from build_ip import find_pinya
from common_html import *
from db_interaction import get_db, get_positions

def fill_in(pd, svg, svgclass, min_x, max_x, min_y, max_y, name='', dyn_props=''):
    if pd['svg_elem'] == 'rect':
        svg = svg + svg_rect.substitute(_svg_id=pd['svg_id'], _class=svgclass, _dyn_props=dyn_props, _name=name, _x=pd['x'], _y=pd['y'], _w=pd['w'], _h=pd['h'])
        min_x = min(min_x, pd['x']); max_x = max(max_x, pd['x']+pd['w'])
        min_y = min(min_y, pd['y']); max_y = max(max_y, pd['y']+pd['h'])
    elif pd['svg_elem'] == 'circle':
        svg = svg + svg_circle.substitute(_svg_id=pd['svg_id'], _class=svgclass, _dyn_props=dyn_props, _name=name, _x=pd['x'], _y=pd['y'], _rx=pd['rx'])
        min_x = min(min_x, pd['x']-pd['rx']); max_x = max(max_x, pd['x']+pd['rx'])
        min_y = min(min_y, pd['y']-pd['rx']); max_y = max(max_y, pd['y']+pd['rx'])
    return [svg, min_x, max_x, min_y, max_y]

def editable_castell_plan(castell_type_id):
    db = get_db()
    position_data = get_positions(db, castell_type_id)
    script = """
<script><![CDATA[
function startMove(evt){
   x1 = evt.clientX;
   y1 = evt.clientY;
   C = evt.target.parentNode;
   C.parentNode.setAttribute("onmousemove","moveIt(evt)")
}
function moveIt(evt){
   translation = C.getAttributeNS(null, "transform").slice(10,-1).split(' ');
   sx = parseInt(translation[0]);
   sy = parseInt(translation[1]);
   C.setAttributeNS(null, "transform", "translate(" + (sx + evt.clientX - x1) + " " + (sy + evt.clientY - y1) + ")");
   x1 = evt.clientX;
   y1 = evt.clientY;
}
function endMove(){
   C.parentNode.setAttributeNS(null, "onmousemove", null)
}
]]></script>
"""
    dyn_props = ' onmousedown="startMove(evt)" onmouseup="endMove(evt)" '
    svg = ''
    svgclass = 'design'
    [min_x, max_x, min_y, max_y] = [1000000, -1000000, 1000000, -1000000]
    for pos, pd in position_data.iteritems():
        [svg, min_x, max_x, min_y, max_y] = fill_in(pd, svg, svgclass, min_x, max_x, min_y, max_y, pd['role_name'], dyn_props)
    min_x = min_x - 500; max_x = max_x + 500; # center the image a little
    min_y = min_y - 10 # and put a little margin on top
    viewbox = 'viewBox="' + str(min_x) + ' ' + str(min_y) + ' ' + str(max_x-min_x) + ' ' + str(max_y-min_y) + '">'
    return head + body + viewbox + script + svg + "</svg>" + "</html>"


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
        [svg, min_x, max_x, min_y, max_y] = fill_in(pd, svg, svgclass, min_x, max_x, min_y, max_y, pd['role_name'])
    min_x = min_x - 500; max_x = max_x + 500; # center the image a little
    viewbox = 'viewBox="' + str(min_x) + ' ' + str(min_y) + ' ' + str(max_x-min_x) + ' ' + str(max_y-min_y) + '">'
    return head + body + viewbox + svg + "</svg>" + "</html>"

if __name__ == "__main__":
    prescribed = dict([(9, 0), (17, 5)])
    position_data = dict()
#    solution = find_pinya(prescribed, position_data)
    f = open("web/index.html", 'w')
#    f.write(solution_as_svg(solution, position_data, prescribed))
    f.write(editable_castell_plan(1))
