import os
import django
import re

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agri_portal.settings")
django.setup()

from portal.models import User, FarmerQuery, ExpertResponse, Crop, ActivityLog

def populate_data():
    # 1. Ensure we have a farmer and an expert to attribute the questions to
    expert, created = User.objects.get_or_create(
        username='expert_john', 
        defaults={'email': 'john@agriportal.com', 'role': 'EXPERT'}
    )
    if created:
        expert.set_password('john123')
        expert.save()
        print("Created new expert account: expert_john")
        
    farmer, created = User.objects.get_or_create(
        username='farmer_bob', 
        defaults={'email': 'bob@farm.com', 'role': 'FARMER'}
    )
    if created:
        farmer.set_password('password123')
        farmer.save()
        print("Created new farmer account: farmer_bob")

    # 2. Parse the markdown QA dataset
    filepath = os.path.join(os.path.dirname(__file__), 'agriculture_qa_dataset.md')
    if not os.path.exists(filepath):
        print(f"Error: Could not find {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to match Farmer Question and Expert Answer pairs
    pattern = re.compile(r'\*\*\d+\.\s*Farmer Question:\*\*\s*(.*?)\r?\n\*\*Expert Answer:\*\*\s*(.*?)(?=\r?\n\r?\n|\r?\n##|\Z)', re.DOTALL)
    matches = pattern.findall(content)

    if not matches:
        print("No questions found using regex parser.")
    else:
        # Clear old questions for a clean slate
        FarmerQuery.objects.all().delete()
        print("Cleared previous Q&A data.")

    count = 0
    for question, answer in matches:
        question = question.strip()
        answer = answer.strip()
        
        # Create the Query
        query = FarmerQuery.objects.create(
            farmer=farmer, 
            question=question, 
            is_answered=True
        )
        
        # Create the Response
        ExpertResponse.objects.create(
            query=query, 
            expert=expert, 
            answer=answer
        )
        count += 1
    
    print(f"Successfully loaded {count} advanced Q&A pairs into the database.")

    # 3. Add basic Crop Information so the Crop Database is also populated
    crops_to_add = [
        ("Rice", "Cereal", "Summer/Kharif", "Clay or Clay Loam", "NPK 120:60:40 kg/ha", "Rice is a water-intensive staple cereal crop that thrives in flooded conditions. It requires careful nitrogen management and monitoring for pests like stem borers. Early detection of blast disease is critical for preventing yield loss."),
        ("Wheat", "Cereal", "Winter/Rabi", "Loam to Clay Loam", "NPK 120:60:40 kg/ha", "Wheat is the world's most planted grain, preferring cool winter climates followed by warm, dry springs. It demands precision irrigation at the crown root initiation (CRI) and flowering stages. Yellow rust is a major threat in humid zones."),
        ("Potato", "Vegetable", "Winter/Spring", "Sandy Loam", "NPK 150:100:100 kg/ha", "Potatoes are high-yielding tuber crops that require loose, well-draining soils for unhindered bulb expansion. Susceptible to Late Blight, prophylactic fungicide sprays are required during periods of high humidity and low temperatures."),
        ("Maize (Corn)", "Cereal", "Summer/Monsoon", "Well-drained Loam", "NPK 120:60:40 kg/ha", "An extremely versatile cereal crop used for food, livestock feed, and biofuels. Maize suffers heavily from waterlogging and requires optimal nitrogen to maximize grain set. Fall Armyworm is an economically devastating pest."),
        ("Tomato", "Vegetable", "Year-round", "Sandy to Clay Loam", "NPK 100:50:50 kg/ha", "A high-value, nutrient-demanding horticultural crop. Proper trellis support and pruning drastically reduce soil-borne diseases. Consistent irrigation prevents Blossom End Rot by ensuring proper calcium uptake."),
        ("Onion", "Vegetable", "Winter/Rabi", "Sandy Loam", "NPK 100:50:50 kg/ha", "A commercially crucial bulb crop. Onions possess shallow root systems and require frequent, light irrigations. Proper curing (drying) before storage is mandatory to prevent neck rot and post-harvest losses."),
        ("Soybean", "Legume / Oilseed", "Summer/Kharif", "Medium Loam", "NPK 20:60:40 kg/ha", "A premier protein and oilseed crop. Soybeans form symbiotic relationships with nitrogen-fixing soil bacteria, reducing the need for synthetic nitrogen fertilizers. Highly susceptible to Yellow Mosaic Virus transmitted by whiteflies."),
        ("Sugarcane", "Cash Crop", "Year-round", "Deep, rich Loamy", "NPK 250:100:100 kg/ha", "A long-duration, high-biomass cash crop grown predominantly for sugar extraction. It demands high water and fertility inputs over a 12-18 month cycle. Red rot is a serious fungal disease capable of wiping out entire plantations.")
    ]
    
    crop_count = 0
    for c in crops_to_add:
        name, category, season, soil, fert, desc = c
        obj, created = Crop.objects.get_or_create(crop_name=name, defaults={
            'category': category,
            'season': season,
            'soil_type': soil,
            'fertilizer': fert,
            'description': desc
        })
        if created:
            crop_count += 1
            
    print(f"Successfully loaded {crop_count} featured crops.")

    # Add an activity log entry
    ActivityLog.objects.create(
        user=expert, 
        action="Imported 30 advanced QA records and established 8 base crops."
    )
    
if __name__ == '__main__':
    populate_data()
