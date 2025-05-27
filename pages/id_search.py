import streamlit as st
from vaccine_scraper import VaccineCertificateScraper

def show_id_search():
    st.markdown("<h2 style='text-align: center;'>البحث برقم الهوية</h2>", unsafe_allow_html=True)
    
    # Input field
    national_id = st.text_input("أدخل رقم الهوية", key="national_id")
    
    if st.button("استعلام"):
        if national_id:
            with st.spinner("جاري البحث..."):
                scraper = VaccineCertificateScraper()
                certificate = scraper.get_certificate(national_id)
                
                if certificate and any(certificate.values()):
                    # Create two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                        st.markdown("<div class='info-title'>معلومات الشخص</div>", unsafe_allow_html=True)
                        
                        # Display personal information
                        st.markdown(f"<p><span class='info-label'>رقم الهوية:</span> <span class='info-value'>{certificate['national_id']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>تاريخ الميلاد:</span> <span class='info-value'>{certificate['date_of_birth']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>الجنس:</span> <span class='info-value'>{certificate['gender']}</span></p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                        st.markdown("<div class='info-title'>معلومات الاتصال</div>", unsafe_allow_html=True)
                        
                        # Display contact information
                        st.markdown(f"<p><span class='info-label'>الهاتف المحمول:</span> <span class='info-value'>{certificate['mobile']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p><span class='info-label'>المحافظة:</span> <span class='info-value'>{certificate['district']}</span></p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("لم يتم العثور على معلومات للرقم المدخل")
        else:
            st.warning("الرجاء إدخال رقم الهوية") 