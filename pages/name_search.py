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

class NameSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.search_platforms = {
            'Social Searcher': {
                'Google Social Search': {
                    'url': 'https://www.social-searcher.com/google-social-search/?q={name}',
                    'description': 'البحث عن الاسم في محركات البحث ومواقع التواصل الاجتماعي'
                },
                'Social Buzz': {
                    'url': 'https://www.social-searcher.com/social-buzz/?q={name}',
                    'description': 'تحليل تأثير الاسم على وسائل التواصل الاجتماعي'
                },
                'Search Users': {
                    'url': 'https://www.social-searcher.com/search-users/?q={name}',
                    'description': 'البحث عن المستخدمين في مواقع التواصل الاجتماعي'
                }
            },
            'Social Media': {
                'Facebook': {
                    'url': 'https://www.facebook.com/search/top?q={name}',
                    'description': 'البحث عن الاسم في فيسبوك'
                },
                'Twitter': {
                    'url': 'https://twitter.com/search?q={name}',
                    'description': 'البحث عن الاسم في تويتر'
                },
                'LinkedIn': {
                    'url': 'https://www.linkedin.com/search/results/people/?keywords={name}',
                    'description': 'البحث عن الاسم في لينكد إن'
                },
                'Instagram': {
                    'url': 'https://www.instagram.com/{name}/',
                    'description': 'البحث عن الاسم في انستغرام'
                }
            },
            'Search Engines': {
                'Google': {
                    'url': 'https://www.google.com/search?q={name}',
                    'description': 'البحث عن الاسم في جوجل'
                },
                'Bing': {
                    'url': 'https://www.bing.com/search?q={name}',
                    'description': 'البحث عن الاسم في بينج'
                },
                'DuckDuckGo': {
                    'url': 'https://duckduckgo.com/?q={name}',
                    'description': 'البحث عن الاسم في دك دك جو'
                }
            },
            'People Search': {
                'Pipl': {
                    'url': 'https://pipl.com/search/?q={name}',
                    'description': 'البحث عن معلومات الأشخاص'
                },
                'Spokeo': {
                    'url': 'https://www.spokeo.com/search?q={name}',
                    'description': 'البحث عن معلومات الاتصال'
                },
                'PeopleFinder': {
                    'url': 'https://www.peoplefinder.com/search?q={name}',
                    'description': 'البحث عن معلومات الأشخاص'
                }
            }
        }
    
    def validate_name(self, name):
        # Check if name is not empty and contains only letters, spaces, and common name characters
        return bool(re.match(r'^[a-zA-Z\u0600-\u06FF\s\-\.]+$', name))
    
    def format_name(self, name):
        # Remove extra spaces and convert to URL-friendly format
        return name.strip().replace(' ', '+')
    
    def search_platform(self, name, platform, tool):
        try:
            search_url = tool['url'].format(name=self.format_name(name))
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

def show_name_search():
    st.markdown("<h2 style='text-align: center;'>البحث بالاسم</h2>", unsafe_allow_html=True)
    
    # Input field
    name = st.text_input("أدخل الاسم", key="name")
    
    # Platform selection
    platforms = st.multiselect(
        "اختر منصات البحث",
        ["Social Searcher", "Social Media", "Search Engines", "People Search"],
        default=["Social Searcher", "Social Media", "Search Engines", "People Search"]
    )
    
    if st.button("بحث"):
        if name:
            searcher = NameSearcher()
            
            if not searcher.validate_name(name):
                st.error("الرجاء إدخال اسم صحيح")
                return
            
            with st.spinner("جاري البحث..."):
                all_results = []
                
                # Search in selected platforms
                for platform in platforms:
                    st.info(f"جاري البحث في {platform}...")
                    platform_tools = searcher.search_platforms.get(platform, {})
                    
                    for tool_name, tool_info in platform_tools.items():
                        tool_info['name'] = tool_name
                        result = searcher.search_platform(name, platform, tool_info)
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
            st.warning("الرجاء إدخال الاسم")
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2024 نظام البحث المتعدد - جميع الحقوق محفوظة</p>", unsafe_allow_html=True) 