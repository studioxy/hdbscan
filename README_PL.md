
# GeoCluster: Aplikacja do Geokodowania i Klasteryzacji Danych Geograficznych

GeoCluster to aplikacja stworzona w Pythonie z użyciem biblioteki Streamlit, która umożliwia geokodowanie miast oraz klasteryzację punktów geograficznych przy użyciu algorytmu HDBSCAN. Aplikacja jest przydatna do analizy i wizualizacji danych geograficznych, umożliwiając użytkownikom identyfikację skupisk (klastrów) miast na mapie.

## Funkcje

1. **Geokodowanie**: Używanie OpenCage API do uzyskiwania współrzędnych geograficznych (szerokości i długości geograficznej) dla miast.
2. **Cache Geokodowania**: Wykorzystanie mechanizmu cache do przechowywania wyników geokodowania, co przyspiesza działanie aplikacji i zmniejsza liczbę zapytań do API.
3. **Klasteryzacja HDBSCAN**: Wykorzystanie algorytmu HDBSCAN do identyfikacji klastrów punktów geograficznych na podstawie ich współrzędnych.
4. **Wizualizacja**: Wyświetlanie wyników klasteryzacji oraz wizualizacja klastrów na mapie.
5. **Eksport Danych**: Eksport wyników klasteryzacji do plików CSV oraz XLSX.

## Używane Biblioteki

- pandas
- geopy
- hdbscan
- scikit-learn
- numpy
- streamlit
- requests
- diskcache
- matplotlib
- openpyxl

## Instalacja

Aby zainstalować wszystkie wymagane biblioteki, użyj poniższego `requirements.txt`:

```
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
```

Możesz zainstalować je za pomocą pip:

```sh
pip install -r requirements.txt
```

## Uruchomienie Aplikacji

Aby uruchomić aplikację, użyj poniższej komendy:

```sh
streamlit run app.py
```

## Jak To Działa

### Geokodowanie

Funkcja `get_location_by_city` odpowiada za geokodowanie miast, korzystając z API OpenCage. Wyniki geokodowania są przechowywane w cache, aby przyspieszyć kolejne zapytania.

### Klasteryzacja HDBSCAN

HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) to algorytm klasteryzacji, który identyfikuje klastry punktów na podstawie ich gęstości. W aplikacji, HDBSCAN jest wykorzystywany do klasteryzacji miast na podstawie ich współrzędnych geograficznych.

#### Parametry HDBSCAN:

- `min_cluster_size`: Minimalna liczba punktów w klastrze. Określa, jak duże muszą być klastry, aby były uznane za istotne.
- `min_samples`: Minimalna liczba próbek wymaganych do utworzenia punktu rdzeniowego (core point). Wpływa na czułość algorytmu na różne gęstości danych.
- `metric`: Metryka używana do obliczania odległości między punktami. W aplikacji używana jest metryka `haversine`, która uwzględnia krzywiznę Ziemi przy obliczaniu odległości między punktami geograficznymi.

### Proces Klasteryzacji

1. **Załaduj Dane**: Użytkownik ładuje plik Excel zawierający dane miast.
2. **Geokodowanie**: Aplikacja geokoduje miasta i zapisuje wyniki w cache.
3. **Klasteryzacja**: Aplikacja stosuje algorytm HDBSCAN do identyfikacji klastrów miast na podstawie ich współrzędnych.
4. **Wizualizacja**: Wyniki klasteryzacji są wyświetlane i wizualizowane na mapie.
5. **Eksport Danych**: Użytkownik może wyeksportować wyniki klasteryzacji do plików CSV lub XLSX.

### Przykład Użycia

1. Uruchom aplikację za pomocą Streamlit.
2. Załaduj plik Excel z danymi miast.
3. Ustaw parametry klasteryzacji (`min_cluster_size` i `min_samples`) za pomocą suwaków.
4. Zobacz wyniki klasteryzacji oraz wizualizację klastrów.
5. Wyeksportuj wyniki do pliku CSV lub XLSX.

## Algorytm HDBSCAN

HDBSCAN to zaawansowany algorytm klasteryzacji, który rozwija algorytm DBSCAN, przekształcając go w algorytm klasteryzacji hierarchicznej, a następnie używając techniki do wyodrębniania płaskiej klasteryzacji na podstawie stabilności klastrów. Kluczową zaletą HDBSCAN jest jego zdolność do znajdowania klastrów o różnej gęstości, co sprawia, że jest bardziej odporny na rzeczywiste dane, gdzie gęstości klastrów nie są jednorodne.

## Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik LICENSE, aby uzyskać szczegóły.
