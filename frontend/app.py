"""
Application Streamlit — Pharma Chatbot.
Page principale : Chatbot client.

Lance avec :
    streamlit run frontend/app.py
"""
import sys
from pathlib import Path

# Ajouter la racine du projet au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

import uuid
from datetime import datetime

import streamlit as st

from frontend.utils.api_client import get_api_client

def traiter_message(prompt: str):
    """
    Traite un message utilisateur :
    1. Ajoute le message dans l'historique
    2. Appelle l'API
    3. Ajoute la réponse du bot
    """
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Appeler l'API
    try:
        response = st.session_state.api_client.chat(
            prompt,
            session_id=st.session_state.session_id,
        )
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["reponse"],
            "details": response,
        })
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"❌ Erreur : {e}",
        })

# ============ CONFIGURATION ============

st.set_page_config(
    page_title="Pharma Chatbot",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============ ÉTAT DE SESSION ============

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_client" not in st.session_state:
    st.session_state.api_client = get_api_client()


# ============ SIDEBAR ============

with st.sidebar:
    st.title("💊 Pharma Chatbot")
    st.caption("Assistant pharmaceutique intelligent")

    st.divider()

    # État de l'API
    api_ok = st.session_state.api_client.health()
    if api_ok:
        st.success("✅ API connectée")
    else:
        st.error("❌ API déconnectée")
        st.caption("Lancez : `uvicorn src.main:app --reload`")

    st.divider()

    st.markdown(f"**Session** : `{st.session_state.session_id}`")

    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.rerun()

    st.divider()

    st.markdown("### 📋 Exemples")
    exemples = [
        "J'ai mal à la tête et de la fièvre",
        "Je tousse et j'ai le nez qui coule",
        "J'ai mal au ventre et la diarrhée",
        "J'ai mal à la poitrine",
    ]
    for ex in exemples:
        if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
            traiter_message(ex)
            st.rerun()

# ============ PAGE PRINCIPALE ============

st.title("💬 Assistant Pharmacie")
st.caption(
    "Décrivez vos symptômes, je vous recommanderai des médicaments adaptés. "
    "⚠️ Ces recommandations ne remplacent pas un avis médical."
)

# Historique des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "💊"):
        st.markdown(msg["content"])

        # Détails pour les réponses du bot
        if msg["role"] == "assistant" and "details" in msg:
            details = msg["details"]
            if details.get("est_urgent"):
                st.error("⚠️ **URGENCE MÉDICALE DÉTECTÉE**")

            if details.get("symptomes_detectes"):
                with st.expander("🔍 Détails de l'analyse"):
                    st.markdown(
                        f"**Symptômes détectés** : "
                        f"{', '.join(details['symptomes_detectes'])}"
                    )

                    if details.get("maladies_probables"):
                        st.markdown("**Maladies probables** :")
                        for m in details["maladies_probables"]:
                            st.markdown(
                                f"- {m['nom']} "
                                f"({m['nb_symptomes']}/{m['total_symptomes']} symptômes)"
                            )

                    if details.get("medicaments_recommandes"):
                        st.markdown("**Médicaments recommandés** :")
                        for med in details["medicaments_recommandes"]:
                            ord_ = " 🔒 ordonnance" if med["ordonnance_requise"] else ""
                            dispo = ""
                            if med.get("stock_disponible") is not None:
                                if med["stock_disponible"] > 0:
                                    dispo = f" — en stock : {med['stock_disponible']}"
                                else:
                                    dispo = " — ⚠️ rupture"
                            st.markdown(
                                f"- **{med['nom']}**{ord_}{dispo}  \n"
                                f"  *{med.get('description', '')}*"
                            )

            if details.get("avertissement"):
                st.warning(details["avertissement"])


# ============ SAISIE ============

# Onglets : texte OU vocal
tab_texte, tab_vocal = st.tabs(["⌨️ Écrire", "🎤 Parler"])

with tab_texte:
    prompt = st.chat_input("Décrivez vos symptômes...", key="chat_text")
    if prompt:
        traiter_message(prompt)
        st.rerun()

with tab_vocal:
    st.caption("Enregistrez votre voix puis cliquez sur 'Traiter l'audio'.")
    audio_value = st.audio_input("Enregistrer votre voix", key="audio_record")

    if audio_value is not None:
        st.audio(audio_value)
        if st.button("🎯 Traiter l'audio", type="primary", use_container_width=True):
            with st.spinner("Transcription et analyse en cours..."):
                try:
                    response = st.session_state.api_client.chat_audio(
                        audio_bytes=audio_value.getvalue(),
                        filename="audio.wav",
                    )

                    # Ajouter la transcription comme message utilisateur
                    transcription = response.get("transcription", {}).get("texte", "")
                    st.session_state.messages.append({
                        "role": "user",
                        "content": f"🎤 {transcription}" if transcription else "🎤 [audio]",
                    })

                    # Ajouter la réponse du bot
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["reponse"],
                        "details": response,
                    })

                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")
