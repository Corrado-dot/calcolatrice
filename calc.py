st.set_page_config(page_title="Calcolatrice", layout="centered")
import streamlit as st
import math

st.set_page_config(page_title="Calcolatrice", layout="centered")
st.title("🧮 Calcolatrice Avanzata")

# Inizializza variabili di stato
for var in ["valori_delta", "valori_molt", "valori_p", "sconti", "cronologia"]:
    if var not in st.session_state:
        st.session_state[var] = []

# Funzioni ausiliarie
def rimuovi_percentuale(val):
    if isinstance(val, str) and "%" in val:
        return float(val.replace("%", "")) / 100
    return float(val)

def esegui_delta():
    try:
        v1, v2 = st.session_state.valori_delta
        return f"{((v2 - v1) / v1 * 100):.3f}%"
    except:
        return "Errore"

def esegui_molt():
    try:
        v1, v2 = st.session_state.valori_molt
        return f"{((v2 * 2) / v1):.2f}"
    except:
        return "Errore"

def esegui_p():
    try:
        v1, v2 = st.session_state.valori_p
        res = v1 - ((100 - v1) / (100 / v2))
        return f"{res:.3f}%"
    except:
        return "Errore"

def sconto_inverso(v):
    try:
        v = float(v)
        return str(round(100 * (1 - 1 / (1 - (v / 100))), 3))
    except:
        return "Errore"

def somma_sconti(s1, s2):
    try:
        composito = (((s1 / 100) + (s2 / 100)) - (s1 / 100 * s2 / 100)) * 100
        return f"{composito:.3f}%"
    except:
        return "Errore"

# Input dell'utente
espr = st.text_input("📥 Inserisci numero o espressione:", "")

# Pulsanti operativi
col1, col2, col3 = st.columns(3)

if col1.button("🧮 Calcola"):
    try:
        risultato = eval(espr)
        st.success(f"Risultato: {risultato}")
        st.session_state.cronologia.insert(0, f"{espr} = {risultato}")
    except:
        st.error("Errore di sintassi")

if col2.button("Δ Delta"):
    try:
        st.session_state.valori_delta.append(rimuovi_percentuale(espr))
        if len(st.session_state.valori_delta) == 2:
            res = esegui_delta()
            st.success(f"Δ: {res}")
            st.session_state.cronologia.insert(0, f"Δ: {res}")
            st.session_state.valori_delta = []
    except:
        st.error("Errore nei dati")

if col3.button("M Moltiplicatore"):
    try:
        st.session_state.valori_molt.append(rimuovi_percentuale(espr))
        if len(st.session_state.valori_molt) == 2:
            res = esegui_molt()
            st.success(f"M: {res}")
            st.session_state.cronologia.insert(0, f"M: {res}")
            st.session_state.valori_molt = []
    except:
        st.error("Errore nei dati")

col4, col5, col6 = st.columns(3)

if col4.button("P Prezzo da sconto"):
    try:
        st.session_state.valori_p.append(rimuovi_percentuale(espr))
        if len(st.session_state.valori_p) == 2:
            res = esegui_p()
            st.success(f"P: {res}")
            st.session_state.cronologia.insert(0, f"P: {res}")
            st.session_state.valori_p = []
    except:
        st.error("Errore nei dati")

if col5.button("S Somma sconti"):
    try:
        s = rimuovi_percentuale(espr)
        st.session_state.sconti.append(s)
        if len(st.session_state.sconti) >= 2:
            res = somma_sconti(st.session_state.sconti[-2], st.session_state.sconti[-1])
            st.success(f"S: {res}")
            st.session_state.cronologia.insert(0, f"S: {res}")
            st.session_state.sconti = [float(res.replace("%", ""))]
    except:
        st.error("Errore nei dati")

if col6.button("1/s Inverso"):
    res = sconto_inverso(espr)
    st.success(f"Inverso: {res}")
    st.session_state.cronologia.insert(0, f"1/s: {res}")

# Cronologia
if st.session_state.cronologia:
    st.markdown("### 📜 Cronologia")
    for voce in st.session_state.cronologia:
        st.write("•", voce)

