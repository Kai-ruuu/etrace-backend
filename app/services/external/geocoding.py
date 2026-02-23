from fastapi import HTTPException
from geopy.geocoders import Nominatim


class GeocodingService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="e-trace")


    def geocode(self, address: str) -> dict:
        try:
            location = self.geolocator.geocode(
                query=address,
                timeout=60
            )

            if location is None:
                raise HTTPException(404, "Address not found.")
            
            return {
                "address": location.address,
                "latitude": location.latitude,
                "longitude": location.longitude,
            }
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500, detail="Unable to geocode address.")