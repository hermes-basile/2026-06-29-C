import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.result1 = None



    def handleCreaGrafo(self, e):

        self._view._btnStampaInfo.disabled = True
        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(
            ft.Text("Stiamo creando il grafo, aspetta qualche secondo.."))
        self._view.update_page()

        # Creare il grafo da model e pulire la view
        self._model.crea_grafo()
        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. ", color="green"))

        self._view._txt_result.controls.append(ft.Text(
            f"Il grafo ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi."))

        self._view._btnStampaInfo.disabled = False
        self.fill_DD()




        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        artista,collegamenti = self._model.artista_grado_maggiore()

        self._view._txt_result.controls.append(
            ft.Text(f"L'artista con grado maggiore è {artista} con {collegamenti} collegamenti. \n" ))


        artista1, peso = self._model.artista_somma_pesi_maggiore()

        self._view._txt_result.controls.append(
            ft.Text(f"L'artista che ha somma dei pesi massima è {artista1} con un peso totale di {peso} \n"))

        self._view._txt_result.controls.append(ft.Text(f"Di seguito la lista ordinata per pesi decrescenti degli archi \n"))

        lista = self._model.ordina_lista()
        for arco in lista:
            self._view._txt_result.controls.append(ft.Text(f"{arco[0]} -- {arco[1]} , con peso {arco[2]['weight']}"))
        self._view.update_page()

    def fill_DD(self):

        self._view._ddArtista.options.clear()
        self._view._ddArtista.value = None
        self.result1 = None

        lista_da_caricare = list(self._model._grafo.nodes())

        for elemento in lista_da_caricare:
            self._view._ddArtista.options.append(
                ft.dropdown.Option(
                    text=str(elemento),
                    data=elemento,
                    on_click=self.readResult1
                )
            )

    def readResult1(self, e):
        self.result1 = e.control.data




    def handleSelezione(self,e):
        scelta_utente = self.result1

        if scelta_utente is None:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione prima di proseguire è necessario scegliere un opzione del dropdown", color="red"))
            self._view.update_page()

            return

        self._view._txt_result.controls.clear()

        txt_in = self._view._txtInN.value

        if txt_in is None or txt_in.strip() == "":
            self._view._txt_result.controls.append(ft.Text(
                "Devi inserire un valore valido", color="red"))
            self._view.update_page()
            return

        try:
            number = int(txt_in)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione, gli unici caratteri ammessi sono da 0 a 9: puoi inserire solo numeri", color="red"))
            self._view._txtInN.value = ""
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text(f"Tutti i dati inseriti sono coerenti", color="green"))

        # controllo eventuali vincoli della traccia
        if number < 2:
            self._view._txt_result.controls.append(
                ft.Text("Il numero deve essere almeno 2", color="red")
            )
            self._view.update_page()
            return


        soluzione, numero_brani_totale = self._model.crea_albero(scelta_utente, number)


        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(ft.Text(f"Il numero totale di artisti è {len(soluzione)}. \n"))
        self._view._txt_result.controls.append(ft.Text(f"Il numero totale di brani è: {numero_brani_totale}"))

        for nodo in soluzione:
            self._view._txt_result.controls.append(ft.Text(f"{nodo}, con {len(nodo.lista_brani)} tracce e inserito in {len(nodo.lista_playlist)} playlist"))
        self._view._txt_result.controls.append(ft.Text(f""))
        self._view.update_page()
