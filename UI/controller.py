import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_product = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        for i in range(2015, 2019):
            self._listYear.append(i)
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))
        allColors = self._model.getColors()
        for color in allColors:
            self._listColor.append(color)
            self._view._ddcolor.options.append(ft.dropdown.Option(color))
        self._view.update_page()

    def handle_graph(self, e):
        color = self._view._ddcolor.value
        year = self._view._ddyear.value
        self._view.txtOut.controls.clear()
        if color is None or year is None:
            self._view.create_alert("Seleziona un colore e un anno!")
            self._view.update_page()
            return
        else:
            grafo = self._model.buildGraph(color, year)
            if grafo:
                self._view.txtOut.controls.append(ft.Text("Grafo creato correttamente!"))
                self._view.txtOut.controls.append(ft.Text(f"{self._model.printGraphDetails()}"))
                results, ripetuti = self._model.getEdgeMaxWeight()
                self._view.txtOut.controls.append(ft.Text("Di seguito i 3 archi con il peso maggiore:"))
                for arco in results:
                    self._view.txtOut.controls.append(ft.Text(f"Arco da {arco[0]} a {arco[1]}, peso={arco[2]}"))
                self._view.txtOut.controls.append(ft.Text(f"Nodi ripetuti:"))
                for ripetuto in ripetuti:
                    self._view.txtOut.controls.append(ft.Text(f"{ripetuto}"))
                self.fillDDProduct()
                self._view.update_page()
                return
            else:
                self._view.txtOut.controls.append(ft.Text("Errore nella creazione del grafo!"))
                self._view.update_page()
                return

    def fillDDProduct(self):
        self._view._ddnode.options.clear()
        nodi = self._model.getNodes()
        for n in nodi:
            self._view._ddnode.options.append(
                ft.dropdown.Option(text=n.Product_number, data=n, on_click=self.readDDProducts))
        self._view.update_page()

    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        if len(self._model.getNodes()) == 0:
            self._view.txtOut2.controls.append(ft.Text("Creare un grafo!"))
            self._view.update_page()
            return
        if self._selected_product is None:
            self._view.txtOut2.controls.append(ft.Text("Selezionare un prodotto!"))
            self._view.update_page()
            return
        componenti = self._model.getPath(self._selected_product)
        if componenti:
            self._view.txtOut2.controls.append(ft.Text(f"Lunghezza: {len(componenti) - 1}"))
            for c in componenti:
                self._view.txtOut2.controls.append(ft.Text(f"{c}"))
            self._view.update_page()
            return
        else:
            self._view.txtOut2.controls.append(ft.Text("Errore durante l'analisi dei componenti!", color='red'))
            self._view.update_page()
            return

    def readDDProducts(self, e):
        if e.control.data is None:
            self._selected_product = None
        else:
            self._selected_product = e.control.data
