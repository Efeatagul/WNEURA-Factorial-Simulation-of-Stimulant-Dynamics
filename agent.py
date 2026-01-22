import numpy as np
from src.config import *

class StochasticAgent:
    def __init__(self, agent_id, genotype):
        self.id = agent_id
        
       
        self.state = np.array([
            1.0,  
            1.0,  
            0.1,  
            0.1,  
            1.0,  
            0.0   
        ], dtype=np.float64)

        
        
        self.willpower_baseline = genotype.get('willpower', 0.5)     
        self.addiction_prone = genotype.get('addiction_prone', 0.1)  
        self.stress_resilience = genotype.get('resilience', 0.5)     

    def compute_external_load(self, t):
        """
        EKONOMİK DOYGUNLUK YASASI (Law of Diminishing Returns)
        Zaman ilerledikçe başarı için gereken efor logaritmik artar.
        """
        k = 0.18 
        
        load = k * np.log(t + 5) 
        return min(1.0, load)

    def transition_rule(self, t):
        """
        MARKOV GEÇİŞ FONKSİYONU: S(t+1) = f(S(t)) + Noise
        """
        
        pfc = self.state[IDX_PFC]
        nac = self.state[IDX_NAC]
        amyg = self.state[IDX_AMYG]
        drug = self.state[IDX_DRUG]
        sleep = self.state[IDX_SLEEP]

        
        ext_load = self.compute_external_load(t)
        self.state[IDX_LOAD] = ext_load

        
        
        capacity = pfc * sleep
        gap = ext_load - capacity 
        
       
        stress_spike = max(0, gap) * (1.0 - self.stress_resilience)
        
        
       
        craving = (1.0 - nac) 
        inhibition = pfc * self.willpower_baseline 
        
        
        risk_prob = (stress_spike + craving + (drug * 0.5)) / (inhibition + 0.01)
        
      
        action_take_drug = False
        
        if np.random.rand() < (risk_prob * 0.1): 
            action_take_drug = True

       
        
     
        if action_take_drug:
            
            self.state[IDX_DRUG] += DRUG_SPIKE
            
            self.state[IDX_NAC] *= TOLERANCE_RATE 
            self.state[IDX_SLEEP] *= SLEEP_PENALTY 
        else:
            
            self.state[IDX_DRUG] *= DRUG_HALF_LIFE

       
        withdrawal = 0.0
        if drug > 0.1 and not action_take_drug:
            withdrawal = 0.2 
        
        target_amyg = stress_spike + withdrawal
       
        self.state[IDX_AMYG] = (0.8 * amyg) + (0.2 * target_amyg)

        
        pfc_decay = ((1.0 - sleep) * 0.1) + (amyg * 0.05)
        self.state[IDX_PFC] = max(0.1, pfc - pfc_decay)
        
        
        if sleep > 0.8:
            self.state[IDX_PFC] = min(1.0, self.state[IDX_PFC] + 0.02)

      
        if self.state[IDX_DRUG] > 0.2:
            self.state[IDX_SLEEP] = max(0.1, sleep * 0.8)
        else:
            self.state[IDX_SLEEP] = min(1.0, sleep + 0.1) 

        
        noise = np.random.normal(0, 0.01, size=6)
        self.state = np.clip(self.state + noise, 0.0, 1.0)

       
        return {
            "PFC": self.state[IDX_PFC],
            "NAc": self.state[IDX_NAC],
            "Amyg": self.state[IDX_AMYG],
            "Load": self.state[IDX_LOAD],
            "Sleep": self.state[IDX_SLEEP],
            "Drug": self.state[IDX_DRUG],
            "Action": 1 if action_take_drug else 0
        }
