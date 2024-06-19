
# GeoCluster: Geocoding and Geographical Data Clustering Application

GeoCluster is a Python application built using the Streamlit library that enables geocoding of cities and clustering of geographical points using the HDBSCAN algorithm. The application is useful for analyzing and visualizing geographical data, allowing users to identify clusters of cities on a map.

## Features

1. **Geocoding**: Use OpenCage API to obtain geographical coordinates (latitude and longitude) for cities.
2. **Geocoding Cache**: Use a cache mechanism to store geocoding results, speeding up the application and reducing the number of API requests.
3. **HDBSCAN Clustering**: Use the HDBSCAN algorithm to identify clusters of geographical points based on their coordinates.
4. **Visualization**: Display clustering results and visualize clusters on a map.
5. **Data Export**: Export clustering results to CSV and XLSX files.

## Libraries Used

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

## Installation

To install all required libraries, use the following `requirements.txt`:

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

Install them using pip:

```sh
pip install -r requirements.txt
```

## Running the Application

To run the application, use the following command:

```sh
streamlit run app.py
```

## How It Works

### Geocoding

The `get_location_by_city` function is responsible for geocoding cities using the OpenCage API. Geocoding results are stored in a cache to speed up subsequent requests.

### HDBSCAN Clustering

HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) is a clustering algorithm that identifies clusters of points based on their density. In the application, HDBSCAN is used to cluster cities based on their geographical coordinates.

#### HDBSCAN Parameters:

- `min_cluster_size`: The minimum number of points in a cluster. Determines how large clusters need to be to be considered significant.
- `min_samples`: The minimum number of samples required to form a core point. Influences the algorithm's sensitivity to different data densities.
- `metric`: The metric used to calculate the distance between points. The application uses the `haversine` metric, which accounts for the Earth's curvature when calculating distances between geographical points.

### Clustering Process

1. **Load Data**: The user uploads an Excel file containing city data.
2. **Geocoding**: The application geocodes the cities and saves the results in the cache.
3. **Clustering**: The application applies the HDBSCAN algorithm to identify clusters of cities based on their coordinates.
4. **Visualization**: Clustering results are displayed and clusters are visualized on a map.
5. **Data Export**: The user can export the clustering results to CSV or XLSX files.

### Example Usage

1. Run the application using Streamlit.
2. Upload an Excel file with city data.
3. Adjust the clustering parameters (`min_cluster_size` and `min_samples`) using the sliders.
4. View the clustering results and cluster visualization.
5. Export the results to a CSV or XLSX file.

## HDBSCAN Algorithm

HDBSCAN is an advanced clustering algorithm that builds on the DBSCAN algorithm by converting it into a hierarchical clustering algorithm and then using a technique to extract a flat clustering based on the stability of clusters. The key advantage of HDBSCAN is its ability to find clusters of varying densities, making it more robust for real-world data where cluster densities are not uniform.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
