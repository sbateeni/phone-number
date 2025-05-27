from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

class VaccineCertificateScraper:
    def __init__(self):
        self.base_url = "https://vaccine.moh.ps/certificate"

    def get_certificate(self, national_id):
        """
        Get vaccination certificate for a given national ID using Selenium
        """
        try:
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in headless mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Initialize the Chrome driver
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Navigate to the certificate page
                driver.get(self.base_url)
                
                # Wait for the input field to be present
                id_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "id_no"))
                )
                
                # Fill in the national ID
                id_input.send_keys(national_id)
                
                # Find and click the submit button
                submit_button = driver.find_element(By.ID, "inquiryBtn")
                submit_button.click()
                
                # Wait for the response
                time.sleep(2)
                
                # Extract certificate information
                certificate_data = {
                    'national_id': self._get_text(driver, '#id_no_span'),
                    'date_of_birth': self._get_text(driver, '#dob_span'),
                    'gender': self._get_text(driver, '#gender_span'),
                    'mobile': self._get_text(driver, '#mobile_span'),
                    'district': self._get_text(driver, '#district_span'),
                    'clinic': self._get_text(driver, '#clinic_span'),
                }
                
                return certificate_data
                
            finally:
                # Always close the driver
                driver.quit()

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def _get_text(self, driver, selector):
        """
        Helper method to get text from an element
        """
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except:
            return None

def main():
    scraper = VaccineCertificateScraper()
    
    # Example usage
    national_id = input("Please enter the national ID: ")
    certificate = scraper.get_certificate(national_id)
    
    if certificate:
        print("\nCertificate Information:")
        print(json.dumps(certificate, indent=2, ensure_ascii=False))
    else:
        print("Failed to retrieve certificate information.")

if __name__ == "__main__":
    main() 