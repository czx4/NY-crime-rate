# 🗺️ NYC Crime Rate Visualization

An interactive web app built with Python and Dash that visualizes crime complaints across New York City's boroughs using up-to-date public data.
This project fetches data via an open API, processes it with Pandas, and presents it through a responsive choropleth map.

## 📌 Features

- 📍 Choropleth map showing crime intensity by NYC borough
- 📅 Slider to filter reports from the past 5 to 2 months
- 📂 Dropdown to filter by crime category (Felony, Misdemeanor, Violation)
- ⚠️ Note: Reports are published with a ~1-month delay, so the most recent data may be incomplete

## 🛠️ Tech Stack

- Python
- Dash (Plotly)
- Dash Bootstrap Components
- Pandas
- Requests
- GeoJSON

## 📈 Data Source

Data is pulled directly from the [NYC Open Data API](https://data.cityofnewyork.us/), using the endpoint for NYPD Complaint Data: https://data.cityofnewyork.us/resource/5uac-w243.json

## 🚀 How to Run Locally

### 1. Clone the repo

git clone https://github.com/czx4/NY-crime-rate.git

cd NY-crime-rate.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the app
python index.py

Then visit http://127.0.0.1:8052 in your browser.

### 📁 File Structure
NY-crime-rate/

├── boroughs.geojson        # GeoJSON file with NYC borough shapes

├── index.py                  # Main Dash app

├── assets/

│   └── style.css           # Custom styling

├── requirements.txt        # Dependencies

└── README.md               # Project description
