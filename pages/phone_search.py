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
import re

class PhoneSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.search_platforms = {
            'Social Media': {
                'Facebook': {
                    'url': 'https://www.facebook.com/login/identify?ctx=recover',
                    'search_url': 'https://www.facebook.com/search/top?q={phone}',
                    'description': 'البحث عن رقم الهاتف في فيسبوك'
                },
                'Twitter': {
                    'url': 'https://twitter.com/search?q={phone}',
                    'description': 'البحث عن رقم الهاتف في تويتر'
                },
                'Instagram': {
                    'url': 'https://www.instagram.com/accounts/password/reset/',
                    'description': 'البحث عن رقم الهاتف في انستغرام'
                },
                'LinkedIn': {
                    'url': 'https://www.linkedin.com/search/results/people/?keywords={phone}',
                    'description': 'البحث عن رقم الهاتف في لينكد إن'
                }
            },
            'Phone Lookup': {
                'Truecaller': {
                    'url': 'https://www.truecaller.com/search/{phone}',
                    'description': 'البحث عن معلومات صاحب الرقم'
                },
                'NumVerify': {
                    'url': 'https://numverify.com/',
                    'description': 'التحقق من معلومات الرقم'
                },
                'PhoneInfoga': {
                    'url': 'https://github.com/sundowndev/phoneinfoga',
                    'description': 'أداة متقدمة للبحث عن معلومات الأرقام'
                }
            },
            'Data Breaches': {
                'HaveIBeenPwned': {
                    'url': 'https://haveibeenpwned.com/',
                    'description': 'البحث عن تسريبات البيانات المرتبطة بالرقم'
                },
                'BreachDirectory': {
                    'url': 'https://breachdirectory.p.rapidapi.com/',
                    'description': 'البحث في قاعدة البيانات المسربة'
                }
            },
            'Messaging Apps': {
                'WhatsApp': {
                    'url': 'https://wa.me/{phone}',
                    'description': 'البحث عن الرقم في واتساب'
                },
                'Telegram': {
                    'url': 'https://t.me/{phone}',
                    'description': 'البحث عن الرقم في تيليجرام'
                },
                'Viber': {
                    'url': 'https://invite.viber.com/?g={phone}',
                    'description': 'البحث عن الرقم في فايبر'
                }
            }
        }
    
    def validate_phone(self, phone):
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        # Check if the number has a valid length (between 10 and 15 digits)
        return len(phone) >= 10 and len(phone) <= 15
    
    def format_phone(self, phone):
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        # Add country code if not present (assuming Egypt +20)
        if not phone.startswith('20'):
            phone = '20' + phone
        return phone
    
    def search_platform(self, phone, platform, tool):
        try:
            search_url = tool['url'].format(phone=phone)
            return {
                'platform': platform,
                'tool': tool['name'],
                'url': search_url,
                'description': tool['description'],
                'found': True
            }
        except Exception as e:
            return {
                'platform': platform,
                'tool': tool['name'],
                'error': str(e),
                'description': tool['description']
            }

def show_phone_search():
    st.markdown("<h2 style='text-align: center;'>البحث برقم الهاتف</h2>", unsafe_allow_html=True)
    
    # Input field
    phone = st.text_input("أدخل رقم الهاتف", key="phone")
    
    # Platform selection
    platforms = st.multiselect(
        "اختر منصات البحث",
        ["Social Media", "Phone Lookup", "Data Breaches", "Messaging Apps"],
        default=["Social Media", "Phone Lookup", "Data Breaches", "Messaging Apps"]
    )
    
    if st.button("بحث"):
        if phone:
            searcher = PhoneSearcher()
            
            if not searcher.validate_phone(phone):
                st.error("الرجاء إدخال رقم هاتف صحيح")
                return
            
            formatted_phone = searcher.format_phone(phone)
            
            with st.spinner("جاري البحث..."):
                all_results = []
                
                # Search in selected platforms
                for platform in platforms:
                    st.info(f"جاري البحث في {platform}...")
                    platform_tools = searcher.search_platforms.get(platform, {})
                    
                    for tool_name, tool_info in platform_tools.items():
                        tool_info['name'] = tool_name
                        result = searcher.search_platform(formatted_phone, platform, tool_info)
                        all_results.append(result)
                
                # Display results
                if all_results:
                    st.success(f"تم العثور على {len(all_results)} نتيجة")
                    
                    # Group results by platform
                    for platform in platforms:
                        platform_results = [r for r in all_results if r.get('platform') == platform]
                        if platform_results:
                            st.markdown(f"### نتائج {platform}")
                            
                            # Create columns for better layout
                            cols = st.columns(2)
                            
                            for idx, result in enumerate(platform_results):
                                with cols[idx % 2]:
                                    st.markdown("---")
                                    if 'tool' in result:
                                        st.markdown(f"**{result['tool']}**")
                                    if 'description' in result:
                                        st.info(result['description'])
                                    if 'url' in result:
                                        st.markdown(f"[فتح الرابط]({result['url']})")
                                    if 'error' in result:
                                        st.error(result['error'])
                else:
                    st.warning("لم يتم العثور على نتائج")
        else:
            st.warning("الرجاء إدخال رقم الهاتف")
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 نظام البحث المتعدد - جميع الحقوق محفوظة</p>", unsafe_allow_html=True) 