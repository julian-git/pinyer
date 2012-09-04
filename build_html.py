from build_ip import find_pinya

def solution_as_svg(solution):
    from string import Template
    svg_rect = Template("""
<g id="${_svg_id}" transform="translate(${_x} ${_y})">
  <rect width="${_w}" height="${_h}" x="-60" y="-20" fill="lightblue"/>
  <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
    svg_circle = Template("""
<g id="${_svg_id}" transform="translate(${_x} ${_y})">
  <circle x="-60" y="-20" r="${_rx}" fill="lightblue"/>
  <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
    svg = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Pinyol</title>
</head>
<body>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
viewBox="0 0 200 200"> 
"""
    for pos, name in solution.iteritems():
        pd = position_data[pos]
        if pd['svg_elem'] == 'rect':
            svg = svg + svg_rect.substitute(_svg_id=pd['svg_id'], _name=name, _x=pd['x'], _y=pd['y'], _w=pd['w'], _h=pd['h'])
        elif pd['svg_elem'] == 'circle':
            svg = svg + svg_circle.substitute(_svg_id=pd['svg_id'], _name=name, _x=pd['x'], _y=pd['y'], _rx=pd['rx'])
    return svg + "</svg>" + "</html>"

if __name__ == "__main__":
    participation = dict([(9, 0), (17, 5)])
    position_data = dict()
    solution = find_pinya(participation, position_data)
    f = open("web/index.html", 'w')
    f.write(solution_as_svg(solution))
