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
  <rect id="${_svg_id}" class="${_class}" ${_dyn_props} width="${_w}" height="${_h}" x="-60" y="-20"/>
  <text id="${_svg_id}_text" class="${_class}" ${_dyn_props} text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")

svg_circle = Template("""
<g transform="translate(${_x} ${_y})">
  <circle id="${_svg_id}" class="${_class}" ${_dyn_props} x="-60" y="-20" r="${_rx}"/>
  <text id="${_svg_id}_text" class="${_class}" ${_dyn_props} text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
