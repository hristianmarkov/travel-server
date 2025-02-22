import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains


@app.route('/api/generate', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json

        # Validation Checks
        errors = []
        if not data.get("howManyPeople"):
            errors.append("howManyPeople is required.")
        if not data.get("randomDestination") and not data.get("destination"):
            errors.append("destination is required when randomDestination is false.")
        if not data.get("randomDates") and (not data.get("departureDate") or not data.get("returnDate")):
            errors.append("departureDate and returnDate are required when randomDates is false.")
        if not data.get("budget") and not data.get("desiredDailyBudget"):
            errors.append("Either desiredDailyBudget or budget range must be provided.")

        if errors:
            return jsonify({"error": " ".join(errors)}), 400

        # Build AI Prompt
        prompt = f"""
        You are a professional travel planner creating a **detailed, structured, and engaging HTML-based travel itinerary**. 
        Format the response using **HTML tags** to ensure proper styling when displayed on a website. 

        - Use **<strong> for bold text**.
        - Use **<br> for line breaks**.
        - Use **tables** for structured information like schedules.
        - Wrap the entire response in a **<div>** so it can be styled in CSS.

        - **Random Destination:** {data.get("randomDestination")}
        - **Destination:** {data.get("destination")}
        - **Random Dates:** {data.get("randomDates")}
        - **Departure Date:** {data.get("departureDate")}
        - **Return Date:** {data.get("returnDate")}
        - **People:** {data.get("howManyPeople")}
        - **Budget:** {data.get("budget") or "Not specified"}
        - **Desired Daily Budget:** {data.get("desiredDailyBudget") or "Not specified"}
        - **Interests:** {", ".join([key for key, value in data.items() if value and key in ["culture", "food", "nature", "adventure", "relaxation", "nightlife", "shopping"]]) or "None specified"}
        - **Accommodation Preferences:** {", ".join([key for key, value in data.items() if value and key in ["hotels", "resorts", "hostels", "villas", "rentals", "unique"]]) or "None specified"}
        - **Pace:** {data.get("pace") or "Not specified"}
        - **Additional Information:** {data.get("extraInformation") or "None"}

        ---

        ## **1️⃣ Trip Overview**
        📍 **Destination:** {data.get("destination") or "A Surprise Adventure"}  
        📅 **Dates:** {data.get("departureDate")} → {data.get("returnDate")}  
        👥 **Number of Travelers:** {data.get("howManyPeople")}  
        💰 **Budget Range:** {data.get("budget") or "Not specified"}  
        🏃 **Travel Pace:** {data.get("pace") or "Balanced"}  
        📌 **Best Time to Visit:** _(Is this a good season to travel? Mention climate, tourist crowds, etc.)_  
        🎭 **Fun Facts:** _(2-3 unique cultural, historical, or quirky facts about the destination.)_  

        📸 **Image of the Destination:** _(Provide an image URL that represents the destination well.)_  

        ---

        ## **2️⃣ Daily Itinerary Breakdown**
        Plan a **detailed daily itinerary**, including activities, times, and costs.

        ### **Day 1 - Arrival in {data.get("destination") or "Your Adventure Begins"}**
        | Time  | Activity | Estimated Cost |
        |-------|----------|---------------|
        | 08:00 AM | **Breakfast at a famous local spot (mention specific cafe/restaurant)** | ${data.get("desiredDailyBudget") or "Not specified"} |
        | 09:30 AM | **Visit a must-see landmark (e.g., a historical site, famous attraction, or scenic spot)** | Include details & cost |
        | 11:00 AM | **Explore a popular local market (best items to buy, unique experiences)** | Free |
        | 01:00 PM | **Lunch at a top-rated restaurant (mention must-try dishes)** | $15 per person |
        | 02:30 PM | **Guided tour of a cultural or historical site (explain why it’s worth visiting, insider tips)** | $30 |
        | 05:00 PM | **Relax at a beautiful park, beach, or viewpoint (describe the best things to do there)** | Free |
        | 07:30 PM | **Dinner with a scenic view (restaurant name & specialty food)** | $25 per person |
        | 09:00 PM | **Nightlife options (recommend bars, rooftop lounges, or cultural shows)** | $$ |

        🚕 **Travel Time Between Locations:** _(Include estimated travel times for taxis, public transport, or walking.)_

        🔹 Repeat the **same format for each day** based on the length of stay.

        ---

        ## **3️⃣ Accommodation Recommendations**
        🏨 **Top Hotels on Booking.com**  
        _(List 2-3 highly rated hotels with pricing, locations, and links.)_

        🏡 **Best Airbnb Stays**  
        _(List 2-3 cozy Airbnb options with pricing and direct links.)_

        ---

        ## **4️⃣ Essential Travel Tips**
        ✅ **Local Etiquette & Customs** _(Important do's and don’ts in the destination.)_  
        ✅ **Weather Forecast for Selected Dates** _(Expected temperatures, rainfall, or seasonal events.)_  
        ✅ **Packing Tips Based on the Season** _(What to bring, best outfits, and must-have travel gear.)_  
        ✅ **Best Local Dishes to Try** _(Signature foods and where to find them.)_  
        ✅ **Best Travel Apps to Use in {data.get("destination") or "the country"}** _(Apps for navigation, translations, and local recommendations.)_  

        ---

        ✈️ **Make this itinerary highly engaging, professional, and visually appealing, as if it were crafted by a top-tier travel agency!**  
        """


        
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
                messages=[
                {"role":"system","content":"You are a professional travel agent"},
                {"role":"user","content":prompt}
            ]
        )
        
        itinerary = chat_completion.choices[0].message.content

        return jsonify({"itinerary": itinerary}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while generating the itinerary."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)