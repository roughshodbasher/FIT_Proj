"""

distanceMatrix = [[0, 2086, 3242, 3331, 9165, 24737, 25172, 19199],
        [1156, 0, 1156, 3611, 10440, 26012, 26448, 10719],
        [2312, 1156, 0, 2884, 8937, 24509, 24944, 9563],
        [5400, 4244, 3518, 0, 5890, 22734, 23169, 11802],
        [10778, 10212, 8795, 6327, 0, 18795, 19344, 13223],
        [30372, 29806, 28389, 25921, 23532, 0, 18879, 33823],
        [17645, 16489, 15333, 27188, 24790, 20628, 0, 14944],
        [13536, 10572, 9416, 23135, 13391, 30161, 15128, 0],    ]
"""
import numpy as np
import random

class minRoute:
    def __init__(self, distanceMatrix, startFinish=False):
        self.distanceMatrix = distanceMatrix
        self.startFinish = startFinish
        self.route = []
        self.order = []

    def getOrder(self):
        self.Solve()
        return self.order



    def Solve(self):
        class Node:
            def __init__(self, Id, distanceToNode):
                self.id = Id
                self.cost = np.inf
                self.parent = None
                self.distanceToNode = distanceToNode
                self.added = False

            def getParent(self):
                return self.parent

            def setParent(self,parentNode):
                self.parent = parentNode

            def getCost(self):
                return self.cost

            def setCost(self, amount):
                self.cost = amount
                return True

        nodeArray = []
        for i in range(len(self.distanceMatrix)):
            nodeArray.append(Node(i,self.distanceMatrix[i]))

        nodeArray[0].cost = 0
        cDist = 0
        Q = nodeArray[:]
        while Q:
            cNode = Q.pop(0)
            cNode.added = True
            for i in range(len(nodeArray)):
                if i != cNode.id and not nodeArray[i].added:
                    nodeArray[i].cost = cNode.cost + cNode.distanceToNode[i]
                    nodeArray[i].setParent(cNode)
            Q = self.nodeSort(Q)
        revOrder = []
        while cNode.getParent():
            revOrder.append(cNode)
            cNode = cNode.getParent()
        revOrder.append(cNode)
        for elem in revOrder:
            self.order = [elem.id] + self.order

    def nodeSort(self,nodeArray):
        if len(nodeArray) == 0:
            return []
        elif len(nodeArray) == 1:
            return nodeArray
        elif len(nodeArray) == 2:
            if nodeArray[0].cost < nodeArray[1].cost:
                return nodeArray
            else:
                return [nodeArray[1],nodeArray[0]]
        else:
            pivot = nodeArray[random.randint(0,len(nodeArray)-1)]
            lhs = []
            rhs = []
            for elem in nodeArray:
                if elem != pivot:
                    if elem.cost < pivot.cost:
                        lhs.append(elem)
                    else:
                        rhs.append(elem)
            return lhs + [pivot] + rhs



if __name__ == "__main__":
    distanceMatrix = [[0, 2086, 3242, 3331, 9165, 24737, 25172, 19199],
                      [1156, 0, 1156, 3611, 10440, 26012, 26448, 10719],
                      [2312, 1156, 0, 2884, 8937, 24509, 24944, 9563],
                      [5400, 4244, 3518, 0, 5890, 22734, 23169, 11802],
                      [10778, 10212, 8795, 6327, 0, 18795, 19344, 13223],
                      [30372, 29806, 28389, 25921, 23532, 0, 18879, 33823],
                      [17645, 16489, 15333, 27188, 24790, 20628, 0, 14944],
                      [13536, 10572, 9416, 23135, 13391, 30161, 15128, 0], ]
    c = minRoute(distanceMatrix)
    print(c.getOrder())