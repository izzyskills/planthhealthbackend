from datetime import datetime
import asyncio
import os
import motor.motor_asyncio

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/disease_prediction_db"
)
db = client.get_database()  # Update this to your database name


# Your Disease model
class Disease:
    def __init__(self, name, description, treatments, disease_image, plant):
        self.name = name
        self.description = description
        self.treatments = treatments
        self.disease_image = disease_image
        self.plant = plant
        self.created_at = datetime.utcnow()

    async def save(self):
        result = await db.diseases.insert_one(self.__dict__)
        return result.inserted_id


# Disease information dictionary - you can expand this with real information
disease_info = {
    # Tomato diseases
    "Tomato___Late_blight": {
        "description": "Late blight is a devastating disease caused by the fungus-like organism Phytophthora infestans. It affects leaves, stems, and fruits of tomato plants, causing dark, water-soaked spots that rapidly enlarge and turn brown.",
        "treatments": [
            "Remove and destroy infected plants",
            "Apply fungicides with active ingredients like chlorothalonil or mancozeb",
            "Maintain good air circulation",
            "Avoid overhead watering",
        ],
    },
    "Tomato___Early_blight": {
        "description": "Early blight is caused by the fungus Alternaria solani. It first appears as small brown spots with concentric rings on lower leaves, which can enlarge and cause leaves to yellow and drop.",
        "treatments": [
            "Remove infected leaves",
            "Apply fungicides (copper-based or chlorothalonil)",
            "Ensure adequate plant spacing",
            "Use mulch to prevent soil splash",
        ],
    },
    "Tomato___Septoria_leaf_spot": {
        "description": "Septoria leaf spot is caused by the fungus Septoria lycopersici. It appears as numerous small, circular spots with dark borders and light centers on lower leaves first, then progresses upward.",
        "treatments": [
            "Remove infected leaves",
            "Apply fungicides",
            "Rotate crops",
            "Avoid overhead watering",
        ],
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "TYLCV is a viral disease transmitted by whiteflies. Infected plants show upward curling of leaves, yellowing leaf margins, stunted growth, and flower drop.",
        "treatments": [
            "Control whitefly populations",
            "Use reflective mulches",
            "Remove and destroy infected plants",
            "Use resistant varieties",
        ],
    },
    "Tomato___Bacterial_spot": {
        "description": "Bacterial spot is caused by Xanthomonas species. It appears as small, water-soaked spots on leaves, stems, and fruits that enlarge and turn dark brown to black.",
        "treatments": [
            "Rotate crops",
            "Use copper-based sprays",
            "Avoid overhead irrigation",
            "Plant resistant varieties",
        ],
    },
    "Tomato___Target_Spot": {
        "description": "Target spot is caused by the fungus Corynespora cassiicola. It appears as brown circular spots with concentric rings that can expand and cause severe defoliation.",
        "treatments": [
            "Apply fungicides",
            "Remove infected leaves",
            "Improve air circulation",
            "Avoid overhead watering",
        ],
    },
    "Tomato___Tomato_mosaic_virus": {
        "description": "Tomato mosaic virus causes mottled light and dark green patterns on leaves, stunted growth, and malformation of leaves or fruits.",
        "treatments": [
            "Remove and destroy infected plants",
            "Control aphids which can spread the virus",
            "Sanitize tools",
            "Plant resistant varieties",
        ],
    },
    "Tomato___Leaf_Mold": {
        "description": "Leaf mold is caused by the fungus Passalora fulva. It appears as pale green to yellowish spots on upper leaf surfaces and olive-green to grayish-brown fuzzy mold on lower surfaces.",
        "treatments": [
            "Improve air circulation",
            "Reduce humidity",
            "Apply fungicides",
            "Remove infected leaves",
        ],
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "description": "Two-spotted spider mites are tiny pests that cause stippling (small dots) on leaves, which later turn yellow and bronze. Webbing may be visible under heavy infestation.",
        "treatments": [
            "Spray plants with water",
            "Apply insecticidal soap or neem oil",
            "Introduce predatory mites",
            "Maintain proper humidity",
        ],
    },
    # Apple diseases
    "Apple___Apple_scab": {
        "description": "Apple scab is caused by the fungus Venturia inaequalis. It appears as olive-green to brown spots on leaves and rough, scabby spots on fruits.",
        "treatments": [
            "Apply fungicides",
            "Remove fallen leaves",
            "Prune for air circulation",
            "Plant resistant varieties",
        ],
    },
    "Apple___Black_rot": {
        "description": "Black rot is caused by the fungus Botryosphaeria obtusa. It affects leaves, fruit, and bark, causing frogeye leaf spots, black fruit rot, and cankers on branches.",
        "treatments": [
            "Prune out diseased branches",
            "Remove mummified fruits",
            "Apply fungicides",
            "Maintain tree vigor",
        ],
    },
    "Apple___Cedar_apple_rust": {
        "description": "Cedar apple rust is caused by the fungus Gymnosporangium juniperi-virginianae. It appears as bright orange-yellow spots on leaves and fruits.",
        "treatments": [
            "Remove nearby cedar trees if possible",
            "Apply fungicides",
            "Plant resistant varieties",
            "Remove infected leaves",
        ],
    },
    # Grape diseases
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "description": "Leaf blight in grapes is caused by the fungus Pseudocercospora vitis. It appears as brown spots that may enlarge and cause leaf drop.",
        "treatments": [
            "Apply fungicides",
            "Prune for better air circulation",
            "Remove fallen leaves",
            "Maintain proper vine spacing",
        ],
    },
    "Grape___Black_rot": {
        "description": "Black rot is caused by the fungus Guignardia bidwellii. It appears as circular, reddish-brown spots on leaves and black, mummified fruits.",
        "treatments": [
            "Apply fungicides",
            "Remove mummified berries",
            "Prune for air circulation",
            "Destroy fallen leaves and fruits",
        ],
    },
    "Grape___Esca_(Black_Measles)": {
        "description": "Esca is a complex fungal disease that causes tiger-striped leaf patterns, black spotting on fruits, and eventually vine dieback.",
        "treatments": [
            "Remove and destroy infected vines",
            "Use clean pruning tools",
            "Apply fungicides",
            "Protect pruning wounds",
        ],
    },
    # Other diseases
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "Northern leaf blight is caused by the fungus Exserohilum turcicum. It appears as long, elliptical, grayish-green or tan lesions on corn leaves.",
        "treatments": [
            "Rotate crops",
            "Apply fungicides",
            "Plant resistant varieties",
            "Remove crop debris",
        ],
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "description": "Gray leaf spot is caused by the fungus Cercospora zeae-maydis. It appears as rectangular, gray to tan lesions that follow leaf veins.",
        "treatments": [
            "Rotate crops",
            "Till under crop debris",
            "Apply fungicides",
            "Plant resistant hybrids",
        ],
    },
    "Corn_(maize)___Common_rust_": {
        "description": "Common rust is caused by the fungus Puccinia sorghi. It appears as small, circular to elongate, cinnamon-brown pustules on both leaf surfaces.",
        "treatments": [
            "Apply fungicides",
            "Plant resistant varieties",
            "Destroy volunteer corn",
            "Early planting",
        ],
    },
    "Strawberry___Leaf_scorch": {
        "description": "Leaf scorch is caused by the fungus Diplocarpon earlianum. It appears as small, purple spots on leaves that develop reddish-purple borders and dark brown centers.",
        "treatments": [
            "Remove infected leaves",
            "Apply fungicides",
            "Improve air circulation",
            "Avoid overhead irrigation",
        ],
    },
    "Peach___Bacterial_spot": {
        "description": "Bacterial spot in peaches is caused by Xanthomonas arboricola. It appears as water-soaked lesions on leaves that become angular and purple-brown, and sunken lesions on fruits.",
        "treatments": [
            "Apply copper-based sprays",
            "Prune for better air circulation",
            "Avoid overhead irrigation",
            "Plant resistant varieties",
        ],
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "description": "Powdery mildew in cherries is caused by Podosphaera clandestina. It appears as white powdery spots on leaves and shoots that may cause leaf curling and stunting.",
        "treatments": [
            "Apply fungicides",
            "Prune for air circulation",
            "Remove infected leaves",
            "Avoid excessive nitrogen fertilization",
        ],
    },
    "Potato___Late_blight": {
        "description": "Late blight in potatoes is caused by Phytophthora infestans. It appears as water-soaked lesions on leaves that quickly enlarge and turn brown, and can spread to tubers.",
        "treatments": [
            "Apply fungicides",
            "Destroy volunteer potatoes",
            "Plant resistant varieties",
            "Harvest promptly",
        ],
    },
    "Potato___Early_blight": {
        "description": "Early blight in potatoes is caused by Alternaria solani. It appears as dark brown to black lesions with concentric rings, typically on older leaves first.",
        "treatments": [
            "Apply fungicides",
            "Rotate crops",
            "Maintain adequate plant nutrition",
            "Space plants properly",
        ],
    },
    "Squash___Powdery_mildew": {
        "description": "Powdery mildew in squash is caused by several fungi. It appears as white powdery spots on leaves and stems that may cause leaf yellowing and defoliation.",
        "treatments": [
            "Apply fungicides or baking soda solution",
            "Remove severely infected leaves",
            "Plant resistant varieties",
            "Space plants properly",
        ],
    },
    "Pepper,_bell___Bacterial_spot": {
        "description": "Bacterial spot in peppers is caused by Xanthomonas species. It appears as small, water-soaked spots that enlarge and turn brown, often with yellow halos.",
        "treatments": [
            "Apply copper-based sprays",
            "Rotate crops",
            "Avoid overhead irrigation",
            "Remove infected leaves",
        ],
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "description": "Citrus greening is caused by bacteria spread by psyllid insects. It causes asymmetrical yellow mottling of leaves, misshapen bitter fruits, and eventual tree decline.",
        "treatments": [
            "Control psyllid populations",
            "Remove infected trees",
            "Plant disease-free nursery stock",
            "Apply nutrients to maintain tree health",
        ],
    },
}

# For healthy plants, create a generic description and empty treatments list
healthy_description = "Healthy plant showing no signs of disease or pest damage. Leaves are normal in color, shape, and pattern for the species."
healthy_treatments = []


async def seed_diseases():
    # Get the list of diseases from your provided list
    disease_list = [
        "Tomato___Late_blight",
        "Tomato___healthy",
        "Grape___healthy",
        "Orange___Haunglongbing_(Citrus_greening)",
        "Soybean___healthy",
        "Squash___Powdery_mildew",
        "Potato___healthy",
        "Corn_(maize)___Northern_Leaf_Blight",
        "Tomato___Early_blight",
        "Tomato___Septoria_leaf_spot",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Strawberry___Leaf_scorch",
        "Peach___healthy",
        "Apple___Apple_scab",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Bacterial_spot",
        "Apple___Black_rot",
        "Blueberry___healthy",
        "Cherry_(including_sour)___Powdery_mildew",
        "Peach___Bacterial_spot",
        "Apple___Cedar_apple_rust",
        "Tomato___Target_Spot",
        "Pepper,_bell___healthy",
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "Potato___Late_blight",
        "Tomato___Tomato_mosaic_virus",
        "Strawberry___healthy",
        "Apple___healthy",
        "Grape___Black_rot",
        "Potato___Early_blight",
        "Cherry_(including_sour)___healthy",
        "Corn_(maize)___Common_rust_",
        "Grape___Esca_(Black_Measles)",
        "Raspberry___healthy",
        "Tomato___Leaf_Mold",
        "Tomato___Spider_mites Two-spotted_spider_mite",
        "Pepper,_bell___Bacterial_spot",
        "Corn_(maize)___healthy",
    ]

    # Clear existing data if needed
    await db.diseases.delete_many({})
    print("Cleared existing diseases from database")

    # Insert diseases
    for disease_name in disease_list:
        # Split into plant and condition
        parts = disease_name.split("___")
        plant = parts[0]
        condition = parts[1]

        # Format plant name (replace underscores with spaces, etc.)
        plant_formatted = plant.replace("_", " ")

        # Create a proper name for the disease
        if condition.lower() == "healthy":
            name = f"Healthy {plant_formatted}"
            description = healthy_description
            treatments = healthy_treatments
        else:
            # Format the condition name (replace underscores with spaces)
            condition_formatted = condition.replace("_", " ")
            name = f"{condition_formatted} on {plant_formatted}"

            # Get description and treatments from our dictionary or use generic ones
            disease_key = disease_name
            if disease_key in disease_info:
                description = disease_info[disease_key]["description"]
                treatments = disease_info[disease_key]["treatments"]
            else:
                description = f"A common disease affecting {plant_formatted} plants. It requires prompt treatment to prevent crop damage."
                treatments = [
                    "Remove infected plant parts",
                    "Apply appropriate fungicides or insecticides",
                    "Improve plant nutrition and growing conditions",
                ]

        # Create disease object
        disease = Disease(
            name=name,
            description=description,
            treatments=treatments,
            disease_image=disease_name,  # Using original name as image identifier
            plant=plant_formatted,
        )

        # Save to database
        inserted_id = await disease.save()
        print(f"Inserted: {name} with ID: {inserted_id}")

    # Get count of inserted documents
    count = await db.diseases.count_documents({})
    print(f"Database seeded with {count} diseases")


# Run the async function
if __name__ == "__main__":
    asyncio.run(seed_diseases())
