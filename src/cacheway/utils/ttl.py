from datetime import datetime,timedelta

def check_ttl(cached_data:dict):
    now = datetime.now()
    duration = timedelta(minutes=1)
    
    for cache_key in list(cached_data.keys()): 
        timestamp = cached_data[cache_key]["timestamp"]
        elapsed_time = now - timestamp
        
        if elapsed_time > duration:
            del cached_data[cache_key]