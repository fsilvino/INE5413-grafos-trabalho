from Relationship import Relationship

class Vertex:
    
    def __init__(self, number, label):
        self.number = number
        self.label = label
        self.relationships = {}

    def addRelationship(self, destinationVertex, weight):
        self.relationships[destinationVertex] = Relationship(destinationVertex, weight)

    def findRelationship(self, vertexNumber):
        if (vertexNumber in self.relationships):
            return self.relationships[vertexNumber]
        return None

    def isNeighborOf(self, vertexNumber):
        return self.findRelationship(vertexNumber) != None

