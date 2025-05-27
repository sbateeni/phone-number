import streamlit as st

def show_phone_search():
    st.markdown("<h2 style='text-align: center;'>البحث برقم الهاتف</h2>", unsafe_allow_html=True)
    st.info("هذه الخدمة قيد التطوير")
    
    phone = st.text_input("أدخل رقم الهاتف", key="phone")
    
    if st.button("بحث"):
        if phone:
            st.warning("هذه الخدمة غير متوفرة حالياً")
        else:
            st.warning("الرجاء إدخال رقم الهاتف") 