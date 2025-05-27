import streamlit as st

def show_email_search():
    st.markdown("<h2 style='text-align: center;'>البحث بالبريد الإلكتروني</h2>", unsafe_allow_html=True)
    st.info("هذه الخدمة قيد التطوير")
    
    email = st.text_input("أدخل البريد الإلكتروني", key="email")
    
    if st.button("بحث"):
        if email:
            st.warning("هذه الخدمة غير متوفرة حالياً")
        else:
            st.warning("الرجاء إدخال البريد الإلكتروني") 