import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from src.config import *

def analyze_results():
    print("🔬 DETAYLI ANALİZ BAŞLATILIYOR (Figure 1-5)...")
    
 
    try:
        df = pd.read_csv(RAW_DATA_PATH)
    except FileNotFoundError:
        print("❌ HATA: Veri yok! Önce runner.py çalıştır.")
        return

    
    plt.style.use('dark_background')
    save_dir = os.path.join(DATA_DIR, 'processed')
    os.makedirs(save_dir, exist_ok=True)

    
    drug_users = df[df['Drug'] > 0.1]['Agent_ID'].unique()
    df['Group'] = df['Agent_ID'].apply(lambda x: 'User' if x in drug_users else 'Control')

  
    print("📸 Çiziliyor: Figure 1 - The Trap...")
    early_phase = df[df['Day'] <= 60]
    
    plt.figure(figsize=(10, 6))
   
    sns.lineplot(data=early_phase[early_phase['Group']=='User'], x='Day', y='Drug', color='cyan', label='Drug Intake')
   
    sns.lineplot(data=early_phase[early_phase['Group']=='User'], x='Day', y='PFC', color='red', label='PFC Health')
    
    plt.title('Figure 1: The Honeymoon Phase (First 60 Days)', fontsize=14, color='white')
    plt.ylabel('Level (normalized)')
    plt.grid(True, alpha=0.1)
    plt.savefig(os.path.join(save_dir, 'Fig1_The_Trap.png'), dpi=300)
    plt.close()

    
    print("📸 Çiziliyor: Figure 2 - Sleep Debt...")
    
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df[df['Group']=='User'], x='Drug', y='Sleep', fill=True, cmap='inferno')
    plt.title('Figure 2: The Sleep Tax (Drug Concentration vs Sleep Quality)', fontsize=14, color='white')
    plt.xlabel('Serum Drug Concentration')
    plt.ylabel('Circadian Efficiency (Sleep)')
    plt.grid(True, alpha=0.1)
    plt.savefig(os.path.join(save_dir, 'Fig2_Sleep_Tax.png'), dpi=300)
    plt.close()

   
    print("📸 Çiziliyor: Figure 3 - Genetic Factors...")
    
    final_day = df[df['Day'] == 365]
    
    plt.figure(figsize=(10, 6))
    
    sc = plt.scatter(final_day['Genotype_Willpower'], final_day['Drug'], 
                     c=final_day['PFC'], cmap='coolwarm', s=100, edgecolors='white', alpha=0.8)
    
    plt.colorbar(sc, label='Final Brain Health (PFC)')
    plt.title('Figure 3: Genetic Resilience (Willpower vs Addiction Outcome)', fontsize=14, color='white')
    plt.xlabel('Genetic Willpower (Born With)')
    plt.ylabel('Final Drug Dependence')
    plt.axhline(y=0.1, color='white', linestyle='--', alpha=0.5, label='Addiction Threshold')
    plt.legend()
    plt.grid(True, alpha=0.1)
    plt.savefig(os.path.join(save_dir, 'Fig3_Genetics.png'), dpi=300)
    plt.close()

    
    print("📸 Çiziliyor: Figure 4 - The Crash...")
    
    mid_phase = df[(df['Day'] > 120) & (df['Day'] < 220)]
    
    plt.figure(figsize=(12, 6))
    
    sns.lineplot(data=mid_phase, x='Day', y='Amyg', hue='Group', palette={'User': 'red', 'Control': 'green'})
    
    plt.title('Figure 4: The Crash Point (Amygdala/Stress Explosion)', fontsize=14, color='white')
    plt.axvline(x=150, color='yellow', linestyle='--', label='Tolerance Wall')
    plt.ylabel('Anxiety / Stress Level')
    plt.legend()
    plt.grid(True, alpha=0.1)
    plt.savefig(os.path.join(save_dir, 'Fig4_The_Crash.png'), dpi=300)
    plt.close()

    
    print("📸 Çiziliyor: Figure 5 - Terminal State...")
    
    plt.figure(figsize=(10, 8))
   
    sns.scatterplot(data=final_day, x='Amyg', y='PFC', hue='Group', size='Drug', sizes=(20, 200), palette='bright')
    
    plt.title('Figure 5: Terminal State (Anxiety vs Willpower)', fontsize=14, color='white')
    plt.xlabel('Chronic Anxiety (Amygdala)')
    plt.ylabel('Cognitive Control (PFC)')
    plt.grid(True, alpha=0.1)
    plt.savefig(os.path.join(save_dir, 'Fig5_Overview.png'), dpi=300)
    plt.close()

    print("-" * 40)
    print(f"✅ TÜM GRAFİKLER HAZIRLANDI: {save_dir}")
    print("Dosyalara tek tek bakıp makale bölümlerini yazabiliriz.")

if __name__ == "__main__":
    analyze_results()
