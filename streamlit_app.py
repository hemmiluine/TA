import streamlit as st
import matplotlib.pyplot as plt

# ==========================================
# INTERFACE DE L'APPLICATION
# ==========================================
st.title("⚗️ Simulateur de Bilan de Matière")
st.write("Nous étudions une réaction totale de la forme :")
st.latex(r"a A + b B \rightarrow c C + d D")

st.divider()

# --- Saisie des données dans deux colonnes ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Coefficients stœchiométriques")
    a = st.number_input("Coefficient a (pour A)", min_value=1, value=1, step=1)
    b = st.number_input("Coefficient b (pour B)", min_value=1, value=1, step=1)
    c = st.number_input("Coefficient c (pour C)", min_value=1, value=1, step=1)
    d = st.number_input("Coefficient d (pour D)", min_value=1, value=1, step=1)

with col2:
    st.subheader("2. État initial (en mol)")
    n0_A = st.number_input("Quantité initiale n0(A)", min_value=0.0, value=0.0, step=0.1)
    n0_B = st.number_input("Quantité initiale n0(B)", min_value=0.0, value=0.0, step=0.1)
    n0_C = st.number_input("Quantité initiale n0(C)", min_value=0.0, value=0.0, step=0.1)
    n0_D = st.number_input("Quantité initiale n0(D)", min_value=0.0, value=0.0, step=0.1)

st.divider()

# ==========================================
# MOTEUR DE CALCUL (Invisible pour l'élève)
# ==========================================
rapport_A = n0_A / a
rapport_B = n0_B / b

if rapport_A < rapport_B:
    x_max = rapport_A
    bilan_texte = "Le réactif A est le réactif limitant (il s'épuise en premier)."
elif rapport_B < rapport_A:
    x_max = rapport_B
    bilan_texte = "Le réactif B est le réactif limitant (il s'épuise en premier)."
else:
    x_max = rapport_A
    bilan_texte = "Le mélange est stœchiométrique (les deux réactifs s'épuisent)."

nf_A = n0_A - a * x_max
nf_B = n0_B - b * x_max
nf_C = n0_C + c * x_max
nf_D = n0_D + d * x_max

# ==========================================
# RÉSULTATS ET GRAPHIQUE
# ==========================================
st.subheader("3. Bilan et Histogramme")
st.success(f"**Conclusion :** {bilan_texte} | $x_{{max}} = {x_max:.2f}$ mol")

# ==========================================
# RÉSULTATS ET GRAPHIQUE OPTIMISÉ
# ==========================================
st.subheader("3. Bilan et Histogramme")
st.success(f"**Conclusion :** {bilan_texte} | $x_{{max}} = {x_max:.2f}$ mol")

# 1. Réorganisation des données : d'abord TOUT l'initial, puis TOUT le final
categories = [
    'A\n(Init)', 'B\n(Init)', 'C\n(Init)', 'D\n(Init)',  # Bloc Initial
    'A\n(Fin)', 'B\n(Fin)', 'C\n(Fin)', 'D\n(Fin)'      # Bloc Final
]

valeurs = [
    n0_A, n0_B, n0_C, n0_D,  # Éléments initiaux
    nf_A, nf_B, nf_C, nf_D   # Éléments finaux
]

# Couleurs adaptées (Clair pour l'initial, Foncé pour le final)
# Rouge = A, Orange = B, Vert = C, Bleu = D
couleurs = [
    '#ff9999', '#ffcc99', '#99ff99', '#99ccff',  # Initial (A, B, C, D)
    '#cc0000', '#ff6600', '#009900', '#0000cc'   # Final (A, B, C, D)
]

# Création de la figure
fig, ax = plt.subplots(figsize=(11, 6))
barres = ax.bar(categories, valeurs, color=couleurs, edgecolor='black', width=0.6)

# Affichage des valeurs au-dessus de chaque barre
for barre in barres:
    hauteur = barre.get_height()
    if hauteur >= 0:
        ax.text(barre.get_x() + barre.get_width()/2, hauteur + 0.02 * (max(valeurs) if max(valeurs) > 0 else 1), 
                f"{hauteur:.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

# --- AJOUT DU "MUR" DE SÉPARATION ---
# Le mur se situe pile entre l'indice 3 (D Init) et l'indice 4 (A Fin), donc à la position x = 3.5
ax.axvline(x=3.5, color='black', linestyle='-', linewidth=3, label="Déroulement de la réaction")

# --- AJOUT DE LA FLÈCHE D'ÉVOLUTION ---
# On dessine une belle flèche qui part du bloc initial vers le bloc final
ax.annotate(
    "ÉVOLUTION DE LA RÉACTION", 
    xy=(4.5, max(valeurs) * 1.1 if max(valeurs) > 0 else 1.0),   # Pointe de la flèche (côté Final)
    xytext=(0.5, max(valeurs) * 1.1 if max(valeurs) > 0 else 1.0), # Début de la flèche (côté Initial)
    arrowprops=dict(facecolor='black', shrink=0.08, headwidth=10, width=3),
    fontsize=10, fontweight='bold', ha='left', va='center'
)

# Habillage de l'axe et grilles
ax.set_ylabel(r"Quantité de matière $n \text{ (mol)}$", fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Titres des deux grands blocs pour guider la lecture
ax.text(1.5, -max(valeurs)*0.15 if max(valeurs) > 0 else -0.15, "ÉTAIT INITIAL", fontsize=12, fontweight='bold', ha='center', color='gray')
ax.text(5.5, -max(valeurs)*0.15 if max(valeurs) > 0 else -0.15, "ÉTAT FINAL", fontsize=12, fontweight='bold', ha='center', color='gray')

# Limite supérieure automatique adaptée pour laisser la place à la flèche en haut
ax.set_ylim(0, max(valeurs) * 1.3 if max(valeurs) > 0 else 1.5)

# Affichage du graphique sur Streamlit
st.pyplot(fig)
