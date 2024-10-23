from graphics import *
import numpy

def main():
    xLength = 400
    yLength = 400
    xCenter = xLength / 2
    yCenter = yLength / 2
    zCenter = 0
    x = 0
    y = 1
    win = GraphWin("Cube", 400, 400, autoflush=False)
    win.setBackground("pink")
    cameraNormVector = [0, 0, -1]
    f = 200  # focal length
    xAng = numpy.pi / 100
    yAng = -numpy.pi / 40
    zAng = numpy.pi / 33


    vertices = [
        [xCenter + 20, yCenter - 20, 20],
        [xCenter - 20, yCenter - 20, 20],
        [xCenter - 20, yCenter + 20, 20],
        [xCenter + 20, yCenter + 20, 20],
        [xCenter + 20, yCenter - 20, -20],
        [xCenter - 20, yCenter - 20, -20],
        [xCenter - 20, yCenter + 20, -20],
        [xCenter + 20, yCenter + 20, -20],
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    # each edge in counter-clockwise order for backface culling.
    faces = [
        (0, 1, 2, 3),
        (4, 6, 6, 5),
        (0, 4, 5, 1),
        (3, 2, 6, 7),
        (0, 3, 7, 4),
        (1, 5, 6, 2) 
    ]

    lines = []
    for edge in edges:
        line = Line(Point(vertices[edge[0]][x], vertices[edge[0]][y]), Point(vertices[edge[1]][x], vertices[edge[1]][y]))
        line.draw(win)
        lines.append(line)
    
    projectionMatrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, -1/f, 1]
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

    rotationXM = [
        [1, 0, 0, 0],
        [0, numpy.cos(xAng), numpy.sin(xAng), 0],
        [0, -numpy.sin(xAng), numpy.cos(xAng), 0],
        [0, 0, 0, 1]
    ]

    rotationYM = [
        [numpy.cos(yAng), 0, numpy.sin(yAng), 0],
        [0, 1, 0, 0],
        [-numpy.sin(yAng), 0, numpy.cos(yAng), 0],
        [0, 0, 0, 1]
    ]

    rotationZM = [
        [numpy.cos(zAng), -numpy.sin(zAng), 0, 0],
        [numpy.sin(zAng), numpy.cos(zAng), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]


    def rotateVertices():
        for i in range(len(vertices)):
            lastx = vertices[i][0]
            lasty = vertices[i][1]
            lastZ = vertices[i][2]

            v = [lastx, lasty, lastZ, 1]

            originV = numpy.dot(v, translateToOriginM) #translate square to the top left window origin
            rotateXV = numpy.dot(originV, rotationXM) #apply rotation to square
            rotateYV = numpy.dot(rotateXV, rotationYM)
            rotateZV = numpy.dot(rotateYV, rotationZM)
            projectV = numpy.dot(rotateZV, projectionMatrix) #project onto xy plane 
            finalV = numpy.dot(projectV, translateToCenterM) #translate back to center of window

            vertices[i][0] = finalV[0] / finalV[3]
            vertices[i][1] = finalV[1] / finalV[3]
            vertices[i][2] = finalV[2] / finalV[3]

    def getFaceNormal(face):
        vert1 = numpy.array(vertices[face[0]])
        vert2 = numpy.array(vertices[face[1]])
        vert3 = numpy.array(vertices[face[2]])
        
        vector1 = vert2 - vert1
        vector2 = vert3 - vert1
        
        normal = numpy.cross(vector1, vector2)
        return normal / numpy.linalg.norm(normal)  # Normalize

    def backfaceCulling():
        facingEdges = set()

        for face in faces:
            normal = getFaceNormal(face)

            edgeCameraDot = numpy.dot(normal, cameraNormVector)

            if edgeCameraDot > 0:
                for i in range(len(face)):
                    edge = (face[i], face[(i+1) % 4])
                    if edge not in facingEdges:
                        facingEdges.add(edge)

        return facingEdges

    running = True
    while running:
        for line in lines:
            line.undraw()

        rotateVertices()
        visibleEdges = backfaceCulling()

        lines = []
        for edge in visibleEdges:
            line = Line(Point(vertices[edge[0]][x], vertices[edge[0]][y]), Point(vertices[edge[1]][x], vertices[edge[1]][y]))
            line.draw(win).setWidth(2)
            line.setFill("black")
            lines.append(line)

        if win.checkMouse():
            break
        time.sleep(0.05)
        
main()