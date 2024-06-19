GeoCluster: Aplikacja do Geokodowania i Klasteryzacji Danych Geograficznych
GeoCluster to aplikacja stworzona w Pythonie z użyciem biblioteki Streamlit, która umożliwia geokodowanie miast oraz klasteryzację punktów geograficznych przy użyciu algorytmu HDBSCAN. Aplikacja jest przydatna do analizy i wizualizacji danych geograficznych, umożliwiając użytkownikom identyfikację skupisk (klastrów) miast na mapie.

Funkcje Aplikacji
Geokodowanie: Używanie OpenCage API do uzyskiwania współrzędnych geograficznych (szerokości i długości geograficznej) dla miast.
Cache Geokodowania: Wykorzystanie mechanizmu cache do przechowywania wyników geokodowania, co przyspiesza działanie aplikacji i zmniejsza liczbę zapytań do API.
Klasteryzacja HDBSCAN: Wykorzystanie algorytmu HDBSCAN do identyfikacji klastrów punktów geograficznych na podstawie ich współrzędnych.
Wizualizacja: Wyświetlanie wyników klasteryzacji oraz wizualizacja klastrów na mapie.
Eksport Danych: Eksport wyników klasteryzacji do plików CSV oraz XLSX.
Używane Biblioteki
pandas
geopy
hdbscan
scikit-learn
numpy
streamlit
requests
diskcache
matplotlib
openpyxl
Instalacja
Aby zainstalować wszystkie wymagane biblioteki, użyj poniższego pliku requirements.txt:

Copy code
pandas
geopy
hdbscan
scikit-learn
numpy
streamlit
requests
diskcache
matplotlib
openpyxl
Możesz zainstalować je za pomocą pip:

sh
Copy code
pip install -r requirements.txt
Uruchomienie Aplikacji
Aby uruchomić aplikację, użyj komendy:

sh
Copy code
streamlit run app.py
Opis Działania
Geokodowanie
Funkcja get_location_by_city odpowiada za geokodowanie miast, korzystając z API OpenCage. Wyniki geokodowania są przechowywane w cache, aby przyspieszyć kolejne zapytania.

Klasteryzacja HDBSCAN
HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) to algorytm klasteryzacji, który identyfikuje skupiska (klastry) punktów na podstawie ich gęstości. W aplikacji, HDBSCAN jest wykorzystywany do klasteryzacji miast na podstawie ich współrzędnych geograficznych.

Parametry HDBSCAN:
min_cluster_size: Minimalna liczba punktów w klastrze. Określa, jak duże muszą być klastry, aby były uznane za istotne.
min_samples: Minimalna liczba próbek wymaganych do utworzenia punktu rdzeniowego (core point). Wpływa na czułość algorytmu na różne gęstości danych.
metric: Metryka używana do obliczania odległości między punktami. W aplikacji używana jest metryka haversine, która uwzględnia krzywiznę Ziemi przy obliczaniu odległości między punktami geograficznymi.
Proces Klasteryzacji
Załaduj Dane: Użytkownik ładuje plik Excel zawierający dane miast.
Geokodowanie: Aplikacja geokoduje miasta i zapisuje wyniki w cache.
Klasteryzacja: Aplikacja stosuje algorytm HDBSCAN do identyfikacji klastrów miast na podstawie ich współrzędnych.
Wizualizacja: Wyniki klasteryzacji są wyświetlane i wizualizowane na mapie.
Eksport Danych: Użytkownik może wyeksportować wyniki klasteryzacji do plików CSV lub XLSX.
Przykład Użycia
Uruchom aplikację za pomocą Streamlit.
Załaduj plik Excel z danymi miast.
Ustaw parametry klasteryzacji (min_cluster_size i min_samples) za pomocą suwaków.
Zobacz wyniki klasteryzacji oraz wizualizację klastrów.
Wyeksportuj wyniki do pliku CSV lub XLSX.
