from Relationship import Relationship

class Vertex:
    
    def __init__(self, number, label):
        self.number = number
        self.label = label
        self.relationships = []

    def addRelationship(self, destinationVertex, weight):
        self.relationships.append(Relationship(destinationVertex, weight))

    def findRelationship(self, vertexNumber):
        for relationship in self.relationships:
            if (relationship.destinationVertex.number == vertexNumber):
                return relationship
        return None

    def isNeighborOf(self, vertexNumber):
        return self.findRelationship(vertexNumber) != None

