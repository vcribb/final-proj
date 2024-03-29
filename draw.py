from display import *
from matrix import *
from gmath import *
import re

def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    while x <= x1:
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z

def draw_scanlineG(x0, z0, x1, z1, y, screen, zbuffer, c1, c2):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
        temp = c2[:]
        c2 = c1[:]
        c1 = temp[:]
    x = x0
    z = z0
    delta_z = 0
    if (x1 - x0 + 1) != 0:
        delta_z = (z1 - z0) / (x1 - x0 + 1)
    delta_r = 0
    if (x1 - x0 + 1) != 0:
        delta_r = (c2[0] - c1[0]) / (x1 - x0 + 1)
    delta_g = 0
    if (x1 - x0 + 1) != 0:
        delta_g = (c2[1] - c1[1]) / (x1 - x0 + 1)
    delta_b = 0
    if (x1 - x0 + 1) != 0:
        delta_b = (c2[2] - c1[2]) / (x1 - x0 + 1)
    while x <= x1:
        temp = [int(item) for item in c1]
        plot(screen, zbuffer, temp, int(x), int(y), int(z))
        x+=1
        z+=delta_z
        c1[0] += delta_r
        c1[1] += delta_g
        c1[2] += delta_b
        
def scanline_convert(polygons, i, screen, zbuffer, color):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

def scanline_convertG(polygons, i, screen, zbuffer, vertexnormals):
    flip = False
    points = [(polygons[i][0], polygons[i][1], polygons[i][2]),
              (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
              (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2])]

    points.sort(key = lambda x: x[1])
    x0 = points[0][0]
    x1 = points[0][0]
    y = int(points[0][1])
    z0 = points[0][2]
    z1 = points[0][2]

    d0 = int(points[2][1]) - y * 1.0 + 1
    d1 = int(points[1][1]) - y * 1.0 + 1
    d2 = int(points[2][1]) - int(points[1][1]) * 1.0 + 1

    dx0 = 0
    if d0 != 0:
        dx0 = (points[2][0] - points[0][0]) / d0
    dz0 = 0
    if d0 != 0:
        dz0 = (points[2][2] - points[0][2]) / d0
    dx1 = 0
    if d1 != 0:
        dx1 = (points[1][0] - points[0][0]) / d1
    dz1 = 0
    if d1 != 0:
        dz1 = (points[1][2] - points[0][2]) / d1

    if points[0] in vertexnormals:
        c0 = vertexnormals[points[0]]
    else:
        print('error')
    if points[1] in vertexnormals:
        c1 = vertexnormals[points[1]]
    else:
        print('error')

    if points[2] in vertexnormals:
        c2 = vertexnormals[points[2]]
    else:
        print('error')

    c0r = c0[0]
    c0g = c0[1]
    c0b = c0[2]
    c1r = c1[0]
    c1g = c1[1]
    c1b = c1[2]
    c2r = c2[0]
    c2g = c2[1]
    c2b = c2[2]

    dc0r = 0
    if d0 != 0:
        dc0r = (c2r - c0r) / d0
    dc0g = 0
    if d0 != 0:
        dc0g = (c2g - c0g) / d0
    dc0b = 0
    if d0 != 0:
        dc0b = (c2b - c0b) / d0
    dc1r = 0
    if d1 != 0:
        dc1r = (c1r - c0r) / d1
    dc1g = 0
    if d1 != 0:
        dc1g = (c1g - c0g) / d1
    dc1b = 0
    if d1 != 0:
        dc1b = (c1b - c0b) / d1

    xc0r = c0[0]
    xc0g = c0[1]
    xc0b = c0[2]
    xc1r = c0[0]
    xc1g = c0[1]
    xc1b = c0[2]
    
    while y <= int(points[2][1]):
        xc0 = [xc0r % 256, xc0g % 256, xc0b % 256]
        xc1 = [xc1r % 256, xc1g % 256, xc1b % 256]
        if (not flip and y >= int(points[1][1])):
            flip = True

            dx1 = 0
            if d2 != 0:
                dx1 = (points[2][0] - points[1][0]) / d2
            dz1 = 0
            if d2 != 0:
                dz1 = (points[2][2] - points[1][2]) / d2
            x1 = points[1][0]
            z1 = points[1][2]

            xc1r = c1r
            xc1g = c1g
            xc1b = c1b
            dc1r = 0
            if d2 != 0:
                dc1r = (c2r - c1r) / d2
            dc1g = 0
            if d2 != 0:
                dc1g = (c2g - c1g) / d2
            dc1b = 0
            if d2 != 0:
                dc1b = (c2b - c1b) / d2
            
        draw_scanlineG(int(x0), z0, int(x1), z1, y, screen, zbuffer, xc0, xc1)
        x0+=dx0
        z0+=dz0
        x1+=dx1
        z1+=dz1
        y+=1
        xc1r += dc1r
        xc1g += dc1g
        xc1b += dc1b 
        xc0r += dc0r
        xc0g += dc0g
        xc0b += dc0b       

def helper(fname):
    points = []
    f = open(fname, 'r')
    for line in f.readlines():
        temp = re.sub(' +', ' ', line)
        line = temp.split(" ")
        if line[0] == 'v':
            points.append([float(line[1]), float(line[2]), float(line[3])])
    f.close()
    return points

def generate_mesh(edges, fname):
    points = helper(fname)
    f = open(fname, 'r')
    for line in f.readlines():
        temp = re.sub(' +', ' ', line)
        line = temp.split(" ")
        if line[0] == 'f':
            obj = line[1:]
            temp = 2
            while temp < len(obj):
                x0 = int(obj[0]) - 1
                x1 = int(obj[temp - 1]) - 1
                x2 = int(obj[temp]) - 1
                add_polygon(edges, points[x0][0], points[x0][1], points[x0][2],
                                   points[x1][0], points[x1][1], points[x1][2],
                                   points[x2][0], points[x2][1], points[x2][2])
                temp+=1
    f.close()

#--------------------------------------------------------------------------

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect):
    if len(polygons) < 2:
        print 'Need at least 3 points to draw'
        return

    point = 0
    while point < len(polygons) - 2:

        #calculate normal of each face
        normal = calculate_normal(polygons, point)[:]

        #print normal
        if normal[2] > 0:

            #lighting comes from flat shading
            color = get_lighting(normal, view, ambient, light, symbols, reflect )

            #when doing gouraud shading, lighting comes from average of vertex normal of points
            scanline_convert(polygons, point, screen, zbuffer, color)

        point+= 3

def draw_polygonsG( polygons, screen, zbuffer, view, ambient, light, symbols, reflect):
    if len(polygons) < 2:
        print 'Need at least 3 points to draw'
        return

    vertexnormals = vertex_normal(polygons)
    #print(vertexnormals)
    #gets a color for each vertex based on previous normal
    for k in vertexnormals:
        vertexnormals[k] = get_lighting(vertexnormals[k], view, ambient, light, symbols, reflect )
    
    point = 0
    while point < len(polygons) - 2:

        #calculate normal of each face
        normal = calculate_normal(polygons, point)[:]

        #print normal
        if normal[2] > 0:

            #lighting that comes from flat shading
            #color = get_lighting(normal, view, ambient, light, symbols, reflect )

            #when doing gouraud shading, lighting comes from average of vertex normal of points
            scanline_convertG(polygons, point, screen, zbuffer, vertexnormals)

        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y) + 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    dz = (z1 - z0) / distance if distance != 0 else 0

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z+= dz
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z )
