import random
import string
from datetime import datetime

def generate():
    prefix = "DEF"
    date = datetime.now().strftime("%Y%m%D")
    
    id = ''.join(random.choices(string.digits, k=6))
    control_sum = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    track = f'{prefix}{date}-{id}-{control_sum}'
    
    return track
    