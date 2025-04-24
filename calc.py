import streamlit as st
import math

st.set_page_config(page_title="Calcolatrice", layout="centered")
st.title("🧮 Calcolatrice Avanzata")

# Inizializzazione stati
for k in ["cronologia", "valori_delta", "valori_molt", "valori_p", "sconti"]:
    if k not in st.session_state:
        st.session_state[k] = []

def rimuovi_percentuale(v):
    if isinstance(v, str) and "%" in v:
        return float(v.replace("%", "")) / 100
    return float(v)

def eval_expr(expr):
    try:
        return eval(expr)
    except:
        return "Errore"

def esegui_delta():
    v = st.session_state.valori_delta
    try:
        return f"{((v[1] - v[0]) / v[0] * 100):.3f}%"
    except:
        return "Errore"

def esegui_molt():
    v = st.session_state.valori_molt
    try:
        return f"{((v[1] * 2) / v[0]):.2f}"
    except:
        return "Errore"

def esegui_p():
    v = st.session_state.valori_p
    try:
        r = v[0] - ((100 - v[0]) / (100 / v[1]))
        return f"{r:.3f}%"
    except:
        return "Errore"

def sconto_inverso(v):
    try:
        v = float(v)
        return f"{round(100 * (1 - 1 / (1 - (v / 100))), 3)}"
    except:
        return "Errore"

def somma_sconti(s1, s2):
    try:
        return f"{(((s1/100)+(s2/100))-(s1/100*s2/100))*100:.3f}%"
    except:
        return "Errore"

# Input principale
expr = st.text_input("Inserisci numero o espressione:", "")

# Calcoli principali
cols = st.columns(3)
if cols[0].button("Calcola"):
    risultato = eval_expr(expr)
    st.session_state.cronologia.insert(0, f"{expr} = {risultato}")
    st.success(f"Risultato: {risultato}")

if cols[1].button("Δ Delta"):
    try:
        st.session_state.valori_delta.append(rimuovi_percentuale(expr))
        if len(st.session_state.valori_delta) == 2:
            res = esegui_delta()
            st.success(f"Δ: {res}")
            st.session_state.cronologia.insert(0, f"Δ: {res}")
            st.session_state.valori_delta.clear()
    except:
        st.error("Errore nei valori")

if cols[2].button("M Moltiplicatore"):
    try:
        st.session_state.valori_molt.append(rimuovi_percentuale(expr))
        if len(st.session_state.valori_molt) == 2:
            res = esegui_molt()
            st.success(f"M: {res}")
            st.session_state.cronologia.insert(0, f"M: {res}")
            st.session_state.valori_molt.clear()
    except:
        st.error("Errore nei valori")

cols2 = st.columns(3)
if cols2[0].button("P Prezzo → Ricavo"):
    try:
        st.session_state.valori_p.append(rimuovi_percentuale(expr))
        if len(st.session_state.valori_p) == 2:
            res = esegui_p()
            st.success(f"P: {res}")
            st.session_state.cronologia.insert(0, f"P: {res}")
            st.session_state.valori_p.clear()
    except:
        st.error("Errore nei valori")

if cols2[1].button("S Somma sconti"):
    try:
        st.session_state.sconti.append(rimuovi_percentuale(expr))
        if len(st.session_state.sconti) >= 2:
            res = somma_sconti(st.session_state.sconti[-2], st.session_state.sconti[-1])
            st.success(f"S: {res}")
            st.session_state.cronologia.insert(0, f"S: {res}")
            st.session_state.sconti = [float(res.replace("%", ""))]
    except:
        st.error("Errore nei valori")

if cols2[2].button("1/s Inverso"):
    res = sconto_inverso(expr)
    st.success(f"Inverso: {res}")
    st.session_state.cronologia.insert(0, f"1/s: {res}")

# Cronologia
if st.session_state.cronologia:
    st.markdown("### 📜 Cronologia")
    for riga in st.session_state.cronologia:
        st.write("•", riga)
