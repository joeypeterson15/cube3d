from graphics import *
import numpy

def main():
    xLength = 400
    yLength = 400
    xCenter = xLength / 2
    yCenter = yLength / 2
    zCenter = 0
    win = GraphWin("Cube", 400, 400, autoflush=False)
    vertices = [
        [xCenter - 20, yCenter + 20, -20],
        [xCenter + 20, yCenter + 20, -20],
        [xCenter + 20, yCenter - 20, -20],
        [xCenter - 20, yCenter - 20, -20],
        [xCenter - 20, yCenter + 20, 20],
        [xCenter + 20, yCenter + 20, 20],
        [xCenter + 20, yCenter - 20, 20],
        [xCenter - 20, yCenter - 20, 20]
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    lines = []
    for edge in edges:
        line = Line(Point(vertices[edge[0]][0], vertices[edge[0]][1]), Point(vertices[edge[1]][0], vertices[edge[1]][1])) #unpack with '*'
        line.draw(win)
        lines.append(line)
    
    projectionMatrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, -1/200, 1]
    ]

    translateToOriginM = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-xCenter, -yCenter, zCenter, 1]
    ]

    translateToCenterM = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [xCenter, yCenter, zCenter, 1]
    ]

    def rotateVertices(angle):
        for i in range(len(vertices)):
            lastx = vertices[i][0]
            lasty = vertices[i][1]
            lastZ = vertices[i][2]

            v = [lastx, lasty, lastZ, 1]

            rotationZaxisM = [
                [numpy.cos(angle), -numpy.sin(angle), 0, 0],
                [numpy.sin(angle), numpy.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
            # rotationYaxisM = [
            #     [numpy.cos(angle), 0, numpy.sin(angle), 0],
            #     [0, 1, 0, 0],
            #     [-numpy.sin(angle), 0, numpy.cos(angle), 0],
            #     [0, 0, 0, 1]
            # ]
            
            originV = numpy.dot(v, translateToOriginM) #translate square to the top left window origin
            rotateV = numpy.dot(originV, rotationZaxisM) #apply rotation to square 
            projectV = numpy.dot(rotateV, projectionMatrix)
            finalV = numpy.dot(projectV, translateToCenterM) #translate back to center of window

            # print('finalV', finalV)

            vertices[i][0] = finalV[0]
            vertices[i][1] = finalV[1]
            vertices[i][2] = finalV[2]
            # vertices[i][0] = finalV[0] / finalV[3]
            # vertices[i][1] = finalV[1] / finalV[3]
            # vertices[i][2] = finalV[2] / finalV[3]

    # def project():
    #     for i in range(len(vertices)):
    #         x = vertices[i][0]
    #         y = vertices[i][1]
    #         z = vertices[i][2]
    
    #         v = [x, y, z, 1]

    #         projectV = numpy.dot(v, projectionMatrix)

    #         vertices[i][0] = projectV[0] / -z
    #         vertices[i][1] = projectV[1] / -z
    #         vertices[i][2] = projectV[2] / -z



    angle_offset = numpy.pi / 35
    angle = angle_offset

    running = True
    while running:
        for line in lines:
            line.undraw()

        rotateVertices(angle)
        # project()

        lines = []
        for edge in edges:
            line = Line(Point(vertices[edge[0]][0], vertices[edge[0]][1]), Point(vertices[edge[1]][0], vertices[edge[1]][1])) #unpack with '*'
            line.draw(win)
            lines.append(line)

        if win.checkMouse():
            break
        time.sleep(0.03)
        
main()