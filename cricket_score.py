# Python program to launch Cricbuzz in a browser, navigate to the IND vs SA Women's Final scorecard,
# and extract the full scorecard details using Selenium and BeautifulSoup.

# Prerequisites:
# 1. Install required packages: pip install selenium beautifulsoup4
# 2. Download ChromeDriver from https://chromedriver.chromium.org/ and add it to your PATH.
# 3. This script assumes the match URL is known; it directly navigates there for simplicity.
#    If you want to search from the homepage, additional logic can be added.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# URL for the IND vs SA Women's World Cup 2025 Final scorecard
match_url = "https://www.cricbuzz.com/live-cricket-scorecard/121681/indw-vs-rsaw-final-icc-womens-world-cup-2025"

# Initialize the Chrome driver
driver = webdriver.Chrome()  # Ensure ChromeDriver is in PATH

try:
    # Navigate to the scorecard page
    print("Launching Cricbuzz and navigating to IND vs SA Women's Final scorecard...")
    driver.get(match_url)
    
    # Wait for the page to load (adjust time if needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cb-scrcrd-sec"))
    )
    time.sleep(2)  # Additional wait for dynamic content
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all scorecard sections (batting, bowling, fall of wickets, etc.)
    # Cricbuzz uses divs with class 'cb-scrcrd-sec cb-col-100 cb-lst-wgt' for main scorecard units
    scorecard_sections = soup.find_all('div', class_='cb-scrcrd-sec cb-col-100 cb-lst-wgt')
    
    print("\n=== FULL SCOREBOARD EXTRACTED ===\n")
    
    # Extract and print text from each section
    for i, section in enumerate(scorecard_sections):
        # Clean and print the text content of each section
        section_text = section.get_text(separator=' | ', strip=True)
        print(f"SECTION {i+1}:\n{section_text}\n{'-'*80}\n")
    
    # Optionally, extract match summary from the top
    match_summary = soup.find('div', class_='cb-nav-main')
    if match_summary:
        summary_text = match_summary.get_text(strip=True)
        print("MATCH SUMMARY:\n", summary_text)
    
    print("\nScorecard extraction complete!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()