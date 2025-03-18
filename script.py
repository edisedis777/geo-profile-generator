#!/usr/bin/env python3
"""
Geo Profile Generator CLI

This script generates realistic fictional profiles with geographical data.
It offers command-line options to customize the output and can export to CSV, Excel, or JSON.
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
from faker import Faker
import openpyxl

# Try to import optional dependencies
try:
    import folium
    from folium.plugins import MarkerCluster
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False


class GeoProfileGenerator:
    """Generator for fictional profiles with geographical data."""

    def __init__(self, locale: str = "de_DE", seed: Optional[int] = None):
        """
        Initialize the generator with specified locale and seed.
        
        Args:
            locale: Locale for generating region-specific data.
            seed: Random seed for reproducibility.
        """
        self.faker = Faker(locale)
        
        # Set seed if provided
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
            
        # Define German states
        self.states = [
            "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", 
            "Niedersachsen", "Mecklenburg-Vorpommern", "Nordrhein-Westfalen", "Rheinland-Pfalz", 
            "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
        ]
        
        # Define ZIP code ranges for each state
        self.zip_code_ranges = {
            "Baden-Württemberg": (70000, 79999),
            "Bayern": (80000, 99999),
            "Berlin": (10000, 19999),
            "Brandenburg": (14000, 14999),
            "Bremen": (28000, 28999),
            "Hamburg": (20000, 29999),
            "Hessen": (60000, 69999),
            "Niedersachsen": (26000, 29999),
            "Mecklenburg-Vorpommern": (17000, 17999),
            "Nordrhein-Westfalen": (40000, 49999),
            "Rheinland-Pfalz": (55000, 59999),
            "Saarland": (66000, 66999),
            "Sachsen": [  # Saxony has two ZIP code ranges
                ("01000", "01999"),  # Range 1 (e.g., Dresden, Chemnitz)
                ("04000", "04999")   # Range 2 (e.g., Leipzig, Zwickau)
            ],
            "Sachsen-Anhalt": (39000, 39999),
            "Schleswig-Holstein": (24000, 25999),
            "Thüringen": (99000, 99999)
        }
        
        # Define first names and last names
        self.first_names_male = [
            "Lukas", "Max", "Paul", "Jonas", "Leon", "Felix", "Finn", "Ben", "Moritz", 
            "Noah", "Johannes", "Tim", "Julian", "David", "Matthias", "Niklas", "Elias", 
            "Alexander", "Tobias", "Samuel", "Lucas", "Jakob", "Fabian", "Andreas", 
            "Markus", "Christian", "Stefan", "Simon", "Benjamin", "Daniel", "Michael", 
            "Johann", "Mark", "Kai", "Martin", "Jakob", "Julian", "Tom", "Nico", 
            "Patrick", "Sebastian", "Bastian", "Hannes", "Matthias", "Rafael", "Georg", 
            "Arthur", "Lennard", "Oskar", "Jan", "Maurice", "Timothy"
        ]
        
        self.first_names_female = [
            "Anna", "Sophie", "Marie", "Emma", "Lena", "Laura", "Mia", "Hannah", "Lina", 
            "Sophie", "Lea", "Sarah", "Charlotte", "Clara", "Amelie", "Lilli", "Emily", 
            "Nina", "Ella", "Katharina", "Isabella", "Julia", "Lisa", "Franziska", 
            "Marlene", "Greta", "Eva", "Luisa", "Paula", "Johanna", "Carla", "Leonie", 
            "Lara", "Alina", "Klara", "Victoria", "Elena", "Sina", "Merle", "Maja", 
            "Selina", "Antonia", "Tessa", "Nadine", "Isabel", "Vanessa", "Daniela", 
            "Verena", "Bettina", "Jana", "Maike", "Melanie"
        ]
        
        self.last_names = [
            "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", 
            "Hoffmann", "Schulz", "Bauer", "Koch", "Richter", "Klein", "Wolf", "Schröder", 
            "Neumann", "Schwarz", "Zimmermann", "Braun", "Schmitt", "Hartmann", "Lange", "Werner", 
            "Krause", "Peters", "Jung", "Roth", "Voigt", "Berger", "Mayer", "Fuchs", "Schulte", 
            "Böhm", "Weiss", "Bergmann", "Kraus", "Vogel", "Lang", "Ziegler", "Sauer", 
            "Weidner", "Meyerhoff", "Weigel", "Weber", "Wirth", "Krämer", "Röder", "Heinrich", 
            "Hahn", "Böttcher", "Schulze"
        ]
        
        # Define common German email providers
        self.email_providers = [
            "gmx.de", "web.de", "t-online.de", "yahoo.de", "freenet.de", "aol.de", "mail.de", 
            "tutanota.de", "hotmail.de", "outlook.de", "1und1.de", "posteo.de", "googlemail.com", 
            "mailbox.org", "arcor.de", "ziggo.de", "gmx.net", "freemail.de", "scholar.de", 
            "mymail.de", "bluewin.ch", "studiemail.de", "uni-mail.de", "gmx.at", "gmx.ch", 
            "email.de", "deutschlandemail.de", "planet-interkom.de", "test.de", "versatel.de", 
            "gmx.us", "gmx.co.uk", "gmx.fr", "mailplus.de", "citymail.de", "iserv.de", 
            "gmx.org", "sapo.de", "mail.ru", "scout24.de", "onlinedeutsch.de", "blitzmail.de", 
            "earthlink.net", "easy-mail.de", "eclipso.de", "freenetmail.de", "mailzilla.de", 
            "surfmail.de", "gmx.us", "altavista.com", "dawnmail.de", "posteo.net"
        ]
        
        # Define city coordinates
        self.city_coords = {
            "Berlin": (52.5200, 13.4050),
            "Munich": (48.1351, 11.5820),
            "Hamburg": (53.5511, 9.9937),
            "Cologne": (50.9375, 6.9603),
            "Frankfurt": (50.1109, 8.6821),
            "Stuttgart": (48.7758, 9.1829),
            "Düsseldorf": (51.2217, 6.7762),
            "Dortmund": (51.5145, 7.4660),
            "Essen": (51.4556, 7.0116),
            "Leipzig": (51.3397, 12.3731),
            "Bremen": (53.0793, 8.8017),
            "Dresden": (51.0504, 13.7373),
            "Hanover": (52.3792, 9.7196),
            "Nuremberg": (49.4521, 11.0767),
            "Duisburg": (51.4344, 6.7623),
            "Bochum": (51.4818, 7.2162),
            "Wuppertal": (51.2562, 7.1500),
            "Bielefeld": (52.0302, 8.5325),
            "Münster": (51.9607, 7.6261),
            "Mannheim": (49.4875, 8.4671),
            "Karlsruhe": (49.0141, 8.4044),
            "Hannover": (52.3792, 9.7196),
            "Nürnberg": (49.4521, 11.0767),
            # Add more cities as needed
        }
        
        # Define purchase items
        self.purchase_items = [
            "Hose", "T-Shirt", "Socken", "Jacke", "Schuhe", "Kleid", "Bluse", "Rock", "Pullover",
            "Jeans", "Shorts", "Mantel", "Anzug", "Mütze", "Schal", "Handschuhe", "Unterwäsche", 
            "Badeanzug", "Jogginghose", "Hemd", "Polo-Shirt", "Top", "Pyjama", "Bikini", "Weste", 
            "Leggings", "Poncho", "Strickjacke", "Overall", "Trainingsanzug", "Stirnband", "Strumpfhose", 
            "Sandalen", "Stiefel", "Sneaker", "Pumps", "Slipper", "Cargohose", "Blazer", "Cardigan", 
            "Gürtel", "Krawatte", "Fliege", "Latzhose", "Trachten", "Dirndl", "Halstuch", "Regenjacke", 
            "Regenhose", "Wanderstiefel", "Kapuzenpullover", "Chinos", "Cargo-Shorts", "Pufferjacke", 
            "Desert Boots", "Loafers", "Espadrilles", "Flip-Flops", "Hausschuhe", "Boxershorts", 
            "Tanktop", "Badehose", "Radlerhose", "Sonnenhut", "Haarband", "Klettschuhe", "Schnürschuhe", 
            "Abendkleid", "Ballkleid", "Ballerinas", "Mokassins", "Zehensandalen", "Bastschuhe", "Segelschuhe", 
            "Wedges", "Plateauschuhe", "Stoffschuhe", "Clogs", "Römersandalen", "Kampfstiefel", "Chelseaboots", 
            "Brogues", "Halbschuhe", "Oxfordschuhe", "Laufschuhe", "Kletterhosen", "Sport-BH", "Funktionsshirt"
        ]

    def generate_zip_code(self, state: str) -> str:
        """
        Generate a random ZIP code based on the state.
        
        Args:
            state: German state name.
        
        Returns:
            A plausible ZIP code for the given state.
        """
        # Get the ZIP code range for the state
        zip_range = self.zip_code_ranges.get(state, (10000, 19999))  # Default to Berlin if state not found
        
        # If the state is Sachsen (Saxony) and has multiple ranges, we handle it differently
        if state == "Sachsen":
            # Randomly select one of the ranges for Sachsen
            zip_range = random.choice(zip_range)
            
        # Generate a random ZIP code within the range
        if isinstance(zip_range, tuple):
            return str(random.randint(int(zip_range[0]), int(zip_range[1])))
        else:
            return zip_range  # If it's already a string range

    def generate_geo_coordinates(self, city: str) -> Tuple[float, float]:
        """
        Generate geographical coordinates for a given city.
        
        Args:
            city: Name of the city.
        
        Returns:
            A tuple of (latitude, longitude).
        """
        # Check if the city is in the city_coords dictionary
        if city in self.city_coords:
            return self.city_coords[city]
        else:
            # Default to a center of Germany if the city is not found
            return (51.1657, 10.4515)  # Germany's approximate center

    def generate_email(self, first_name: str, last_name: str) -> str:
        """
        Generate a plausible email address for a person.
        
        Args:
            first_name: Person's first name.
            last_name: Person's last name.
        
        Returns:
            A synthetic email address.
        """
        # Choose a random email provider
        email_provider = random.choice(self.email_providers)
        
        # Create a username with optional formatting variations
        format_type = random.randint(1, 4)
        
        if format_type == 1:
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 100)}"
        elif format_type == 2:
            username = f"{first_name.lower()[0]}{last_name.lower()}{random.randint(1, 100)}"
        elif format_type == 3:
            username = f"{first_name.lower()}{last_name.lower()[0]}{random.randint(1, 100)}"
        else:
            username = f"{last_name.lower()}.{first_name.lower()}{random.randint(1, 100)}"
            
        # Return the full email address
        return f"{username}@{email_provider}"

    def generate_address(self, state: str) -> Tuple[str, str]:
        """
        Generate a random address based on the state.
        
        Args:
            state: German state name.
        
        Returns:
            A tuple of (zip_city, street).
        """
        # Generate a random ZIP code based on the state
        zip_code = self.generate_zip_code(state)
        city = self.faker.city()
        street = f"{self.faker.street_name()} {self.faker.building_number()}"
        
        return f"{zip_code} {city}", street

    def generate_birthday(self, min_age: int = 18, max_age: int = 80) -> str:
        """
        Generate a random birthday within the specified age range.
        
        Args:
            min_age: Minimum age in years.
            max_age: Maximum age in years.
        
        Returns:
            A birthday in 'YYYY-MM-DD' format."
            """
        # Calculate the date range based on the age
        end_date = datetime.now()
        start_date = end_date.replace(year=end_date.year - max_age)
        
        # Generate a random birth date within the range
        birth_date = self.faker.date_of_birth(minimum_age=min_age, maximum_age=max_age)
        
        return birth_date.strftime("%Y-%m-%d")
    
    def generate_price(self) -> float:
      """
      Generate a random price for a purchase item.
      
      Returns:
          A float representing the price in Euro.
      """
    # Generate a price between 5 and 199.99 Euro
      price = round(random.uniform(5.0, 199.99), 2)
      return price

def generate_stueckzahl(self) -> int:
    """
    Generate a random quantity for a purchase.
    
    Returns:
        An integer representing the quantity.
    """
    # Most common case: quantity of 1
    if random.random() < 0.7:
        return 1
    else:
        # Sometimes buy multiple items (2-5)
        return random.randint(2, 5)

def generate_sales_tax(self) -> float:
    """
    Generate sales tax rate.
    
    Returns:
        A float representing the tax rate (0.19 or 0.07).
    """
    # Standard rate (19%) or reduced rate (7%)
    return 0.19 if random.random() < 0.8 else 0.07

def generate_purchase_type(self) -> str:
    """
    Generate a purchase type (online or in-store).
    
    Returns:
        A string representing the purchase type.
    """
    purchase_types = ["Online", "In-Store"]
    return random.choice(purchase_types)

def generate_profile(self) -> Dict:
    """
    Generate a complete fictional profile.
    
    Returns:
        A dictionary containing the profile data.
    """
    # Generate gender
    gender = "male" if random.random() < 0.5 else "female"
    
    # Generate first name based on gender
    if gender == "male":
        first_name = random.choice(self.first_names_male)
    else:
        first_name = random.choice(self.first_names_female)
    
    # Generate last name
    last_name = random.choice(self.last_names)
    
    # Generate email
    email = self.generate_email(first_name, last_name)
    
    # Generate state and address
    state = random.choice(self.states)
    zip_city, street = self.generate_address(state)
    
    # Generate birthday
    birthday = self.generate_birthday()
    
    # Generate purchase details
    item = random.choice(self.purchase_items)
    price = self.generate_price()
    quantity = self.generate_stueckzahl()
    tax_rate = self.generate_sales_tax()
    purchase_type = self.generate_purchase_type()
    
    # Calculate totals
    subtotal = price * quantity
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    
    # Extract city for coordinates
    city = zip_city.split(" ", 1)[1] if " " in zip_city else "Berlin"
    lat, lon = self.generate_geo_coordinates(city)
    
    # Create profile dictionary
    profile = {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "email": email,
        "birthday": birthday,
        "street": street,
        "zip_city": zip_city,
        "state": state,
        "latitude": lat,
        "longitude": lon,
        "purchase_item": item,
        "price": round(price, 2),
        "quantity": quantity,
        "tax_rate": tax_rate,
        "tax_amount": round(tax_amount, 2),
        "subtotal": round(subtotal, 2),
        "total": round(total, 2),
        "purchase_type": purchase_type,
        "purchase_date": self.faker.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return profile

def generate_profiles(self, count: int = 10) -> List[Dict]:
    """
    Generate multiple profiles.
    
    Args:
        count: Number of profiles to generate.
    
    Returns:
        A list of profile dictionaries.
    """
    profiles = []
    for _ in range(count):
        profiles.append(self.generate_profile())
    return profiles

def create_dataframe(self, profiles: List[Dict]) -> pd.DataFrame:
    """
    Create a DataFrame from profiles.
    
    Args:
        profiles: List of profile dictionaries.
    
    Returns:
        A pandas DataFrame with all profiles.
    """
    return pd.DataFrame(profiles)

def save_to_csv(self, df: pd.DataFrame, file_path: str) -> None:
    """
    Save the DataFrame to a CSV file.
    
    Args:
        df: DataFrame to save.
        file_path: Path for the output file.
    """
    df.to_csv(file_path, index=False)
    print(f"Data saved to CSV: {file_path}")

def save_to_excel(self, df: pd.DataFrame, file_path: str) -> None:
    """
    Save the DataFrame to an Excel file.
    
    Args:
        df: DataFrame to save.
        file_path: Path for the output file.
    """
    if not EXCEL_AVAILABLE:
        print("Error: openpyxl is not installed. Cannot save to Excel format.")
        print("Install it with 'pip install openpyxl'")
        return
    
    df.to_excel(file_path, index=False)
    print(f"Data saved to Excel: {file_path}")

def save_to_json(self, profiles: List[Dict], file_path: str) -> None:
    """
    Save profiles to a JSON file.
    
    Args:
        profiles: List of profile dictionaries.
        file_path: Path for the output file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
    print(f"Data saved to JSON: {file_path}")

def create_map(self, df: pd.DataFrame, file_path: str) -> None:
    """
    Create an interactive map with the profile locations.
    
    Args:
        df: DataFrame with profile data.
        file_path: Path for the output HTML file.
    """
    if not FOLIUM_AVAILABLE:
        print("Error: folium is not installed. Cannot create map.")
        print("Install it with 'pip install folium'")
        return
    
    # Create map centered on Germany
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each profile
    for _, row in df.iterrows():
        popup_html = f"""
        <b>{row['first_name']} {row['last_name']}</b><br>
        {row['street']}<br>
        {row['zip_city']}<br>
        <b>Purchase:</b> {row['quantity']}x {row['purchase_item']}<br>
        <b>Total:</b> €{row['total']:.2f}
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)
    
    # Save map to file
    m.save(file_path)
    print(f"Map saved to: {file_path}")


def main():
    """Main function to run the script from command line."""
    parser = argparse.ArgumentParser(description="Generate synthetic profiles with geographical data")
    
    # Add arguments
    parser.add_argument("-n", "--num", type=int, default=10,
                        help="Number of profiles to generate (default: 10)")
    parser.add_argument("-o", "--output", type=str, default="profiles",
                        help="Output file name without extension (default: profiles)")
    parser.add_argument("-f", "--format", type=str, choices=["csv", "excel", "json", "all"], 
                        default="csv", help="Output format (default: csv)")
    parser.add_argument("-l", "--locale", type=str, default="de_DE",
                        help="Locale for generating data (default: de_DE)")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="Random seed for reproducibility")
    parser.add_argument("-m", "--map", action="store_true",
                        help="Create an interactive map visualization")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize generator
    generator = GeoProfileGenerator(locale=args.locale, seed=args.seed)
    
    # Generate profiles
    profiles = generator.generate_profiles(args.num)
    
    # Create DataFrame
    df = generator.create_dataframe(profiles)
    
    # Save data based on format
    if args.format == "csv" or args.format == "all":
        generator.save_to_csv(df, f"{args.output}.csv")
    
    if args.format == "excel" or args.format == "all":
        generator.save_to_excel(df, f"{args.output}.xlsx")
    
    if args.format == "json" or args.format == "all":
        generator.save_to_json(profiles, f"{args.output}.json")
    
    # Create map if requested
    if args.map:
        generator.create_map(df, f"{args.output}_map.html")


if __name__ == "__main__":
    main()