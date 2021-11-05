import get_spending
import streamlit as st
import streamlit.components.v1 as components
import locale

year=2021

locale.setlocale(locale.LC_ALL, '')
st.set_page_config(page_title='US Tax Allocation', layout='wide', page_icon='💰')
components.html(
    """
    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js"
    crossorigin="anonymous"></script>
        <script>
            SplunkRum.init({
            beaconUrl: 'https://rum-ingest.us1.signalfx.com/v1/rum',
            rumAuth: '{AUTH}',
            app: 'tax-allocation'
        });
    </script>
    """
)
st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: 0rem;
        padding-bottom: 1rem;
    }} </style> """, unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center;">Federal US Tax Allocation Calculator</h1>', unsafe_allow_html=True)
search = st.text_input('Tax Payment', value='$', help='Enter the amount of money you paid in taxes for '+str(year)+' (without commas)')
if st.button('Calculate'):
    st.text('Calculating... (this might take a minute)')
    output_text = get_spending.run(year, float(search.replace('$','')))
    st.markdown(output_text, unsafe_allow_html=True)