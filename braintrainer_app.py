
import streamlit as st
import pandas as pd
import random

# Laad vraagdata uit CSV
@st.cache_data
def laad_vragen(csv_path):
    df = pd.read_csv(csv_path)
    return df

# Selecteer willekeurige vragen
def selecteer_vragen(df, categorie, aantal=10):
    df_cat = df[df['categorie'] == categorie]
    return df_cat.sample(n=min(aantal, len(df_cat))).reset_index(drop=True)

# Streamlit-app
st.title("🧠 HBO Braintrainer")

# CSV upload of voorbeeldbestand gebruiken
voorbeeld_pad = "voorbeeld_vragen.csv"
vragen_csv = st.file_uploader("Upload een CSV met vragen:", type="csv")
if vragen_csv is not None:
    df_vragen = laad_vragen(vragen_csv)
else:
    st.info("Geen bestand geüpload. Voorbeeldbestand wordt gebruikt.")
    df_vragen = laad_vragen(voorbeeld_pad)

# Categorieën tonen
categorieën = df_vragen['categorie'].unique()
categorie = st.selectbox("Kies een toetscategorie:", categorieën)

# Selecteer vragen en start quiz
vragen = selecteer_vragen(df_vragen, categorie)
score = 0
antwoorden = []

st.subheader(f"Toets: {categorie}")
for i, rij in vragen.iterrows():
    st.markdown(f"**Vraag {i+1}:** {rij['vraag']}")
    keuze = st.radio(
        label="",
        options=[rij['optie_a'], rij['optie_b'], rij['optie_c'], rij['optie_d']],
        key=f"vraag_{i}"
    )
    antwoorden.append(keuze)
    if keuze == rij[f"optie_{rij['correcte_optie'].lower()}"]:
        score += 1

# Resultaten
if st.button("Bekijk resultaat"):
    st.success(f"Je scoorde {score} van de {len(vragen)}!")
    if 'scoregeschiedenis' not in st.session_state:
        st.session_state.scoregeschiedenis = []
    st.session_state.scoregeschiedenis.append((categorie, score, len(vragen)))

# Toon geschiedenis
if 'scoregeschiedenis' in st.session_state:
    st.markdown("### 📊 Scoregeschiedenis")
    for i, (cat, s, totaal) in enumerate(st.session_state.scoregeschiedenis):
        st.write(f"{i+1}. {cat}: {s}/{totaal}")
