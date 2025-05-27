import streamlit as st
import os
from pages.id_search import show_id_search
from pages.email_search import show_email_search
from pages.phone_search import show_phone_search
from pages.name_search import show_name_search
from pages.address_search import show_address_search

# Set page config
st.set_page_config(
    page_title="نظام البحث المتعدد",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        direction: rtl;
    }
    .stButton>button {
        width: 100%;
    }
    .info-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-title {
        color: #1f77b4;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .info-label {
        font-weight: bold;
        color: #666;
    }
    .info-value {
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .sidebar-title {
        color: #1f77b4;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("<div class='sidebar-title'>القائمة الرئيسية</div>", unsafe_allow_html=True)

# Define pages
PAGES = {
    "البحث برقم الهوية": show_id_search,
    "البحث بالبريد الإلكتروني": show_email_search,
    "البحث برقم الهاتف": show_phone_search,
    "البحث بالاسم": show_name_search,
    "البحث بالعنوان": show_address_search
}

# Create sidebar navigation
selected_page = st.sidebar.radio("اختر نوع البحث", list(PAGES.keys()))

# Main content area
st.markdown("<h1 style='text-align: center;'>نظام البحث المتعدد</h1>", unsafe_allow_html=True)

# Show selected page
PAGES[selected_page]()

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2024 نظام البحث المتعدد - جميع الحقوق محفوظة</p>", unsafe_allow_html=True) 