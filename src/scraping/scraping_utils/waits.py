"""
Realiza uma pausa aleatória durante a coleta
"""

import random

def pausa_aleatoria(min = 1.3, max = 4.8):
    return random.uniform(min, max)