"""
WNEURA RESEARCH CONFIGURATION
Simulation Parameters & Hyperparameters
"""

import os


IDX_PFC   = 0  
IDX_NAC   = 1  
IDX_AMYG  = 2  
IDX_LOAD  = 3  
IDX_SLEEP = 4  
IDX_DRUG  = 5  


TOTAL_DAYS = 365            
POPULATION_SIZE = 100       
LOG_INTERVAL = 1            


DRUG_HALF_LIFE = 0.75       
DRUG_SPIKE = 0.8            
TOLERANCE_RATE = 0.995     
SLEEP_PENALTY = 0.5         


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_simulation_data.csv')
