import rhinoscriptsyntax as rs
import Rhino
import math
import codecs

obj = rs.GetObject("Select Object")

box = rs.GetBox()
box_param = rs.AddBox(box)
box_point = rs.BoundingBox(box_param)
rs.DeleteObject(box_param)

distance_x = rs.GetReal("Vertical Distance", 0.4)
height = rs.GetReal("Z height",0.0)
filament = rs.GetReal("Filament Diameter",1.75)
Layerheight = rs.GetReal("Layer Height",0.2)
extrude_temp = rs.GetReal("Extrude temperture",205)
bed_temp = rs.GetReal("Bed temperture",60)
printspeed = rs.GetReal("Print speed",2500)
multi = rs.GetReal("Extrude multiply",1.0)

plane = Rhino.Geometry.Plane(box_point[0], box_point[1], box_point[2])
u_dir = rs.Distance(box_point[0], box_point[1])
v_dir = rs.Distance(box_point[1], box_point[2])
surface = rs.AddPlaneSurface(plane, u_dir, v_dir)

box_value = box_point[6]

array_z_number = int(box_value[2] // Layerheight)

if surface:
    array_lines=[]
    line = rs.AddLine(box_point[0],box_point[3])
    array_number = int(box_value[0] // distance_x)

    #Array line
    if line:
        i = 0
        for i in range(array_number):
            offset_x = distance_x * i
            line_copy = (offset_x, 0, 0)
            array_lines.append(rs.CopyObject( line, line_copy ))


    n = 0
    for n in range(array_z_number):
        offset_z = Layerheight * n
        surface_copy = (0,0,offset_z)
        array_surface = rs.CopyObject(surface ,surface_copy)
        intersect_crv = rs.IntersectBreps(obj, array_surface)
        if intersect_crv is None:
            break

        intersect_srf = rs.AddPlanarSrf(intersect_crv)

        if intersect_srf is None:
            break
        rs.DeleteObjects(intersect_crv)
        rs.DeleteObjects(array_surface)





        # Project down
        results = rs.ProjectCurveToSurface(array_lines, intersect_srf, (0,0,-1))

        rs.DeleteObjects(intersect_srf)

        #rs.DeleteObject(array_line)

        #rs.DeleteObject(line)
