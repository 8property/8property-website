import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from typing import List, Dict, Any

class GoogleSheetsService:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Google Sheets client with service account credentials."""
        try:
            # Path to the service account JSON file
            credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'service_account.json')
            
            with open(credentials_path, "r") as f:
                creds_json = json.load(f)
            
            # Replace escaped newlines with actual newlines in the private_key
            creds_json["private_key"] = creds_json["private_key"].replace("\\n", "\n")

            creds = ServiceAccountCredentials.from_json_keyfile_dict(
                creds_json, self.scope
            )
            self.client = gspread.authorize(creds)
            print("Google Sheets client initialized successfully.")
        except Exception as e:
            print(f"Error initializing Google Sheets client: {e}")
            raise e
    
    def get_sheet_data(self, sheet_url: str, worksheet_index: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve all data from a Google Sheet as a list of dictionaries.
        
        Args:
            sheet_url (str): The URL of the Google Sheet
            worksheet_index (int): Index of the worksheet (default: 0 for first sheet)
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries representing rows
        """
        try:
            # Open the spreadsheet by URL
            spreadsheet = self.client.open_by_url(sheet_url)
            
            # Get the specified worksheet
            worksheet = spreadsheet.get_worksheet(worksheet_index)
            
            # Get all records as a list of dictionaries
            data = worksheet.get_all_records()
            
            return data
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: Spreadsheet not found at URL: {sheet_url}")
            return []
        except gspread.exceptions.NoValidUrlKeyFound:
            print(f"Error: Invalid Google Sheet URL format: {sheet_url}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while fetching sheet data: {e}")
            return []
    
    def get_28hse_listings(self) -> List[Dict[str, Any]]:
        """Get 28Hse property listings."""
        sheet_url = "https://docs.google.com/spreadsheets/d/1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74/edit?gid=0#gid=0"
        return self.get_sheet_data(sheet_url)
    
    def get_centaline_listings(self) -> List[Dict[str, Any]]:
        """Get Centaline property listings."""
        sheet_url = "https://docs.google.com/spreadsheets/d/1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM/edit?gid=0#gid=0"
        return self.get_sheet_data(sheet_url)
    
    def get_squarefoot_listings(self) -> List[Dict[str, Any]]:
        """Get Squarefoot property listings."""
        sheet_url = "https://docs.google.com/spreadsheets/d/1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0/edit?gid=0#gid=0"
        return self.get_sheet_data(sheet_url)
    
    def get_hk01_news(self) -> List[Dict[str, Any]]:
        """Get HK01 news articles."""
        sheet_url = "https://docs.google.com/spreadsheets/d/1TQUlIfvv4k_hgf4vFlPULz4HD32x22qBxJMIdEwDC9g/edit?gid=0#gid=0"
        return self.get_sheet_data(sheet_url)
    
    def get_all_property_listings(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all property listings from all sources."""
        return {
            "28hse": self.get_28hse_listings(),
            "centaline": self.get_centaline_listings(),
            "squarefoot": self.get_squarefoot_listings()
        }
    
    def search_properties(self, query: str = "", min_price: int = None, max_price: int = None, 
                         rooms: str = None, development: str = None) -> List[Dict[str, Any]]:
        """
        Search properties across all sources with filters.
        
        Args:
            query (str): General search query
            min_price (int): Minimum price filter
            max_price (int): Maximum price filter
            rooms (str): Number of rooms filter
            development (str): Development name filter
        
        Returns:
            List[Dict[str, Any]]: Filtered property listings
        """
        all_listings = []
        
        # Get listings from all sources
        sources = self.get_all_property_listings()
        for source_name, listings in sources.items():
            for listing in listings:
                listing['source'] = source_name  # Add source information
                all_listings.append(listing)
        
        # Apply filters
        filtered_listings = all_listings
        
        if query:
            query_lower = query.lower()
            filtered_listings = [
                listing for listing in filtered_listings
                if (query_lower in listing.get('title', '').lower() or
                    query_lower in listing.get('address', '').lower() or
                    query_lower in listing.get('development', '').lower())
            ]
        
        if min_price is not None or max_price is not None:
            def extract_price(price_str):
                """Extract numeric price from price string like '$18,000'"""
                try:
                    # Remove currency symbols and commas, then convert to int
                    price_clean = price_str.replace('$', '').replace(',', '').replace(' ', '')
                    return int(price_clean)
                except (ValueError, AttributeError):
                    return 0
            
            filtered_listings = [
                listing for listing in filtered_listings
                if self._price_in_range(extract_price(listing.get('price', '0')), min_price, max_price)
            ]
        
        if rooms:
            filtered_listings = [
                listing for listing in filtered_listings
                if rooms in listing.get('rooms', '')
            ]
        
        if development:
            development_lower = development.lower()
            filtered_listings = [
                listing for listing in filtered_listings
                if development_lower in listing.get('development', '').lower()
            ]
        
        return filtered_listings
    
    def _price_in_range(self, price: int, min_price: int = None, max_price: int = None) -> bool:
        """Check if price is within the specified range."""
        if min_price is not None and price < min_price:
            return False
        if max_price is not None and price > max_price:
            return False
        return True

