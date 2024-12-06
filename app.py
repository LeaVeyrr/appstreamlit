import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu


def charger_donnees_comptes(fichier_csv):
    data = pd.read_csv(fichier_csv)

    comptes = {
        "usernames": {
            row["username"]: {
                "username": row["username"],
                "name": row["name"],
                "password": row["password"],
                "email": row["email"],
                "failed_login_attemps": row["failed_login_attemps"],
                "logged_in": row["logged_in"],
                "role": row["role"],
            }
            for _, row in data.iterrows()
        }
    }
    return comptes


fichier_csv = (
    "https://raw.githubusercontent.com/LeaVeyrr/streamlit3/refs/heads/main/users.csv"
)
lesDonneesDesComptes = charger_donnees_comptes(fichier_csv)

# Authenticator
authenticator = Authenticate(
    lesDonneesDesComptes,
    "app_cookie",
    "cookie_key",
    30,  # Expiration en jours
)

authenticator.login()

if st.session_state.get("authentication_status"):

    username = st.session_state["username"]

    with st.sidebar:

        st.write(f"Bonjour, {username}!")
        selection = option_menu(menu_title=None, options=["Accueil", "Photos"])

        authenticator.logout("Se déconnecter")

    if selection == "Accueil":
        st.title("Bienvenue au paradis des chats ✨")
        st.image(
            "https://uploads.dailydot.com/2018/10/olli-the-polite-cat.jpg?q=65&auto=format&w=1200&ar=2:1&fit=crop"
        )
    elif selection == "Photos":
        st.title("Album photo des chats ✨")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(
                "https://preview.redd.it/origin-of-this-cat-template-meme-v0-4783qbjaqfgb1.jpg?width=640&crop=smart&auto=webp&s=dd15e8ce354aa4a69423bbdc7a1e8d7d3664e7c4"
            )
        with col2:
            st.image("https://imgflip.com/s/meme/Smiling-Cat.jpg")
        with col3:
            st.image(
                "https://ew.com/thmb/0_PyYU_Nym5fWeedIxPb6WHiuRQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/b31-92532f841b9349638d226a6c62aa9e85.jpg"
            )
else:
    st.error("Authentification requise pour accéder au contenu.")
