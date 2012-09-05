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
