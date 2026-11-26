"""Comprehensive agronomic disease knowledge base for PlantVillage classes and base repo crops."""

from typing import Dict, Any

DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    # --- APPLE ---
    "Apple___Apple_scab": {
        "plant": "Apple",
        "display_name": "Apple Scab",
        "is_healthy": False,
        "description": "Apple scab produces velvety, olive-green to dark brown circular lesions on leaves, which gradually turn black and corky. Affected leaves often distort, turn yellow, and drop prematurely.",
        "cause": "Fungal infection caused by Venturia inaequalis. Thrives in cool, damp, and rainy spring conditions where foliage remains wet for prolonged periods.",
        "treatment": "Prune infected twigs and heavily spotted foliage. Apply appropriate copper-based or captan fungicides at bud break and petal fall according to label instructions.",
        "prevention": "Rake and destroy fallen leaves in autumn to eliminate overwintering spores. Prune tree canopies to maximize sunlight penetration and air circulation. Plant scab-resistant cultivars (such as Liberty or Enterprise)."
    },
    "Apple___Black_rot": {
        "plant": "Apple",
        "display_name": "Black Rot",
        "is_healthy": False,
        "description": "Characterized by 'frog-eye' leaf spots—small purple flecks enlarging into circular brown lesions with purple margins. Can also cause fruit mummification and branch cankers.",
        "cause": "Fungal pathogen Botryosphaeria obtusa. Overwinters in mummified apples, dead wood, and bark cankers, spreading via windblown rain.",
        "treatment": "Remove and prune out all cankers, dead branches, and mummified fruit during winter dormancy. Apply thiophanate-methyl or captan fungicide sprays during early season growth.",
        "prevention": "Maintain tree vigor with balanced fertilizer. Promptly remove diseased tree debris and sanitize pruning tools between cuts with 70% alcohol or diluted bleach."
    },
    "Apple___Cedar_apple_rust": {
        "plant": "Apple",
        "display_name": "Cedar Apple Rust",
        "is_healthy": False,
        "description": "Bright yellow-orange or reddish-orange circular spots on the upper leaf surfaces, later developing small tube-like fruiting structures (aecia) underneath the leaf.",
        "cause": "Fungus Gymnosporangium juniperi-virginianae, which requires both an apple/crabapple and an Eastern red cedar / juniper host to complete its two-year life cycle.",
        "treatment": "Apply protectant fungicides (such as myclobutanil or mancozeb) starting when cedar galls form gelatinous horns in spring until terminal shoot growth halts.",
        "prevention": "Remove cedar galls and eradicate wild Eastern red cedars within 1 to 2 miles of orchards where feasible. Choose resistant apple varieties like Redfree, Prima, or William's Pride."
    },
    "Apple___healthy": {
        "plant": "Apple",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "The foliage is vibrant, uniformly green, free from spots, discoloration, or deformities. Leaf margins are crisp and cellular structure is strong.",
        "cause": "Optimal plant health with balanced irrigation, nutrient management, and absence of active fungal or bacterial pathogens.",
        "treatment": "No corrective treatment needed. Maintain regular cultural practices.",
        "prevention": "Continue standard seasonal monitoring, balanced fertilization, mulching, and proper pruning for light airflow."
    },

    # --- BLUEBERRY ---
    "Blueberry___healthy": {
        "plant": "Blueberry",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Leaves display deep green coloration with intact cuticles, without signs of chlorosis, blight, or powdery mildew.",
        "cause": "Optimal soil acidity (pH 4.5–5.2), adequate organic matter, and effective moisture drainage.",
        "treatment": "No treatment required. The bush is performing vigorously.",
        "prevention": "Maintain acidic soil pH through elemental sulfur or acid-forming fertilizers, mulch with pine bark, and irrigate with clean, low-salinity water."
    },

    # --- CHERRY ---
    "Cherry_(including_sour)___Powdery_mildew": {
        "plant": "Cherry",
        "display_name": "Powdery Mildew",
        "is_healthy": False,
        "description": "White powdery fungal patches appear on young leaves and succulent shoots. Leaves often cup, curl upward, crinkle, and become stunted or distorted.",
        "cause": "Fungus Podosphaera clandestina. Favored by high relative humidity and warm temperatures, especially in dense shaded canopies with low direct sunlight.",
        "treatment": "Spray sulfur or horticultural oil sprays upon earliest symptom discovery. In severe infestations, rotate with systemic sterol-inhibitor (DMI) fungicides.",
        "prevention": "Avoid overhead sprinkler irrigation that keeps leaves wet. Prune the inner canopy annually to foster wind ventilation and dry foliage quickly."
    },
    "Cherry_(including_sour)___healthy": {
        "plant": "Cherry",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Clean, smooth, deep green cherry foliage showing vigorous leaf development and active photosynthetic capacity.",
        "cause": "Healthy root system, adequate winter chilling hours, and absence of foliar pathogens.",
        "treatment": "No action required.",
        "prevention": "Maintain preventive early-spring copper sprays for bacterial canker and implement balanced seasonal watering."
    },

    # --- CORN (MAIZE) ---
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "plant": "Corn",
        "display_name": "Gray Leaf Spot",
        "is_healthy": False,
        "description": "Narrow, rectangular, tan-to-gray lesions restricted by leaf veins. Under prolonged humidity, grayish spore clusters develop inside the lesions.",
        "cause": "Fungus Cercospora zeae-maydis. Proliferates in warm, humid weather (over 80°F / 27°C and >90% RH) with extended periods of morning fog or dew.",
        "treatment": "In high-yield commercial fields, apply strobilurin or triazole fungicides at VT (tasseling) through R1 (silking) if disease pressure threatens the ear leaf.",
        "prevention": "Rotate crops with non-grass crops (e.g. soybeans), till corn residue where conservation permits, and select hybrids with high genetic tolerance."
    },
    "Corn_(maize)___Common_rust_": {
        "plant": "Corn",
        "display_name": "Common Rust",
        "is_healthy": False,
        "description": "Small, powdery, cinnamon-brown pustules (uredinia) scattered across both upper and lower leaf surfaces. Pustules rupture the epidermis, exposing rusty spores.",
        "cause": "Fungus Puccinia sorghi. Spores are carried long distances on southerly wind currents during cool, moist periods (60–75°F / 16–24°C).",
        "treatment": "Typically not economically damaging in field corn, but sweet corn or inbred seed corn can be treated with approved fungicides if pustules appear prior to tasseling.",
        "prevention": "Plant resistant hybrid seed carrying the Rp gene. Early planting helps crops mature before high-volume spore arrivals."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "plant": "Corn",
        "display_name": "Northern Leaf Blight",
        "is_healthy": False,
        "description": "Large, elongated, cigar-shaped grayish-green to tan lesions (1 to 6 inches long) that develop on lower leaves and progress upward into the canopy.",
        "cause": "Fungus Exserohilum turcicum (syn. Helminthosporium turcicum). Favored by moderate temperatures (65–80°F / 18–27°C) and heavy morning dews.",
        "treatment": "Foliar fungicides containing azoxystrobin, pyraclostrobin, or propiconazole can be applied between tassel and silking if lesions appear on the three leaves below the ear.",
        "prevention": "Incorporate resistant hybrid genetics (Ht genes), practice minimum two-year crop rotation, and manage surface crop debris."
    },
    "Corn_(maize)___healthy": {
        "plant": "Corn",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Broad, vibrant green leaves with sturdy midribs and no lesions, rust pustules, or insect chewing damage.",
        "cause": "Balanced nitrogen availability, proper plant spacing, and clean growing conditions.",
        "treatment": "None needed.",
        "prevention": "Ensure adequate soil nitrogen, maintain weed control, and scout weekly during vegetative and reproductive stages."
    },

    # --- GRAPE ---
    "Grape___Black_rot": {
        "plant": "Grape",
        "display_name": "Black Rot",
        "is_healthy": False,
        "description": "Small, circular reddish-brown leaf lesions with darker margins that later form tiny black fruiting specks (pycnidia). Berries shrivel into hard black mummies.",
        "cause": "Fungus Guignardia bidwellii. Spores disperse in spring during rain and infect young green tissues when leaves remain wet for 6–24 hours.",
        "treatment": "Apply myclobutanil, captan, or mancozeb sprays starting at 1- to 3-inch shoot growth and continue at 10- to 14-day intervals through bloom and post-bloom.",
        "prevention": "Prune out mummified berry clusters and dead cankers during dormant pruning. Train vines on trellises to facilitate quick foliage drying."
    },
    "Grape___Esca_(Black_Measles)": {
        "plant": "Grape",
        "display_name": "Esca (Black Measles)",
        "is_healthy": False,
        "description": "Distinctive 'tiger-stripe' interveinal chlorosis and necrosis on mature leaves. Berries develop small, dark purple-to-black spots resembling measles.",
        "cause": "Complex wood-cankering fungal infection primarily involving Phaeomoniella chlamydospora, Phaeoacremonium minimum, and Fomitiporia mediterranea.",
        "treatment": "There is no cure for systemic vine infection. Prune infected cordons back to healthy white wood; paint large pruning cuts with antifungal wound sealants.",
        "prevention": "Avoid pruning vines during wet weather when wood canker spores are airborne. Disinfect pruning shears and practice delayed double-pruning."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "plant": "Grape",
        "display_name": "Leaf Blight (Isariopsis)",
        "is_healthy": False,
        "description": "Angular, irregular reddish-brown to dark necrotic spots on leaves. Severe infections lead to premature defoliation and compromised grape sugar ripening.",
        "cause": "Fungal pathogen Pseudocercospora vitis (formerly Phaeoisariopsis vitis). Thrives in warm, humid microclimates with restricted canopy airflow.",
        "treatment": "Copper-based fungicides or mancozeb sprays provide effective suppression when applied upon initial appearance of spots.",
        "prevention": "Shoot thinning, leaf pulling around the fruit zone, and canopy hedging to promote wind drying and sunlight penetration."
    },
    "Grape___healthy": {
        "plant": "Grape",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Lush, well-developed palmate leaves with healthy green margins, robust petiole attachment, and vibrant photosynthetic activity.",
        "cause": "Balanced vine nutrition, proper trellis management, and absence of fungal or viral stress.",
        "treatment": "No action needed.",
        "prevention": "Maintain dormant pruning sanitation, balanced potassium and magnesium nutrition, and routine canopy management."
    },

    # --- ORANGE ---
    "Orange___Haunglongbing_(Citrus_greening)": {
        "plant": "Orange",
        "display_name": "Citrus Greening (HLB)",
        "is_healthy": False,
        "description": "Blotchy, asymmetrical leaf mottle (yellowing that crosses leaf veins unevenly). Twig dieback, small lopsided bitter fruit, and premature fruit drop follow.",
        "cause": "Bacterium Candidatus Liberibacter asiaticus, vectored by the Asian citrus psyllid (Diaphorina citri).",
        "treatment": "Currently no cure exists. Provide aggressive foliar micronutrient feeding (zinc, manganese, iron) to support tree longevity; infected dying trees should be rogued to protect neighbors.",
        "prevention": "Control psyllid vectors with targeted insecticide sprays and beneficial predatory wasps (Tamarixia radiata). Plant only certified disease-free nursery stock in screened structures."
    },

    # --- PEACH ---
    "Peach___Bacterial_spot": {
        "plant": "Peach",
        "display_name": "Bacterial Spot",
        "is_healthy": False,
        "description": "Small water-soaked polygonal spots on leaves that turn purple-brown and drop out, creating a characteristic 'shot-hole' effect. May cause leaf yellowing and defoliation.",
        "cause": "Bacterium Xanthomonas arboricola pv. pruni. Spread by wind-driven rain and dew, entering through stomata and pruning wounds.",
        "treatment": "Apply dormant copper sprays before bud swell. During the growing season, low-dose fixed coppers or oxytetracycline sprays can reduce spread.",
        "prevention": "Plant resistant cultivars (such as Redhaven, Biscoe, or Candor). Avoid excess nitrogen fertilizers that produce soft, vulnerable vegetative growth."
    },
    "Peach___healthy": {
        "plant": "Peach",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Gracefully curved, lanceolate leaves with deep green color, smooth edges, and no shot-holes, curl, or bacterial lesions.",
        "cause": "Vigorous rootstock, clean orchard management, and proper dormant spray timing.",
        "treatment": "None needed.",
        "prevention": "Ensure annual dormant copper application for peach leaf curl and maintain open-center vase pruning."
    },

    # --- BELL PEPPER ---
    "Pepper,_bell___Bacterial_spot": {
        "plant": "Bell Pepper",
        "display_name": "Bacterial Spot",
        "is_healthy": False,
        "description": "Small, water-soaked, circular to irregular dark spots on leaves, often surrounded by faint yellow halos. Leaves yellow and drop, exposing fruit to sunscald.",
        "cause": "Bacterium Xanthomonas campestris pv. vesicatoria. Spreads rapidly in hot (75–90°F / 24–32°C), humid, rainy conditions via splashing water.",
        "treatment": "Apply copper hydroxide mixed with mancozeb upon symptom onset. Biological treatments using Bacillus subtilis or bacteriophages can suppress colonization.",
        "prevention": "Use certified pathogen-free seed and resistant hybrids (races 1–10). Avoid overhead sprinkler irrigation and clean stakes and tools."
    },
    "Pepper,_bell___healthy": {
        "plant": "Bell Pepper",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Uniformly green, shiny bell pepper leaves showing sturdy petiole attachment, clean blades, and active vegetative growth.",
        "cause": "Balanced calcium and magnesium nutrition, drip irrigation, and disease-free nursery transplanting.",
        "treatment": "No action needed.",
        "prevention": "Maintain consistent drip irrigation, mulch beds to suppress soil splash, and rotate away from Solanaceae crops."
    },

    # --- POTATO ---
    "Potato___Early_blight": {
        "plant": "Potato",
        "display_name": "Early Blight",
        "is_healthy": False,
        "description": "Dark brown to black necrotic spots with characteristic concentric rings, creating a 'target board' pattern on older, lower foliage.",
        "cause": "Fungus Alternaria solani. Attacking stressed, senescing, or nutrient-deficient plants during alternating dry and wet periods.",
        "treatment": "Spray protective fungicides (chlorothalonil, mancozeb) or translaminar fungicides (azoxystrobin, difenoconazole) at first sign of target spots.",
        "prevention": "Maintain adequate plant nitrogen and potassium levels to prevent premature vine senescence. Rotate crops on a 3- to 4-year cycle."
    },
    "Potato___Late_blight": {
        "plant": "Potato",
        "display_name": "Late Blight",
        "is_healthy": False,
        "description": "Large, irregular, water-soaked dark green to black lesions on leaves and stems that expand rapidly. Under high humidity, delicate white fungal growth appears on undersides.",
        "cause": "Oomycete Phytophthora infestans (the pathogen responsible for the Irish Potato Famine). Capable of destroying entire fields within days under cool, wet conditions (60–70°F / 15–21°C).",
        "treatment": "Immediately destroy heavily infected plants. Apply targeted systemic anti-oomycete compounds (such as metalaxyl, cymoxanil, or mandipropamid) immediately.",
        "prevention": "Plant only certified disease-free seed tubers. Eliminate cull piles, avoid overhead watering, and destroy infected vines before tuber harvest."
    },
    "Potato___healthy": {
        "plant": "Potato",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Compound leaves are lush green, firm, free of necrotic target spots, water-soaking, or aphid distortion.",
        "cause": "Optimum soil moisture, balanced N-P-K nutrition, and clean certified seed tubers.",
        "treatment": "None needed.",
        "prevention": "Scout lower foliage twice weekly for early blight, hill plants well to protect tubers, and maintain drip irrigation."
    },

    # --- RASPBERRY ---
    "Raspberry___healthy": {
        "plant": "Raspberry",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Serrated pinnate leaves with vibrant green upper surfaces and silvery-white undersides, showing strong cane vigor.",
        "cause": "Well-drained soil, regular cane thinning, and good microclimate air circulation.",
        "treatment": "None needed.",
        "prevention": "Prune out spent floricanes immediately after harvest and thin primocanes to prevent dense humid canopies."
    },

    # --- SOYBEAN ---
    "Soybean___healthy": {
        "plant": "Soybean",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Trifoliate leaves exhibiting healthy rich green color, active nitrogen nodulation, and intact leaf margins.",
        "cause": "Effective Bradyrhizobium bacterial nodulation and lack of foliar fungal pathogens.",
        "treatment": "None needed.",
        "prevention": "Maintain rotation with corn or small grains, control broadleaf weeds, and scout for soybean aphids."
    },

    # --- SQUASH ---
    "Squash___Powdery_mildew": {
        "plant": "Squash",
        "display_name": "Powdery Mildew",
        "is_healthy": False,
        "description": "White talcum-powder-like spots develop across both upper and lower leaf surfaces, petioles, and stems. Severely infected leaves turn yellow, brown, and brittle.",
        "cause": "Fungus Podosphaera xanthii (syn. Sphaerotheca fuliginea). Favored by dry leaves, warm temperatures (70–85°F / 21–29°C), and high atmospheric humidity.",
        "treatment": "Apply potassium bicarbonate, neem oil, or sulfur-based sprays at earliest detection. For severe cases, use myclobutanil or boscalid fungicides.",
        "prevention": "Plant powdery-mildew-tolerant squash varieties. Space plants generously to ensure ample air circulation and avoid overhead sprinkling."
    },

    # --- STRAWBERRY ---
    "Strawberry___Leaf_scorch": {
        "plant": "Strawberry",
        "display_name": "Leaf Scorch",
        "is_healthy": False,
        "description": "Numerous small, dark purple or reddish spots without light centers. Lesions coalesce so that entire leaf margins appear scorched and curl upward.",
        "cause": "Fungus Diplocarpon earlianum. Spreads via splashing rainwater and dew, thriving when leaves stay damp for more than 9–12 hours.",
        "treatment": "Remove and discard old infected leaves after harvest. Apply captan or copper-based sprays during early spring emergence.",
        "prevention": "Plant on raised beds with straw mulch to prevent soil splashing. Avoid overhead irrigation and plant resistant varieties."
    },
    "Strawberry___healthy": {
        "plant": "Strawberry",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Trifoliate leaves with vibrant emerald green coloring, serrated edges, and healthy crowns free from angular spots or scorch.",
        "cause": "Adequate soil drainage, straw mulching, and balanced feeding.",
        "treatment": "None needed.",
        "prevention": "Renovate strawberry beds after fruiting, maintain drip lines under plastic, and remove dead leaves before winter dormancy."
    },

    # --- TOMATO ---
    "Tomato___Bacterial_spot": {
        "plant": "Tomato",
        "display_name": "Bacterial Spot",
        "is_healthy": False,
        "description": "Small, dark, greasy or water-soaked circular spots (1–3 mm) that turn brown-black and often have narrow yellow halos. Leaves eventually scorch and drop.",
        "cause": "Bacteria Xanthomonas perforans / X. vesicatoria. Splashes between leaves during rains and sprinkler irrigation; enters through stomata and trichomes.",
        "treatment": "Spray fixed copper combined with mancozeb to overcome copper tolerance. Biologicals like Serenade (Bacillus subtilis) help suppress spread.",
        "prevention": "Use certified clean seed, disinfect seedbeds, rotate out of solanaceous crops for 2 years, and strictly water at root level using drip tubes."
    },
    "Tomato___Early_blight": {
        "plant": "Tomato",
        "display_name": "Early Blight",
        "is_healthy": False,
        "description": "Concentric rings forming a distinctive 'target board' pattern within brown, dying patches on older lower leaves. Surrounding tissue turns yellow.",
        "cause": "Fungus Alternaria linariae (formerly Alternaria solani). Overwinters in old tomato vines and weeds; spores splash onto lower foliage from the soil.",
        "treatment": "Prune away lower yellowing and infected leaves. Apply protective fungicides such as chlorothalonil, copper, or bio-fungicides every 7–10 days.",
        "prevention": "Mulch the soil heavily around tomato plants to stop soil splash. Prune lower suckers up to 12 inches from ground level to improve airflow."
    },
    "Tomato___Late_blight": {
        "plant": "Tomato",
        "display_name": "Late Blight",
        "is_healthy": False,
        "description": "Rapidly expanding, pale green to olive-brown water-soaked lesions that turn dark brown and oily. White fuzzy mildew appears on undersides in humid air.",
        "cause": "Oomycete Phytophthora infestans. Spreads on air currents for miles under cool, foggy, wet weather (60–70°F / 15–21°C). Highly destructive.",
        "treatment": "Remove and bag infected plants immediately to prevent neighborhood epidemic. Apply targeted fungicides (mancozeb, chlorothalonil, or cymoxanil) before rains.",
        "prevention": "Plant resistant cultivars (such as Mountain Magic, Defiant PhR, or Iron Lady). Avoid overhead watering and scout tomato and potato plantings daily."
    },
    "Tomato___Leaf_Mold": {
        "plant": "Tomato",
        "display_name": "Leaf Mold",
        "is_healthy": False,
        "description": "Pale greenish-yellow spots with indistinct borders on upper leaf surfaces. Olive-green to velvety brown mold develops heavily on leaf undersides.",
        "cause": "Fungus Passalora fulva (syn. Cladosporium fulvum). Common in high tunnels and greenhouses where relative humidity exceeds 85%.",
        "treatment": "Improve greenhouse ventilation and lower humidity below 80%. Spray with copper fungicides or bio-fungicides at the first sign of yellow patches.",
        "prevention": "Increase row spacing, run exhaust fans, and water only early in the day so leaves dry before sunset. Choose leaf-mold resistant greenhouse varieties."
    },
    "Tomato___Septoria_leaf_spot": {
        "plant": "Tomato",
        "display_name": "Septoria Leaf Spot",
        "is_healthy": False,
        "description": "Abundant small (2–4 mm) circular spots with dark brown margins and sunken, light gray or tan centers containing tiny black specks (pycnidia).",
        "cause": "Fungus Septoria lycopersici. Spores splash up from infested soil or crop debris onto lower leaves during rains or overhead watering.",
        "treatment": "Strip off infected bottom leaves immediately. Spray protective fungicides (copper, chlorothalonil) thoroughly covering upper and lower leaf surfaces.",
        "prevention": "Apply 3 inches of clean straw or plastic mulch to shield against soil splash. Practice 3-year crop rotation and stake vines upright."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "plant": "Tomato",
        "display_name": "Two-Spotted Spider Mite",
        "is_healthy": False,
        "description": "Fine yellow, bronze, or white stippling (tiny dots) across leaf blades. Fine silken webbing appears under leaves and on stems; leaves dry up and drop.",
        "cause": "Microscopic arachnid Tetranychus urticae. Populations explode during hot, dry, and dusty weather (above 85°F / 29°C).",
        "treatment": "Spray insecticidal soap, neem oil, or horticultural oils, paying strict attention to leaf undersides where mites feed. Introduce predatory mites (Phytoseiulus persimilis).",
        "prevention": "Keep plants well-watered to prevent drought stress. Hose down dusty roads/pathways nearby and avoid broad-spectrum pyrethroids that eliminate predatory bugs."
    },
    "Tomato___Target_Spot": {
        "plant": "Tomato",
        "display_name": "Target Spot",
        "is_healthy": False,
        "description": "Small pinpoint brown lesions that expand into circular brown spots with concentric rings and clear-cut margins. May cause severe defoliation and sunken fruit spots.",
        "cause": "Fungus Corynespora cassiicola. Proliferates in warm, humid tropical and subtropical climates with frequent showers.",
        "treatment": "Apply protectant fungicides (mancozeb, chlorothalonil, or azoxystrobin) in scheduled rotations. Remove heavily spotted lower foliage.",
        "prevention": "Ensure good canopy ventilation with rigorous pruning and staking. Avoid working in wet tomato fields."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "plant": "Tomato",
        "display_name": "Yellow Leaf Curl Virus",
        "is_healthy": False,
        "description": "Severe upward curling and cupping of leaflets, marked yellowing (chlorosis) along margins, reduced leaf size, and severe plant stunting. Flower drop prevents fruit set.",
        "cause": "Begomovirus transmitted by the sweetpotato / silverleaf whitefly (Bemisia tabaci).",
        "treatment": "There is no chemical cure for plant viral infections. Pull and bag infected plants immediately to prevent whiteflies from acquiring and spreading the virus.",
        "prevention": "Control whiteflies using yellow sticky traps, insecticidal soaps, or systemic insecticides. Grow virus-resistant varieties (such as Tycoon, Sakura, or Red Deuce) under 50-mesh insect netting."
    },
    "Tomato___Tomato_mosaic_virus": {
        "plant": "Tomato",
        "display_name": "Tomato Mosaic Virus (ToMV)",
        "is_healthy": False,
        "description": "Mottling with alternating light and dark green patches, leaf distortion ('shoestringing' or fern-like leaves), and general plant stunting.",
        "cause": "Tobamovirus (ToMV). Extremely stable virus transmitted mechanically by touch, contaminated hands, pruning shears, stakes, and tobacco products.",
        "treatment": "Infected plants cannot be cured and must be carefully pulled and destroyed. Wash hands and tools in 20% nonfat dry milk or 10% trisodium phosphate.",
        "prevention": "Plant certified virus-free seed and resistant hybrids (labeled with 'T' or 'ToMV'). Tobacco users must wash hands thoroughly with soap before handling tomato plants."
    },
    "Tomato___healthy": {
        "plant": "Tomato",
        "display_name": "Healthy Leaf",
        "is_healthy": True,
        "description": "Vigorous, rich green pinnate leaves with strong aroma, erect petioles, and no lesions, yellowing, or curling symptoms.",
        "cause": "Optimal soil nutrients, consistent drip irrigation, proper staking, and absence of insect vectors.",
        "treatment": "No corrective treatment needed.",
        "prevention": "Maintain staking, mulch base against soil splash, water at root level, and prune lower leaves as the vine grows."
    },

    # --- BASE REPO CROPS (Banana, Cacao, Coffee) for reference & expansion ---
    "banana___black_sigatoka": {
        "plant": "Banana",
        "display_name": "Black Sigatoka",
        "is_healthy": False,
        "description": "Dark brown to black narrow streaks parallel to leaf veins, coalescing into large necrotic spots with yellow halos, causing premature leaf death.",
        "cause": "Fungus Pseudocercospora fijiensis. Spreads through wind and rain splash in warm, humid tropical conditions.",
        "treatment": "Deleafing (removing infected leaf portions) and scheduled application of protectant and systemic fungicides.",
        "prevention": "Improve field drainage, maintain proper plant spacing, and plant resistant banana hybrids."
    },
    "banana___fusarium_wilt": {
        "plant": "Banana",
        "display_name": "Fusarium Wilt (Panama Disease)",
        "is_healthy": False,
        "description": "Progressive yellowing of older leaves starting from margins, petiole buckling, and internal vascular browning inside pseudostem.",
        "cause": "Soil-borne fungus Fusarium oxysporum f. sp. cubense (TR4). Persists in soil for decades.",
        "treatment": "No cure once infected. Quarantine field, eradicate infected mats, and strictly disinfect footwear and farm machinery.",
        "prevention": "Plant only certified tissue-culture plantlets and implement strict farm biosecurity protocols."
    },
    "banana___healthy": {
        "plant": "Banana",
        "display_name": "Healthy Banana Leaf",
        "is_healthy": True,
        "description": "Broad, intact, vibrant emerald green leaf blades without necrotic streaks or marginal wilting.",
        "cause": "Healthy root system, adequate potassium nutrition, and disease-free suckers.",
        "treatment": "None needed.",
        "prevention": "Maintain drainage ditches and regular leaf health inspections."
    },
    "cacao___monilia": {
        "plant": "Cacao",
        "display_name": "Moniliasis (Frosty Pod Rot)",
        "is_healthy": False,
        "description": "Irregular dark brown lesions on pods followed by a dense white/cream fungal bloom that destroys cacao beans.",
        "cause": "Fungus Moniliophthora roreri, airborne spores infecting young cacao cherelles and pods.",
        "treatment": "Weekly sanitation pruning to remove and bury all infected pods before fungal spore bloom occurs.",
        "prevention": "Prune shade trees to allow morning sun drying and plant tolerant clones."
    },
    "cacao___black_pod": {
        "plant": "Cacao",
        "display_name": "Black Pod Rot",
        "is_healthy": False,
        "description": "Brown, water-soaked lesions that rapidly expand across the entire pod surface, turning it chocolate-brown to black.",
        "cause": "Phytophthora palmivora and related species, spread by rain splash and ants.",
        "treatment": "Apply copper-based fungicides during rainy seasons and harvest ripe pods promptly.",
        "prevention": "Maintain shade tree pruning, weed management, and clear drainage canals."
    },
    "cacao___healthy": {
        "plant": "Cacao",
        "display_name": "Healthy Cacao",
        "is_healthy": True,
        "description": "Glossy green leaves and clean healthy pods without fungal crusts or water-soaked lesions.",
        "cause": "Balanced agroforestry shade, good drainage, and regular field sanitation.",
        "treatment": "None needed.",
        "prevention": "Maintain routine pruning and monthly pod inspection."
    },
    "coffee___leaf_rust": {
        "plant": "Coffee",
        "display_name": "Coffee Leaf Rust (Roya)",
        "is_healthy": False,
        "description": "Bright powdery orange-yellow spots on the underside of coffee leaves with corresponding pale yellow chlorotic spots on top. Heavy infection triggers severe defoliation.",
        "cause": "Fungus Hemileia vastatrix. Spores disperse by rain splash and wind, requiring moisture to germinate on leaf undersides.",
        "treatment": "Apply systemic fungicides (such as cyproconazole or triadimefon) or copper sprays timed to early rainy season flushes.",
        "prevention": "Plant rust-resistant varieties (such as Castillo, Obata, or Marsellesa) and ensure balanced potassium and shade management."
    },
    "coffee___healthy": {
        "plant": "Coffee",
        "display_name": "Healthy Coffee Leaf",
        "is_healthy": True,
        "description": "Deep lustrous green foliage with crisp wavy margins, free of rust powder or cercospora spots.",
        "cause": "Optimal elevation, shade balance, and balanced N-P-K-B nutrition.",
        "treatment": "None needed.",
        "prevention": "Prune coffee trees systematically and apply preventive copper sprays before rainy seasons."
    }
}


def get_disease_info(class_label: str) -> Dict[str, Any]:
    """Retrieve disease info by label, or generate structured fallback."""
    if class_label in DISEASE_KNOWLEDGE_BASE:
        info = DISEASE_KNOWLEDGE_BASE[class_label].copy()
        info["class_label"] = class_label
        return info

    # Clean label into readable names if not explicitly in dictionary
    parts = class_label.split("___")
    plant = parts[0].replace("_", " ").title() if parts else "Plant"
    condition = parts[1].replace("_", " ").title() if len(parts) > 1 else class_label
    is_healthy = "healthy" in condition.lower()

    if is_healthy:
        return {
            "class_label": class_label,
            "plant": plant,
            "display_name": f"Healthy {plant}",
            "is_healthy": True,
            "description": f"The foliage shows normal, healthy growth characteristic of {plant}.",
            "cause": "Good general cultural practices and absence of observable symptoms.",
            "treatment": "No treatment required. Maintain current care regimen.",
            "prevention": "Continue standard watering, sunlight, and soil monitoring."
        }
    else:
        return {
            "class_label": class_label,
            "plant": plant,
            "display_name": f"{plant} - {condition}",
            "is_healthy": False,
            "description": f"Symptoms indicative of {condition} observed on {plant} leaf tissue.",
            "cause": f"Pathogen or physiological stress associated with {condition}.",
            "treatment": "Isolate affected foliage, prune damaged areas, and consult localized agricultural extension guides.",
            "prevention": "Improve ventilation, avoid overhead watering, and maintain clean tools."
        }
