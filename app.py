import streamlit as st
import pandas as pd
import time
import requests
import random
from datetime import datetime, timedelta

# --- CONFIGURATION N8N ---
WEBHOOK_URL_DEVIS = "https://n8n.srv1159353.hstgr.cloud/webhook-test/c8f039e9-89af-4d1a-b378-8e77a0a348b0"
WEBHOOK_URL_VEILLE = "" 

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Excelia | Portail Intelligence BTP",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME & CSS PREMIUM ---
def local_css():
    st.markdown("""
    <style>
        /* Import Font Google: Plus Jakarta Sans (SaaS Standard) */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #1e293b;
        }

        /* Background global */
        .stApp {
            background-color: #f1f5f9; /* Slate 100 */
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }

        /* Headers */
        h1, h2, h3 {
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.025em;
        }
        
        /* Custom Cards */
        .premium-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        }

        /* Boutons Gradient Premium */
        div.stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 12px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            transition: all 0.3s ease;
            width: 100%;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(79, 70, 229, 0.4);
        }

        /* Input Styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #cbd5e1;
            padding: 10px; 
            background-color: #f8fafc;
        }
        .stTextInput > div > div > input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
        }

        /* Métriques */
        div[data-testid="stMetric"] {
            background-color: white;
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.85rem;
            color: #64748b;
        }
        div[data-testid="stMetricValue"] {
            font-weight: 700;
            color: #0f172a;
        }

        /* File Uploader */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #94a3b8;
            border-radius: 16px;
            padding: 30px;
            background-color: #f8fafc;
            transition: border 0.3s;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #6366f1;
            background-color: #eff6ff;
        }

        /* Login Box centering */
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- ETAT DE SESSION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- LOGIQUE DE LOGIN ---
def login_screen():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.write("")
        st.write("")
        st.write("")
        
        # Container style carte
        with st.container():
            st.markdown("""
            <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); border: 1px solid #e2e8f0; text-align: center;">
                <h1 style="background: -webkit-linear-gradient(45deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">Excelia.</h1>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">Intelligence Artificielle pour le BTP</p>
                <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 20px 0;">
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.text_input("Identifiant Espace Pro", value="Entreprise BTP Demo")
                st.text_input("Mot de passe", type="password", value="********")
                st.write("")
                submit = st.form_submit_button("Accéder au Portail", use_container_width=True)
                
                if submit:
                    with st.spinner("Authentification sécurisée..."):
                        time.sleep(1) # Fake loading
                        st.session_state['logged_in'] = True
                        st.rerun()

# --- INTERFACE PRINCIPALE ---
def main_app():
    # SIDEBAR
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <h2 style="margin:0; font-size: 1.5rem; color: #4f46e5;">Excelia<span style="color:#cbd5e1;">.ai</span></h2>
            <span style="font-size: 0.75rem; background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 12px; font-weight: 600;">ENTERPRISE</span>
        </div>
        """, unsafe_allow_html=True)
        
        choix_agent = st.radio(
            "MENU PRINCIPAL",
            ["📊 Dashboard & Veille", "⚡ Chiffrage Intelligent"],
            index=1,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # User Profile Widget
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px; background: #f8fafc; border-radius: 12px;">
            <div style="width: 35px; height: 35px; background: #4f46e5; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">CD</div>
            <div>
                <div style="font-size: 0.9rem; font-weight: 600;">Client Demo</div>
                <div style="font-size: 0.75rem; color: #64748b;">Admin</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Déconnexion", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # CONTENU
    if choix_agent == "⚡ Chiffrage Intelligent":
        render_devis_page()
    elif choix_agent == "📊 Dashboard & Veille":
        render_veille_page()

# --- PAGE 1: DEVIS ---
def render_devis_page():
    # Header Section
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Générateur de Devis IA")
        st.markdown("<p style='color: #64748b; margin-top: -10px;'>Analysez vos plans PDF et générez des chiffrages précis en quelques secondes.</p>", unsafe_allow_html=True)
    with col_h2:
        st.markdown("""
        <div style="text-align: right;">
            <span style="background: #dcfce7; color: #166534; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">● Système Opérationnel</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")

    # Main Layout
    col_left, col_right = st.columns([1.8, 1])

    with col_left:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("1. Configuration du Projet")
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption("INFORMATION CLIENT")
            prenom = st.text_input("Prénom", placeholder="Jean")
            nom = st.text_input("Nom", placeholder="Dupont")
            email = st.text_input("Email Professionnel *", placeholder="client@email.com")
            telephone = st.text_input("Mobile *", placeholder="06 00 00 00 00")
        
        with c2:
            st.caption("LOCALISATION CHANTIER")
            adresse = st.text_input("Adresse", placeholder="10 rue de la Paix")
            ville = st.text_input("Ville", placeholder="Paris")
            col_cp, col_pays = st.columns([1, 1])
            code_postal = col_cp.text_input("Code Postal", placeholder="75000")
            pays = col_pays.text_input("Pays", value="France", disabled=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("2. Documents Techniques")
        st.markdown("L'IA analyse les plans architecturaux (PDF) ou les croquis (Images/DWG).")
        uploaded_file = st.file_uploader("Déposez vos plans ici", type=['pdf', 'png', 'jpg', 'dwg'], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="premium-card" style="background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);">', unsafe_allow_html=True)
        st.subheader("🚀 Lancer l'analyse")
        st.markdown("Vérifiez que toutes les informations obligatoires (*) sont remplies avant de soumettre.")
        
        warning_placeholder = st.empty()
        
        if st.button("Générer le Devis maintenant", use_container_width=True):
            if not email or not telephone or not uploaded_file:
                warning_placeholder.warning("⚠️ Veuillez remplir l'email, le téléphone et ajouter un fichier.")
            else:
                handle_submission(prenom, nom, email, telephone, adresse, ville, code_postal, pays, uploaded_file)
        
        st.markdown("---")
        st.caption("🔒 Vos données sont traitées de manière sécurisée et ne sont pas partagées avec des tiers.")
        st.markdown('</div>', unsafe_allow_html=True)

def handle_submission(prenom, nom, email, telephone, adresse, ville, code_postal, pays, uploaded_file):
    # Logique de soumission (similaire à ton code original, mais avec UX toast)
    if not WEBHOOK_URL_DEVIS:
        with st.spinner("🤖 L'IA analyse les surfaces et les matériaux..."):
            time.sleep(3)
        st.toast("✅ Analyse terminée avec succès!", icon="🎉")
        st.balloons()
        
        # Affichage simulation
        with st.expander("📄 Aperçu du Devis (Mode Simulation)", expanded=True):
            data = {
                "Désignation": ["Préparation des supports", "Peinture Velours (Salon)", "Pose Parquet Chêne", "Plinthes"],
                "Qté": ["120 m²", "120 m²", "45 m²", "30 ml"],
                "Prix Unitaire": ["5.00 €", "18.00 €", "55.00 €", "12.00 €"],
                "Total HT": ["600 €", "2 160 €", "2 475 €", "360 €"]
            }
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            st.markdown("### Total Estimé: **5 595 € HT**")
            st.info("💡 Ceci est une démo. Connectez votre Webhook N8N pour le mode réel.")
    else:
        with st.spinner("Envoi des données au cerveau N8N..."):
            try:
                files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                form_data = {
                    'prenom': prenom, 'nom': nom, 'email': email, 
                    'telephone': telephone, 'adresse': adresse, 
                    'ville': ville, 'code_postal': code_postal, 'pays': pays
                }
                response = requests.post(WEBHOOK_URL_DEVIS, files=files, data=form_data)
                
                if response.status_code == 200:
                    st.toast("Devis généré et envoyé par email !", icon="📩")
                    st.balloons()
                    
                    try:
                        result = response.json()
                        if 'data' in result:
                            st.dataframe(pd.DataFrame(result['data']), use_container_width=True)
                        if 'pdf_url' in result:
                            st.success(f"Document prêt : [Télécharger le PDF]({result['pdf_url']})")
                    except:
                        st.success("Traitement effectué.")
                else:
                    st.error(f"Erreur serveur : {response.status_code}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")

# --- PAGE 2: VEILLE & DASHBOARD ---
def render_veille_page():
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Tableau de Bord Stratégique")
        st.markdown("<p style='color: #64748b; margin-top: -10px;'>Vue d'ensemble des opportunités du marché en temps réel.</p>", unsafe_allow_html=True)
    with col_h2:
        if st.button("🔄 Actualiser"):
            st.toast("Synchronisation des appels d'offres...", icon="⏳")
            time.sleep(1)
            st.toast("Données à jour !", icon="✅")

    # Metrics Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Opportunités Détectées", "42", "+12% this week")
    kpi2.metric("Montant Moyen", "450 k€", "-2%")
    kpi3.metric("Taux de Conversion", "18%", "+5%")
    kpi4.metric("Dossiers en cours", "7", "Actif")

    st.write("")

    # Charts Section
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("📈 Tendances des Marchés")
        # Fake Data for Chart
        chart_data = pd.DataFrame({
            "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
            "Offres": [12, 19, 15, 25, 32, 28],
            "Remportés": [2, 4, 3, 6, 8, 7]
        })
        st.bar_chart(chart_data.set_index("Mois"), color=["#e2e8f0", "#4f46e5"], height=250)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("🎯 Répartition")
        st.write("Par type de lot")
        # Simple progress bars mimicking a distribution chart
        st.caption("Gros Œuvre")
        st.progress(0.7)
        st.caption("CVC / Plomberie")
        st.progress(0.45)
        st.caption("Électricité")
        st.progress(0.3)
        st.markdown('</div>', unsafe_allow_html=True)

    # Data Table Section
    st.subheader("Derniers Appels d'Offres")
    
    # Enhanced DataFrame
    df_offres = pd.DataFrame([
        {"Statut": "🔥 Urgent", "Projet": "Rénovation École V. Hugo", "Localisation": "Paris (75)", "Budget": 450000, "Date Limite": "2024-07-01"},
        {"Statut": "🆕 Nouveau", "Projet": "Construction Immeuble R+4", "Localisation": "Lyon (69)", "Budget": 2100000, "Date Limite": "2024-08-15"},
        {"Statut": "⚠️ En Cours", "Projet": "Extension Gymnase Municipal", "Localisation": "Nantes (44)", "Budget": 320000, "Date Limite": "2024-07-20"},
        {"Statut": "🆕 Nouveau", "Projet": "Réfection Toiture Mairie", "Localisation": "Bordeaux (33)", "Budget": 85000, "Date Limite": "2024-06-30"},
    ])

    st.dataframe(
        df_offres,
        column_config={
            "Budget": st.column_config.NumberColumn("Budget (€)", format="%.0f €"),
            "Date Limite": st.column_config.DateColumn("Date Limite", format="DD/MM/YYYY"),
            "Statut": st.column_config.TextColumn("Priorité"),
        },
        use_container_width=True,
        hide_index=True
    )

# --- APP ROUTER ---
if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_screen()
    else:
        main_app()
