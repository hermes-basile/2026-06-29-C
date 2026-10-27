import copy
from itertools import count

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.lista_nodi_totale = DAO.getAllNodes()

        self.idMapObject = {}
        for nodo in self.lista_nodi_totale:
            self.idMapObject[nodo.ArtistId] = nodo

        self._grafo = nx.Graph()


    def crea_grafo(self):

        self._grafo.clear()

        lista_id = DAO.getNodi()

        lista_nodi = []

        for id_nodo in lista_id:
            nodo = self.idMapObject[id_nodo]
            DAO.fillbrani(nodo)
            DAO.fillplaylist(nodo)
            lista_nodi.append(nodo)

        self._grafo.add_nodes_from(lista_nodi)

        self.add_archi_model()

    def add_archi_model(self):
        lista_nodi = list(self._grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i + 1, len(lista_nodi)):

                u = lista_nodi[i]
                v = lista_nodi[j]
                lista_playlist_u = set(u.lista_playlist)

                lista_playlist_v = set(v.lista_playlist)

                set_comune = lista_playlist_u & lista_playlist_v
                peso = len(set_comune)

                if peso > 0:
                    self._grafo.add_edge(u, v, weight= peso)


    def artista_somma_pesi_maggiore(self):
        nodo_maggiore = None
        peso_ottimo = None
        lista_nodi = list(self._grafo.nodes())
        for nodo in lista_nodi:
            peso_totale = self._grafo.degree(nodo, weight="weight")
            if nodo_maggiore is None and peso_ottimo is None:
                peso_ottimo = peso_totale
                nodo_maggiore = nodo
            if peso_totale > peso_ottimo:
                peso_ottimo = peso_totale
                nodo_maggiore = nodo

        return nodo_maggiore, peso_ottimo


    def artista_grado_maggiore(self):
        lista_nodi = self._grafo.nodes()
        nodo_ottimo = None
        archi_ottimi = None
        for nodo in lista_nodi:
            numero_archi = self._grafo.degree(nodo)
            if nodo_ottimo is None and archi_ottimi is None:
                nodo_ottimo = nodo
                archi_ottimi = numero_archi

            if numero_archi >= archi_ottimi:
                nodo_ottimo = nodo
                archi_ottimi = numero_archi

        return nodo_ottimo, archi_ottimi

    def ordina_lista(self):
        lista_archi = list(self._grafo.edges(data=True))
        if len(lista_archi) >= 10:
            lista_archi_ordinata = sorted(lista_archi, key=lambda arco: (-arco[2]["weight"], arco[0].Name, arco[1].Name))
            return lista_archi_ordinata[:10]

    def crea_albero(self, source, N):
        # lista dove viene salvata la soluzione
        self.soluzione = []

        # condizione che deve migliorare la soluzione
        self.numero_brani_totale = 0

        # attiva ricorsione
        self.ricorsione([source], N)

        # ritorna soluzione finale
        return self.soluzione, self.numero_brani_totale

    def ricorsione(self, parziale, N):
        if len(parziale) == N:

            if self.calcola_brani_lista(parziale) > self.numero_brani_totale:
                #print("ho trovato dei brani in più")
                self.numero_brani_totale  = self.calcola_brani_lista(parziale)
                self.soluzione = copy.deepcopy(parziale)
            return

        set_candidati = set()
        for nodo_parziale in parziale:
            for vicino in self._grafo.neighbors(nodo_parziale):
                set_candidati.add(vicino)

        for candidato in set_candidati:
           # print("ho trovato candidati")

            if self.is_ammissibile(candidato, parziale):
               #print("ho trovato un ammissibile")
               parziale.append(candidato)
               self.ricorsione(parziale, N)
               parziale.pop()

    def calcola_brani_lista(self,lista):
        count = 0
        for nodo in lista:
            brani_nodo = len(nodo.lista_brani)
            #print("brani_nodo",brani_nodo)
            count += brani_nodo
        return count

    def is_ammissibile(self, candidato, parziale):
        if candidato in parziale:
            #print("Il candidato è in parziale")
            return False
        for nodo_parziale in parziale:
            if self._grafo.has_edge(candidato, nodo_parziale):
                peso = self._grafo[candidato][nodo_parziale]["weight"]
                if peso == 1:
                     return False
        return True

    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)