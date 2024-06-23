import pandas as pd
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut
import hdbscan
from sklearn.metrics import pairwise_distances
import numpy as np
import streamlit as st
import time
import requests
import diskcache as dc
import logging
import folium

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = '8b8372e874b5486cbf75316d0cacab81'
CACHE_DIR = 'geocode_cache'

geolocator = OpenCage(api_key=API_KEY)
cache = dc.Cache(CACHE_DIR)

def get_cached_location(city_name, country=None, postal_code=None):
    key = f"{city_name},{country or ''},{postal_code or ''}"
    if key in cache:
        logger.info(f"Znaleziono w cache: {key}")
        return cache[key]
    else:
        logger.info(f"Nie znaleziono w cache: {key}")
    return None

def check_geocode_api_status():
    url = f"https://api.opencagedata.com/geocode/v1/json?q=London&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 402:
        logger.error("Limit API geokodowania osiągnięty lub wymagana płatność. Sprawdź klucz API lub status konta.")
        st.error("Limit API geokodowania osiągnięty lub wymagana płatność. Sprawdź klucz API lub status konta.")
        return False
    elif response.status_code != 200:
        logger.error(f"Błąd API geokodowania: {response.status_code} - {response.text}")
        st.error(f"Błąd API geokodowania: {response.status_code} - {response.text}")
        return False
    return True

def get_location_by_city(city_name, country=None, postal_code=None, retries=3, delay=5):
    if not check_geocode_api_status():
        return pd.Series([np.nan, np.nan, 'API Error'], index=['Lat', 'Lon', 'Source'])

    cached_location = get_cached_location(city_name, country, postal_code)
    if cached_location is not None:
        logger.info(f"Geokodowanie adresu: {city_name}, {postal_code or ''}, {country or ''} - użyto cache")
        return pd.Series([cached_location[0], cached_location[1], 'Cache'], index=['Lat', 'Lon', 'Source'])

    address = f"{city_name}, {postal_code or ''}, {country or ''}".strip(", ")
    for attempt in range(retries):
        try:
            location = geolocator.geocode(address)
            if location:
                logger.info(f"Geokodowanie adresu: {address} - użyto API")
                key = f"{city_name},{country or ''},{postal_code or ''}"
                cache[key] = (location.latitude, location.longitude)
                return pd.Series([location.latitude, location.longitude, 'API'], index=['Lat', 'Lon', 'Source'])
            else:
                logger.warning(f"Geokodowanie adresu: {address} - nie znaleziono")
                return pd.Series([np.nan, np.nan, 'Not Found'], index=['Lat', 'Lon', 'Source'])
        except (GeocoderUnavailable, GeocoderTimedOut) as e:
            logger.warning(f"Próba {attempt + 1} nie powiodła się dla {city_name} z błędem: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"Nie udało się geokodować miasta: {city_name} po {retries} próbach. Błąd: {str(e)}")
                return pd.Series([np.nan, np.nan, 'Error'], index=['Lat', 'Lon', 'Source'])
        except Exception as e:
            logger.error(f"Nieoczekiwany błąd podczas geokodowania: {str(e)}")
            return pd.Series([np.nan, np.nan, 'Error'], index=['Lat', 'Lon', 'Source'])

def load_data(data):
    try:
        df = pd.read_excel(data)
        logger.info("Kolumny w załadowanym pliku: %s", df.columns.tolist())
        st.write("Kolumny w załadowanym pliku:", df.columns.tolist())

        if 'city' not in df.columns:
            logger.error("Brakuje wymaganej kolumny 'city' w załadowanym pliku.")
            st.error("Brakuje wymaganej kolumny 'city' w załadowanym pliku.")
            return None

        if 'country' not in df.columns:
            logger.warning("Brakuje kolumny 'country'. Ustawiamy na None.")
            st.warning("Brakuje kolumny 'country'. Ustawiamy na None.")
            df['country'] = None
        if 'postal_code' not in df.columns:
            logger.warning("Brakuje kolumny 'postal_code'. Ustawiamy na None.")
            st.warning("Brakuje kolumny 'postal_code'. Ustawiamy na None.")
            df['postal_code'] = None

        # Progress bar for geocoding
        progress_bar = st.progress(0)
        total_locations = len(df)
        processed_locations = 0

        location_placeholder = st.empty()

        def geocode_and_update_progress(row):
            nonlocal processed_locations
            location_placeholder.text(f"Processing {processed_locations + 1}/{total_locations}: {row['city']}")
            location = get_location_by_city(row['city'], row['country'], row['postal_code'])
            processed_locations += 1
            progress_bar.progress(processed_locations / total_locations)
            return location

        with st.spinner('Geocoding locations...'):
            df[['Lat', 'Lon', 'Source']] = df.apply(geocode_and_update_progress, axis=1)

        logger.info("Dane zostały załadowane i przetworzone pomyślnie.")
        location_placeholder.text("Geocoding complete.")
        return df
    except Exception as e:
        logger.error(f"Błąd podczas ładowania danych: {str(e)}")
        st.error(f"Błąd podczas ładowania danych: {str(e)}")
        return None

def calculate_centroids(df):
    centroids = df.groupby('Cluster')[['Lat', 'Lon']].mean().rename(columns={'Lat': 'Centroid_Lat', 'Lon': 'Centroid_Lon'})
    logger.info("Centroidy zostały obliczone.")
    return centroids

def calculate_distances(df, centroids):
    coords = df[['Lat', 'Lon']].values
    centroid_coords = centroids.loc[df['Cluster']].values
    df['Odległość od Centroidu (km)'] = np.diag(pairwise_distances(np.radians(coords), np.radians(centroid_coords))) * 6371.0088
    logger.info("Odległości od centroidów zostały obliczone.")
    return df

def cluster_data(df, min_cluster_size, min_samples):
    df = df.dropna(subset=['Lat', 'Lon'])

    coords = df[['Lat', 'Lon']].values
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric='haversine')
    df['Cluster'] = clusterer.fit_predict(np.radians(coords))
    centroids = calculate_centroids(df)
    df = df.join(centroids, on='Cluster')
    df = calculate_distances(df, centroids)
    logger.info("Dane zostały sklasteryzowane.")
    return df

def validate_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error("Brakuje następujących wymaganych kolumn: %s", ', '.join(missing_columns))
        st.error(f"Brakuje następujących wymaganych kolumn: {', '.join(missing_columns)}")
        return False
    return True

def plot_cluster_on_map(cluster, cluster_num):
    map_cluster = folium.Map(location=[cluster['Lat'].mean(), cluster['Lon'].mean()], zoom_start=6)
    for idx, row in cluster.iterrows():
        folium.Marker([row['Lat'], row['Lon']], popup=row['city']).add_to(map_cluster)
    return map_cluster

def max_distance_in_cluster(cluster):
    if len(cluster) < 2:
        return 0
    coords = cluster[['Lat', 'Lon']].values
    distances = pairwise_distances(np.radians(coords), metric='haversine') * 6371.0088
    return distances.max()

# Funkcja czyszcząca plik cache
def clear_cache():
    cache.clear()
    logger.info("Plik cache został wyczyszczony.")
    st.write("Plik cache został wyczyszczony.")

# Przycisk do wyczyszczenia pliku cache
if st.button('Wyczyść cache'):
    clear_cache()

# Załaduj dane
uploaded_file = st.file_uploader("Wybierz plik")
if uploaded_file is not None:
    # Clear the session state if a new file is uploaded
    if 'last_uploaded_file' not in st.session_state or st.session_state.last_uploaded_file != uploaded_file:
        st.session_state.last_uploaded_file = uploaded_file
        st.session_state.df = load_data(uploaded_file)

    df = st.session_state.df
    if df is not None:
        min_cluster_size = st.slider('Minimalna liczba punktów w klastrze', min_value=2, max_value=100, value=5, step=1)
        min_samples = st.slider('Minimalna liczba próbek', min_value=1, max_value=100, value=5, step=1)
        df = cluster_data(df, min_cluster_size, min_samples)

        required_columns = ['Cluster', 'city', 'Lat', 'Lon', 'Odległość od Centroidu (km)', 'Centroid_Lat', 'Centroid_Lon', 'Source']
        if 'cntr' in df.columns:
            required_columns.append('cntr')
        if 'val' in df.columns:
            required_columns.append('val')

        if validate_columns(df, required_columns):
            clusters = df[df['Cluster'] != -1]
            non_clusters = df[df['Cluster'] == -1]

            num_locations = len(df)
            num_clusters = clusters['Cluster'].nunique()
            num_clustered_locations = len(clusters)
            num_non_clustered_locations = len(non_clusters)

            summary_data = {
                "Total Locations": [num_locations],
                "Clustered Locations": [num_clustered_locations],
                "Non-Clustered Locations": [num_non_clustered_locations],
                "Number of Clusters": [num_clusters]
            }

            summary_df = pd.DataFrame(summary_data)

            st.write("Podsumowanie:")
            st.table(summary_df)

            for cluster_num in clusters['Cluster'].unique():
                cluster = clusters[clusters['Cluster'] == cluster_num]
                st.write(f"Miasta w klastrze {cluster_num}:")

                col1, col2 = st.columns([2, 1])
                
                with col1:
                    cluster_columns = ['city', 'Lat', 'Lon', 'Odległość od Centroidu (km)', 'Centroid_Lat', 'Centroid_Lon', 'Source']
                    if 'cntr' in cluster.columns:
                        cluster_columns.append('cntr')
                    if 'val' in cluster.columns:
                        cluster_columns.append('val')
                    st.table(cluster[cluster_columns])
                    if 'val' in cluster.columns:
                        cluster_sum = cluster['val'].sum()
                        st.write(f"Suma 'val' dla klastra {cluster_num}: {cluster_sum}")

                with col2:
                    map_cluster = plot_cluster_on_map(cluster, cluster_num)
                    st_folium(map_cluster, width=700, height=500)

                # Add feedback on the shape of the cluster
                st.write(f"Cluster {cluster_num} - Number of points: {len(cluster)}")
                max_dist = max_distance_in_cluster(cluster)
                st.write(f"Maximum distance between points in cluster {cluster_num}: {max_dist:.2f} km")

            st.write('Skla steryzowane Miasta:')
            st.table(clusters[required_columns])

            st.write('Nieskla steryzowane Miasta:')
            st.table(non_clusters[['city', 'Lat', 'Lon', 'Source']])

            df_copy = clusters[required_columns]
            if st.button('Skopiuj tabelę do schowka'):
                df_copy.to_clipboard(index=False)
                st.success('Tabela została skopiowana do schowka')

            if st.button('Eksportuj do CSV'):
                df_copy.to_csv('wyniki_klastrowania.csv', index=False)
                st.success('Wyniki zostały wyeksportowane do wyniki_klastrowania.csv')

            if st.button('Eksportuj do XLSX'):
                with pd.ExcelWriter('wyniki_klastrowania.xlsx') as writer:
                    df_copy.to_excel(writer, sheet_name='Skla steryzowane Miasta', index=False)
                    for cluster_num in clusters['Cluster'].unique():
                        cluster[cluster_columns].to_excel(writer, sheet_name=f'Klastra {cluster_num}', index=False)
                st.success('Wyniki zostały wyeksportowane do wyniki_klastrowania.xlsx')
