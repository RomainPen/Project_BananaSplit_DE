import psutil
from playwright.sync_api import sync_playwright
import time

def get_chrome_processes_memory():
    """Get total memory usage of all Chrome processes in GB"""
    total_memory = 0
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            if 'chrome' in proc.info['name'].lower():
                total_memory += proc.info['memory_info'].rss
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return total_memory / (1024 * 1024 * 1024)  # Convert to GB

def measure_chrome_memory():
    """Measure memory usage of multiple Chrome instances"""
    # Kill any existing Chrome processes
    for proc in psutil.process_iter(['name']):
        try:
            if 'chrome' in proc.info['name'].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    time.sleep(2)  # Wait for processes to close
    
    initial_memory = get_chrome_processes_memory()
    print(f"Initial Chrome memory usage: {initial_memory:.2f} GB")
    
    browsers = []
    measurements = []
    
    with sync_playwright() as p:
        # Launch browsers one by one and measure memory impact
        for i in range(5):  # Test with 5 browsers
            print(f"\nLaunching browser {i+1}")
            
            # Measure before launch
            before_launch = get_chrome_processes_memory()
            
            # Launch browser
            browser = p.chromium.launch(headless=False)
            browsers.append(browser)
            
            # Wait for browser to stabilize
            time.sleep(5)
            
            # Measure after launch
            after_launch = get_chrome_processes_memory()
            
            # Calculate difference
            difference = after_launch - before_launch
            measurements.append(difference)
            
            print(f"Chrome memory before browser {i+1}: {before_launch:.2f} GB")
            print(f"Chrome memory after browser {i+1}: {after_launch:.2f} GB")
            print(f"Memory impact of browser {i+1}: {difference:.2f} GB")
            
            # Load a test page
            page = browser.new_page()
            page.goto('https://www.atptour.com')
            time.sleep(5)
            
            # Measure after page load
            after_page = get_chrome_processes_memory()
            page_impact = after_page - after_launch
            print(f"Additional memory after loading page: {page_impact:.2f} GB")
            
            # Get total system memory info
            system_memory = psutil.virtual_memory()
            print(f"System memory used: {(system_memory.used/1024/1024/1024):.2f} GB")
            print(f"System memory available: {(system_memory.available/1024/1024/1024):.2f} GB")
        
        print("\nSummary:")
        print(f"Average memory per browser: {sum(measurements)/len(measurements):.2f} GB")
        print(f"Maximum memory impact for a single browser: {max(measurements):.2f} GB")
        print(f"Minimum memory impact for a single browser: {min(measurements):.2f} GB")
        
        # Clean up
        for browser in browsers:
            browser.close()
        
        time.sleep(5)  # Wait for processes to close
        
        # Final memory measurement
        final_memory = get_chrome_processes_memory()
        print(f"\nFinal Chrome memory usage after closing all browsers: {final_memory:.2f} GB")
        print(f"Memory not immediately recovered: {final_memory - initial_memory:.2f} GB")
        
        # Final system memory info
        system_memory = psutil.virtual_memory()
        print(f"Final system memory used: {(system_memory.used/1024/1024/1024):.2f} GB")
        print(f"Final system memory available: {(system_memory.available/1024/1024/1024):.2f} GB")

if __name__ == "__main__":
    measure_chrome_memory()