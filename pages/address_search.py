import streamlit as st

def show_address_search():
    st.markdown("<h2 style='text-align: center;'>البحث بالعنوان</h2>", unsafe_allow_html=True)
    st.info("هذه الخدمة قيد التطوير")
    
    address = st.text_input("أدخل العنوان", key="address")
    
    if st.button("بحث"):
        if address:
            st.warning("هذه الخدمة غير متوفرة حالياً")
        else:
            st.warning("الرجاء إدخال العنوان") 