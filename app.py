import streamlit as st
from pages import id_search, email_search, phone_search, name_search, address_search

# Set page config
st.set_page_config(
    page_title="OSINT Framework - نظام البحث المتعدد",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        direction: rtl;
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin: 0.5rem 0;
        padding: 0.8rem;
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        border: none;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .info-title {
        font-size: 1.4em;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2c3e50;
    }
    .info-label {
        font-weight: bold;
        color: #2c3e50;
        font-size: 1.1em;
    }
    .info-value {
        color: #34495e;
        font-size: 1.1em;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 1rem;
    }
    .sidebar-title {
        color: #1a237e;
        font-size: 2em;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    .sidebar-subtitle {
        color: #303f9f;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .search-category {
        font-weight: bold;
        color: #1a237e;
        margin: 1rem 0;
        font-size: 1.3em;
        padding: 10px;
        border-radius: 5px;
        background-color: #e8eaf6;
    }
    .platform-icon {
        font-size: 1.4em;
        margin-right: 0.5rem;
    }
    .search-description {
        font-size: 1em;
        color: #455a64;
        margin: 0.8rem 0;
        line-height: 1.5;
    }
    .search-features {
        font-size: 0.95em;
        color: #546e7a;
        margin: 0.8rem 0;
        padding-right: 1.5rem;
        line-height: 1.6;
    }
    .search-features li {
        margin: 0.5rem 0;
    }
    .menu-title {
        color: #1a237e;
        font-size: 1.4em;
        text-align: center;
        margin: 1.5rem 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h1 class='sidebar-title'>OSINT Framework</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 class='sidebar-subtitle'>نظام البحث المتعدد</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Main menu
st.sidebar.markdown("<h3 class='menu-title'>اختر نوع البحث</h3>", unsafe_allow_html=True)

# Define pages with categories and detailed descriptions
PAGES = {
    "البحث برقم الهوية": {
        "function": id_search.show_id_search,
        "description": "البحث عن رقم الهاتف باستخدام رقم الهوية",
        "features": [
            "عرض معلومات الشخص"
        ],
        "icon": "🪪",
        "color": "#4CAF50"
    },
    "البحث بالبريد الإلكتروني": {
        "function": email_search.show_email_search,
        "description": "البحث عن البريد الإلكتروني في قوائم البريد السوداء، بيانات التسريب، والتحقق من صحة البريد",
        "features": [
            "البحث في قوائم البريد السوداء",
            "التحقق من تسريبات البيانات",
            "البحث في مواقع التواصل الاجتماعي",
            "التحقق من صحة البريد الإلكتروني"
        ],
        "icon": "📧",
        "color": "#2196F3"
    },
    "البحث برقم الهاتف": {
        "function": phone_search.show_phone_search,
        "description": "البحث عن معلومات باستخدام رقم الهاتف",
        "features": [
            "البحث في مواقع التواصل الاجتماعي",
            "التحقق من معلومات صاحب الرقم",
            "البحث في تطبيقات المراسلة",
            "التحقق من تسريبات البيانات"
        ],
        "icon": "📱",
        "color": "#9C27B0"
    },
    "البحث بالاسم": {
        "function": name_search.show_name_search,
        "description": "البحث عن معلومات باستخدام الاسم",
        "features": [
            "البحث في Social Searcher",
            "البحث في مواقع التواصل الاجتماعي",
            "البحث في محركات البحث",
            "البحث في مواقع البحث عن الأشخاص"
        ],
        "icon": "👤",
        "color": "#FF9800"
    },
    "البحث بالعنوان": {
        "function": address_search.show_address_search,
        "description": "البحث عن معلومات باستخدام العنوان",
        "features": [
            "البحث في خرائط جوجل",
            "البحث في السجلات العقارية",
            "البحث في المواقع الجغرافية"
        ],
        "icon": "📍",
        "color": "#F44336"
    }
}

# Create buttons for each page with descriptions and features
for page_name, page_info in PAGES.items():
    st.sidebar.markdown(f"""
        <div class='search-category' style='background-color: {page_info['color']}20; border-right: 4px solid {page_info['color']};'>
            <span class='platform-icon'>{page_info['icon']}</span> {page_name}
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
        <div class='info-box' style='border-right: 3px solid {page_info['color']};'>
            <div class='search-description'>{page_info['description']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class='search-features'>", unsafe_allow_html=True)
    for feature in page_info['features']:
        st.sidebar.markdown(f"• {feature}")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    if st.sidebar.button(f"بدء البحث في {page_name}", key=page_name):
        st.session_state['current_page'] = page_name
    st.sidebar.markdown("---")

# Footer
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <p style='color: #1a237e; font-size: 1.1em; font-weight: bold;'>© 2024 OSINT Framework</p>
        <p style='color: #303f9f; font-size: 1em;'>نظام البحث المتعدد</p>
        <p style='color: #455a64; font-size: 0.9em;'>جميع الحقوق محفوظة</p>
    </div>
""", unsafe_allow_html=True)

# Show selected page
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "البحث برقم الهوية"

# Display the selected page
PAGES[st.session_state['current_page']]['function']() 