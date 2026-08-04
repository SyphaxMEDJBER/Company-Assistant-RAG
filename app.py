import streamlit as st

from src.generation import generate_answer

st.title("Assistant IT — NovaTech Solutions")

question = st.text_input("Pose ta question :")

# "and question" : evite d'appeler generate_answer("") si on clique sans rien taper.
if st.button("Envoyer") and question:
    # generate_answer() peut prendre du temps (appel a Ollama) : le spinner
    # donne un retour visuel pendant l'attente plutot qu'un ecran fige.
    with st.spinner("Recherche en cours..."):
        answer = generate_answer(question)
    st.write(answer)
