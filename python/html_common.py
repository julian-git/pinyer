from string import Template

head = Template("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>El pinyer gracienc- ${_title}</title>
<link rel="stylesheet" type="text/css" media="screen" href="css/pinyer.css" />
</head>
""")

body = Template("""<body>
<h1>${_name}</h1>
<h2>${_desc}</h2>
""")

svg_head = Template("""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
 viewBox="${_vx} ${_vy} ${_vw} ${_vh}"> 
""")

svg_rect = Template("""
<g id="${_svg_id}" transform="translate(${_x} ${_y}) rotate(${_angle})">
  <rect id="${_svg_id}_cont" class="${_class}"  width="${_rw}" height="${_rh}" x="${_rx}" y="${_ry}"/>
  <g transform="rotate(90) translate(0 6)">
  <text id="${_svg_id}_text" class="${_class} vtext" text-anchor="middle">${_svg_text}</text>
  </g>
</g>
""")

svg_circle = Template("""
<g transform="translate(${_x} ${_y})">
  <circle id="${_svg_id}" class="${_class}" x="-60" y="-20" r="${_rx}"/>
  <text id="${_svg_id}_text" class="${_class}" text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")

script = """
<script type="text/javascript" src="js/jquery.js"></script>
<script type="text/javascript" src="js/jquery-ui.js"></script>
"""
