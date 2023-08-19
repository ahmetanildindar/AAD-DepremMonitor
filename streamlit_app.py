#%%
import pandas as pd 
import streamlit as st 
import datetime as dt 

#
#
#%%
st.set_page_config( page_title="AAD AFAD EQE Monitor", layout="wide")
#
#%%
@st.cache_resource
def afad_reader( first , last ) :

    """
    url_master = "https://deprem.afad.gov.tr/apiv2/event/filter?minlat=34&maxlat=40&minlon=33&maxlon=43&start=2023-02-06%2000:00:00&end=2023-08-10%2000:00:00&format=csv"
    """
    url_master = f"https://deprem.afad.gov.tr/apiv2/event/filter?minlat=36&maxlat=42&minlon=26&maxlon=45&start={first}&end={last}&minmag=3.0&format=csv"

    #
    AFAD_eqe_son_okuma_df = pd.read_csv( url_master)
    AFAD_eqe_son_okuma_df["Date"] = pd.to_datetime( AFAD_eqe_son_okuma_df["Date"] )
    #
    return( AFAD_eqe_son_okuma_df )
#
def kayitli_depremler( ) : 
    mevcut_depremler_df = pd.read_csv( "AAD-AFAD_Depremler.csv")

    return( mevcut_depremler_df)
#
#%% ===========================================================================
st.markdown(f"### AAD AFAD Depremler")

tab_giris , tab_bakis , tab_detay = st.tabs(["AnaSayfa","GenelBakış","Analiz"])
#------------------------------------------------------------------------------
with tab_giris : 
    st.write("Bakıs")
    onceki_depremler_df = kayitli_depremler( )

    # st.dataframe( onceki_depremler_df)
    st.data_editor( onceki_depremler_df)


with tab_bakis : 
    last = dt.datetime.today().strftime("%Y-%m-%d") + "%2000:00:00"
    first = (dt.datetime.today() - dt.timedelta(days = 1 )).strftime("%Y-%m-%d") + "%2000:00:00"

    #------------------------------------------------------------------------------

    AFAD_eqe_df = afad_reader( first , last ) 

    # AFAD_eqe_df.to_csv( "AAD-AFAD_Depremler.csv" , index = False)

    #------------------------------------------------------------------------------

    st.dataframe( AFAD_eqe_df)
    st.markdown("---")
    st.map( data = AFAD_eqe_df , latitude="Latitude", longitude = "Longitude" , size = "Magnitude")
# %%
