from fastapi import FastAPI, APIRouter
from shapely.geometry import Point
import geopandas as gpd
import json

router = APIRouter(prefix="/api/nearby-places", tags=["nearby-places"])


@router.get("/api/nearby-places")
def get_nearby_places(lat: float, lon: float):
    hotel_point = Point(lon, lat)

    df = gpd.GeoDataFrame(
        crs="EPSG:4326"
    )
    df["distance_km"] = df.geometry.distance(hotel_point) * 111

    nearby = df[df["distance_km"] < 1]
    return json.loads(nearby.to_json())
