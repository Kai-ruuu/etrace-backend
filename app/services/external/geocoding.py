from geopy.geocoders import Nominatim


class GeocodingService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="e-trace")


    def geocode(self, address: str) -> dict:
        location = self.geolocator.geocode(
            query=address,
            timeout=60
        )
        return {
            "address": location.address,
            "coords": {
                "latitude": location.latitude,
                "longitude": location.longitude,
            }
        }