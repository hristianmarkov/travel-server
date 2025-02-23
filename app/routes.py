from flask import request, jsonify
import openai
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def setup_routes(app):
    @app.route('/generate-trip-overview', methods=['POST'])
    def generate_trip_overview():
        """Generates a short 6-sentence trip overview."""
        try:
            data = request.json
            destination = data.get("destination", "a popular travel destination")
            budget = data.get("budget", "mid-range")
            departure_date = data.get("departureDate", "2025-01-01")
            return_date = data.get("returnDate", "2025-01-07")
            focus = ", ".join([key for key, value in data.items() if value is True and key in [
                "unique", "culture", "food", "nature", "adventure", "relaxation", "nightlife", "shopping"]]) or "general tourism"
            accommodation = ", ".join([key for key, value in data.items() if value is True and key in [
                "hotels", "resorts", "hostels", "villas", "rentals"]]) or "hotels"
            pace = data.get("pace", "balanced")

            # Construct prompt
            prompt = f"""
            You are a professional travel agent. Return only valid JSON (no extra text, quotes, or disclaimers) with exactly six fields.

            Generate the following JSON structure for a {budget} budget trip to {destination} from {departure_date} to {return_date}, focusing on {focus}, with {accommodation} accommodation and a {pace} travel pace:

            {{
            "date": "Explain why {departure_date} to {return_date} is a good time to visit {destination}.",
            "budget": "Explain why a {budget} budget fits this trip well.",
            "location": "Explain what makes {destination} unique or attractive.",
            "focus": "Explain why {destination} is good for {focus}.",
            "accommodation": "Explain why {accommodation} is suitable for this trip.",
            "pace": "Explain why a {pace} travel pace works best."
            }}
            """


            # OpenAI API Call
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional travel agent"},
                    {"role": "user", "content": prompt}
                ]
            )

            itinerary = chat_completion.choices[0].message.content

            return jsonify({"itinerary": itinerary}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route('/generate-trip-breakdown', methods=['POST'])
    def generate_trip_breakdown():
        """Generates a high-level day-by-day itinerary."""
        try:
            data = request.json
            destination = data.get("destination", "Paris")
            num_days = int(data.get("howManyDays", 5))

            prompt = f"""
            Generate a {num_days}-day itinerary for a trip to {destination}.
            Provide 3-5 activities per day in JSON:
            {{
              "days": [
                {{"day": 1, "activities": ["Visit Eiffel Tower", "Explore Louvre", "Dinner in a bistro"]}},
                {{"day": 2, "activities": ["Day trip to Versailles", "Seine River walk", "Wine tasting"]}}
              ]
            }}
            """

            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional travel agent"},
                    {"role": "user", "content": prompt}
                ]
            )

            itinerary = chat_completion.choices[0].message.content

            return jsonify({"itinerary": itinerary}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route('/generate-trip-details', methods=['POST'])
    def generate_trip_details():
        """Expands each day’s activities with descriptions, costs, and durations."""
        try:
            data = request.json
            destination = data.get("destination", "Paris")
            day = data.get("day", 1)
            activities = data.get("activities", [])

            if not activities:
                return jsonify({"error": "No activities provided"}), 400

            activities_list = ", ".join(activities)
            prompt = f"""
            Provide a breakdown for Day {day} in {destination}:
            Activities: {activities_list}

            For each, provide:
            - Description
            - Duration
            - Cost per person
            - Why visit.

            Format:
            {{
              "day": {day},
              "details": [
                {{"activity": "Eiffel Tower", "description": "...", "duration": "2 hours", "cost": "$20", "why_visit": "..."}}
              ]
            }}
            """

            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional travel agent"},
                    {"role": "user", "content": prompt}
                ]
            )

            itinerary = chat_completion.choices[0].message.content

            return jsonify({"itinerary": itinerary}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
