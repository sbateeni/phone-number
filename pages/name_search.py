import streamlit as st

def show_name_search():
    st.markdown("<h2 style='text-align: center;'>البحث بالاسم</h2>", unsafe_allow_html=True)
    st.info("هذه الخدمة قيد التطوير")
    
    name = st.text_input("أدخل الاسم", key="name")
    
    if st.button("بحث"):
        if name:
            st.warning("هذه الخدمة غير متوفرة حالياً")
        else:
            st.warning("الرجاء إدخال الاسم") 