import streamlit as st
import pandas as pd
import altair as alt

# Charger les données
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/votre_utilisateur/votre_repo/main/alertes_par_semaine_antibiotiques_2024.xlsx"
    df = pd.read_excel(url)
    return df

df = load_data()

# Liste des antibiotiques disponibles
antibiotiques = sorted(df['Antibiotic'].unique())

# Sélectionner un antibiotique
antibiotique_choisi = st.selectbox("Sélectionnez un antibiotique :", antibiotiques)

# Filtrer les données
df_filtre = df[df['Antibiotic'] == antibiotique_choisi]

# Créer le graphique
base = alt.Chart(df_filtre).encode(
    x=alt.X('Semaine:O', title='Semaine'),
    y=alt.Y('% Resistance:Q', title='% de résistance'),
    tooltip=['Semaine', '% Resistance', 'Seuil Alerte (%)', 'Alerte']
)

courbe = base.mark_line(color='steelblue')
points = base.mark_circle(size=60).encode(
    color=alt.condition(
        alt.datum.Alerte == 'OUI',
        alt.value('red'),  # Rouge si alerte
        alt.value('steelblue')  # Bleu sinon
    )
)

# Ligne horizontale du seuil d'alerte
seuil_value = df_filtre['Seuil Alerte (%)'].iloc[0]
ligne_seuil = alt.Chart(pd.DataFrame({'y': [seuil_value]})).mark_rule(
    color='orange', strokeDash=[5,5]
).encode(y='y:Q')

# Combiner
graphique = (courbe + points + ligne_seuil).properties(
    title=f'Evolution de la résistance pour {antibiotique_choisi}',
    width=700,
    height=400
).interactive()

st.altair_chart(graphique, use_container_width=True)
