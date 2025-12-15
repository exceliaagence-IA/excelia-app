import streamlit as st
import pandas as pd
import time
import requests

# --- 1. CONFIGURATION DE LA PAGE (Doit être la 1ère ligne) ---
st.set_page_config(
    page_title="Excelia Agence - Portail IA",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LE "MAQUILLAGE" (CSS AVANCÉ) ---
# C'est ici que la magie opère pour transformer le look standard
st.markdown("""
    <style>
    /* Import de la police Inter (plus moderne) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* COULEURS EXCELIA (Violet) */
    :root {
        --primary: #7c3aed;
        --primary-hover: #6d28d9;
        --bg-light: #f8fafc;
    }

    /* Enlever le vide en haut de page */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Style des BOUTONS (Dégradé Violet) */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(124, 58, 237, 0.3);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.4);
    }

    /* Style des CARTES (Metrics) */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: scale(1.02);
        border-color: #7c3aed;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #0f172a;
        font-weight: 700;
    }

    /* Zone d'UPLOAD plus jolie */
    div[data-testid="stFileUploader"] section {
        background-color: #f8fafc;
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 30px;
    }
    div[data-testid="stFileUploader"] section:hover {
        border-color: #7c3aed;
        background-color: #f3f0ff;
    }

    /* Inputs (Champs texte) */
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 10px;
    }
    .stTextInput input:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
    }
    
    /* Expander (Cadres pliables) */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Cacher le menu hamburger Streamlit et le footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURATION N8N (LIENS) ---
WEBHOOK_URL_DEVIS = "https://n8n.srv1159353.hstgr.cloud/webhook/c8f039e9-89af-4d1a-b378-8e77a0a348b0"
WEBHOOK_URL_VEILLE = ""

# --- 4. GESTION DU LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.write("")
        st.write("")
        st.write("")
        # Carte de login
        with st.container():
            st.markdown("""
            <div style='background-color: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); text-align: center; border: 1px solid #e2e8f0;'>
                <h1 style='color: #7c3aed; margin-bottom: 0;'>Excelia.</h1>
                <p style='color: #64748b; margin-top: 10px;'>Portail Intelligence Artificielle BTP</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            with st.form("login_form"):
                st.text_input("Identifiant", value="Entreprise Demo")
                st.text_input("Mot de passe", type="password", value="********")
                st.write("")
                submit = st.form_submit_button("Se connecter au portail")
                
                if submit:
                    st.session_state['logged_in'] = True
                    st.rerun()
    st.stop()

# --- 5. SIDEBAR (MENU) ---
with st.sidebar:
    st.title("Excelia.")
    st.caption("v1.0 • BÊTA PRIVÉE")
    st.write("")
    
    choix_agent = st.radio(
        "AGENTS DISPONIBLES",
        ["📝 Chiffrage & Devis", "🔍 Veille Stratégique"],
        label_visibility="collapsed"
    )
    
    st.write("")
    st.write("")
    with st.container():
        st.markdown("""
        <div style='background-color: #f1f5f9; padding: 15px; border-radius: 10px;'>
            <small style='color: #64748b; font-weight: bold;'>COMPTE ACTIF</small><br>
            <strong>Client Demo SAS</strong><br>
            <span style='color: #10b981; font-size: 12px;'>● En ligne</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    if st.button("Se déconnecter"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- 6. AGENT CHIFFRAGE ---
if choix_agent == "📝 Chiffrage & Devis":
    # En-tête avec badge
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.title("Chiffrage Automatique")
        st.markdown("Transformez vos plans en devis détaillés en quelques secondes.")
    with col_t2:
        st.markdown("""
        <div style='text-align: right; padding-top: 20px;'>
            <span style='background-color: #dbeafe; color: #1e40af; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;'>IA GEN-2 READY</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Formulaire dans un cadre propre
    with st.expander("👤 Informations du Client (Requis pour le devis)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            prenom = st.text_input("Prénom")
            nom = st.text_input("Nom")
            email = st.text_input("Email pro *")
        with c2:
            telephone = st.text_input("Téléphone mobile *")
            adresse = st.text_input("Adresse du chantier")
            ville = st.text_input("Ville & CP")
            pays = st.text_input("Pays", value="France")

    st.write("")
    st.markdown("### 📂 Déposez votre plan")
    uploaded_file = st.file_uploader("", type=['pdf', 'png', 'jpg'], help="L'IA analyse mieux les PDF vectoriels originaux.")

    if uploaded_file:
        st.success("✅ Fichier prêt à l'envoi !")
        
        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            if st.button("🚀 Lancer l'analyse IA"):
                if not WEBHOOK_URL_DEVIS:
                     st.error("⚠️ URL Webhook non configurée.")
                elif not email:
                     st.warning("⚠️ L'email est obligatoire.")
                else:
                    with st.spinner("🤖 L'IA Excelia analyse les pièces et matériaux..."):
                        try:
                            # Préparation payload
                            files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                            form_data = {
                                'first_name': prenom, 'last_name': nom,
                                'email': email, 'phone': telephone,
                                'address': adresse, 'city': ville, 'country': pays
                            }
                            # Envoi
                            r = requests.post(WEBHOOK_URL_DEVIS, files=files, data=form_data)
                            
                            if r.status_code == 200:
                                st.balloons()
                                res = r.json()
                                st.markdown("### 📊 Résultat de l'analyse")
                                
                                # Si PDF généré
                                if 'pdf_url' in res:
                                    st.markdown(f"""
                                    <a href="{res['pdf_url']}" target="_blank" style="text-decoration: none;">
                                        <div style="background-color: #ecfdf5; border: 1px solid #10b981; color: #065f46; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold;">
                                            📥 Télécharger le Devis Officiel (PDF)
                                        </div>
                                    </a>
                                    """, unsafe_allow_html=True)
                                
                                # Si données tabulaires
                                if 'data' in res:
                                    st.dataframe(pd.DataFrame(res['data']), use_container_width=True)
                            else:
                                st.error(f"Erreur IA ({r.status_code}) : {r.text}")
                        except Exception as e:
                            st.error(f"Erreur de connexion : {e}")

# --- 7. AGENT VEILLE ---
elif choix_agent == "🔍 Veille Stratégique":
    st.title("Veille Appels d'Offre")
    st.markdown("Opportunités détectées ce matin selon vos critères `Gros Œuvre` en `Île-de-France`.")
    st.write("")
    
    # 3 KPIs style "Cards"
    k1, k2, k3 = st.columns(3)
    k1.metric("Offres Détectées", "14", "+3 ce matin")
    k2.metric("Budget Moyen", "840 k€", "Stable")
    k3.metric("Taux de pertinence", "94%", "High")
    
    st.write("")
    st.markdown("### 📋 Dernières opportunités")
    
    # Tableau propre
    df = pd.DataFrame([
        {"Marché": "Rénovation Groupe Scolaire", "Lieu": "Paris 15", "Budget": "450k €", "Urgence": "🔥 Haute"},
        {"Marché": "Construction 24 Logements", "Lieu": "Massy (91)", "Budget": "2.1M €", "Urgence": "Moyenne"},
        {"Marché": "Réfection Toiture Mairie", "Lieu": "Versailles", "Budget": "85k €", "Urgence": "Faible"},
    ])
    
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Urgence": st.column_config.TextColumn(
                "Priorité",
                help="Calculé par l'IA selon vos délais"
            )
        }
    )
    
    st.write("")
    if st.button("🔄 Forcer une actualisation manuelle"):
        st.toast("Lancement du scraper N8N...")
