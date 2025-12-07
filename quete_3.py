import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import os.path

# --- ÉTAPE 1 : CRÉATION DU FICHIER CSV (Si absent) ---
# Ce bloc crée le fichier 'users.csv' automatiquement s'il n'existe pas
if not os.path.exists('users.csv'):
    # On hache les mots de passe pour la sécurité (requis par le module)
    hashed_passwords = stauth.Hasher(['utilisateurMDP', 'rootMDP']).generate()
    
    data = {
        'username': ['utilisateur', 'root'],  # Identifiant de connexion
        'name': ['Utilisateur Test', 'Super Admin'],     # Nom affiché
        'password': hashed_passwords,
        'email': ['user@gmail.com', 'admin@gmail.com'],
        'failed_login_attemps': [0, 0],
        'logged_in': [False, False],
        'role': ['utilisateur', 'administrateur']
    }
    df_creation = pd.DataFrame(data)
    df_creation.to_csv('users.csv', index=False)


# --- ÉTAPE 2 : LECTURE ET CONVERSION DES DONNÉES ---
# On lit le CSV
df_users = pd.read_csv('users.csv')

# On convertit le DataFrame en dictionnaire pour le module d'authentification
credentials = {'usernames': {}}
for index, row in df_users.iterrows():
    credentials['usernames'][row['username']] = {
        'name': row['name'],
        'password': row['password'],
        'email': row['email'],
        'role': row['role']
    }

# --- ÉTAPE 3 : CONFIGURATION DE L'AUTHENTIFICATION ---
authenticator = stauth.Authenticate(
    credentials,
    "cookie_mon_site",
    "cle_secrete_aleatoire",
    30,
)

# Affiche le widget de connexion
authenticator.login('main')

# On récupère les états directement depuis la mémoire de session
authentication_status = st.session_state['authentication_status']
name = st.session_state['name']
username = st.session_state['username']

# --- ÉTAPE 4 : GESTION DE L'AFFICHAGE ---
if authentication_status is False:
    st.error('Nom d\'utilisateur ou mot de passe incorrect')
elif authentication_status is None:
    st.warning('Veuillez entrer vos identifiants')

elif authentication_status is True:
    # >>> TOUT LE CONTENU DU SITE EST ICI <<<
    
    # Barre latérale (Sidebar)
    with st.sidebar:
        st.write(f"👋 Bienvenue **{st.session_state['name']}**")
        
        selected = option_menu(
            "Menu Principal",
            ["Accueil", "Album Photo"],
            icons=["house", "camera"],
            default_index=0,
        )
        
        # Le bouton de déconnexion doit être dans la sidebar
        authenticator.logout('Déconnexion', 'sidebar')

    # Contenu Principal
    if selected == "Accueil":
        st.title("🏠 Page d'Accueil")
        st.write("Bienvenue sur le contenu réservé aux utilisateurs connectés.")
        st.image("https://img.20mn.fr/di_oluWvTli0AKiedxHyPik/1444x920_mulita-armadillo-of-six-bands-on-to-white-background")   
        # Affichage du rôle pour vérification
        user_role = credentials['usernames'][username]['role']
        st.info(f"Vous êtes connecté en tant que : {user_role}")

    elif selected == "Album Photo":
        st.title("📸 Les photos de la bestiole")
                
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image("https://preview.redd.it/is-this-armadillo-old-enough-to-be-on-its-own-v0-hymqn32a3g0b1.png?width=1080&crop=smart&auto=webp&s=99c761e4cd3ab6d44cf76ed4b3ccd7874370bbc9", caption="tatou 1")
        with col2:
            st.image("https://static.nationalgeographic.fr/files/styles/image_3200/public/minden_90731712.jpg?w=1600/301/301", caption="tatou 2")
        with col3:

            st.image("https://leblogusadedom.com/wp/wp-content/uploads/2016/11/IMG_8960-2-Copier-Copier.jpg", caption="tatou 3")
