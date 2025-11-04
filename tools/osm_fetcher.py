#!/usr/bin/env python3
"""
OSM Data Fetcher for Pokémon Qbone - Pokéliga Edition
Henter geodata fra OpenStreetMap for Vennesla-området
"""

import json
import argparse
import requests
from typing import Dict, List, Tuple

# Vennesla bounding box (lat, lon)
VENNESLA_BBOX = {
    "south": 58.25,
    "west": 7.90,
    "north": 58.35,
    "east": 8.05
}

OVERPASS_API = "http://overpass-api.de/api/interpreter"


def build_overpass_query(bbox: Dict[str, float]) -> str:
    """
    Bygger Overpass QL-query for å hente relevante data
    
    Args:
        bbox: Bounding box med south, west, north, east
        
    Returns:
        Overpass QL query string
    """
    bbox_str = f"{bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']}"
    
    query = f"""
    [out:json][timeout:60];
    (
      // Bygninger
      way["building"]({bbox_str});
      relation["building"]({bbox_str});
      
      // Veier
      way["highway"]({bbox_str});
      
      // Vann
      way["natural"="water"]({bbox_str});
      way["waterway"]({bbox_str});
      
      // Interessepunkter
      node["amenity"]({bbox_str});
      node["shop"]({bbox_str});
      node["tourism"]({bbox_str});
      
      // Natur
      way["natural"="wood"]({bbox_str});
      way["landuse"="forest"]({bbox_str});
    );
    out body;
    >;
    out skel qt;
    """
    return query


def fetch_osm_data(bbox: Dict[str, float]) -> Dict:
    """
    Henter OSM-data fra Overpass API
    
    Args:
        bbox: Bounding box for området
        
    Returns:
        JSON-data fra OSM
    """
    query = build_overpass_query(bbox)
    
    print(f"Henter OSM-data for område: {bbox}")
    print("Dette kan ta litt tid...")
    
    try:
        response = requests.post(
            OVERPASS_API,
            data={'data': query},
            timeout=120
        )
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ Hentet {len(data.get('elements', []))} elementer")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Feil ved henting av data: {e}")
        return {}


def categorize_elements(osm_data: Dict) -> Dict[str, List]:
    """
    Kategoriserer OSM-elementer etter type
    
    Args:
        osm_data: Rå OSM-data
        
    Returns:
        Dict med kategoriserte elementer
    """
    categories = {
        "buildings": [],
        "roads": [],
        "water": [],
        "forests": [],
        "poi": []
    }
    
    for element in osm_data.get('elements', []):
        tags = element.get('tags', {})
        
        if 'building' in tags:
            categories["buildings"].append(element)
        elif 'highway' in tags:
            categories["roads"].append(element)
        elif 'natural' in tags and tags['natural'] in ['water', 'wood']:
            if tags['natural'] == 'water':
                categories["water"].append(element)
            else:
                categories["forests"].append(element)
        elif 'waterway' in tags:
            categories["water"].append(element)
        elif any(key in tags for key in ['amenity', 'shop', 'tourism']):
            categories["poi"].append(element)
    
    return categories


def save_data(data: Dict, output_file: str):
    """
    Lagrer data til JSON-fil
    
    Args:
        data: Data som skal lagres
        output_file: Filsti for output
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Data lagret til {output_file}")
    except IOError as e:
        print(f"✗ Feil ved lagring: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Hent OSM-data for Pokémon Qbone kartutvikling"
    )
    parser.add_argument(
        '--area',
        default='vennesla',
        help='Område å hente data for (default: vennesla)'
    )
    parser.add_argument(
        '--output',
        default='data/vennesla_osm.json',
        help='Output-fil for data (default: data/vennesla_osm.json)'
    )
    parser.add_argument(
        '--categorize',
        action='store_true',
        help='Kategoriser elementer etter type'
    )
    
    args = parser.parse_args()
    
    # Hent data
    osm_data = fetch_osm_data(VENNESLA_BBOX)
    
    if not osm_data:
        print("Ingen data hentet. Avslutter.")
        return
    
    # Kategoriser hvis ønsket
    if args.categorize:
        print("\nKategoriserer elementer...")
        categorized = categorize_elements(osm_data)
        
        print("\nStatistikk:")
        for category, elements in categorized.items():
            print(f"  {category}: {len(elements)} elementer")
        
        output_data = {
            "metadata": {
                "area": args.area,
                "bbox": VENNESLA_BBOX,
                "total_elements": len(osm_data.get('elements', []))
            },
            "categorized": categorized,
            "raw": osm_data
        }
    else:
        output_data = osm_data
    
    # Lagre data
    save_data(output_data, args.output)
    print("\n✓ Ferdig!")


if __name__ == "__main__":
    main()
