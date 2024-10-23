from graphics import *
import numpy

def main():
    xLength = 400
    yLength = 400
    xCenter = xLength / 2
    yCenter = yLength / 2
    zCenter = 0
    win = GraphWin("Cube", 400, 400, autoflush=False)
    win.setBackground("pink") 

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
        line = Line(Point(vertices[edge[0]][0], vertices[edge[0]][1]), Point(vertices[edge[1]][0], vertices[edge[1]][1])) #unpack with '*'
        line.draw(win)
        lines.append(line)
    
    f = 200  # focal length
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

    def rotateVertices(angle):
        for i in range(len(vertices)):
            lastx = vertices[i][0]
            lasty = vertices[i][1]
            lastZ = vertices[i][2]

            v = [lastx, lasty, lastZ, 1]

            rotationZM = [
                [numpy.cos(angle), -numpy.sin(angle), 0, 0],
                [numpy.sin(angle), numpy.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]

            yAng = numpy.pi / 75
            rotationYM = [
                [numpy.cos(yAng), 0, numpy.sin(yAng), 0],
                [0, 1, 0, 0],
                [-numpy.sin(yAng), 0, numpy.cos(yAng), 0],
                [0, 0, 0, 1]
            ]

            xAng = numpy.pi / 100
            rotationXM = [
                [1, 0, 0, 0],
                [0, numpy.cos(xAng), numpy.sin(xAng), 0],
                [0, -numpy.sin(xAng), numpy.cos(xAng), 0],
                [0, 0, 0, 1]
            ]

            originV = numpy.dot(v, translateToOriginM) #translate square to the top left window origin
            rotateXV = numpy.dot(originV, rotationXM) #apply rotation to square
            rotateYV = numpy.dot(rotateXV, rotationYM)
            rotateZV = numpy.dot(rotateYV, rotationZM)
            projectV = numpy.dot(rotateZV, projectionMatrix) #project onto axis 
            finalV = numpy.dot(projectV, translateToCenterM) #translate back to center of window

            vertices[i][0] = finalV[0] / finalV[3]
            vertices[i][1] = finalV[1] / finalV[3]
            vertices[i][2] = finalV[2] / finalV[3]

    cameraNormVector = [0, 0, -1] 
    # def getFacingEdges(): # trying out "back-face culling". checking if the norm of the edge
    #     facingEdges = set(edges)

    #     for edge in edges:
    #         vertice1 = vertices[edge[0]]
    #         vertice2 = vertices[edge[1]]
    #         vector1 = [vertice1[0] - xCenter, vertice1[1] - yCenter, vertice1[2]]
    #         vector2 = [vertice2[0] - xCenter, vertice2[1] - yCenter, vertice2[2]]

    #         edgeCameraCrossProduct = numpy.cross(vector1, vector2)
    #         # print('edgeCameraCrossProduct:', edgeCameraCrossProduct)
    #         edgeCameraDot = numpy.dot(edgeCameraCrossProduct, cameraNormVector)
    #         # print('edgeCameraDot:', edgeCameraDot)
    #         if edgeCameraDot >= 0:
    #             facingEdges.remove(edge)
        
    #     return facingEdges
    

    def getFaceNormal(face):
        # Get 3 vertices of the face to define a plane
        vert1 = numpy.array(vertices[face[0]])
        vert2 = numpy.array(vertices[face[1]])
        vert3 = numpy.array(vertices[face[2]])
        
        # Calculate two vectors on the face
        vector1 = vert2 - vert1
        vector2 = vert3 - vert1
        
        # Compute the normal using cross product
        normal = numpy.cross(vector1, vector2)
        return normal / numpy.linalg.norm(normal)  # Normalize the normal vector

    def getFacingEdges():
        facingEdges = set()

        for face in faces:
            # Get the normal of the face
            normal = getFaceNormal(face)
            # print('normal', normal)

            # Dot product of normal and camera direction
            edgeCameraDot = numpy.dot(normal, cameraNormVector)
            # print('edgeCameraDot')

            if edgeCameraDot > 0:  # If the face is facing the camera
                # Add edges of the face to the facing edges set
                for i in range(len(face)):
                    edge = (face[i], face[(i+1) % 4])  # Create edge pair
                    if edge not in facingEdges:
                        facingEdges.add(edge)

        return facingEdges
    

    angle_offset = numpy.pi / 33
    angle = angle_offset
    running = True
    while running:
        for line in lines:
            line.undraw()

        rotateVertices(angle)
        facingEdges = getFacingEdges()

        lines = []
        for edge in facingEdges:
            line = Line(Point(vertices[edge[0]][0], vertices[edge[0]][1]), Point(vertices[edge[1]][0], vertices[edge[1]][1])) #unpack with '*'
            line.draw(win).setWidth(2)
            line.setFill("white")
            lines.append(line)

        if win.checkMouse():
            break
        time.sleep(0.05)
        
main()