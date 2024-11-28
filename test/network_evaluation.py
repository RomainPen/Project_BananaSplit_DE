import psutil
from playwright.sync_api import sync_playwright
import time

def format_bytes(bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def measure_network_usage():
    
    with sync_playwright() as p:
        print("Starting network usage measurement...")
        browser = p.chromium.launch(headless=False)
        
        
        # 1. First page - Archive page for a specific year
        page_1 = browser.new_page()
        print("\n1 : Loading season of 2010")
        before_load = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        page_1.goto('https://www.atptour.com/en/scores/results-archive?tournamentType=atpgs&year=2010')
        time.sleep(5)  # Wait for all content to load
        after_load = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        page_load_bytes_1 = after_load - before_load
        print(f"Loading season 2010 load used: {format_bytes(page_load_bytes_1)}")
        page_1.close()


        # 2. Tournament page (sample)
        page_2 = browser.new_page()
        print("\n2 : Loading 1 tournament page of 2010")
        before_load = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        page_2.goto('https://www.atptour.com/en/scores/archive/brisbane/339/2010/results')
        time.sleep(5)  # Wait for all content to load
        after_load = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        page_load_bytes_2 = after_load - before_load
        print(f"Loading 1 tournament page of 2010 load used: {format_bytes(page_load_bytes_2)}")
        page_2.close()


        # 3. match page (sample)
        page_3 = browser.new_page()
        print("\n3 : Loading 1 match page of 2010")
        before_load = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        page_3.goto('https://www.atptour.com/en/scores/results-archive?tournamentType=atpgs&year=2010')
        time.sleep(5)  # Wait for all content to load
        after_load = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        page_load_bytes_3 = after_load - before_load
        print(f"Loading 1 match page of 2010 load used: {format_bytes(page_load_bytes_3)}")
        page_3.close()
    


    
    sum_date_recv = (page_load_bytes_1 + page_load_bytes_2 + page_load_bytes_3)
    print(f"\nsummary for one request : {format_bytes(sum_date_recv)}")
        
        
    print("\nNetwork Usage Summary:")
    # Estimate for full year
    # Let's estimate based on your actual scraping pattern
    tournaments_per_year = 60  # approximate
    matches_per_tournament = 70  # approximate
    
    estimated_yearly_bytes = page_load_bytes_1 + (page_load_bytes_2 * int(tournaments_per_year))  + (page_load_bytes_3 * matches_per_tournament * tournaments_per_year)  
    
    print(f"estimated_yearly_bytes : {format_bytes(estimated_yearly_bytes)}")
    print(f"Per concurrent browser (assuming 4 browsers): {format_bytes(estimated_yearly_bytes/4)}")

    nb_season = 10
    estimated_total_bytes = (page_load_bytes_1 + (page_load_bytes_2 * int(tournaments_per_year))  + (page_load_bytes_3 * matches_per_tournament * tournaments_per_year))*nb_season

    print(f"estimated_total_bytes : {format_bytes(estimated_total_bytes)}")
    print(f"Per concurrent browser (assuming 4 browsers): {format_bytes(estimated_total_bytes/4)}")

if __name__ == "__main__":
    measure_network_usage()