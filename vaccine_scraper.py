import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class VaccineCertificateScraper:
    def __init__(self):
        self.base_url = "https://vaccine.moh.ps/certificate"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_certificate(self, national_id):
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Initialize the driver
            driver = webdriver.Chrome(options=chrome_options)
            
            # Navigate to the certificate page
            driver.get(self.base_url)
            time.sleep(2)  # Wait for page to load
            
            # Find and fill the ID input field
            id_input = driver.find_element(By.ID, "id_no")
            id_input.send_keys(national_id)
            
            # Find and click the submit button
            submit_button = driver.find_element(By.ID, "inquiryBtn")
            submit_button.click()
            
            # Wait for results to load
            time.sleep(3)
            
            # Extract certificate information
            certificate = {
                'national_id': national_id,
                'name': self._get_element_text(driver, "name_span"),
                'date_of_birth': self._get_element_text(driver, "dob_span"),
                'gender': self._get_element_text(driver, "gender_span"),
                'mobile': self._get_element_text(driver, "mobile_span"),
                'district': self._get_element_text(driver, "district_span"),
                'clinic': self._get_element_text(driver, "clinic_span")
            }
            
            # Get vaccination appointments
            appointments = self._get_appointments(driver)
            certificate['appointments'] = appointments
            
            # Get vaccination doses
            doses = self._get_doses(driver)
            certificate['doses'] = doses
            
            driver.quit()
            return certificate
            
        except Exception as e:
            print(f"Error getting certificate: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    def _get_element_text(self, driver, element_id):
        try:
            element = driver.find_element(By.ID, element_id)
            return element.text
        except:
            return ""
    
    def _get_appointments(self, driver):
        appointments = []
        try:
            container = driver.find_element(By.ID, "appointmentsContainer")
            steps = container.find_elements(By.CLASS_NAME, "process-step")
            
            for step in steps:
                try:
                    date = step.find_element(By.CLASS_NAME, "process-step-circle-content").text
                    clinic = step.find_element(By.CLASS_NAME, "process-step-content").find_element(By.TAG_NAME, "h4").text
                    year = step.find_element(By.CLASS_NAME, "process-step-content").find_element(By.TAG_NAME, "p").text
                    
                    appointments.append({
                        'date': date,
                        'clinic': clinic,
                        'year': year
                    })
                except:
                    continue
        except:
            pass
        return appointments
    
    def _get_doses(self, driver):
        doses = []
        try:
            container = driver.find_element(By.ID, "dosesContainer")
            steps = container.find_elements(By.CLASS_NAME, "process-step")
            
            for step in steps:
                try:
                    date = step.find_element(By.CLASS_NAME, "process-step-circle-content").text
                    clinic = step.find_element(By.CLASS_NAME, "process-step-content").find_element(By.TAG_NAME, "h4").text
                    vaccine = step.find_element(By.CLASS_NAME, "process-step-content").find_elements(By.TAG_NAME, "p")[0].text
                    dose_number = step.find_element(By.CLASS_NAME, "process-step-content").find_elements(By.TAG_NAME, "p")[1].text
                    
                    doses.append({
                        'date': date,
                        'clinic': clinic,
                        'vaccine': vaccine,
                        'dose_number': dose_number
                    })
                except:
                    continue
        except:
            pass
        return doses 