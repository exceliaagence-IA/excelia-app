import streamlit as st
import pandas as pd
import time

# --- CONFIGURATION DE LA PAGE (Doit être la première ligne) ---
st.set_page_config(
    page_title="Excelia Agence - Portail IA",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS PERSONNALISÉ (Pour imiter le design Violet/Dark du React) ---
st.markdown("""
    <style>
    /* Couleurs Principales (Violet Excelia) */
    :root {
        --primary-color: #7c3aed;
        --background-color: #ffffff;
        --secondary-background-color: #f8fafc;
        --text-color: #0f172a;
    }
    
    /* Boutons personnalisés en Violet */
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
    
    /* Style des titres */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #7c3aed, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Cards / Métriques */
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Upload Zone plus jolie */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1;
        border-radius: 15px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ETAT DE LA SESSION (Login fictif) ---
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

# --- SIDEBAR (Menu Latéral) ---
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
    # Infos client
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
        st.markdown("Déposez vos plans. **L'IA s'occupe du reste.**")
    with col_h2:
        st.success("Agent v2.1 • Online")

    st.write("") # Spacer

    # Zone d'Upload
    uploaded_file = st.file_uploader("Glissez votre plan PDF ici", type=['pdf', 'png', 'dwg'])

    if uploaded_file:
        st.info("Fichier reçu. Prêt pour l'analyse.")
        
        if st.button("Lancer l'analyse IA (Simulation N8N)", use_container_width=True):
            with st.spinner("Traitement N8N en cours... Identification des pièces..."):
                time.sleep(2.5) # Simulation attente
            
            st.balloons()
            st.success("Analyse terminée avec succès !")
            
            # Résultats
            col_res1, col_res2 = st.columns([2, 1])
            
            with col_res1:
                st.subheader("Données extraites")
                data = {
                    "Lot": ["Peinture", "Sol", "Elec"],
                    "Désignation": ["Murs et Plafonds (RDC)", "Parquet Flottant Chêne", "Remise aux normes TGBT"],
                    "Surface": ["120 m²", "85 m²", "1 u"],
                    "Prix Est.": ["2 400 €", "4 500 €", "1 500 €"]
                }
                st.table(pd.DataFrame(data))
                st.markdown("**Total HT: 8 400 €**")
                
            with col_res2:
                st.subheader("Téléchargements")
                st.info("Vos documents sont prêts.")
                st.download_button("📄 Devis Client.pdf", data="PDF", file_name="devis.pdf", use_container_width=True)
                st.download_button("📊 Métré Détail.csv", data="CSV", file_name="metre.csv", use_container_width=True)

# --- PAGE: AGENT APPELS D'OFFRE ---
elif choix_agent == "🔍 Veille Appels d'Offre":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Veille Stratégique")
        st.markdown("Les meilleures opportunités filtrées par IA.")
    with col_h2:
        if st.button("🔄 Synchro (08:00)"):
            st.toast("Actualisation en cours...")

    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Opportunités du jour", "12", "+2 New")
    kpi2.metric("Budget Moyen", "840k €", "Stable")
    kpi3.metric("Cibles Actives", "Île-de-France", "Gros Œuvre")

    st.markdown("---")

    # Tableau des offres
    st.subheader("Marchés détectés")
    
    df_offres = pd.DataFrame([
        {"Titre": "Rénovation École Victor Hugo", "Lieu": "Paris 12e", "Budget": "450k €", "Date": "01 Juil", "Urgent": False},
        {"Titre": "Construction Immeuble R+4", "Lieu": "Lyon (69)", "Budget": "2.1M €", "Date": "15 Août", "Urgent": False},
        {"Titre": "Réfection Toiture Mairie", "Lieu": "Bordeaux (33)", "Budget": "80k €", "Date": "Demain", "Urgent": True},
        {"Titre": "Extension Gymnase", "Lieu": "Nantes (44)", "Budget": "320k €", "Date": "20 Juil", "Urgent": False},
    ])

    # Affichage intelligent avec surbrillance des urgences
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
