import streamlit as st
import math

st.set_page_config(page_title="Calcolatrice", layout="centered")
st.title("🧮 Calcolatrice Avanzata")

# Stati iniziali
if "input" not in st.session_state:
    st.session_state.input = ""
if "cronologia" not in st.session_state:
    st.session_state.cronologia = []
if "valori_delta" not in st.session_state:
    st.session_state.valori_delta = []
if "valori_molt" not in st.session_state:
    st.session_state.valori_molt = []
if "valori_p" not in st.session_state:
    st.session_state.valori_p = []
if "sconti" not in st.session_state:
    st.session_state.sconti = []
def rimuovi_percentuale(val):
    if isinstance(val, str) and "%" in val:
        return float(val.replace("%", "")) / 100
    return float(val)

def safe_eval(expr):
    try:
        return str(eval(expr))
    except:
        return "Errore"

def calcolo_delta():
    try:
        a, b = st.session_state.valori_delta
        r = (b - a) / a * 100
        return f"{r:.3f}%"
    except:
        return "Errore"

def calcolo_molt():
    try:
        a, b = st.session_state.valori_molt
        r = (b * 2) / a
        return f"{r:.2f}"
    except:
        return "Errore"

def calcolo_p():
    try:
        a, b = st.session_state.valori_p
        r = a - ((100 - a) / (100 / b))
        return f"{r:.3f}%"
    except:
        return "Errore"

def sconto_inverso(val):
    try:
        val = float(val)
        r = 100 * (1 - 1 / (1 - (val / 100)))
        return f"{r:.3f}"
    except:
        return "Errore"

def somma_sconti(s1, s2):
    try:
        return f"{(((s1/100)+(s2/100))-(s1/100*s2/100))*100:.3f}%"
    except:
        return "Errore"
def crea_pulsanti():
    layout = [
        ["1/s", "S", "P", "M"],
        ["📋", "📥", "Δ", "C"],
        ["%", "x²", "√", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["+/-", "0", ".", "="]
    ]

    for riga in layout:
        cols = st.columns(len(riga))
        for i, tasto in enumerate(riga):
            with cols[i]:
                if tasto == "=":
                    if st.button(tasto):
                        if st.session_state.input:
                            st.session_state.cronologia.append(st.session_state.input)
                            st.session_state.input = safe_eval(st.session_state.input)
                            st.session_state.input = st.session_state.input
                else:
                    if st.button(tasto):
                        if tasto == "C":
                            st.session_state.input = ""
                        elif tasto == "📋":
                            st.session_state.input = st.session_state.input.replace(",", ".")
                            st.session_state.input = st.session_state.input.replace(".", ",")
                            st.session_state.input = st.session_state.input
                            st.session_state.input
                        elif tasto == "📥":
                            st.session_state.input = st.session_state.input
                        elif tasto == "S":
                            st.session_state.sconti.append(float(st.session_state.input))
                            st.session_state.input = somma_sconti(st.session_state.sconti[0],st.session_state.sconti[1])
                        elif tasto == "1/s":
                            st.session_state.input = sconto_inverso(st.session_state.input)
                        elif tasto == "Δ":
                            st.session_state.valori_delta.append(rimuovi_percentuale(st.session_state.input))
                            if len(st.session_state.valori_delta) == 2:
                                st.session_state.input = calcolo_delta()
                        elif tasto == "M":
                            st.session_state.valori_molt.append(rimuovi_percentuale(st.session_state.input))
                            if len(st.session_state.valori_molt) == 2:
                                st.session_state.input = calcolo_molt()
                        elif tasto == "P":
                            st.session_state.valori_p.append(rimuovi_percentuale(st.session_state.input))
                            if len(st.session_state.valori_p) == 2:
                                st.session_state.input = calcolo_p()
                        elif tasto == "x²":
                            st.session_state.input = str(float(st.session_state.input)**2)
                        elif tasto == "√":
                            st.session_state.input = str(math.sqrt(float(st.session_state.input)))
                        elif tasto == "+/-":
                            if st.session_state.input.startswith("-"):
                                st.session_state.input = st.session_state.input[1:]
                            else:
                                st.session_state.input = "-" + st.session_state.input
                        else:
                            st.session_state.input += tasto

def mostra_risultato():
    if st.session_state.input:
        st.subheader(f"Risultato: {st.session_state.input}")

def mostra_cronologia():
    if st.session_state.cronologia:
        st.subheader("Cronologia:")
        for entry in st.session_state.cronologia:
            st.write(entry)

def app():
    # Impostazioni iniziali
    if 'input' not in st.session_state:
        st.session_state.input = ""
    if 'cronologia' not in st.session_state:
        st.session_state.cronologia = []
    if 'valori_delta' not in st.session_state:
        st.session_state.valori_delta = []
    if 'valori_molt' not in st.session_state:
        st.session_state.valori_molt = []
    if 'valori_p' not in st.session_state:
        st.session_state.valori_p = []
    if 'sconti' not in st.session_state:
        st.session_state.sconti = []
    
    st.title("Calcolatrice Avanzata")
    
    # Mostra input corrente
    st.text_input("Operazione in corso:", value=st.session_state.input, key="input", disabled=True)

    # Crea pulsanti per la calcolatrice
    crea_pulsanti()

    # Mostra il risultato
    mostra_risultato()

    # Mostra cronologia dei calcoli
    mostra_cronologia()

if __name__ == "__main__":
    app()
