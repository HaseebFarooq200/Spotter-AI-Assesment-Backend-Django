import googlemaps
from decouple import config
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import math


class TripViewSet(APIView):
    permission_classes = []

    def post(self, request):
        GOOGLE_MAPS_API_KEY = config("GOOGLE_MAPS_API_KEY")

        current_location = request.data.get("CurrentLocation")
        pickup_location = request.data.get("PickupLocation")
        dropoff_location = request.data.get("DropoffLocation")
        current_cycle_used = float(request.data.get("CurrentCycleUsed", 0))

        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

        # Geocode helper
        def geocode(address):
            result = gmaps.geocode(address)
            if result:
                loc = result[0]["geometry"]["location"]
                return (loc["lat"], loc["lng"])
            return None

        coords = [
            geocode(current_location),
            geocode(pickup_location),
            geocode(dropoff_location),
        ]

        if None in coords:
            return Response(
                {"error": "Failed to geocode one or more addresses"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Directions request
        route = gmaps.directions(
            origin=coords[0],
            destination=coords[2],
            waypoints=[coords[1]],
            mode="driving",
        )

        if not route:
            return Response(
                {"error": "No route found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract distance & duration
        leg = route[0]["legs"][0]
        total_distance_km = leg["distance"]["value"] / 1000
        total_duration_hr = leg["duration"]["value"] / 3600

        # Add pickup + dropoff buffers (1hr each)
        total_duration_hr += 2

        # ELD limits
        max_drive_per_day = 11
        max_on_duty = 14
        rest_period = 10
        max_cycle = 70

        # Calculate required days
        required_days = math.ceil(total_duration_hr / max_drive_per_day)

        # Fuel stops (every 1600 km)
        num_fuel_stops = math.floor(total_distance_km / 1600)

        stops = []
        for i in range(num_fuel_stops):
            stops.append({"type": "fuel", "day": (i % required_days) + 1})

        for d in range(required_days):
            stops.append({"type": "rest", "day": d + 1})

        # Generate ELD log sheets
        def generate_logs(total_hours):
            logs = []
            remaining = total_hours
            day = 1
            while remaining > 0:
                drive_today = min(remaining, max_drive_per_day)
                duty_today = drive_today + 3
                duty_today = min(duty_today, max_on_duty)

                log = {
                    "day": day,
                    "events": [
                        {"status": "off-duty", "start": 0, "end": 5},
                        {"status": "sleeper-berth", "start": 5, "end": 6},
                        {"status": "on-duty", "start": 6, "end": 7},
                        {"status": "driving", "start": 7, "end": 7 + drive_today},
                        {"status": "on-duty", "start": 7 + drive_today, "end": duty_today + 6},
                        {"status": "sleeper-berth", "start": duty_today + 6, "end": duty_today + 8},
                        {"status": "off-duty", "start": duty_today + 8, "end": 24},
                    ],
                }
                logs.append(log)

                remaining -= drive_today
                day += 1
            return logs

        eld_logs = generate_logs(total_duration_hr)

        remaining_cycle = max_cycle - (current_cycle_used + total_duration_hr)

        return Response(
            {
                "route": route,
                "summary": {
                    "total_distance_km": round(total_distance_km, 2),
                    "total_duration_hr": round(total_duration_hr, 2),
                    "required_days": required_days,
                    "remaining_cycle_hours": remaining_cycle,
                },
                "stops": stops,
                "eld_logs": eld_logs,
                "cycle_used": current_cycle_used,
            },
            status=status.HTTP_200_OK,
        )
