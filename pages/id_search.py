import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IDSearcher:
    def __init__(self):
        self.base_url = "https://vaccine.moh.ps/certificate"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_info(self, national_id):
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
            
            # Extract basic information only
            info = {
                'national_id': national_id,
                'name': self._get_element_text(driver, "name_span"),
                'date_of_birth': self._get_element_text(driver, "dob_span"),
                'gender': self._get_element_text(driver, "gender_span"),
                'mobile': self._get_element_text(driver, "mobile_span"),
                'district': self._get_element_text(driver, "district_span")
            }
            
            driver.quit()
            return info
            
        except Exception as e:
            print(f"Error getting info: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    def _get_element_text(self, driver, element_id):
        try:
            element = driver.find_element(By.ID, element_id)
            return element.text
        except:
            return ""

def show_id_search():
    st.markdown("<h2 style='text-align: center;'>البحث برقم الهوية</h2>", unsafe_allow_html=True)
    
    # Input field
    national_id = st.text_input("أدخل رقم الهوية", key="national_id")
    
    if st.button("استعلام"):
        if national_id:
            with st.spinner("جاري البحث..."):
                searcher = IDSearcher()
                info = searcher.get_info(national_id)
                
                if info and any(info.values()):
                    # Create two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                        st.markdown("<div class='info-title'>معلومات الشخص</div>", unsafe_allow_html=True)
                        
                        # Display personal information
                        st.markdown(f"<p><span class='info-label'>رقم الهوية:</span> <span class='info-value'>{info['national_id']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>الاسم:</span> <span class='info-value'>{info['name']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>تاريخ الميلاد:</span> <span class='info-value'>{info['date_of_birth']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>الجنس:</span> <span class='info-value'>{info['gender']}</span></p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                        st.markdown("<div class='info-title'>معلومات الاتصال</div>", unsafe_allow_html=True)
                        
                        # Display contact information
                        st.markdown(f"<p><span class='info-label'>الهاتف المحمول:</span> <span class='info-value'>{info['mobile']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>المحافظة:</span> <span class='info-value'>{info['district']}</span></p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("لم يتم العثور على معلومات للرقم المدخل")
        else:
            st.warning("الرجاء إدخال رقم الهوية")
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 نظام البحث المتعدد - جميع الحقوق محفوظة</p>", unsafe_allow_html=True) 