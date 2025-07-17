# Database Management Guide
## Property Agency System

This guide covers comprehensive database management for your property agency system, including Google Sheets management, data migration options, and advanced database operations.

## Table of Contents

1. [Current Database Architecture](#current-database-architecture)
2. [Google Sheets Management](#google-sheets-management)
3. [Data Migration Strategies](#data-migration-strategies)
4. [Database Optimization](#database-optimization)
5. [Backup and Recovery](#backup-and-recovery)
6. [Data Quality Management](#data-quality-management)
7. [Performance Monitoring](#performance-monitoring)
8. [Scaling Considerations](#scaling-considerations)

---

## Current Database Architecture

### Google Sheets as Primary Database

Your system currently uses Google Sheets as the primary database with the following structure:

**Active Sheets**:
- **28Hse Properties**: `1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74`
- **Centaline Properties**: `1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM`
- **Squarefoot Properties**: `1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0`
- **HK01 News**: `1TQUlIfvv4k_hgf4vFlPULz4HD32x22qBxJMIdEwDC9g`

**Data Schema**:
```
Properties Table Structure:
- title/development: Property name
- price: Monthly rental price
- address: Property location
- rooms: Number of bedrooms
- gross_area: Floor area in square feet
- image_url: Primary property image
- listing_url: Original listing URL
- agency: Real estate agency
- contact_person: Agent contact
- source: Data source (28hse, centaline, squarefoot)
- Additional image URLs (image_url2, image_url3, etc.)
```

### Advantages of Current Setup
- **Easy Manual Management**: Direct editing in familiar spreadsheet interface
- **Real-time Collaboration**: Multiple team members can edit simultaneously
- **Automatic Backups**: Google handles data backup and recovery
- **Cost-Effective**: Free for reasonable usage levels
- **API Integration**: Well-documented Google Sheets API
- **Version History**: Built-in change tracking

### Limitations to Consider
- **API Rate Limits**: 100 requests per 100 seconds per user
- **Concurrent Access**: Limited concurrent write operations
- **Query Limitations**: No complex SQL-like queries
- **Data Types**: All data stored as strings
- **Scalability**: Performance degrades with very large datasets (>100k rows)

---

## Google Sheets Management

### 1. Daily Management Tasks

#### 1.1 Data Quality Checks
```python
import gspread
import pandas as pd
from datetime import datetime, timedelta

class SheetsManager:
    def __init__(self, credentials_path):
        self.gc = gspread.service_account(credentials_path)
        self.sheets = {
            '28hse': '1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74',
            'centaline': '1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM',
            'squarefoot': '1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0'
        }
    
    def check_data_quality(self, source):
        """Check data quality for a specific source"""
        sheet = self.gc.open_by_key(self.sheets[source]).sheet1
        data = sheet.get_all_records()
        
        issues = []
        for i, row in enumerate(data, 2):  # Start from row 2
            # Check required fields
            if not row.get('title'):
                issues.append(f"Row {i}: Missing title")
            if not row.get('price'):
                issues.append(f"Row {i}: Missing price")
            if not row.get('image_url'):
                issues.append(f"Row {i}: Missing image URL")
            if not row.get('listing_url'):
                issues.append(f"Row {i}: Missing listing URL")
            
            # Check data format
            if row.get('price') and not any(char.isdigit() for char in str(row['price'])):
                issues.append(f"Row {i}: Invalid price format")
        
        return issues
    
    def remove_duplicates(self, source):
        """Remove duplicate entries based on listing URL"""
        sheet = self.gc.open_by_key(self.sheets[source]).sheet1
        data = sheet.get_all_records()
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(data)
        
        # Remove duplicates based on listing_url
        original_count = len(df)
        df_clean = df.drop_duplicates(subset=['listing_url'], keep='last')
        removed_count = original_count - len(df_clean)
        
        if removed_count > 0:
            # Clear sheet and update with clean data
            sheet.clear()
            # Update with headers and clean data
            sheet.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())
            print(f"Removed {removed_count} duplicates from {source}")
        
        return removed_count
    
    def archive_old_data(self, source, days_old=90):
        """Archive properties older than specified days"""
        sheet = self.gc.open_by_key(self.sheets[source]).sheet1
        data = sheet.get_all_records()
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        current_data = []
        archived_data = []
        
        for row in data:
            # Assuming you have a date field or can determine age
            # This is a simplified example
            if self._is_recent_property(row, cutoff_date):
                current_data.append(row)
            else:
                archived_data.append(row)
        
        # Update main sheet with current data
        if current_data:
            sheet.clear()
            df = pd.DataFrame(current_data)
            sheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        # Save archived data to separate sheet
        if archived_data:
            self._save_archived_data(source, archived_data)
        
        return len(archived_data)
```

#### 1.2 Automated Maintenance Script
```python
#!/usr/bin/env python3
"""
Daily maintenance script for Google Sheets database
Run this script daily via cron job
"""

import sys
import logging
from datetime import datetime
from sheets_manager import SheetsManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/sheets_maintenance.log'),
        logging.StreamHandler()
    ]
)

def daily_maintenance():
    """Run daily maintenance tasks"""
    manager = SheetsManager('/path/to/credentials.json')
    
    for source in ['28hse', 'centaline', 'squarefoot']:
        logging.info(f"Starting maintenance for {source}")
        
        try:
            # Check data quality
            issues = manager.check_data_quality(source)
            if issues:
                logging.warning(f"Data quality issues in {source}: {len(issues)} issues found")
                # Send alert email here
            
            # Remove duplicates
            removed = manager.remove_duplicates(source)
            if removed > 0:
                logging.info(f"Removed {removed} duplicates from {source}")
            
            # Archive old data (optional)
            archived = manager.archive_old_data(source, days_old=90)
            if archived > 0:
                logging.info(f"Archived {archived} old properties from {source}")
                
        except Exception as e:
            logging.error(f"Error processing {source}: {str(e)}")
    
    logging.info("Daily maintenance completed")

if __name__ == "__main__":
    daily_maintenance()
```

### 2. Advanced Sheet Operations

#### 2.1 Bulk Data Operations
```python
class BulkOperations:
    def __init__(self, sheets_manager):
        self.manager = sheets_manager
    
    def bulk_update_prices(self, source, price_updates):
        """Update multiple property prices at once"""
        sheet = self.manager.gc.open_by_key(self.manager.sheets[source]).sheet1
        
        # Get current data
        data = sheet.get_all_records()
        
        # Create updates list for batch operation
        updates = []
        for i, row in enumerate(data, 2):  # Start from row 2
            listing_url = row.get('listing_url')
            if listing_url in price_updates:
                # Update price in row i, assuming price is in column B
                updates.append({
                    'range': f'B{i}',
                    'values': [[price_updates[listing_url]]]
                })
        
        # Batch update
        if updates:
            sheet.batch_update(updates)
            print(f"Updated {len(updates)} prices in {source}")
    
    def bulk_add_properties(self, source, new_properties):
        """Add multiple properties at once"""
        sheet = self.manager.gc.open_by_key(self.manager.sheets[source]).sheet1
        
        # Get current data to find next empty row
        current_data = sheet.get_all_values()
        next_row = len(current_data) + 1
        
        # Prepare data for batch insert
        values = []
        for prop in new_properties:
            row = [
                prop.get('title', ''),
                prop.get('price', ''),
                prop.get('address', ''),
                prop.get('rooms', ''),
                prop.get('gross_area', ''),
                prop.get('image_url', ''),
                prop.get('listing_url', ''),
                prop.get('agency', ''),
                prop.get('contact_person', ''),
                # Add more fields as needed
            ]
            values.append(row)
        
        # Batch insert
        if values:
            range_name = f'A{next_row}:I{next_row + len(values) - 1}'
            sheet.update(range_name, values)
            print(f"Added {len(values)} properties to {source}")
```

#### 2.2 Data Validation and Cleaning
```python
class DataValidator:
    def __init__(self, sheets_manager):
        self.manager = sheets_manager
    
    def validate_image_urls(self, source):
        """Check if image URLs are accessible"""
        import requests
        
        sheet = self.manager.gc.open_by_key(self.manager.sheets[source]).sheet1
        data = sheet.get_all_records()
        
        broken_urls = []
        for i, row in enumerate(data, 2):
            image_url = row.get('image_url')
            if image_url:
                try:
                    response = requests.head(image_url, timeout=10)
                    if response.status_code != 200:
                        broken_urls.append((i, image_url))
                except:
                    broken_urls.append((i, image_url))
        
        return broken_urls
    
    def standardize_price_format(self, source):
        """Standardize price format across all properties"""
        import re
        
        sheet = self.manager.gc.open_by_key(self.manager.sheets[source]).sheet1
        data = sheet.get_all_records()
        
        updates = []
        for i, row in enumerate(data, 2):
            price = row.get('price', '')
            if price:
                # Extract numbers and format consistently
                numbers = re.findall(r'\d+', price.replace(',', ''))
                if numbers:
                    formatted_price = f"${int(numbers[0]):,}"
                    if formatted_price != price:
                        updates.append({
                            'range': f'B{i}',  # Assuming price is in column B
                            'values': [[formatted_price]]
                        })
        
        if updates:
            sheet.batch_update(updates)
            print(f"Standardized {len(updates)} prices in {source}")
    
    def clean_contact_info(self, source):
        """Clean and standardize contact information"""
        sheet = self.manager.gc.open_by_key(self.manager.sheets[source]).sheet1
        data = sheet.get_all_records()
        
        updates = []
        for i, row in enumerate(data, 2):
            contact = row.get('contact_person', '')
            if contact:
                # Remove extra spaces and standardize format
                cleaned = ' '.join(contact.split())
                if cleaned != contact:
                    updates.append({
                        'range': f'I{i}',  # Assuming contact is in column I
                        'values': [[cleaned]]
                    })
        
        if updates:
            sheet.batch_update(updates)
            print(f"Cleaned {len(updates)} contact entries in {source}")
```

---

## Data Migration Strategies

### 1. Migration to PostgreSQL

If you need better performance and advanced features, PostgreSQL is recommended:

#### 1.1 Database Setup
```sql
-- Create database
CREATE DATABASE property_agency;

-- Connect to database
\c property_agency;

-- Create properties table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    price VARCHAR(50),
    address TEXT,
    rooms VARCHAR(50),
    gross_area VARCHAR(100),
    saleable_area VARCHAR(100),
    floor VARCHAR(50),
    image_url TEXT,
    listing_url TEXT UNIQUE,
    agency VARCHAR(200),
    contact_person VARCHAR(200),
    source VARCHAR(20) NOT NULL,
    development VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create indexes for better performance
CREATE INDEX idx_properties_source ON properties(source);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_rooms ON properties(rooms);
CREATE INDEX idx_properties_active ON properties(is_active);
CREATE INDEX idx_properties_created ON properties(created_at);

-- Create full-text search index
CREATE INDEX idx_properties_search ON properties USING gin(to_tsvector('english', title || ' ' || address));

-- Create additional tables for normalized data
CREATE TABLE agencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    contact_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    agency_id INTEGER REFERENCES agencies(id),
    contact_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create property images table for multiple images
CREATE TABLE property_images (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 1.2 Migration Script
```python
import psycopg2
import gspread
import json
from datetime import datetime
import logging

class DatabaseMigrator:
    def __init__(self, postgres_config, google_credentials):
        # PostgreSQL connection
        self.conn = psycopg2.connect(**postgres_config)
        self.cur = self.conn.cursor()
        
        # Google Sheets connection
        self.gc = gspread.service_account(google_credentials)
        
        self.sheets = {
            '28hse': '1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74',
            'centaline': '1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM',
            'squarefoot': '1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0'
        }
    
    def migrate_all_data(self):
        """Migrate all data from Google Sheets to PostgreSQL"""
        for source, sheet_id in self.sheets.items():
            logging.info(f"Migrating {source} data...")
            self.migrate_source_data(source, sheet_id)
        
        self.conn.commit()
        logging.info("Migration completed successfully")
    
    def migrate_source_data(self, source, sheet_id):
        """Migrate data from a specific Google Sheet"""
        sheet = self.gc.open_by_key(sheet_id).sheet1
        data = sheet.get_all_records()
        
        for row in data:
            try:
                # Insert main property data
                property_id = self.insert_property(row, source)
                
                # Insert additional images
                self.insert_property_images(property_id, row)
                
                # Insert agency and agent data
                self.insert_agency_agent(row)
                
            except Exception as e:
                logging.error(f"Error migrating row: {e}")
                continue
    
    def insert_property(self, row, source):
        """Insert property data and return property ID"""
        query = """
            INSERT INTO properties (
                title, price, address, rooms, gross_area, saleable_area,
                floor, image_url, listing_url, agency, contact_person,
                source, development
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) ON CONFLICT (listing_url) DO UPDATE SET
                title = EXCLUDED.title,
                price = EXCLUDED.price,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id;
        """
        
        values = (
            row.get('title', ''),
            row.get('price', ''),
            row.get('address', ''),
            row.get('rooms', ''),
            row.get('gross_area', ''),
            row.get('saleable_area', ''),
            row.get('floor', ''),
            row.get('image_url', ''),
            row.get('listing_url', ''),
            row.get('agency', ''),
            row.get('contact_person', ''),
            source,
            row.get('development', '')
        )
        
        self.cur.execute(query, values)
        result = self.cur.fetchone()
        return result[0] if result else None
    
    def insert_property_images(self, property_id, row):
        """Insert additional property images"""
        if not property_id:
            return
        
        # Look for additional image URLs (image_url2, image_url3, etc.)
        for key, value in row.items():
            if key.startswith('image_url') and key != 'image_url' and value:
                query = """
                    INSERT INTO property_images (property_id, image_url, is_primary)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """
                self.cur.execute(query, (property_id, value, False))
    
    def create_sync_job(self):
        """Create a job to keep PostgreSQL in sync with Google Sheets"""
        sync_script = """
        #!/usr/bin/env python3
        # Sync job to update PostgreSQL from Google Sheets
        
        import psycopg2
        import gspread
        from datetime import datetime
        
        def sync_data():
            # Your sync logic here
            pass
        
        if __name__ == "__main__":
            sync_data()
        """
        
        with open('/opt/property_sync.py', 'w') as f:
            f.write(sync_script)
        
        # Add to crontab
        import subprocess
        subprocess.run(['crontab', '-l'], capture_output=True)
        # Add: 0 */2 * * * /usr/bin/python3 /opt/property_sync.py
```

### 2. Migration to MongoDB

For document-based storage with flexible schema:

```python
from pymongo import MongoClient
import gspread

class MongoMigrator:
    def __init__(self, mongo_uri, google_credentials):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.property_agency
        self.properties = self.db.properties
        
        self.gc = gspread.service_account(google_credentials)
        
    def migrate_to_mongo(self):
        """Migrate Google Sheets data to MongoDB"""
        sheets = {
            '28hse': '1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74',
            'centaline': '1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM',
            'squarefoot': '1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0'
        }
        
        for source, sheet_id in sheets.items():
            sheet = self.gc.open_by_key(sheet_id).sheet1
            data = sheet.get_all_records()
            
            documents = []
            for row in data:
                # Prepare document
                doc = {
                    'title': row.get('title', ''),
                    'price': row.get('price', ''),
                    'address': row.get('address', ''),
                    'rooms': row.get('rooms', ''),
                    'gross_area': row.get('gross_area', ''),
                    'listing_url': row.get('listing_url', ''),
                    'agency': row.get('agency', ''),
                    'contact_person': row.get('contact_person', ''),
                    'source': source,
                    'images': [url for key, url in row.items() if key.startswith('image_url') and url],
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                documents.append(doc)
            
            # Bulk insert with upsert
            if documents:
                for doc in documents:
                    self.properties.update_one(
                        {'listing_url': doc['listing_url']},
                        {'$set': doc},
                        upsert=True
                    )
        
        # Create indexes
        self.properties.create_index('source')
        self.properties.create_index('listing_url', unique=True)
        self.properties.create_index([('title', 'text'), ('address', 'text')])
```

---

