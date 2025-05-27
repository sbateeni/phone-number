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
        padding: 0.5rem;
        border-radius: 5px;
        background-color: #f0f2f6;
        border: 1px solid #ddd;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e6e9ef;
        border-color: #1f77b4;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #ddd;
    }
    .info-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #1f77b4;
    }
    .info-label {
        font-weight: bold;
        color: #1f77b4;
    }
    .info-value {
        color: #2c3e50;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .sidebar-title {
        color: #1f77b4;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 1rem;
    }
    .search-category {
        font-weight: bold;
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    .platform-icon {
        font-size: 1.2em;
        margin-right: 0.5rem;
    }
    .search-description {
        font-size: 0.9em;
        color: #666;
        margin-top: 0.5rem;
    }
    .search-features {
        font-size: 0.85em;
        color: #888;
        margin-top: 0.5rem;
        padding-right: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h1 class='sidebar-title'>OSINT Framework</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 class='sidebar-title'>نظام البحث المتعدد</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Main menu
st.sidebar.markdown("<h3 style='text-align: center;'>اختر نوع البحث</h3>", unsafe_allow_html=True)

# Define pages with categories and detailed descriptions
PAGES = {
    "البحث برقم الهوية": {
        "function": id_search.show_id_search,
        "description": "البحث عن رقم الهاتف باستخدام رقم الهوية",
        "features": [
            "عرض معلومات الشخص",
        ],
        "icon": "🪪"
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
        "icon": "📧"
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
        "icon": "📱"
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
        "icon": "👤"
    },
    "البحث بالعنوان": {
        "function": address_search.show_address_search,
        "description": "البحث عن معلومات باستخدام العنوان",
        "features": [
            "البحث في خرائط جوجل",
            "البحث في السجلات العقارية",
            "البحث في المواقع الجغرافية"
        ],
        "icon": "📍"
    }
}

# Create buttons for each page with descriptions and features
for page_name, page_info in PAGES.items():
    st.sidebar.markdown(f"<div class='search-category'>{page_info['icon']} {page_name}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='info-box'>{page_info['description']}</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='search-features'>", unsafe_allow_html=True)
    for feature in page_info['features']:
        st.sidebar.markdown(f"• {feature}")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    if st.sidebar.button(f"بدء البحث في {page_name}", key=page_name):
        st.session_state['current_page'] = page_name
    st.sidebar.markdown("---")

# Footer
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p>© 2025 OSINT Framework</p>
        <p>نظام البحث المتعدد</p>
        <p>جميع الحقوق محفوظة</p>
    </div>
""", unsafe_allow_html=True)

# Show selected page
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "البحث برقم الهوية"

# Display the selected page
PAGES[st.session_state['current_page']]['function']() 