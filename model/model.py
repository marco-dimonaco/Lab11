import networkx as nx
from database.DAO import DAO
import copy


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._bestdTot = 0
        self._bestComp = []

    def buildGraph(self, color, year):
        nodes = DAO.getNodesColor(color)
        self._grafo.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.Product_number] = n
        self.addEdges(color, year)
        return True

    def addEdges(self, color, year):
        allEdges = DAO.getAllEdges(self._idMap, color, year)
        for edge in allEdges:
            if edge.p1 in self._grafo.nodes and edge.p2 in self._grafo.nodes:
                self._grafo.add_edge(edge.p1, edge.p2, weight=edge.peso)

    def getEdgeMaxWeight(self):
        result = []
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if self._grafo.has_edge(n1, n2) and (n2.Product_number, n1.Product_number, self._grafo[n1][n2]['weight']) not in result:
                    result.append((n1.Product_number, n2.Product_number, self._grafo[n1][n2]['weight']))
        result.sort(key=lambda x: x[2], reverse=True)
        result_tot = []
        for i in range(0, 3):
            result_tot.append(result[i])

        nodi_ripetuti = []
        for result in result_tot:
            name_to_count1 = result[0]
            count1 = sum(name_to_count1 in t for t in result_tot)
            name_to_count2 = result[1]
            count2 = sum(name_to_count2 in t for t in result_tot)
            if count1 > 1 and name_to_count1 not in nodi_ripetuti:
                nodi_ripetuti.append(name_to_count1)
            if count2 > 1 and name_to_count2 not in nodi_ripetuti:
                nodi_ripetuti.append(name_to_count2)
        return result_tot, nodi_ripetuti

    def getPath(self, p0):
        # caching con variabili della classe
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [p0]
        for p in self._grafo.neighbors(p0):
            parziale.append(p)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestComp

    def _ricorsione(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache
        if len(parziale)-1 > self._bestdTot:
                self._bestComp = copy.deepcopy(parziale)
                self._bestdTot = len(parziale)-1
        # verifico se posso aggiungere un altro elemento
        for a in self._grafo.neighbors(parziale[-1]):
            if a not in parziale and self._grafo[parziale[-1]][a]["weight"] >= self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(a)
                self._ricorsione(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    @staticmethod
    def getColors():
        return DAO.getAllColors()

    def printGraphDetails(self):
        return f"Il grafo ha {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi"

    def getNodes(self):
        return self._grafo.nodes

    def getEdges(self):
        return self._grafo.edges
