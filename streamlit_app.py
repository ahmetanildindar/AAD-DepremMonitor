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
    AFAD_eqe_1_df = pd.read_csv( url_master)
    AFAD_eqe_1_df["Date"] = pd.to_datetime( AFAD_eqe_1_df["Date"] )
    #
    return( AFAD_eqe_1_df)
#
#%%

st.title("AAD AFAD Depremler")
#--------------------
last = dt.datetime.today().strftime("%Y-%m-%d") + "%2000:00:00"
first = (dt.datetime.today() - dt.timedelta(days=3)).strftime("%Y-%m-%d") + "%2000:00:00"

AFAD_eqe_df = afad_reader( first , last ) 

st.dataframe( AFAD_eqe_df)
st.markdown("---")
st.map( data = AFAD_eqe_df , latitude="Latitude", longitude = "Longitude" , size = "Magnitude")
# %%