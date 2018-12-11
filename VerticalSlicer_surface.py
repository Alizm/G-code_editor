import rhinoscriptsyntax as rs
import math
import codecs

surf_id = rs.GetObject("Select Surface")
rect_prof = rs.SurfaceEditPoints(surf_id)
distance_x = rs.GetReal("Vertical Distance", 0.4)
height = rs.GetReal("Offset Z",0.18)
filament = rs.GetReal("Filament Diameter",1.75)
Layerheight = rs.GetReal("Layer Height",0.2)
extrude_temp = rs.GetReal("Extrude temperture",205)
bed_temp = rs.GetReal("Bed temperture",60)
printspeed = rs.GetReal("Print speed",2500)
multi = rs.GetReal("Extrude multiply",1.0)

width = rect_prof[3]

#Line
line = rs.AddLine(rect_prof[0],rect_prof[1])
array_number = int(width[0] // distance_x)

#Array line
if line:
    i = 0
    for i in range(array_number):
        offset_x = distance_x * i
        line_copy = (offset_x, 0, 0)
        array_line = rs.CopyObject( line, line_copy )

        # Project down
        results = rs.ProjectCurveToSurface(array_line, surf_id, (0,0,-1))
        rs.DeleteObject(array_line)

    rs.DeleteObject(line)

# to get curve number
    crvs = rs.ObjectsByType(4, True)
    line_number = (len(crvs))
    filename = rs.SaveFileName("Save", "G-code (*.gcode)|*.gcode||")
    f = codecs.open(filename, 'w', 'utf-8')

    f.write('G90\n')
    f.write('M83\n')
    f.write('M106 S0\n')
    #f.write('M106 S60\n')
    #f.write('M104 S205 T0\n')
    #f.write('M109 S205 T0\n')
    f.write('M140 S{0}\n'.format(bed_temp))
    f.write('M104 S{0} T0\n'.format(extrude_temp))
    f.write('M109 S{0} T0\n'.format(extrude_temp))
    f.write('G28\n')
    f.write('G92 E0\n')
    f.write('G1 E-1.0000 F1800\n')
    f.write("G1 Z6.475 F1000\n")


    for l in range(line_number):
        startPoint = rs.CurveStartPoint(crvs[l])
        endPoint = rs.CurveEndPoint(crvs[l])
        e_dist = rs.Distance(startPoint,endPoint)
        Evalue = 0
        Evalue += float((multi * e_dist * distance_x * Layerheight) / float(math.pi * (float(filament/2.0) ** 2)))

        textGcode = "G1 X" + str(endPoint[0]) + " Y" + str(endPoint[1]) + " Z" + str(height) + " F1800\n"
        textGcode += "G1 X" + str(startPoint[0]) + " Y" + str(startPoint[1]) + " Z" + str(height) + " E" + str(Evalue) + " F" + str(printspeed) + "\n"

        f.write(textGcode)

    f.write('M104 S0\n')
    f.write('M140 S0\n')
    f.write('M84\n')

    f.close()
    rs.DeleteObjects(crvs)
