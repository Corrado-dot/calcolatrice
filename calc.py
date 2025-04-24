import tkinter as tk
import math

class Tooltip:
    def __init__(self, widget, text, timeout=3000):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.timeout = timeout
        self.after_id = None

        widget.bind("<Enter>", self.mostra_tooltip)
        widget.bind("<Leave>", self.nascondi_tooltip)
        


    def mostra_tooltip(self, event=None):
        if self.tooltip or not self.text:
            return
        x = y = 0
        x += self.widget.winfo_rootx() + 50
        y += self.widget.winfo_rooty() + 30
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip, text=self.text, justify='left',
            background="#ffffe0", relief='solid', borderwidth=1,
            font=("Segoe UI", 10)
        )
        label.pack(ipadx=4, ipady=2)
        self.after_id = self.tooltip.after(self.timeout, self.nascondi_tooltip)

    def nascondi_tooltip(self, event=None):
        if self.tooltip:
            if self.after_id:
                self.tooltip.after_cancel(self.after_id)
                self.after_id = None
            self.tooltip.destroy()
            self.tooltip = None

class Calcolatrice:
    def __init__(self, root):
        self.root = root
        self.root.title("Calcolatrice")
        self.root.geometry("400x700")
        self.root.resizable(False, False)

        self.equazione = ""
        self.input_corrente = ""
        self.valori_delta = []
        self.valori_molt = []
        self.sconti = []
        self.valori_p = []
        self.reset_input = False

        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.btn_color = "#2d2d2d"
        self.highlight = "#007acc"
        self.schermo_font_size = 30

        self.root.configure(bg=self.bg_color)

        self.schermo = tk.Label(
            root, text="", anchor="e", bg=self.bg_color, fg=self.fg_color,
            font=("Segoe UI", self.schermo_font_size), relief="sunken", bd=5, height=2
        )
        self.schermo.pack(fill="both")

        self.crea_pulsanti()
        self.crea_cronologia()
        self.root.bind("<Key>", self.gestisci_tastiera)
    def gestisci_tastiera(self, event):
        tasto = event.char.lower()
        if tasto == "x":
            tasto = "*"
        if tasto in "0123456789.+-*/":
            self.premi(tasto)
        elif event.keysym == "Return":
            self.premi("=")
        elif event.keysym == "BackSpace":
            self.premi("⌫")
        elif tasto.lower() == "c":
            self.premi("C")
        elif event.keysym == "Escape":
            self.root.destroy()
        elif tasto.lower() == "d":
            self.premi("Δ")
        elif tasto.lower() == "m":
            self.premi("M")
        elif tasto.lower() == "p":
            self.premi("P")
        elif tasto.lower() == "s":
            self.premi("S")
        elif tasto.lower() == "%":
            self.premi("%")
        elif tasto.lower() == "i":
            self.premi("1/s")


    

    def aggiorna_schermo(self):
        testo = self.input_corrente if self.input_corrente else self.equazione
        self._adatta_font(testo)
        self.schermo.config(text=testo)

    def _adatta_font(self, testo):
        lunghezza = len(testo)
        if lunghezza <= 10:
            size = 30
        elif lunghezza <= 15:
            size = 24
        elif lunghezza <= 20:
            size = 18
        else:
            size = 14
        if size != self.schermo_font_size:
            self.schermo_font_size = size
            self.schermo.config(font=("Segoe UI", self.schermo_font_size))

    def premi(self, tasto):
        if tasto in "0123456789.":
            if self.reset_input:
                self.input_corrente = ""
                self.reset_input = False
            self.input_corrente += str(tasto)
        elif tasto in "+-*/":
            if self.input_corrente:
                self.equazione += self.input_corrente
            self.equazione += tasto
            self.input_corrente = ""
        elif tasto == "=":
            if self.input_corrente:
                self.valori_p.append(self.rimuovi_percentuale(self.input_corrente))
                self.valori_delta.append(self.rimuovi_percentuale(self.input_corrente))
                self.valori_molt.append(self.rimuovi_percentuale(self.input_corrente))
            if len(self.valori_p) == 2:
                self.esegui_calcolo_p()
            elif len(self.valori_delta) == 2:
                self.esegui_calcolo_delta_formula()
            elif len(self.valori_molt) == 2:
                self.esegui_calcolo_molt()
            else:
                try:
                    self.equazione += self.input_corrente
                    risultato = eval(self.equazione)
                    operazione = self.equazione
                    self.input_corrente = str(risultato)
                    self.equazione = ""
                    self.aggiungi_a_cronologia(risultato, operazione)
                except:
                    self.input_corrente = "Errore"
                    self.equazione = ""
                self.valori_p = []
                self.valori_delta = []
                self.valori_molt = []
        elif tasto == "C":
            self.equazione = ""
            self.input_corrente = ""
            self.valori_delta = []
            self.sconti = []
            self.valori_p = []
            self.valori_molt = []
        elif tasto == "📋":
            contenuto = self.input_corrente if self.input_corrente else self.equazione
            if contenuto:
                self.root.clipboard_clear()
                contenuto = contenuto.replace("%", "")
                contenuto = contenuto.replace(".", ",")
                self.root.clipboard_append(contenuto)
        elif tasto == "📥":  # Incolla
            try:
                contenuto = self.root.clipboard_get()
                contenuto = contenuto.replace("%", "")  
                contenuto = contenuto.replace(".", "")  # Rimuove i punti
                contenuto = contenuto.replace(",", ".")  # Sostituisce virgole con punto
                float(contenuto)  # Verifica se è un numero valido
                self.input_corrente = contenuto
            except:
                self.input_corrente = "Errore"
        elif tasto == "CE":
            self.input_corrente = ""
        elif tasto == "⌫":
            self.input_corrente = self.input_corrente[:-1]
        elif tasto == "+/-":
            if self.input_corrente.startswith("-"):
                self.input_corrente = self.input_corrente[1:]
            elif self.input_corrente:
                self.input_corrente = "-" + self.input_corrente
        elif tasto == "√":
            try:
                valore = float(self.input_corrente)
                self.input_corrente = str(math.sqrt(valore))
            except:
                self.input_corrente = "Errore"
        elif tasto == "x²":
            try:
                valore = float(self.input_corrente)
                self.input_corrente = str(valore ** 2)
            except:
                self.input_corrente = "Errore"
        elif tasto == "1/s":
            try:
                valore = float(self.input_corrente)
                self.input_corrente = str(round(100 * (1 - 1 / (1 - (valore / 100))), 3))
            except:
                self.input_corrente = "Errore"
        elif tasto == "%":
            try:
                if self.equazione and self.input_corrente:
                    for op in "+-*/":
                        if op in self.equazione:
                            parti = self.equazione.rsplit(op, 1)
                            if len(parti) == 2:
                                base = float(parti[0])
                                percentuale = float(self.input_corrente)
                                valore_percentuale = base * percentuale / 100
                                self.input_corrente = str(valore_percentuale)
                                break
                else:
                    valore = float(self.input_corrente)
                    self.input_corrente = str(valore / 100)
            except:
                self.input_corrente = "Errore"
        elif tasto == "Δ":
            if self.input_corrente:
                self.valori_delta.append(self.rimuovi_percentuale(self.input_corrente))
                self.input_corrente = ""
            if len(self.valori_delta) == 2:
                self.esegui_calcolo_delta_formula()
        elif tasto == "M":
            if self.input_corrente:
                self.valori_molt.append(self.rimuovi_percentuale(self.input_corrente))
                self.input_corrente = ""
            if len(self.valori_molt) == 2:
                self.esegui_calcolo_molt()
        elif tasto == "P":
            if self.input_corrente:
                self.valori_p.append(self.rimuovi_percentuale(self.input_corrente))
                self.input_corrente = ""
            if len(self.valori_p) == 2:
                self.esegui_calcolo_p()

        elif tasto == "S":
            self.applica_sconto()

        self.aggiorna_schermo()

    def rimuovi_percentuale(self, valore):
        if isinstance(valore, str) and "%" in valore:
            return float(valore.replace("%", "")) / 100
        return float(valore)

    def esegui_calcolo_delta_formula(self):
        try:
            val1, val2 = self.valori_delta
            risultato = (val2 - val1) / val1 * 100
            self.input_corrente = f"{risultato:.3f}%"
            operazione = f"{val1:.3f} Δ {val2:.3f}"
            self.aggiungi_a_cronologia(self.input_corrente, operazione)
        except:
            self.input_corrente = "Errore"
        self.valori_delta = []
    def esegui_calcolo_molt(self):
        try:
            val1, val2 = self.valori_molt
            risultato = (val2 * 2) / val1
            self.input_corrente = f"{risultato:.2f}"
            operazione = f"{val1:.3f} M {val2:.3f}"
            self.aggiungi_a_cronologia(self.input_corrente, operazione)
        except:
            self.input_corrente = "Errore"
        self.valori_molt = []
    def esegui_calcolo_p(self):
        try:
            val1, val2 = self.valori_p
            risultato = val1 - ((100 - val1) / (100 / val2))
            self.input_corrente = f"{risultato:.3f}%"
            operazione = f"{val1:.3f} P {val2:.3f}"
            self.aggiungi_a_cronologia(self.input_corrente, operazione)
        except:
            self.input_corrente = "Errore"
        self.valori_p = []

    def applica_sconto(self):
        try:
            if self.input_corrente:
                sconto = self.rimuovi_percentuale(self.input_corrente)
                self.input_corrente = ""

                if not self.sconti:
                    self.sconti.append(sconto)
                else:
                    self.sconti.append(sconto)
                    if len(self.sconti) >= 2:
                        s1, s2 = self.sconti[-2], self.sconti[-1]
                        sconto_composito = (((s1 / 100) + (s2 / 100)) - (s1 / 100 * s2 / 100)) * 100
                        self.input_corrente = f"{sconto_composito:.3f}%"
                        operazione = f"{s1:.3f} S {s2:.3f}"
                        self.aggiungi_a_cronologia(self.input_corrente, operazione)
                        self.sconti = [sconto_composito]
                        self.reset_input = True
        except:
            self.input_corrente = "Errore"
            self.sconti = []

    def crea_pulsanti(self):
        layout = [
            ["1/s", "S", "P", "M"],
            ["📋", "📥", "Δ", "C"],
            ["%", "x²", "√", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="]
        ]
        griglia = tk.Frame(self.root, bg=self.bg_color)
        griglia.pack(expand=True, fill="both")
        for riga_idx, riga in enumerate(layout):
            for col_idx, testo in enumerate(riga):
                btn = tk.Button(
                    griglia, text=testo, font=("Segoe UI", 20),
                    bg=self.btn_color, fg=self.fg_color,
                    activebackground=self.highlight,
                    command=lambda t=testo: self.premi(t)
                )
                btn.grid(row=riga_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                if testo == "S":
                    Tooltip(btn, "Somma sconti a cascata (es. 10% S 20%)")
                if testo == "1/s":
                    Tooltip(btn, "Calcola sconto inverso")
                if testo == "M":
                    Tooltip(btn, "Moltiplicatore VM avendo Netto e T1")
                if testo == "P":
                    Tooltip(btn, "Calcolo sconto partendo da sc.acq. e ric.desiderata")
                if testo == "Δ":
                    Tooltip(btn, "Calcolo delta tra due valori")
                if testo == "📋":
                    Tooltip(btn, "Copia")
                if testo == "📥":
                    Tooltip(btn, "Incolla")



        for i in range(len(layout)):
            griglia.rowconfigure(i, weight=1)
        for j in range(4):
            griglia.columnconfigure(j, weight=1)

    def crea_cronologia(self):
        self.cronologia = tk.Listbox(self.root, bg=self.bg_color, fg=self.fg_color,
                                     font=("Segoe UI", 12), height=6)
        self.cronologia.pack(fill="both", padx=5, pady=5)

    def aggiungi_a_cronologia(self, valore, operazione=None):
        if operazione:
            self.cronologia.insert(0, f"Calcolo: {operazione} = {valore}")
        else:
            self.cronologia.insert(0, f"Risultato: {valore}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Calcolatrice(root)
    root.mainloop()
