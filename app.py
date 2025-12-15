import streamlit as st
import pandas as pd
import time
import requests # Nécessaire pour parler à N8N

# --- CONFIGURATION N8N (C'est ici que tu colles tes liens !) ---
# Mets tes liens N8N entre les guillemets.
WEBHOOK_URL_DEVIS = "https://n8n.srv1159353.hstgr.cloud/webhook-test/c8f039e9-89af-4d1a-b378-8e77a0a348b0"
WEBHOOK_URL_VEILLE = "" # Ex: "https://ton-n8n.com/webhook/..."

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Excelia Agence - Portail IA",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    :root {
        --primary-color: #7c3aed;
        --background-color: #ffffff;
        --secondary-background-color: #f8fafc;
        --text-color: #0f172a;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.39);
    }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
    h1 {
        background: -webkit-linear-gradient(45deg, #7c3aed, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1;
        border-radius: 15px;
        padding: 20px;
    }
    /* Style pour les inputs */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ETAT DE LA SESSION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- ECRAN DE LOGIN ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h2 style='text-align: center;'>Excelia Agence</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Portail IA & BTP</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("Identifiant", value="Entreprise BTP Demo")
            st.text_input("Mot de passe", type="password", value="********")
            submit = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit:
                st.session_state['logged_in'] = True
                st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Excelia.")
    st.markdown("---")
    st.caption("AGENTS INTELLIGENTS")
    
    choix_agent = st.radio(
        "Navigation",
        ["📝 Chiffrage & Devis", "🔍 Veille Appels d'Offre"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    col_u1, col_u2 = st.columns([1, 3])
    with col_u1:
        st.write("👤")
    with col_u2:
        st.write("**Client Demo**")
        st.caption("Premium Account")
        
    if st.button("Déconnexion", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()

# --- PAGE: AGENT DEVIS ---
if choix_agent == "📝 Chiffrage & Devis":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Chiffrage & Devis")
        st.markdown("Remplissez les infos et déposez vos plans. **L'IA s'occupe du reste.**")
    with col_h2:
        st.success("Agent v2.1 • Online")

    st.write("")

    # --- NOUVEAU FORMULAIRE CLIENT (Style GHL) ---
    with st.expander("📋 Informations du Chantier & Client", expanded=True):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.subheader("Contact")
            prenom = st.text_input("Prénom")
            nom = st.text_input("Nom")
            email = st.text_input("Email *")
            telephone = st.text_input("Téléphone *")
            
        with col_f2:
            st.subheader("Adresse du projet")
            adresse = st.text_input("Adresse postale")
            ville = st.text_input("Ville")
            code_postal = st.text_input("Code Postal")
            pays = st.text_input("Pays", value="France")

    st.write("")

    uploaded_file = st.file_uploader("Glissez votre plan PDF ici (Plan Maison)", type=['pdf', 'png', 'dwg'])

    if uploaded_file:
        st.info("Fichier reçu. Prêt pour l'analyse.")
        
        # Petit check pour encourager à remplir les champs
        if not email or not telephone:
            st.warning("⚠️ Pensez à remplir l'Email et le Téléphone pour que le devis soit complet.")

        if st.button("Lancer l'analyse IA", use_container_width=True):
            
            # 1. SI AUCUN WEBHOOK N'EST CONFIGURÉ (Mode Simulation)
            if not WEBHOOK_URL_DEVIS:
                with st.spinner("Mode Démo : Simulation de l'analyse..."):
                    time.sleep(2.5)
                st.balloons()
                st.success(f"Devis généré pour {prenom} {nom} !")
                
                # Fausses données pour la démo
                data = {
                    "Lot": ["Peinture", "Sol", "Elec"],
                    "Désignation": ["Murs et Plafonds (RDC)", "Parquet Flottant Chêne", "Remise aux normes TGBT"],
                    "Surface": ["120 m²", "85 m²", "1 u"],
                    "Prix Est.": ["2 400 €", "4 500 €", "1 500 €"]
                }
                st.table(pd.DataFrame(data))
                st.markdown("**Total HT: 8 400 €**")
                st.warning("⚠️ Ceci est une simulation. Ajoutez votre lien Webhook N8N dans le code.")

            # 2. SI LE WEBHOOK EST CONFIGURÉ (Mode Réel)
            else:
                with st.spinner("Envoi du dossier complet à l'IA Excelia (N8N)..."):
                    try:
                        # Préparation du fichier
                        files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        
                        # Préparation des données du formulaire
                        form_data = {
                            'prenom': prenom,
                            'nom': nom,
                            'email': email,
                            'telephone': telephone,
                            'adresse': adresse,
                            'ville': ville,
                            'code_postal': code_postal,
                            'pays': pays
                        }
                        
                        # Envoi à N8N (Fichier + Données)
                        response = requests.post(WEBHOOK_URL_DEVIS, files=files, data=form_data)
                        
                        if response.status_code == 200:
                            st.balloons()
                            st.success("Analyse réelle terminée !")
                            
                            # On s'attend à ce que N8N renvoie du JSON
                            result = response.json()
                            
                            if 'data' in result:
                                st.table(pd.DataFrame(result['data']))
                            
                            if 'pdf_url' in result:
                                st.markdown(f"[📥 Télécharger le Devis PDF]({result['pdf_url']})")
                            
                        else:
                            st.error(f"Erreur IA : {response.status_code}")
                            
                    except Exception as e:
                        st.error(f"Erreur de connexion : {e}")


# --- PAGE: AGENT APPELS D'OFFRE ---
elif choix_agent == "🔍 Veille Appels d'Offre":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Veille Stratégique")
        st.markdown("Les meilleures opportunités filtrées par IA.")
    with col_h2:
        if st.button("🔄 Synchro (08:00)"):
            st.toast("Actualisation en cours...")
            # Ici, tu pourras ajouter requests.get(WEBHOOK_URL_VEILLE) plus tard

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Opportunités du jour", "12", "+2 New")
    kpi2.metric("Budget Moyen", "840k €", "Stable")
    kpi3.metric("Cibles Actives", "Île-de-France", "Gros Œuvre")

    st.markdown("---")

    st.subheader("Marchés détectés")
    
    # Données simulées par défaut
    df_offres = pd.DataFrame([
        {"Titre": "Rénovation École Victor Hugo", "Lieu": "Paris 12e", "Budget": "450k €", "Date": "01 Juil", "Urgent": False},
        {"Titre": "Construction Immeuble R+4", "Lieu": "Lyon (69)", "Budget": "2.1M €", "Date": "15 Août", "Urgent": False},
        {"Titre": "Réfection Toiture Mairie", "Lieu": "Bordeaux (33)", "Budget": "80k €", "Date": "Demain", "Urgent": True},
        {"Titre": "Extension Gymnase", "Lieu": "Nantes (44)", "Budget": "320k €", "Date": "20 Juil", "Urgent": False},
    ])

    st.dataframe(
        df_offres,
        column_config={
            "Urgent": st.column_config.CheckboxColumn(
                "Urgent",
                help="Marchés à traiter en priorité",
                default=False,
            ),
        },
        use_container_width=True,
        hide_index=True
    )
