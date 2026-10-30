import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuration du style des graphiques
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.autolayout': True})

# 2. Création du dossier figures s'il n'existe pas
os.makedirs('figures', exist_ok=True)

# 3. Chargement des données (ajuste le chemin si ton fichier est dans 'data/logs_reseau.csv')
data_path = 'logs_reseau.csv' if os.path.exists('logs_reseau.csv') else 'data/logs_reseau.csv'
df = pd.read_csv(data_path)

print(f"Nombre de lignes initiales : {len(df)}")

# --- ÉTAPE 1 : NETTOYAGE DES DONNÉES ---
# 1. Supprimer les doublons exacts
df = df.drop_duplicates()

# 2. Mettre le protocole en MAJUSCULES
if 'protocol' in df.columns:
    df['protocol'] = df['protocol'].astype(str).str.upper().str.strip()

# 3. Remplacer les bytes_sent manquants par la médiane de la colonne[cite: 6]
if 'bytes_sent' in df.columns:
    mediane_bytes = df['bytes_sent'].median()
    df['bytes_sent'] = df['bytes_sent'].fillna(mediane_bytes)

nb_lignes_apres = int(len(df))
print(f"Nombre de lignes après nettoyage : {nb_lignes_apres}")

# --- ÉTAPE 2 : CALCUL DES RÉSULTATS[cite: 6] ---
top_port = int(df['dst_port'].mode()[0]) if 'dst_port' in df.columns and not df['dst_port'].mode().empty else 0

total_connexions = len(df)
nb_deny = len(df[df['action'].astype(str).str.upper() == 'DENY']) if 'action' in df.columns else 0
taux_deny_pct = round((nb_deny / total_connexions) * 100, 2) if total_connexions > 0 else 0.0

ip_scanner = str(df.groupby('src_ip')['dst_port'].nunique().idxmax()) if 'src_ip' in df.columns else "N/A"
ip_exfiltration = str(df.groupby('src_ip')['bytes_sent'].sum().idxmax()) if 'src_ip' in df.columns else "N/A"

# Dictionnaire des résultats
resultats = {
    "nb_lignes_apres_nettoyage": nb_lignes_apres,
    "top_port": top_port,
    "taux_deny_pct": taux_deny_pct,
    "ip_scanner": ip_scanner,
    "ip_exfiltration": ip_exfiltration
}

# Affichage des résultats dans le notebook
print("\n--- RÉSULTATS CALCULÉS ---")
print(json.dumps(resultats, indent=4))

# Sauvegarde automatique dans resultats.json[cite: 6]
with open('resultats.json', 'w', encoding='utf-8') as f:
    json.dump(resultats, f, indent=4)


# --- ÉTAPE 3 : GÉNÉRATION DES GRAPHIQUES (Matplotlib & Seaborn) ---

# Graphique 1 : Top 5 des ports de destination les plus fréquents (Seaborn Barplot)
plt.figure(figsize=(9, 5))
top_ports = df['dst_port'].value_counts().head(5).reset_index()
top_ports.columns = ['dst_port', 'count']
ax = sns.barplot(data=top_ports, x='dst_port', y='count', palette='Blues_r', hue='dst_port', legend=False)
plt.title('Top 5 des ports de destination les plus fréquents', fontsize=14, fontweight='bold')
plt.xlabel('Port de destination', fontsize=12)
plt.ylabel('Nombre de connexions', fontsize=12)
plt.savefig('figures/top_ports.png', dpi=300)
plt.show()

# Graphique 2 : Répartition des actions ALLOW / DENY (Matplotlib Pie Chart)
plt.figure(figsize=(6, 6))
action_counts = df['action'].value_counts()
colors = ['#2ecc71', '#e74c3c'] # Vert pour ALLOW, Rouge pour DENY
plt.pie(action_counts, labels=action_counts.index, autopct='%1.1f%%', colors=colors, startangle=90, explode=(0.05, 0.0))
plt.title('Répartition des actions (ALLOW / DENY)', fontsize=14, fontweight='bold')
plt.savefig('figures/repartition_allow_deny.png', dpi=300)
plt.show()

# Graphique 3 : Volume total d'octets envoyés par type d'appareil (Seaborn Barplot)
plt.figure(figsize=(9, 5))
bytes_device = df.groupby('device_type')['bytes_sent'].sum().reset_index()
sns.barplot(data=bytes_device, x='device_type', y='bytes_sent', palette='Oranges_r', hue='device_type', legend=False)
plt.title("Volume total d'octets envoyés par type d'appareil", fontsize=14, fontweight='bold')
plt.xlabel("Type d'appareil", fontsize=12)
plt.ylabel("Total bytes_sent (Octets)", fontsize=12)
plt.xticks(rotation=15)
plt.savefig('figures/bytes_par_appareil.png', dpi=300)
plt.show()

print("\n--- TOUT EST TERMINÉ ---")
print("Les graphiques ont été enregistrés dans le dossier 'figures/' et le fichier 'resultats.json' a été mis à jour !")