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

class EmailSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.osint_tools = {
            'Mail Blacklists': {
                'MXToolbox': 'https://mxtoolbox.com/blacklists.aspx',
                'Spamhaus': 'https://check.spamhaus.org/',
                'MultiRBL': 'https://multirbl.valli.org/',
                'AbuseIPDB': 'https://www.abuseipdb.com/check/'
            },
            'Breach Data': {
                'HaveIBeenPwned': 'https://haveibeenpwned.com/',
                'BreachDirectory': 'https://breachdirectory.p.rapidapi.com/',
                'DeHashed': 'https://dehashed.com/',
                'Leak-Lookup': 'https://leak-lookup.com/'
            },
            'Email Verification': {
                'Email Validator': 'https://email-validator.net/',
                'Email Hippo': 'https://tools.verifyemailaddress.io/',
                'Email Checker': 'https://email-checker.net/',
                'Zero Bounce': 'https://www.zerobounce.net/'
            },
            'Common Email Formats': {
                'Email Format': 'https://www.email-format.com/',
                'Find Email Format': 'https://findemailformat.com/',
                'Email Permutator': 'https://www.metacrawler.com/email-permutator/',
                'Email Finder': 'https://hunter.io/email-finder'
            },
            'Email Search': {
                'TheHarvester': 'https://github.com/laramies/theHarvester',
                'Holehe': 'https://github.com/megadose/holehe',
                'Email Finder': 'https://www.emailfinder.com/',
                'Find That Lead': 'https://findthatlead.com/'
            }
        }
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def search_category(self, email, category):
        results = []
        if category in self.osint_tools:
            for tool_name, url in self.osint_tools[category].items():
                try:
                    # Format URL if it contains {email} placeholder
                    search_url = url.format(email=email) if '{email}' in url else url
                    
                    results.append({
                        'platform': category,
                        'tool': tool_name,
                        'url': search_url,
                        'found': True,
                        'details': f'رابط البحث في {tool_name}',
                        'search_url': search_url,
                        'instructions': self.get_tool_instructions(tool_name, category)
                    })
                except Exception as e:
                    results.append({
                        'platform': category,
                        'tool': tool_name,
                        'error': str(e),
                        'details': f'حدث خطأ أثناء البحث في {tool_name}'
                    })
        return results
    
    def get_tool_instructions(self, tool_name, category):
        instructions = {
            'Mail Blacklists': {
                'MXToolbox': 'أدخل البريد الإلكتروني في حقل البحث للتحقق من القوائم السوداء',
                'Spamhaus': 'استخدم البريد الإلكتروني للتحقق من وجوده في قوائم Spamhaus',
                'MultiRBL': 'أدخل البريد الإلكتروني للتحقق من وجوده في قوائم RBL متعددة',
                'AbuseIPDB': 'استخدم البريد الإلكتروني للتحقق من التقارير السابقة'
            },
            'Breach Data': {
                'HaveIBeenPwned': 'أدخل البريد الإلكتروني للتحقق من تسريبات البيانات',
                'BreachDirectory': 'استخدم البريد الإلكتروني للبحث في قاعدة البيانات المسربة',
                'DeHashed': 'أدخل البريد الإلكتروني للبحث في قاعدة البيانات المسربة',
                'Leak-Lookup': 'استخدم البريد الإلكتروني للبحث في التسريبات'
            },
            'Email Verification': {
                'Email Validator': 'أدخل البريد الإلكتروني للتحقق من صحته',
                'Email Hippo': 'استخدم البريد الإلكتروني للتحقق من وجوده',
                'Email Checker': 'أدخل البريد الإلكتروني للتحقق من صحته',
                'Zero Bounce': 'استخدم البريد الإلكتروني للتحقق من صحته'
            },
            'Common Email Formats': {
                'Email Format': 'أدخل اسم النطاق للعثور على تنسيقات البريد الإلكتروني الشائعة',
                'Find Email Format': 'استخدم اسم النطاق للبحث عن تنسيقات البريد الإلكتروني',
                'Email Permutator': 'أدخل الاسم والنطاق لإنشاء تنسيقات محتملة للبريد الإلكتروني',
                'Email Finder': 'استخدم الاسم والنطاق للعثور على البريد الإلكتروني'
            },
            'Email Search': {
                'TheHarvester': 'أداة سطر الأوامر للبحث عن البريد الإلكتروني',
                'Holehe': 'أداة سطر الأوامر للتحقق من وجود البريد الإلكتروني في مواقع مختلفة',
                'Email Finder': 'أدخل الاسم والنطاق للعثور على البريد الإلكتروني',
                'Find That Lead': 'استخدم الاسم والنطاق للبحث عن البريد الإلكتروني'
            }
        }
        return instructions.get(category, {}).get(tool_name, 'استخدم البريد الإلكتروني للبحث')

def show_email_search():
    st.markdown("<h2 style='text-align: center;'>البحث بالبريد الإلكتروني</h2>", unsafe_allow_html=True)
    
    # Input field
    email = st.text_input("أدخل البريد الإلكتروني", key="email")
    
    # Platform selection
    platforms = st.multiselect(
        "اختر منصات البحث",
        ["Mail Blacklists", "Breach Data", "Email Verification", "Common Email Formats", "Email Search"],
        default=["Mail Blacklists", "Breach Data", "Email Verification", "Common Email Formats", "Email Search"]
    )
    
    if st.button("بحث"):
        if email:
            searcher = EmailSearcher()
            
            if not searcher.validate_email(email):
                st.error("الرجاء إدخال بريد إلكتروني صحيح")
                return
            
            with st.spinner("جاري البحث..."):
                all_results = []
                
                # Search in selected platforms
                for platform in platforms:
                    st.info(f"جاري البحث في {platform}...")
                    platform_results = searcher.search_category(email, platform)
                    all_results.extend(platform_results)
                
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
                                    if 'url' in result:
                                        st.markdown(f"[فتح الرابط]({result['url']})")
                                    if 'details' in result:
                                        st.markdown(result['details'])
                                    if 'instructions' in result:
                                        st.info(result['instructions'])
                                    if 'search_url' in result:
                                        st.markdown(f"[فتح صفحة البحث]({result['search_url']})")
                                    if 'error' in result:
                                        st.error(result['error'])
                else:
                    st.warning("لم يتم العثور على نتائج")
        else:
            st.warning("الرجاء إدخال البريد الإلكتروني")
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 نظام البحث المتعدد - جميع الحقوق محفوظة</p>", unsafe_allow_html=True) 