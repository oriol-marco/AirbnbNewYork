from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import seaborn as sns
sns.set_style("whitegrid")
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static
import json

st.set_page_config(layout="wide", page_title="Airbnb New York City", page_icon="images/airbnb_logo.jpg")
st.set_option('deprecation.showPyplotGlobalUse', False)


@st.cache
def get_data():
    return pd.read_csv("data/New_York_Airbnb.csv")

@st.cache
def get_logo_image():
    return Image.open("images/airbnb_logo.jpg")

def main():

    df = get_data()

    ##################### SIDEBAR #####################

    st.sidebar.image(get_logo_image(), use_column_width=False, width=300)
    st.sidebar.header("Welcome!")

    st.sidebar.markdown(" ")
    st.sidebar.markdown("*Soc estudiant del màster de ciència de dades a la Universitat Oberta de Catalunya*")

    st.sidebar.markdown("**Author**: Oriol Marco")
    st.sidebar.markdown("**Mail**: omarcosan@uoc.edu")

    st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/oriolmarcosanchez)")
    st.sidebar.markdown("- [Github](https://github.com/oriol-marco)")

    st.sidebar.markdown("**Version:** 1.0.0")


    ##################### Introducció #####################

    st.image("images/New-York-City-Brooklyn-Bridge-Panorama-Juergen-Roth-2.jpg", caption=None, width=None, use_column_width='always', clamp=False, channels="RGB", output_format="auto")

    st.title("Airbnb New York City")
    st.markdown('-----------------------------------')

    st.markdown("""A través de les dades d'Airbnb NY i les dades de criminalitat i de la xarxa de metro de la ciutat de Nova York, 
    realitzarem una anàlisi exploratòria i oferirem informació sobre aquestes dades. Per això utilitzarem les dades que podem trobar al lloc web *Kaggle*, 
    les quals contenen les dades de reserves a la web de Airbnb per l'any 2019 i relacionarem aquestes amb les dades de criminalitat per districte de la ciutat 
    i la proximitat dels habitatges a una estació de metro.""")

    st.markdown("A continuació podeu trobar els links que redirigeixen a les dades utilitzades en aquesta anàlisi:")
    st.markdown("- [Airbnb](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data)")
    st.markdown("- [Criminalitat](https://www.kaggle.com/datasets/brunacmendes/nypd-complaint-data-historic-20062019)")
    st.markdown("- [Metro](https://www.kaggle.com/datasets/new-york-state/nys-nyc-transit-subway-entrance-and-exit-data)")

    st.header("Resum de les dades")

    st.markdown("""Airbnb és una plataforma que proporciona i dona l'oportunitat d'enllaçar dos grups de persones: els amfitrions i els clients. Qualsevol persona amb una sala oberta o espai 
    lliure pot proporcionar serveis a Airbnb per a la comunitat global. És una bona manera de proporcionar uns ingressos addicionals amb un esforç mínim. També és una manera fàcil d'anunciar un
    espai disponible, ja que la plataforma té un trànsit molt elevat d'usuaris i una base d'usuaris global per donar-li suport. Airbnb ofereix una manera fàcil de monetitzar l'espai que seria malgastat.""")

    st.markdown("""D'altra banda, tenim els clients amb necessitats molt específiques; alguns d'aquests poden estar buscant un allotjament assequible prop dels llocs d'interés de la ciutat, mentre que uns altres busquen un apartament 
    de luxe al costat del mar. Poden ser grups, famílies o individus locals i estrangers. Després de cada visita, els convidats tenen l'oportunitat de puntuar i deixar els seus comentaris respecte a la seva experiència al llarg de l'estada.
     Intentarem esbrinar què contribueix a la popularitat de la aplicació i realitzar l'estudi de les dades per aconseguir aquest objectiu, veient la relació dels diferents atributs.""")

    st.markdown('-------------------------------------')

    st.header("Airbnb a la ciutat de Nova York: anàlisis de les dades")
    st.markdown("""A continuació es presenten els primers 10 registres de dades d'Airbnb. Aquests registres s'agrupen al llarg de 15 columnes o atributs amb una varietat d'informació com el nom de l'amfitrió, el preu, el tipus d'habitació, 
    el mínim de nits, revisions i revisions per mes, entre d'altres com pot ser la geolocalització.""")

    st.markdown("""Començarem familiaritzant-nos amb els diferents atributs del conjunt de dades, per entendre què representa cada característica. Això és important, perquè una mala comprensió de les característiques podria fer que cometéssim
     errors en l'anàlisi de dades. També intentarem reduir el nombre de columnes que contenen o no contenen informació que pugui utilitzar-se per a respondre a les nostres preguntes.""")

    st.markdown("Per tal de dur a terme el l'anàlisi de les dades, ho farem mitjançant un projecte de visualització de dades, on es podran veure gràfics i taules que ens ajudaran a entendre millor les dades i a respondre a les nostres preguntes.")

    st.dataframe(df.head(10), width=None, height=None)

    st.markdown("Un altre punt sobre les dades, és que permet ordenar el dataframe en fer clic a qualsevol capçalera d'una columna, una manera més flexible d'ordenar les dades per visualitzar-les.")

    ##################### Distribució geogràfica #####################

    st.header("Localització de les reserves d'Airbnb a Nova York")

    st.markdown("Veiem quina és la densitat d'habitatges disponibles segons la seva distribució geogràfica")

    fig = folium.Map([40.7128,-73.9354],zoom_start=10.7)
    HeatMap(df[['latitude','longitude']].dropna(),radius=8,gradient={0.2:'blue',0.4:'purple',0.6:'orange',1.0:'red'}).add_to(fig)

    map_data = st_folium(fig, width=1500, height=500)


    st.markdown("""El primer llistat d'Airbnb a Nova York va ser a Harlem l'any 2008, i el creixement des de llavors ha estat exponencial. A continuació destaquem la distribució geogràfica dels llistats. Inicialment, podem filtrar-los per rang de preus,
     nombre mínim de nits disponibles i nombre de revisions, de manera que s'afegeix més flexibilitat en cercar un lloc.""")
    st.markdown("També podríem filtrar llistant **preu**, **nits mínimes** en una llista o el mínim de **reviews rebudes**.")

    values = st.slider("Price Range ($)", float(df.price.min()), float(df.price.clip(upper=10000.).max()), (400., 1500.))
    min_nights_values = st.slider('Minimum Nights', 0, 30, (1))
    reviews = st.slider('Minimum Reviews', 0, 700, (0))
    st.map(df.query(f"price.between{values} and minimum_nights<={min_nights_values} and number_of_reviews>={reviews}")[["latitude", "longitude"]].dropna(how="any"), zoom=10)

    st.markdown("""En general, el mapa mostra que les ubicacions al centre de la ciutat són més cares, mentre que a les afores els habitatges són més econòmics (un patró que probablement no només existeix a Nova York). A més, el centre de la ciutat
     sembla tenir el seu propi patró.""")

    st.markdown("""Sorprenentment, l'illa de Manhattan té la concentració més alta d'airbnbs amb preu elevat. Alguns també estan dispersos per Brooklyn, degut a l'augment de la popularitat al districte. 
    L'etiqueta de preu més elevada és de 1000 dòlars. Una altra idea probable és que si sabem que una ubicació específica està molt a prop d'un lloc que considerem car, molt probablement tota l'àrea d'arrodoniment serà cara.""")

    st.markdown("""Les ubicacions més valorades també tendeixen a ser les més cares. De nou, el centre de Manhattan i les zones adjacents de Brooklyn reben les puntuacions més altes, amb East Village com a excepció.""")
    st.markdown("""Si analitzem la densitat d'habitatges disponibles, es pot veure que al voltant de Manhattan hi ha molts menys pisos que en comparació amb les àrees adjacents , a més, la majoria dels punts d'interès (Empire State Buildind, Times Square, Central Park))
     es troben en zones "barates", especialment al voltant del districte de Dam Square.""")

    st.markdown("Veiem quina és la distribució dels habitatges segons el districte al qual pertanyen")

    #######################################################################################################################


    ##################### Àrees d'interés #####################

    st.header("Què estàs buscant?")
    st.write(f"Fora de les {df.shape[1]} columnes del dataset principal, es possible que es vulgui veure una part d'aquest dataframe. Per exemple, podem escollir les columnes que volem veure i ordenar-les per preu, nombre de nits, nombre de revisions, etc.")
    st.markdown("_**Nota:** D'una manera més convenient, per filtrar les nostres dades, és possible filtrar-les a través de les següents funcions: **Price**, **Room Type**, **Minimum of Nights**, **District(Neighbourhood)**, **Host Name**, **Reviews**_")
    defaultcols = ["host_name", "price", "minimum_nights", "room_type", "neighbourhood", "number_of_reviews", "distance_to_nearest_subway"]
    cols = st.multiselect('What attributes do you need to view?', df.columns.tolist(), default=defaultcols)
    st.dataframe(df[cols].head(10))

    ##################### Preu #####################

    st.header("Distribució del preu")
    st.markdown("""El preu mitjà d'un Airbnb a Nova York és de 152 dòlars, però aquest preu varia molt en funció de la ubicació, el tipus de llistat i el nombre de nits. Els llistats de Manhattan tenen un preu mitjà de 196 dòlars,
     mentre que els de Brooklyn tenen un preu mitjà de 124 dòlars.""")
    st.markdown("Veiem quina és la distribució del preu")

    values = st.slider("Price range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
    fig = px.histogram(df.query(f"price.between{values}"), 
                        x="price",
                        nbins=20, 
                        title="Price distribution",
                        width=1000, 
                        height=500,
                        color_discrete_sequence=['indianred'],
                        opacity=0.8)
    fig.update_xaxes(title="Price ($)")
    fig.update_yaxes(title="No. of listings")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)

    st.markdown("""Es pot observar que la disposició del preu és molt concentrada al voltant dels 100 dòlars, amb una gran majoria de llistats que tenen un preu inferior a 200 dòlars.""")

    st.markdown("A continuació es mostra la distribució dels preus segons la seva localització")

    data_geo = json.load(open('data/rawData/neighbourhoods.geojson'))


    price_by_neighbourhood = df.groupby("neighbourhood")["price"].mean().reset_index()

    df_price_by_neighbourhood = pd.DataFrame(price_by_neighbourhood)

    #st.table(df_price_by_neighbourhood.sort_values("price", ascending=False).head(10))

    #######################################################################################################################

    add_select = st.selectbox("What type of map do you want to see?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))

    map_ny = folium.Map(location=[40.7128,-73.9354], tiles=add_select, zoom_start=10.5)

    price_values = st.slider("Price range", float(df_price_by_neighbourhood.price.min()), float(df_price_by_neighbourhood.price.clip(upper=400.).max()), (50., 250.))

    folium.Choropleth(geo_data = data_geo,
                    data=df_price_by_neighbourhood.query(f"price.between{values}"),
                    columns=['neighbourhood', 'price'],
                    key_on='feature.properties.neighbourhood',
                    fill_color='YlOrRd',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name='Price ($)',
    ).add_to(map_ny)

    folium_static(map_ny, width=1500, height=500)

    st.markdown("_**Nota:** En aquest cas s'ha realitzat un tall en el preu de la reserva en 400$, ja que el rang de 50 a 400$ inclou el 95% de les reserves fetes a Airbnb_")
    st.markdown("_**Nota:** Els barris colorejats de color negre són barris on no es disposa de les dades._")


    #######################################################################################################################


    ##################### Districtes #####################

    st.header("Distribució del preu per districte")
    st.markdown("""La ciutat de Nova York abasta cinc divisions administratives a nivell de comtat anomenades * boroughs *: ** Bronx **, ** Brooklyn **, ** Manhattan **, ** Queens ** i ** Staten Island **. Cada * borough * coincideix amb
     un comtat respectiu de l'estat de Nova York. Els boroughs de Queens i Bronx són concurrents amb els comtats del mateix nom, mentre que els boroughs de Manhattan, Brooklyn i Staten Island corresponen als de Nova York, Kings i Richmond, respectivament.""")
    st.markdown("Un altre punt important que és possible observar és que el preu mitjà al districte de Manhattan pot ser molt més alt que altres districtes. Manhattan té un preu mitjà pròxim al doble que el del districte del Bronx")

    fig = px.bar(df.groupby("neighbourhood_group")["price"].mean().reset_index(), 
                 x="neighbourhood_group", 
                 y="price", 
                 title="Average price by District",
                 width=1000, 
                 height=500,
                 color_discrete_sequence=['indianred'],
                 opacity=0.8)

    fig.update_xaxes(title="District")
    fig.update_yaxes(title="Average price ($)")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)


    fig = px.histogram(df.query(f"price.between{values}"), 
                        x="price",
                        nbins=20, 
                        title="Price distribution by District",
                        width=1000, 
                        height=600,
                        color="neighbourhood_group",
                        color_discrete_sequence=px.colors.qualitative.T10,
                        marginal="box",
                        opacity=0.8,
                        barmode="overlay")
    fig.update_xaxes(title="Price ($)")
    #fig.update_yaxes(title="No. of listings")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)


    st.markdown("""Veiem quina és la distribució del preu segons els barris. Degut a que hi ha una gran quantitat de barris, només mostrarem els 10 barris més cars i els 10 més barats.""")

    col1, col2 = st.columns(2, gap='small')

    with col1:
        fig = px.bar(df.groupby("neighbourhood").price.mean().sort_values(ascending=True).reset_index().head(10),
                    y="neighbourhood",
                    x="price",
                    color_discrete_sequence=['indianred'],
                    title="Top 10 cheapest neighbourhoods",
                    opacity=0.8,
                    width=700,
                    height=500)
        fig.update_yaxes(title="Neighbourhood")
        fig.update_xaxes(title="Average price ($)")
        fig.update_layout(title_font_size=20)
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(df.groupby("neighbourhood").price.mean().sort_values(ascending=False).reset_index().head(10),
                    y="neighbourhood",
                    x="price",
                    color_discrete_sequence=['indianred'],
                    title="Top 10 most expensive neighbourhoods",
                    opacity=0.8,
                    width=700,
                    height=500)
        fig.update_yaxes(title="Neighbourhood")
        fig.update_xaxes(title="Average price ($)")
        fig.update_layout(title_font_size=20)
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig)

    st.markdown("""El barri més car de Nova York és ** Fort Wadsworth **, amb un preu mitjà de 800 dòlars per dia. En canvi el barri més econòmic és el Bull's Head, amb un preu mitjà de 48 dòlars.""")



    ##################### Disponibilitat #####################

    st.header("Disponibilitat i distribució")
    st.markdown("""L'atribut **availability_365** ens indica el nombre de dies que el llistat està disponible durant l'any. Els valors poden ser de 0 a 365.
     Si el valor és 0, el llistat no està disponible durant l'any. Si el valor és 365, el llistat està disponible durant tot l'any.""")

    neighborhood = st.radio("District", df.neighbourhood_group.unique())
    is_expensive = st.checkbox("Expensive Listings")
    is_expensive = " and price<100" if not is_expensive else ""

    @st.cache
    def get_availability(show_exp, neighborhood):
        return df.query(f"""neighbourhood_group==@neighborhood{is_expensive}\
            and availability_365>0""").availability_365.describe(\
                percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

    st.table(get_availability(is_expensive, neighborhood))
    st.markdown("_**Nota:** Hi ha 18431 registres amb *disponibilitat_365** 0 (zero). En aquest cas els he ignorat._")
    st.markdown("""Amb 156 dies, Manhattan té la mitjana de disponibilitat més baixa. Amb 223, Staten Island té la mitjana de disponibilitat més alta. Si incloem els habitatges més cars (més de 100 dòlars per dia),
     els números són 164 per Brooklyn i 225 per Staten Island.""")

    st.header("Disponibilitat per districte")
    st.markdown("""Veiem quina és la distribució de la disponibilitat segons el districte""")

    fig = px.histogram(df.query(f"availability_365>0{is_expensive}"), 
                        x="availability_365",
                        nbins=20, 
                        title="Availability distribution by District",
                        width=1000, 
                        height=600,
                        color="neighbourhood_group",
                        color_discrete_sequence=px.colors.qualitative.T10,
                        marginal="box",
                        opacity=0.8,
                        barmode="overlay")

    fig.update_xaxes(title="Availability (days)")
    #fig.update_yaxes(title="No. of listings")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)

    st.markdown("""Veiem que la majoria dels llistats tenen una disponibilitat de 0 a 100 dies. Els llistats de Brooklyn tenen una distribució més concentrada que els de Manhattan.""")
    st.markdown("""Si incloem els habitatges més cars (més de 100 dòlars per dia), la distribució és molt similar.""")

    ##################### Estança mínima #####################

    st.header("Estança mínima")
    st.markdown("""L'atribut **minimum_nights** ens indica el nombre mínim de nits que cal reservar per a poder allotjar-se a l'habitatge.""")

    fig = px.box(df.query(f"minimum_nights<15"), 
                x="neighbourhood_group", 
                y="minimum_nights", 
                color="neighbourhood_group", 
                color_discrete_sequence=px.colors.qualitative.T10, 
                title="Minimum nights by District",
                width=1000, 
                height=600)

    fig.update_xaxes(title="District")
    fig.update_yaxes(title="Minimum nights")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)


    st.markdown("_**Nota:** Hi ha 11 registres amb *minimum_nights** 0 (zero). En aquest cas els he ignorat. D'altre banda, s'ha filtrat el dataframe per obtenir només els registres amb una reserva mínima inferior als 15 dies, ja que és el periode habitual de vacances_")
    st.markdown("""Com es pot observar, la mitjana de nits mínimes per reservar a tots els districtes és de 2 nits. En el cas de Manhattan o Brooklyn, s'observa que hi ha força regsitres al voltant de les 3 nits mínimes""")

    ##################### Room types by district #####################

    st.header("Tipus d'habitatge per districte")

    st.markdown("""L'atribut **room_type** ens indica el tipus d'habitació que ofereix l'habitatge.""")
    st.markdown("""Veiem quins són els tipus d'habitació més comuns per a cada districte.""")
    st.markdown("""revisem la relació entre el tipus de propietat i el veïnat. La pregunta principal que pretenem respondre és si els diferents districtes constitueixen diferents tipus de lloguer. Tot i que en el conjunt de dades expandit hi ha més de 20 tipus,
     ens centrarem en el top 4 pel seu recompte total a la ciutat i la comprensió de la seva distribució en cada districte.""")

    room_types_df = df.groupby(['neighbourhood_group', 'room_type']).size().reset_index(name='Quantity')
    room_types_df = room_types_df.rename(columns={'neighbourhood_group': 'District', 'room_type':'Room Type'})
    room_types_df['Percentage'] = room_types_df.groupby(['District'])['Quantity'].apply(lambda x:100 * x / float(x.sum()))

    fig = px.bar(room_types_df,
                x="District",
                y="Percentage",
                color="Room Type",
                color_discrete_sequence=px.colors.qualitative.T10,
                title="Room types by District",
                width=1000,
                height=600)

    fig.update_xaxes(title="District")
    fig.update_yaxes(title="Percentage")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""Podem veure que els llistats de *Private Room* són més alts en nombre en tots els districtes, excepte Manhattan i Staten Island. Staten Island té més propietat d'estil «House» que «Apartments», per tant, probablement els únics
     llistats possibles són els apartaments. Aquesta anàlisi sembla intuïtiu, ja que sabem que Staten Island no és tan densament poblada i té molt espai.""")
    st.markdown("""Els llistats amb més disponibilitat de la tipologia *Entire home/apt* es troben a Manhattan, constituint el 60% de totes les propietats en aquest districte. La següent és Staten Island amb el 47%.""")
    st.markdown("""Queens, Brooklyn i el Bronx també tenen molta disponibilitat pel que fa a *Private Room*. A Queens, el 59% dels apartaments són del tipus *Private Room*, siguent més elevat que al Bronx.""")
    st.markdown("""Els tipus de llistats *Shared Room* també són comuns a Nova York. El Bronx constitueix el 5% del tipus de llistat *Shared Room*, seguit de Queens amb el 3,5% d'aquesta tipologia d'habitatge""")

    ##################### Price Average by Room Type #####################

    st.header("Preu mitjà per tipus d'habitatge")

    st.markdown("""L'atribut **price** ens indica el preu de l'habitatge en dòlars.""")
    st.markdown("""Veiem quin és el preu mitjà per tipus d'habitatge.""")

    avg_price_room = df.groupby("room_type").price.mean().reset_index()\
          .round(2).sort_values("price", ascending=False)\
          .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))

    avg_price_room = avg_price_room.rename(columns={'room_type':'Room Type', 'avg_price': 'Average Price ($)', })

    st.table(avg_price_room)

    st.markdown("Com es pot observar, el preu mitjà per *Entire home/apt* és de 211,79 dòlars, seguit de *Private Room* amb 89,78 dòlars i *Shared Room* amb 70,12 dòlars.")
    st.markdown("""Podem observar que el preu mig per un apartament està molt per sobre del preu mitjà per una habitació privada. Això pot ser degut a que els apartaments són més grans i tenen més espai, per tant, el preu per persona és més baix. I que aquest últims es troben
    amb un preu pròxim al dels hotels.""")

    st.markdown("Veiem quina és la distribució dels preus per tipus d'habitatge i districte.")


    avg_price_district = df.groupby(["neighbourhood_group", "room_type"]).price.mean().reset_index()\
            .round(2).sort_values("price", ascending=True)\
            .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))

    avg_price_district = avg_price_district.rename(columns={'neighbourhood_group':'District', 'room_type':'Room Type', 'avg_price': 'Average Price ($)' })

    fig = px.bar(avg_price_district,
                x="District", 
                y="Average Price ($)", 
                color="Room Type", 
                color_discrete_sequence=px.colors.qualitative.T10, 
                title="Price by Room Type and District", 
                width=1000, 
                height=600)

    fig.update_xaxes(title="District")
    fig.update_yaxes(title="Price ($)")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""El preu mitjà per *Entire home/apt* és més elevat a Manhattan, seguit de Brooklyn i Queens. Bronx té el preu mitjà més baix per aquest tipus d'habitatge.""")
    st.markdown("""El preu mitjà per *Private Room* és més elevat a Manhattan, seguit de Brooklyn i Queens. Staten Island té el preu mitjà més baix per aquest tipus d'habitatge.""")
    st.markdown("""El preu mitjà per *Shared Room* és més elevat a Manhattan, seguit de Brooklyn i Bronx. Staten Island té el preu mitjà més baix per aquest tipus d'habitatge.""")

    fig = px.strip(df,
                x="room_type",
                y="reviews_per_month",
                color="neighbourhood_group",
                facet_row_spacing=0.1,
                color_discrete_sequence=px.colors.qualitative.T10,
                title="Reviews per Month by Room Type and District",
                width=1000,
                height=600)

    fig.update_xaxes(title="Room Type")
    fig.update_yaxes(title="Reviews per Month")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""Els apartaments *Entire home/apt* tenen més valoracions per mes a Manhattan, seguit de Brooklyn i Queens. Bronx té el menor nombre de valoracions per mes per aquest tipus d'habitatge.""")
    st.markdown("""Les habitacions privades *Private Room* tenen més valoracions per mes a Queens, seguit de Manhattan i Brooklyn. Bronx té el menor nombre de valoracions per mes per aquest tipus d'habitatge.""")
    st.markdown("""Les habitacions compartides *Shared Room* tenen més valoracions per mes a Manhattan, seguit de Brooklyn i Bronx. Staten Island té el menor nombre de valoracions per mes per aquest tipus d'habitatge.""")
    st.markdown(""".""")


    ##################### Most Rated Hosts #####################

    st.header("Els millors amfitrions")

    st.markdown("""L'atribut **host_name** ens indica el nom de l'amfitrió.""")
    st.markdown("""Veiem quins són els amfitrions amb més valoracions.""")

    top_hosts = df.groupby("host_name").number_of_reviews.count().reset_index()\
            .sort_values("number_of_reviews", ascending=False)\
            .assign(count=lambda x: x.pop("number_of_reviews").apply(lambda y: "%.0f" % y))

    top_hosts = top_hosts.rename(columns={'host_id': 'Host Id', 'host_name':'Host Name', 'count': 'Number of Reviews', })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.table(top_hosts.head(10))


    with col2:
        fig = px.bar(df.groupby("host_name").number_of_reviews.count().sort_values(ascending=False).reset_index().head(5),
                x="host_name", 
                y="number_of_reviews",
                color_discrete_sequence=['indianred'], 
                title="Top 5 Hosts", 
                width=800, 
                height=600)

        fig.update_xaxes(title="Host Name")
        fig.update_yaxes(title="Number of Reviews")
        fig.update_layout(title_font_size=20)
        fig.update_layout(title_x=0.45)
        #fig.update_layout(barmode='group')
        st.plotly_chart(fig)

    ##################### Subway Station distance #####################

    st.header("Distància a la estació de metro més propera")

    st.markdown("""L'atribut **neighbourhood_group** ens indica el districte on es troba l'habitatge.""")
    st.markdown("""Veiem quina és la distància mitjana a la estació de metro més propera segons el districte on està localitzat l'habitatge.""")

    avg_distance = df.groupby("neighbourhood_group")["distance_to_nearest_subway"].mean().reset_index()\
            .round(2).sort_values("distance_to_nearest_subway", ascending=True)\
            .assign(avg_distance=lambda x: x.pop("distance_to_nearest_subway").apply(lambda y: "%.2f" % y))

    avg_distance = avg_distance.rename(columns={'neighbourhood_group':'District', 'avg_distance': 'Average Distance (km)' })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.table(avg_distance)

    with col2:    

        fig = px.bar(avg_distance,
                    x="District", 
                    y="Average Distance (km)", 
                    color_discrete_sequence=['indianred'], 
                    title="Average Distance to Subway Station by District", 
                    width=700, 
                    height=400)

        fig.update_xaxes(title="District")
        fig.update_yaxes(title="Distance (km)")
        fig.update_layout(title_font_size=20)
        fig.update_layout(title_x=0.45)
        #fig.update_layout(barmode='group')
        st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""La distància mitjana a la estació de metro més propera és més elevada a Staten Island, seguit de Queens i Bronx. Manhattan té la distància mitjana més baixa, próxima a 100 metres. Això té tot
     el sentit, ja que Manhattan és el districte més petit i el que té més estacions de metro.""")

    avg_distance = df.groupby(["neighbourhood_group", "neighbourhood" ])["distance_to_nearest_subway"].mean().reset_index()\
            .round(2).sort_values("distance_to_nearest_subway", ascending=True)\
            .assign(avg_distance=lambda x: x.pop("distance_to_nearest_subway").apply(lambda y: "%.2f" % y))

    avg_distance = avg_distance.rename(columns={'neighbourhood':'Neighbourhood', 'avg_distance': 'Average Distance (km)' })

    fig = px.bar(avg_distance,
                x="Neighbourhood", 
                y="Average Distance (km)",
                color = "neighbourhood_group", 
                color_discrete_sequence=px.colors.qualitative.T10, 
                title="Average Distance to Subway Station by District and Neightbourhood", 
                width=1500, 
                height=600)

    fig.update_xaxes(title="Neighbourhood")
    fig.update_yaxes(title="Distance (km)")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""Tal i com hem pogut observar amb el gràfic anterior, tots els habitatges dins del districte de Manhattan es troben a menys de 300m d'una estació de metro. En canvi, a mesura que ens allunyem del centre de la ciutat,
     la distància a la estació de metro més propera augmenta fins arribar als 14 km dins del districte de Sataten Island.""")
    st.markdown("""El cas de Staten Island és un cas particular, dins de la ciutat de Nova York, ja que es troba localitzat a l'altre banda del riu Hudson, cosa que impossibilita la construcció d'una xarxa extensa de metro.
     En aquest cas, per anar al centre de la ciutat, tenim altres opcions de transport, com són els ferris o el tren.""")
    st.markdown("""Aquesta informació ens pot ser útil per a decidir on allotjar-nos. Si volem estar a prop de la ciutat, Manhattan és la millor opció. Si volem estar a prop de la natura, Brooklyn és la millor opció.
     Si volem estar a prop de la platja, Staten Island és la millor opció.""")

    st.markdown("Veiem quina relació hi ha entre la distància a la estació de metro més propera i el preu de l'habitatge.")

    values = st.slider("Distance to Subway Station (km)", float(df.distance_to_nearest_subway.min()), float(df.distance_to_nearest_subway.clip(upper=15.).max()), (0.1, 3.))

    fig = px.scatter(df.query(f"distance_to_nearest_subway>={values[0]} & distance_to_nearest_subway<={values[1]}"), 
                    x="distance_to_nearest_subway", 
                    y="price", 
                    color="neighbourhood_group", 
                    color_discrete_sequence=px.colors.qualitative.T10, 
                    title="Price vs Distance to Subway Station", 
                    width=1500, 
                    height=600)

    fig.update_xaxes(title="Distance (km)")
    fig.update_yaxes(title="Price ($)")
    fig.update_layout(title_font_size=20)
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""El preu de l'habitatge és més elevat a prop de les estacions de metro. Això té tot el sentit, ja que a prop de les estacions de metro hi ha més activitat, i per tant, hi ha més demanda d'habitatges.""")
    st.markdown("""A mesura que ens allunyem de les estacions de metro, el preu de l'habitatge disminueix. Això també té tot el sentit, ja que a mesura que ens allunyem de les estacions de metro, la demanda d'habitatges disminueix.""")
    st.markdown("""Aquesta informació ens pot ser útil per a decidir on allotjar-nos. Si volem estar a prop de la ciutat, Manhattan és la millor opció. Si volem estar a prop de la natura, Brooklyn és la millor opció.
     Si volem estar a prop de la platja, Staten Island és la millor opció.""")

    st.markdown("Veiem la distribució dels habitatges segons la seva distància a la estació de metro més propera.")

    ################################################################################################################

    distance_to_subway = df.groupby("neighbourhood")["distance_to_nearest_subway"].mean().reset_index()

    df_distance_by_neighbourhood = pd.DataFrame(distance_to_subway)

    map_nyork = folium.Map(location=[40.7128,-73.9354], tiles=add_select, zoom_start=10.5)

    distance_values = st.slider("Distance range", float(df_distance_by_neighbourhood.distance_to_nearest_subway.min()), float(df_distance_by_neighbourhood.distance_to_nearest_subway.clip(upper=5.).max()), (0., 1.))

    folium.Choropleth(geo_data = data_geo,
                    data=df_distance_by_neighbourhood.query(f"distance_to_nearest_subway.between{distance_values}"),
                    columns=['neighbourhood', 'distance_to_nearest_subway'],
                    key_on='feature.properties.neighbourhood',
                    fill_color='YlOrRd',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name='Distance (km)',
    ).add_to(map_nyork)

    folium_static(map_nyork, width=1500, height=500)

    st.markdown("_**Nota:** En aquest cas s'ha realitzat un tall en la distància a l'estació de metro més propera en 5 km_. Les distàncies predeterminades són dins del rang  de 0 a 1 km._")
    st.markdown("_**Nota:** Els barris colorejats de color negre són barris on no es disposa de les dades, o bé están fora de rang mostrat al mapa._")

    ################################################################################################################

    ##############################Criminality Index#######################################

    st.header("Índex de criminalitat")

    st.markdown("Veiem quina és la distribució de la criminalitat per districte.")

    df_criminality = df[["neighbourhood_group", "crimes"]]
    df_criminality = df_criminality.drop_duplicates(subset = "crimes").sort_values(by = "crimes", ascending = False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.table(df_criminality)

    with col2:

        fig = px.bar(df_criminality,
                    x="neighbourhood_group",
                    y="crimes",
                    color_discrete_sequence=['indianred'],
                    title="Total crimes by District",
                    width=700,
                    height=400)

        fig.update_xaxes(title="District")
        fig.update_yaxes(title="Total crimes by District")
        fig.update_layout(title_font_size=20)
        fig.update_layout(title_x=0.45)
        st.plotly_chart(fig)

    st.markdown("Algunes observacions clau del gràfic són:")
    st.markdown("""El districte de Brooklyn és el que té més criminalitat, seguit de Manhattan. Això té sentit, ja que en aquest cas no es distingeiex entre la tipologia del crim. En aquest sentit, Brooklyn i Manhattan són
     son els dos districtes amb més població i més afluència de turistes, i per tant, més activitat.""")
    st.markdown("""Per poder fer un estudi en profunditat i poder relacionar l'índex de criminalitat amb el preu dels habitatges, hauríem de discernir entre la tipologia de crims, ja que no és el mateix un assessinat que un robatori del telèfon.
     S'hauria de fer un estudi de criminalitat per cada tipologia de crim.""")

    st.markdown("Conclusions")

    st.markdown("A través d'aquest projecte d'anàlisi i visualització de dades exploratòries, vam obtenir diverses idees interessants sobre el mercat de lloguer d'Airbnb. A continuació resumirem les respostes a les preguntes que volíem respondre al començament del projecte:")

    st.markdown("*Com varien els preus dels llistats segons la ubicació? Quines localitats de NYC tenen una alta valoració per part dels convidats? Els preus són més alts per als lloguers més propers als punts calents de la ciutat o bé més propers a les estacions de metro?. Els lloguers que estan molt valorats a la ubicació per l'amfitrió també tenen preus més alts")

    st.markdown("*Està correlacionada la demanda i els preus dels lloguers?* Els preus mitjans dels lloguers augmenten al llarg de l'any, el que es correlaciona amb la demanda.")

    st.markdown("""Hi una relació directa del preu del lloguer amb l'índex de criminalitat del districte? En aquest sentit, el preu del lloguer no està directament relacionat amb l'índex
     de criminalitat del districte, ja que el preu del lloguer és més alt en els districtes amb més criminalitat. Això és normal ja que en aquest cas, hem comptabilitzat el total dels crims
      comesos, sense tenir en compte la tipologia d'aquests crims.""")

    st.header("Limitacions")

    st.markdown(" - No teníem dades durant els últims anys i per tant no podíem comparar les tendències de lloguer actuals amb les tendències passades.")

    st.markdown(" Per sota de les dades utilitzades en aquesta investigació està disponible per a la investigació reproduïble.")


    st.markdown('-----------------------------------------------------')
    st.text('Developed by Oriol Marco - 01/2023')
    st.text('Mail: oriolmarcosan@gmail.com')




    st.markdown("## Good Journey to New York!!!")
    st.write("Yeaah! Ja tens el millor viatge a Nova York. Clicka a sota per celebrar-ho.")
    btn = st.button("Celebra-ho!")
    if btn:
        st.balloons()

if __name__ == '__main__':
    main()