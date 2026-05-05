#!/usr/bin/env python3
"""
Prague Travel Map Creator
Converts a KML file with Prague locations into a beautiful interactive Folium map.
"""

from pathlib import Path
import folium
from folium import plugins
from typing import Dict, List, Tuple
from lxml import etree

# Color mapping from KML style IDs to Folium colors
COLOR_MAP = {
    "cute": "pink",         # Pink for romantic spots
    "beer": "green",        # Green for beer bars
    "food": "blue",         # Blue for food spots
    "view": "orange",       # Orange for viewpoints
}

ICON_MAP = {
    "cute": "heart",
    "beer": "beer",
    "food": "cutlery",
    "view": "camera",
}

EMOJI_MAP = {
    "cute": "❤️",
    "beer": "🍺",
    "food": "🍽️",
    "view": "📷",
}

PLACE_DESCRIPTIONS = {
    "🏨 Our hotel (start & end)": "Cozy hotel base near the river, perfect for resting between adventures.",
    "✨ Morning wander – Old Town Square": "Historic square with the Astronomical Clock, charming cafes, and street artists.",
    "🌉 Slow walk – Charles Bridge": "One of Prague's most famous bridges, lined with statues and romantic river views.",
    "🏰 Exploring views – Prague Castle": "A majestic hilltop castle complex with sweeping city panoramas.",
    "🌇 Sunset moment – Letná Park": "A peaceful park with the best sunset views over the city and river.",
    "🍖 Quick bite – Naše maso": "A top spot for fresh Czech sausages and a delicious meat-lover's lunch.",
    "🍷 Nice dinner – Eska": "Modern Czech restaurant with a creative menu in a stylish industrial space.",
    "🍽️ Cozy food stop – Kantýna": "A meat-focused dining hall offering hearty local dishes in a cozy setting.",
    "🥐 Slow morning – Café Savoy": "Classic café with elegant interiors, great coffee, and pastries for breakfast.",
    "🍺 First drink – Lokál": "A popular beer hall with classic Czech lager and a friendly local atmosphere.",
    "🍺 Craft beers – BeerGeek": "A craft beer bar with a rotating tap list and a relaxed vibe.",
    "🍺 Something different – Bad Flash": "An eclectic bar known for creative drinks and a fun, neon-lit scene.",
    "🌇 Sunset together – Riegrovy Sady": "A green park with laid-back picnic spots and postcard-perfect sunset views.",
    "🏰 Hidden calm – Vyšehrad": "Historic fortress grounds offering quiet walks and scenic views away from the crowds.",
    "🌿 Quiet walk – Kampa Island": "Island oasis by the river, perfect for a romantic stroll and riverside charm.",
    "🍷 Wine bar date – Vinograf": "Charming wine bar with a curated list of Czech and international wines.",
}

def parse_kml(kml_file: str) -> Dict:
    """Parse KML file and extract placemarks with their styles."""
    with open(kml_file, 'rb') as f:
        tree = etree.parse(f)
    root = tree.getroot()
    
    # Handle KML namespace
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Extract all placemarks
    placemarks = []
    linestrings = []
    
    for placemark in root.findall('.//kml:Placemark', ns):
        name_elem = placemark.find('kml:name', ns)
        name = name_elem.text if name_elem is not None else 'Unnamed'
        
        style_elem = placemark.find('kml:styleUrl', ns)
        style_url = style_elem.text if style_elem is not None else ''
        style_id = style_url.lstrip('#') if style_url else 'cute'
        
        # Check for Point
        point = placemark.find('.//kml:Point', ns)
        if point is not None:
            coords_elem = point.find('kml:coordinates', ns)
            if coords_elem is not None and coords_elem.text:
                coords_text = coords_elem.text.strip()
                lng, lat, alt = coords_text.split(',')
                placemarks.append({
                    'name': name,
                    'lat': float(lat),
                    'lng': float(lng),
                    'style': style_id,
                    'type': 'point'
                })
        
        # Check for LineString (routes)
        linestring = placemark.find('.//kml:LineString', ns)
        if linestring is not None:
            coords_elem = linestring.find('kml:coordinates', ns)
            if coords_elem is not None and coords_elem.text:
                coords_text = coords_elem.text.strip()
                coords = []
                for coord in coords_text.split():
                    lng, lat, alt = coord.split(',')
                    coords.append([float(lat), float(lng)])
                if coords:
                    linestrings.append({
                        'name': name,
                        'coords': coords,
                        'style': style_id,
                        'type': 'line'
                    })
    
    return {
        'placemarks': placemarks,
        'linestrings': linestrings
    }

def create_folium_map(kml_data: Dict, output_file: str = 'prague_map.html'):
    """Create an interactive Folium map from parsed KML data."""
    
    # Calculate center of map (approximate Prague center)
    center_lat, center_lng = 50.0755, 14.4378
    
    # Create map with a cuter tile style
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=13,
        tiles='CartoDB positron',
        prefer_canvas=True
    )
    
    # Add feature groups for each style
    feature_groups = {
        'cute': folium.FeatureGroup(name='❤️ Romantic Spots', show=True),
        'beer': folium.FeatureGroup(name='🍺 Beer & Nightlife', show=True),
        'food': folium.FeatureGroup(name='🍽️ Food', show=True),
        'view': folium.FeatureGroup(name='🌆 Views & Walks', show=True),
    }
    
    # Add markers from placemarks with custom HTML popups and flyer-style emoji icons
    for placemark in kml_data['placemarks']:
        style = placemark['style']
        color = COLOR_MAP.get(style, 'pink')
        emoji = EMOJI_MAP.get(style, '✨')
        description = PLACE_DESCRIPTIONS.get(
            placemark['name'],
            "A lovely Prague destination with its own special atmosphere."
        )
        
        # Create fancy HTML popup
        popup_html = f'''
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 16px 18px; min-width: 220px; border-radius: 18px;
                    background: linear-gradient(135deg, #ff8a80 0%, #ff80ab 100%);
                    color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.18);">
            <h3 style="margin: 0 0 8px 0; font-size: 17px; letter-spacing: 0.5px;">{placemark['name']}</h3>
            <p style="margin: 0; font-size: 13px; opacity: 0.95; line-height: 1.4;">
                {description}
            </p>
            <p style="margin: 10px 0 0 0; font-size: 12px; opacity: 0.85;">
                Category: {style.title()} · {emoji}
            </p>
        </div>
        '''
        popup = folium.Popup(popup_html, max_width=260, max_height=180)
        
        icon_html = f'''
        <div class="flyer-marker marker-{style}">
            <span class="emoji">{emoji}</span>
        </div>
        '''
        marker_icon = folium.DivIcon(
            html=icon_html,
            icon_size=(48, 48),
            icon_anchor=(24, 24),
            class_name=''
        )
        
        folium.Marker(
            location=[placemark['lat'], placemark['lng']],
            popup=popup,
            tooltip=placemark['name'],
            icon=marker_icon,
        ).add_to(feature_groups.get(style, m))
    
    # We do not render route lines here, keeping the map cleaner and more flyer-like.
    
    # Add feature groups to map
    for fg in feature_groups.values():
        fg.add_to(m)
    
    # Add layer control with nice styling
    folium.LayerControl(collapsed=False, position='topright').add_to(m)
    
    # Add animated title and styling like a flyer
    title_html = '''
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
        @keyframes dash {
            to { stroke-dashoffset: -40; }
        }
        .map-title {
            position: fixed;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            padding: 18px 28px;
            background: radial-gradient(circle at top left, #ffe3f8, #ff9de5);
            border-radius: 999px;
            font-size: 22px;
            font-weight: 800;
            color: #432d5d;
            z-index: 9999;
            box-shadow: 0 18px 40px rgba(255, 102, 204, 0.18);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            animation: float 3.8s ease-in-out infinite;
            letter-spacing: 0.8px;
        }
        .flyer-badge {
            position: fixed;
            top: 95px;
            left: 20px;
            padding: 14px 20px;
            background: linear-gradient(135deg, #fff4e6 0%, #ffb3c6 100%);
            border-radius: 22px;
            color: #5a3d62;
            font-size: 13px;
            font-weight: 600;
            z-index: 9998;
            box-shadow: 0 10px 30px rgba(117, 86, 131, 0.15);
            animation: pulse 4s ease-in-out infinite;
        }
        .flyer-overlay {
            position: fixed;
            bottom: 100px;
            left: 20px;
            width: 220px;
            line-height: 1.5;
            font-size: 12px;
            color: #4b2b6a;
            z-index: 9998;
            background: rgba(255,255,255,0.92);
            border-radius: 24px;
            padding: 16px 18px;
            box-shadow: 0 18px 40px rgba(86, 72, 140, 0.12);
            backdrop-filter: blur(8px);
        }
        .flyer-marker {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.18);
            animation: pulse 2.3s ease-in-out infinite;
        }
        .marker-cute { background: radial-gradient(circle, #ff9de0, #d674ff); }
        .marker-beer { background: radial-gradient(circle, #b6ff7d, #32cd32); }
        .marker-food { background: radial-gradient(circle, #80d4ff, #2b73ff); }
        .marker-view { background: radial-gradient(circle, #ffd26a, #ff7f50); }
        .animated-route {
            stroke-dasharray: 12, 10;
            animation: dash 4s linear infinite;
            stroke-linecap: round;
        }
        .leaflet-container {
            border-radius: 20px;
            overflow: hidden;
        }
        .leaflet-popup-content-wrapper {
            border-radius: 18px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.18) !important;
        }
        .leaflet-popup-tip {
            background: #ff90cb;
        }
        .leaflet-marker-icon {
            filter: drop-shadow(0 6px 18px rgba(0,0,0,0.2));
        }
        .leaflet-control-layers-expanded {
            border-radius: 16px;
            box-shadow: 0 18px 40px rgba(0,0,0,0.18);
        }
    </style>
    <div class="map-title">Prague with You ❤️🍺</div>
    <div class="flyer-badge">Your cute Prague guide: food, beer, views, love</div>
    <div class="flyer-overlay">✨ Wander together<br>🍷 Eat deliciously<br>🌇 Catch sunset views<br>🍺 Toast under fairy lights</div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    m.save(output_file)
    print(f"✨ Map created successfully: {output_file}")
    return output_file

def main():
    """Main function to create the Prague map."""
    kml_file = 'prague_locations.kml'
    
    if not Path(kml_file).exists():
        print(f"Error: {kml_file} not found!")
        return
    
    print("📍 Parsing KML file...")
    kml_data = parse_kml(kml_file)
    print(f"   Found {len(kml_data['placemarks'])} locations and {len(kml_data['linestrings'])} routes")
    
    print("🗺️  Creating Folium map...")
    output_file = create_folium_map(kml_data, 'prague_map.html')
    
    print(f"\n✅ Done! Open {output_file} in your browser to see the map.")

if __name__ == '__main__':
    main()
