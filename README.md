# Geo Profile Generator
[![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?logo=vsc&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/Markdown-%23000000.svg?logo=markdown&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This Python Jupyter Notebook generates a dataset of fictional individuals with realistic German attributes and visualizes their geographical distribution on an interactive map.

![Screenshot 2025-03-13 at 11 57 15](https://github.com/user-attachments/assets/1048d74c-7a78-4fb9-8ed1-17e9ea1fc69f)

![Screenshot 2025-03-13 at 11 58 08](https://github.com/user-attachments/assets/fa500d65-c2a9-4d5b-9b69-e1f871f006b7)

## Features
- **Profile Attributes**:
  - Unique ID (UUID)
  - Salutation (Herr/Frau)
  - First and last names (common German names)
  - Address (street, city, ZIP code)
  - Telephone number and email address (with German providers)
  - Geographical coordinates (latitude/longitude)
  - Date of birth (1940–2020)
  - Purchase details (price, quantity, sales tax, purchase type, total amount)

- **Data Generation**:
  - Generates profiles for German cities with realistic ZIP code prefixes.
  - Progress updates printed at 10% intervals during generation.
  - Optimized with list comprehension for large datasets.

- **Output Options**:
  - Saves data to Excel (`.xlsx`) and CSV (`.csv`) files.
  - Saves an interactive HTML map with gender-filtered markers.

- **Map Visualization**:
  - Clusters markers by gender ("Herr" in blue, "Frau" in pink) with toggleable layers.
  - Detailed popups showing ID, name, address, email, phone, birthday, purchase type, quantity (Stuckzahl), sales tax, and total amount.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/geo-profile-generator.git
   cd german-profile-generator

2. Set Up a Virtual Environment (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Dependencies
faker - For generating realistic random data
pandas - For managing and exporting the dataset
folium - For interactive map visualization
openpyxl - For Excel file export

Install them manually if you don’t use a requirements.txt:
```
pip install faker pandas folium openpyxl
```

## Usage
Run the script with default settings (1000 profiles, Excel/CSV export, map generation):
```bash
python script.py
```

Customize the number of profiles and output options (for example 500 profiles):
```python
from script import main
# Generate 500 profiles, save to Excel and CSV, and create a map
df = main(num_profiles=500, save_excel=True, save_csv=True, create_map=True)
```

## Output Files
- random_data_500.xlsx - Excel file with all profiles
- random_data_500.csv - CSV file with all profiles
- geo_profiles_map.html - Interactive map file (open in a browser)

## Example Map
The map features:
- Blue markers for "Herr" (males) with fa-male icons.
- Pink markers for "Frau" (females) with fa-female icons.
- Layer control to toggle gender visibility.
- Popups with detailed profile information.

Sample Popup
```text
Herr Lukas Müller
ID: 12345678...
Address: Hauptstraße 12, 10123 Berlin
Email: lukas.müller123@gmx.de
Phone: +491234567890
Birthday: 1985-06-15
Purchase: Hose
Quantity (Stuckzahl): 5
Sales Tax: 19%
Total: €123.45
```

## Contributing
Contributions are welcome! 


## License
This project is licensed under the MIT License - see the LICENSE file for details.
