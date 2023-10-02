#%%
import pandas as pd
import streamlit as st
import datetime as dt
import plotly.figure_factory as ff

#
#%%
st.set_page_config( page_title="AAD Deprem Monitor", layout="wide")
#
#%%
# @st.cache_data
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
st.markdown(f"### AAD Depremler")

tab_giris , tab_bakis , tab_analiz , tab_test = st.tabs(["Ana Sayfa","Genel Bakış","Analiz","Test"])
#------------------------------------------------------------------------------
with tab_giris :
    st.markdown("### Bu sayfa nedir\nBu site minik bir arayışın sonucudur. Zira sismisite analizi açısından bir çok araşm olmakla beraber bir şekilde özelleştirilebilir bir arayüz arayışındaydım. Bu site ile bearber çözüm gelmiş oldu.\n\nDepremlere ait bilgiler AFAD'ın web sitesinden alınmaktadır.\n\nAhmet Anıl Dindar")

with tab_bakis :

    onceki_depremler_df = kayitli_depremler( ) ;

    onceki_depremler_df["Date"] = pd.to_datetime( onceki_depremler_df["Date"] , yearfirst = True )

    metin = f"Şu anda bu sitede önceden kaydedilmiş **{len( onceki_depremler_df)}** adet deprem bulunmaktadır. En büyük deprem **{onceki_depremler_df[ onceki_depremler_df.Magnitude == onceki_depremler_df.Magnitude.max() ].iloc[0].Type} {onceki_depremler_df.Magnitude.max()}**, **{onceki_depremler_df[ onceki_depremler_df.Magnitude == onceki_depremler_df.Magnitude.max() ].iloc[0].Date}** tarihinde **{onceki_depremler_df[ onceki_depremler_df.Magnitude == onceki_depremler_df.Magnitude.max() ].iloc[0].Location}** konumunda gözlenmiştir."

    st.markdown( metin)

    onceki_depremler_df = onceki_depremler_df[ onceki_depremler_df["Country"] == "Türkiye"]

    onceki_depremler_df["MagnitudeCircleSize"] = 1_000 * onceki_depremler_df["Magnitude"] 

    st.dataframe( onceki_depremler_df )

    st.map( data = onceki_depremler_df , latitude="Latitude", longitude = "Longitude" , size = "MagnitudeCircleSize")


with tab_analiz :

    tab_zaman , tab_konum = st.tabs( ["Zaman aralığına bağlı" , "Konum bilgisine bağlı"])

    with tab_zaman :
        st.markdown( f"**Analiz Zamanı** : _{dt.datetime.now().strftime('%Y_%m%d-%H:%M:%S')}_")

        col_ilk , col_son = st.columns( 2)
        with col_ilk:
            ilk_gun = st.date_input("İlk gün")

            first = ilk_gun.strftime("%Y-%m-%d") + "%2000:00:00"
        with col_son:
            son_gun = st.date_input("Son gün")

            last = son_gun.strftime("%Y-%m-%d") + "%2023:59:00"

        button_show = st.button( "Depremleri göster")
        #------------------------------------------------------------------------------
        if button_show :
            AFAD_eqe_df = afad_reader( first , last )
            if len( AFAD_eqe_df ) == 0 :
                st.write( "Deprem yok")

            AFAD_eqe_df = AFAD_eqe_df.dropna( subset="Province")
            #AFAD_eqe_df = AFAD_eqe_df.dropna( by="Province")

            # AFAD_eqe_df.to_csv( "AAD-AFAD_Depremler.csv" , index= False)
            try : 
                birlestirilmis_df = pd.concat( [ onceki_depremler_df , AFAD_eqe_df] , axis= 0  )

                birlestirilmis_df = birlestirilmis_df.drop_duplicates( subset="EventID", keep = "last" )

                birlestirilmis_df.to_csv( "AAD-AFAD_Depremler.csv" , index= False)

                # st.dataframe( birlestirilmis_df)
            except Exception as err  :
                st.write("Birleştirme yok")

            metin = f"{ilk_gun} ile {son_gun} zaman aralığında kaydedilmiş **{len( AFAD_eqe_df)}** adet deprem bulunmaktadır. En büyük deprem **{AFAD_eqe_df[ AFAD_eqe_df.Magnitude == AFAD_eqe_df.Magnitude.max() ].iloc[0].Type} {AFAD_eqe_df.Magnitude.max()}**, **{AFAD_eqe_df[ AFAD_eqe_df.Magnitude == AFAD_eqe_df.Magnitude.max() ].iloc[0].Date}** tarihinde **{AFAD_eqe_df[ AFAD_eqe_df.Magnitude == AFAD_eqe_df.Magnitude.max() ].iloc[0].Location}** konumunda gözlenmiştir."

            st.markdown( metin)

            #------------------------------------------------------------------------------

            st.dataframe( AFAD_eqe_df)

            if len (AFAD_eqe_df) != 0 : 
                AFAD_eqe_df["MagnitudeCircleSize"] = 1_000 * AFAD_eqe_df["Magnitude"] 

                st.map( AFAD_eqe_df , latitude = "Latitude" , longitude = "Longitude" , size = "MagnitudeCircleSize")


            # st.map( data = AFAD_eqe_df , latitude="Latitude", longitude = "Longitude" , size = "Magnitude" , color= [0.0, 0.0 , 0.0 , 1.0])
    with tab_konum :
        st.markdown( f"**Analiz Zamanı** : _{dt.datetime.now().strftime('%Y_%m%d-%H:%M:%S')}_")

        iller = onceki_depremler_df["Province"].sort_values().unique()

        st_iller = st.multiselect( "İl seçiniz", iller)

        tick_zaman_analiz = st.checkbox( "Zaman aralığı seç" )

        if tick_zaman_analiz : 
            col_ilk , col_son = st.columns( 2)
            with col_ilk:
                ilk_gun_analiz = st.date_input("İlk gün 1")

                first_analiz = ilk_gun_analiz.strftime("%Y-%m-%d") + "%2000:00:00"
            with col_son:
                son_gun_analiz = st.date_input("Son gün 1")

                last_analiz = son_gun_analiz.strftime("%Y-%m-%d") + "%2023:59:00"

        if st_iller : 
            # onceki_depremler_secili_df = onceki_depremler_df.query(f"Province in {st_iller}")
            if tick_zaman_analiz == False : 
                onceki_depremler_secili_df = onceki_depremler_df[ onceki_depremler_df["Province"].isin( st_iller)]
            else : 
                onceki_depremler_secili_df = onceki_depremler_df[ onceki_depremler_df["Province"].isin( st_iller)]
                #
                onceki_depremler_secili_df = onceki_depremler_secili_df[ (onceki_depremler_secili_df.Date >= ilk_gun_analiz)  &   (onceki_depremler_secili_df.Date <= son_gun_analiz)  ]


            button_show_secili = st.button("Secili konumları göster")

            if button_show_secili :
                st.dataframe( onceki_depremler_secili_df)

                          
                st.map( data = onceki_depremler_secili_df , latitude="Latitude", longitude = "Longitude" , size = "Magnitude")


                st.bar_chart(onceki_depremler_secili_df , x = "Date" , y = "Depth")
                    
# with tab_test : 
#     # center on Liberty Bell, add marker
#     m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
#     folium.Marker(
#         [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
#     ).add_to(m)

#     # call to render Folium map in Streamlit, but don't get any data back
#     # from the map (so that it won't rerun the app when the user interacts)
#     st_folium(m, width=725, returned_objects=[])

# %%
