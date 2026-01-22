import pandas as pd
import numpy as np
import time
import sys
from src.config import *
from src.agent import StochasticAgent

def generate_population(size):
    """
    100 Farklı 'Fıtratta' İnsan Yaratır.
    Kimi iradeli, kimi strese gelemiyor, kimi bağımlılığa yatkın.
    """
    population = []
    print(f"🧬 GENETİK HAVUZ OLUŞTURULUYOR: {size} Denek")
    
    for i in range(size):
        
        willpower = np.random.normal(0.5, 0.15)
        resilience = np.random.normal(0.5, 0.15)
        addiction_prone = np.random.normal(0.3, 0.2) 
        
        
        genotype = {
            "willpower": np.clip(willpower, 0.1, 0.95),
            "resilience": np.clip(resilience, 0.1, 0.95),
            "addiction_prone": np.clip(addiction_prone, 0.05, 0.9)
        }
        
        agent = StochasticAgent(agent_id=i, genotype=genotype)
        population.append(agent)
        
    return population

def run_clinical_trial():
    """
    DENEYİ BAŞLATIR
    """
    start_time = time.time()
    agents = generate_population(POPULATION_SIZE)
    all_data = []

    print(f"🚀 SİMÜLASYON BAŞLATILIYOR ({TOTAL_DAYS} Gün)...")
    print("-" * 50)

   
    total_steps = POPULATION_SIZE * TOTAL_DAYS
    current_step = 0

    for agent in agents:
        for day in range(1, TOTAL_DAYS + 1):
          
            daily_stats = agent.transition_rule(day)
            
            
            daily_stats["Agent_ID"] = agent.id
            daily_stats["Day"] = day
            daily_stats["Genotype_Willpower"] = agent.willpower_baseline
            
            all_data.append(daily_stats)
            
            current_step += 1
        
        
        if agent.id % 10 == 0:
            sys.stdout.write(f"\r⏳ İlerleme: %{round((current_step / total_steps)*100, 1)} tamamlandı.")
            sys.stdout.flush()

    print(f"\n✅ SİMÜLASYON TAMAMLANDI!")
    print("-" * 50)

    
    print("💾 Veriler işleniyor ve kaydediliyor...")
    df = pd.DataFrame(all_data)
    

    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"📄 DOSYA OLUŞTURULDU: {RAW_DATA_PATH}")
    print(f"⏱️ Geçen Süre: {round(time.time() - start_time, 2)} saniye")

if __name__ == "__main__":
    run_clinical_trial()
