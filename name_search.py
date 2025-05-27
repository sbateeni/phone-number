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

class NameSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def search_facebook(self, name):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=chrome_options)
            
            # Search Facebook
            search_url = f"https://www.facebook.com/search/top?q={name}"
            driver.get(search_url)
            time.sleep(2)
            
            # Get search results
            results = []
            elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
            for element in elements[:5]:  # Get first 5 results
                try:
                    profile_link = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    profile_name = element.find_element(By.CSS_SELECTOR, 'span').text
                    results.append({
                        'name': profile_name,
                        'link': profile_link,
                        'platform': 'Facebook'
                    })
                except:
                    continue
            
            driver.quit()
            return results
        except Exception as e:
            print(f"Facebook search error: {str(e)}")
            return []

    def search_twitter(self, name):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=chrome_options)
            
            # Search Twitter
            search_url = f"https://twitter.com/search?q={name}&src=typed_query"
            driver.get(search_url)
            time.sleep(2)
            
            # Get search results
            results = []
            elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
            for element in elements[:5]:  # Get first 5 results
                try:
                    profile_link = element.find_element(By.CSS_SELECTOR, 'a[role="link"]').get_attribute('href')
                    profile_name = element.find_element(By.CSS_SELECTOR, 'span').text
                    results.append({
                        'name': profile_name,
                        'link': profile_link,
                        'platform': 'Twitter'
                    })
                except:
                    continue
            
            driver.quit()
            return results
        except Exception as e:
            print(f"Twitter search error: {str(e)}")
            return []

    def search_linkedin(self, name):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=chrome_options)
            
            # Search LinkedIn
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={name}"
            driver.get(search_url)
            time.sleep(2)
            
            # Get search results
            results = []
            elements = driver.find_elements(By.CSS_SELECTOR, 'div.entity-result__item')
            for element in elements[:5]:  # Get first 5 results
                try:
                    profile_link = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    profile_name = element.find_element(By.CSS_SELECTOR, 'span.entity-result__title-text').text
                    results.append({
                        'name': profile_name,
                        'link': profile_link,
                        'platform': 'LinkedIn'
                    })
                except:
                    continue
            
            driver.quit()
            return results
        except Exception as e:
            print(f"LinkedIn search error: {str(e)}")
            return []

    def search_google(self, name):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=chrome_options)
            
            # Search Google
            search_url = f"https://www.google.com/search?q={name}"
            driver.get(search_url)
            time.sleep(2)
            
            # Get search results
            results = []
            elements = driver.find_elements(By.CSS_SELECTOR, 'div.g')
            for element in elements[:5]:  # Get first 5 results
                try:
                    link = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    title = element.find_element(By.CSS_SELECTOR, 'h3').text
                    results.append({
                        'title': title,
                        'link': link,
                        'platform': 'Google'
                    })
                except:
                    continue
            
            driver.quit()
            return results
        except Exception as e:
            print(f"Google search error: {str(e)}")
            return []

def show_name_search():
    st.markdown("<h2 style='text-align: center;'>البحث بالاسم</h2>", unsafe_allow_html=True)
    
    # Input field
    name = st.text_input("أدخل الاسم", key="name")
    
    # Platform selection
    platforms = st.multiselect(
        "اختر منصات البحث",
        ["Facebook", "Twitter", "LinkedIn", "Google"],
        default=["Facebook", "Twitter", "LinkedIn", "Google"]
    )
    
    if st.button("بحث"):
        if name:
            with st.spinner("جاري البحث..."):
                searcher = NameSearcher()
                all_results = []
                
                # Search in selected platforms
                if "Facebook" in platforms:
                    st.info("جاري البحث في Facebook...")
                    facebook_results = searcher.search_facebook(name)
                    all_results.extend(facebook_results)
                
                if "Twitter" in platforms:
                    st.info("جاري البحث في Twitter...")
                    twitter_results = searcher.search_twitter(name)
                    all_results.extend(twitter_results)
                
                if "LinkedIn" in platforms:
                    st.info("جاري البحث في LinkedIn...")
                    linkedin_results = searcher.search_linkedin(name)
                    all_results.extend(linkedin_results)
                
                if "Google" in platforms:
                    st.info("جاري البحث في Google...")
                    google_results = searcher.search_google(name)
                    all_results.extend(google_results)
                
                # Display results
                if all_results:
                    st.success(f"تم العثور على {len(all_results)} نتيجة")
                    
                    # Group results by platform
                    for platform in platforms:
                        platform_results = [r for r in all_results if r['platform'] == platform]
                        if platform_results:
                            st.markdown(f"### نتائج {platform}")
                            for result in platform_results:
                                with st.expander(result.get('name', result.get('title', 'بدون عنوان'))):
                                    st.markdown(f"**الرابط:** [{result['link']}]({result['link']})")
                                    if 'name' in result:
                                        st.markdown(f"**الاسم:** {result['name']}")
                                    if 'title' in result:
                                        st.markdown(f"**العنوان:** {result['title']}")
                else:
                    st.warning("لم يتم العثور على نتائج")
        else:
            st.warning("الرجاء إدخال الاسم") 