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

# Création du graphique
categories = ['A (Initial)', 'A (Final)', 'B (Initial)', 'B (Final)', 
              'C (Initial)', 'C (Final)', 'D (Initial)', 'D (Final)']
valeurs = [n0_A, nf_A, n0_B, nf_B, n0_C, nf_C, n0_D, nf_D]
couleurs = ['#ff9999', '#cc0000', '#ffcc99', '#ff6600', '#99ff99', '#009900', '#99ccff', '#0000cc']

fig, ax = plt.subplots(figsize=(10, 5))
barres = ax.bar(categories, valeurs, color=couleurs, edgecolor='black', width=0.6)

for barre in barres:
    hauteur = barre.get_height()
    if hauteur >= 0:
        ax.text(barre.get_x() + barre.get_width()/2, hauteur + 0.05, 
                f"{hauteur:.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel(r"Quantité de matière $n \text{ (mol)}$")
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.set_ylim(0, max(valeurs) * 1.2 if max(valeurs) > 0 else 1.0)

# Affichage du graphique dans l'application
st.pyplot(fig)