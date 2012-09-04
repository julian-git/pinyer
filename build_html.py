from build_ip import find_pinya

def solution_as_svg(solution):
    from string import Template
    head = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Pinyol</title>
<link rel="stylesheet" type="text/css" media="screen" href="css/pinyol.css" />
</head>
"""
    body = """<body>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
"""
    svg_rect = Template("""
<g transform="translate(${_x} ${_y})">
  <rect id="${_svg_id}" width="${_w}" height="${_h}" x="-60" y="-20"/>
  <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
    svg_circle = Template("""
<g transform="translate(${_x} ${_y})">
  <circle id="${_svg_id}" x="-60" y="-20" r="${_rx}"/>
  <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
    svg = ''
    [min_x, max_x, min_y, max_y] = [1000000, -1000000, 1000000, -1000000]
    for pos, name in solution.iteritems():
        pd = position_data[pos]
        if pd['svg_elem'] == 'rect':
            svg = svg + svg_rect.substitute(_svg_id=pd['svg_id'], _name=name, _x=pd['x'], _y=pd['y'], _w=pd['w'], _h=pd['h'])
            min_x = min(min_x, pd['x']); max_x = max(max_x, pd['x']+pd['w'])
            min_y = min(min_y, pd['y']); max_y = max(max_y, pd['y']+pd['h'])
        elif pd['svg_elem'] == 'circle':
            svg = svg + svg_circle.substitute(_svg_id=pd['svg_id'], _name=name, _x=pd['x'], _y=pd['y'], _rx=pd['rx'])
            min_x = min(min_x, pd['x']-pd['rx']); max_x = max(max_x, pd['x']+pd['rx'])
            min_y = min(min_y, pd['y']-pd['rx']); max_y = max(max_y, pd['y']+pd['rx'])
    min_x = min_x - 500; max_x = max_x + 500; # center the image a little
    viewbox = 'viewBox="' + str(min_x) + ' ' + str(min_y) + ' ' + str(max_x-min_x) + ' ' + str(max_y-min_y) + '">'
    return head + body + viewbox + svg + "</svg>" + "</html>"

if __name__ == "__main__":
    participation = dict([(9, 0), (17, 5)])
    position_data = dict()
    solution = find_pinya(participation, position_data)
    f = open("web/index.html", 'w')
    f.write(solution_as_svg(solution))
