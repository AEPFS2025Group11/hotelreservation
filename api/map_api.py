from fastapi import FastAPI, APIRouter
from shapely.geometry import Point
import geopandas as gpd
import json

router = APIRouter(prefix="/api/nearby-places", tags=["nearby-places"])


@router.get("/api/nearby-places")
def get_nearby_places(lat: float, lon: float):
    hotel_point = Point(lon, lat)

    places = [
        {"name": "Grossmünster", "type": "sehenswürdigkeit", "lat": 47.3706, "lon": 8.5456},
        {"name": "Kunsthaus Zürich", "type": "sehenswürdigkeit", "lat": 47.3702, "lon": 8.5480},
        {"name": "Sprüngli", "type": "restaurant", "lat": 47.3686, "lon": 8.5383},
    ]

    df = gpd.GeoDataFrame(
        places,
        geometry=gpd.points_from_xy([p["lon"] for p in places], [p["lat"] for p in places]),
        crs="EPSG:4326"
    )
    df["distance_km"] = df.geometry.distance(hotel_point) * 111

    nearby = df[df["distance_km"] < 1]
    return json.loads(nearby.to_json())
