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

tab_giris , tab_bakis , tab_analiz = st.tabs(["Ana Sayfa","Genel Bakış","Analiz"])
#------------------------------------------------------------------------------
with tab_giris : 
    st.markdown("### Bu sayfa nedir\nBu site minik bir arayışın sonucudur. Zira sismisite analizi açısından bir çok araşm olmakla beraber bir şekilde özelleştirilebilir bir arayüz arayışındaydım. Bu site ile bearber çözüm gelmiş oldu.\n\nAhmet Anıl Dindar")

with tab_bakis : 

    onceki_depremler_df = kayitli_depremler( ) ;

    metin = f"Şu anda bu sitede önceden kaydedilmiş {len( onceki_depremler_df)} adet deprem bulunmaktadır. En büyük deprem **{onceki_depremler_df[ onceki_depremler_df.Magnitude == onceki_depremler_df.Magnitude.max() ].iloc[0].Type} {onceki_depremler_df.Magnitude.max()}**, **{onceki_depremler_df[ onceki_depremler_df.Magnitude == onceki_depremler_df.Magnitude.max() ].iloc[0].Date}** tarihinde **{onceki_depremler_df[ onceki_depremler_df.Magnitude == onceki_depremler_df.Magnitude.max() ].iloc[0].Location}** konumunda gözlenmiştir."
    
    # st.data_editor( onceki_depremler_df)

    st.markdown( metin)

    st.map( data = onceki_depremler_df , latitude="Latitude", longitude = "Longitude" , size = "Magnitude")



with tab_analiz : 
    last = dt.datetime.today().strftime("%Y-%m-%d") + "%2000:00:00"
    first = (dt.datetime.today() - dt.timedelta(days = 1 )).strftime("%Y-%m-%d") + "%2000:00:00"

    #------------------------------------------------------------------------------

    AFAD_eqe_df = afad_reader( first , last ) 
    AFAD_eqe_df["Magnitude"] *= 5

    # AFAD_eqe_df.to_csv( "AAD-AFAD_Depremler.csv" , index = False)

    #------------------------------------------------------------------------------

    st.dataframe( AFAD_eqe_df)
    st.markdown("---")
    st.map( data = AFAD_eqe_df , latitude="Latitude", longitude = "Longitude" , size = "Magnitude")
# %%
