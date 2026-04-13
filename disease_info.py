"""
disease_info.py - Clinical descriptions, precautions, and metadata per class
"""

DISEASE_INFO = {
    "Acne": {
        "emoji": "🔴",
        "description": (
            "Acne vulgaris is a chronic inflammatory skin condition involving "
            "hair follicles and sebaceous glands. It manifests as blackheads, "
            "whiteheads, papules, pustules, or cysts, most commonly on the face, "
            "chest, and back."
        ),
        "precautions": [
            "Wash affected areas gently twice a day with a mild cleanser",
            "Avoid touching or popping pimples to prevent scarring",
            "Use non-comedogenic (oil-free) skincare and makeup products",
            "Stay hydrated and maintain a balanced diet",
            "Consult a dermatologist if severe or persistent",
        ],
        "severity": "Mild to Moderate",
        "color": "#FF6B6B",
    },
    "Acne_Scars": {
        "emoji": "🟤",
        "description": (
            "Acne scars are permanent textural changes or indentations in the skin "
            "that result from severe acne. They occur when the dermis is damaged "
            "during the healing process of inflamed acne lesions."
        ),
        "precautions": [
            "Apply broad-spectrum sunscreen (SPF 30+) daily to prevent darkening",
            "Avoid picking or squeezing existing acne to prevent new scars",
            "Use gentle exfoliants containing AHA/BHA ingredients",
            "Keep skin well-moisturized to support healing",
            "Consult a dermatologist for treatment options (laser, microneedling, etc.)",
        ],
        "severity": "Cosmetic",
        "color": "#B8860B",
    },
    "Contact_Dermatitis": {
        "emoji": "🟠",
        "description": (
            "Contact dermatitis is a localized inflammatory skin reaction caused by "
            "direct contact with an irritant (irritant contact dermatitis) or allergen "
            "(allergic contact dermatitis). It presents as red, itchy, sometimes blistered skin."
        ),
        "precautions": [
            "Identify and avoid the triggering substance or allergen",
            "Rinse the affected area with cool water immediately after contact",
            "Apply cool, wet compresses to soothe irritated skin",
            "Avoid scratching to prevent secondary infection",
            "See a doctor if reaction is severe, spreading, or involves eyes/throat",
        ],
        "severity": "Mild to Severe",
        "color": "#FF8C00",
    },
    "Eczema_Atopic_Dermatitis": {
        "emoji": "🔵",
        "description": (
            "Atopic dermatitis (eczema) is a chronic, relapsing inflammatory skin condition "
            "characterized by dry, itchy, and inflamed skin. It is associated with a "
            "dysfunctional skin barrier and is often linked to other allergic conditions."
        ),
        "precautions": [
            "Moisturize skin at least twice daily with fragrance-free emollients",
            "Take short, lukewarm showers and pat skin dry gently",
            "Wear soft, breathable fabrics like cotton",
            "Avoid known triggers such as stress, sweat, harsh soaps, and allergens",
            "Follow prescribed treatment plans from a dermatologist",
        ],
        "severity": "Chronic / Moderate to Severe",
        "color": "#4169E1",
    },
    "Folliculitis": {
        "emoji": "🟡",
        "description": (
            "Folliculitis is the inflammation of one or more hair follicles, "
            "caused by bacterial (commonly Staphylococcus aureus), fungal, or viral "
            "infections. It presents as small red bumps or white-headed pimples around follicles."
        ),
        "precautions": [
            "Keep skin clean and avoid sharing towels, razors, or clothing",
            "Shave carefully with a clean, sharp razor in the direction of hair growth",
            "Avoid tight clothing that causes friction on skin",
            "Use warm compresses to relieve discomfort",
            "Seek medical attention if infection spreads or does not improve",
        ],
        "severity": "Mild to Moderate",
        "color": "#FFD700",
    },
    "Fungal_Infection": {
        "emoji": "🍄",
        "description": (
            "Fungal skin infections (dermatomycoses) are caused by various fungi "
            "including dermatophytes, yeasts, and molds. Common types include ringworm, "
            "athlete's foot, and jock itch, presenting as ring-shaped, scaly, itchy rashes."
        ),
        "precautions": [
            "Keep affected areas clean and completely dry",
            "Wear breathable, moisture-wicking clothing and socks",
            "Avoid sharing personal items like towels, socks, or shoes",
            "Change socks and underwear daily",
            "Use antifungal powder in high-moisture areas as prevention",
        ],
        "severity": "Mild to Moderate",
        "color": "#228B22",
    },
    "Hyperpigmentation": {
        "emoji": "🟫",
        "description": (
            "Hyperpigmentation refers to darkened patches of skin caused by excess "
            "melanin production. It can be triggered by sun exposure, inflammation "
            "(post-inflammatory hyperpigmentation), hormonal changes, or medications."
        ),
        "precautions": [
            "Apply broad-spectrum SPF 30+ sunscreen every day, even indoors",
            "Wear protective clothing and hats in direct sunlight",
            "Avoid picking at skin lesions, scabs, or acne",
            "Use gentle, brightening skincare products with vitamin C or niacinamide",
            "Consult a dermatologist for targeted treatment options",
        ],
        "severity": "Cosmetic",
        "color": "#8B4513",
    },
    "NormalSkin": {
        "emoji": "✅",
        "description": (
            "No significant skin disease detected. The skin appears to be in a healthy, "
            "normal condition without visible signs of common dermatological conditions. "
            "Routine skincare and sun protection are recommended."
        ),
        "precautions": [
            "Maintain a consistent skincare routine: cleanse, moisturize, and protect",
            "Apply SPF 30+ sunscreen daily for UV protection",
            "Stay hydrated and eat a balanced diet rich in antioxidants",
            "Get adequate sleep and manage stress levels",
            "Schedule annual skin check-ups with a dermatologist",
        ],
        "severity": "None",
        "color": "#00C851",
    },
    "Pseudofolliculitis_Barbae": {
        "emoji": "🪒",
        "description": (
            "Pseudofolliculitis barbae (razor bumps) is a chronic inflammatory condition "
            "where shaved hairs curl back into the skin, causing foreign body reactions. "
            "It predominantly affects individuals with curly hair in beard and neck areas."
        ),
        "precautions": [
            "Let facial hair grow out and trim instead of close shaving",
            "Use a single-blade razor and shave in the direction of hair growth",
            "Apply warm compresses before shaving to soften hair",
            "Use gentle chemical exfoliants to free ingrown hairs",
            "Consider laser hair removal as a long-term solution (consult dermatologist)",
        ],
        "severity": "Mild to Moderate",
        "color": "#9370DB",
    },
    "Rosacea": {
        "emoji": "🌹",
        "description": (
            "Rosacea is a chronic inflammatory skin condition primarily affecting the face, "
            "causing persistent redness, visible blood vessels (telangiectasia), and sometimes "
            "acne-like bumps. It is often triggered by environmental and lifestyle factors."
        ),
        "precautions": [
            "Identify and avoid personal triggers (spicy food, alcohol, sun, heat, stress)",
            "Use gentle, fragrance-free skincare products for sensitive skin",
            "Apply sunscreen daily — UV exposure is a major trigger",
            "Avoid extreme temperatures, hot beverages, and vigorous exercise",
            "Follow a dermatologist's treatment plan for flare management",
        ],
        "severity": "Chronic / Moderate",
        "color": "#FF69B4",
    },
    "Seborrheic_Dermatitis": {
        "emoji": "❄️",
        "description": (
            "Seborrheic dermatitis is a common, chronic inflammatory skin condition "
            "affecting sebaceous gland-rich areas (scalp, face, chest). It causes "
            "scaly patches, red skin, and stubborn dandruff, often linked to Malassezia yeast."
        ),
        "precautions": [
            "Use antifungal shampoos containing ketoconazole or selenium sulfide regularly",
            "Avoid harsh products that strip the skin's natural oils",
            "Manage stress, which can worsen flares",
            "Gently remove scales — do not scratch or pick",
            "See a dermatologist for prescription treatments during severe flares",
        ],
        "severity": "Chronic / Mild to Moderate",
        "color": "#87CEEB",
    },
    "Sunburn": {
        "emoji": "☀️",
        "description": (
            "Sunburn is acute skin inflammation caused by overexposure to UV radiation. "
            "It presents as red, warm, painful, and sometimes blistered skin, and is a "
            "significant risk factor for long-term skin damage and melanoma."
        ),
        "precautions": [
            "Apply cool (not ice-cold) compresses or take cool baths for relief",
            "Use aloe vera gel or after-sun lotion to soothe and moisturize",
            "Stay hydrated — drink plenty of water",
            "Avoid further sun exposure until healed; wear protective clothing",
            "Seek medical attention if severe blistering, fever, or nausea occurs",
        ],
        "severity": "Mild to Severe",
        "color": "#FF4500",
    },
    "Vitiligo": {
        "emoji": "🤍",
        "description": (
            "Vitiligo is a chronic autoimmune disorder where melanocytes are destroyed, "
            "causing irregular white patches of skin due to loss of pigment. It can affect "
            "any body part and may expand over time, though it is not contagious or painful."
        ),
        "precautions": [
            "Apply high-SPF (50+) sunscreen to depigmented patches — they burn easily",
            "Consider camouflage cosmetics to cover patches if desired",
            "Protect skin from trauma, as injuries may trigger new patches (Koebner effect)",
            "Join a support group; vitiligo can have significant emotional impact",
            "Consult a dermatologist about repigmentation therapies (phototherapy, biologics)",
        ],
        "severity": "Chronic / Cosmetic",
        "color": "#E0E0E0",
    },
}
