# 🗺️ Prague Travel Map Creator

A cute interactive map of Prague locations for your trip with your girlfriend! Converts a KML file into a beautiful Folium-powered HTML map with categories like romantic spots, food, nightlife, and scenic views.

## Features

✨ **Beautiful interactive map** with customized markers
❤️ **Category-based organization** (romantic, food, beer, views)
🎨 **Color-coded markers** for easy navigation
📍 **Popup information** for each location
🛤️ **Route visualization** showing your planned path

## Requirements

- Python 3.7+
- folium
- lxml (for better KML parsing)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your KML file is named `prague_locations.kml`
2. Run the script:

```bash
python create_map.py
```

3. Open `prague_map.html` in your browser to view the interactive map!

## KML Format

The script expects a KML file with:
- **Folders** for categories (optional but organized)
- **Placemarks** with Point or LineString geometries
- **Styles** with style IDs (cute, beer, food, view)
- **Coordinates** in the format: `longitude,latitude,altitude`

### Style Categories

- `cute` - Romantic/quiet spots (pink/purple markers)
- `beer` - Beer bars & nightlife (green markers)
- `food` - Restaurants & cafes (blue markers)
- `view` - Scenic viewpoints (orange markers)

## Map Output

The generated `prague_map.html` includes:
- Interactive map centered on Prague
- Toggleable feature layers
- Hover tooltips for location names
- Click popups for more information
- Title overlay with custom styling

## Customization

Edit `create_map.py` to:
- Change map tiles (search for folium tile providers)
- Modify marker colors in `COLOR_MAP`
- Adjust zoom level (default: 13)
- Add different marker icons in `ICON_MAP`

Enjoy your Prague adventure! 🍺❤️
