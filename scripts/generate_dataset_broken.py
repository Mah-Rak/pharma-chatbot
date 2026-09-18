# Format : (nom, [symptomes], gravité, categorie)
MALADIES = [
    # ===== ORL / RESPIRATOIRE (12) =====
    ("Grippe", ["fievre", "courbatures", "fatigue", "mal_de_tete", "toux_seche"], "normale", "orl"),
    ("Rhume", ["nez_qui_coule", "eternuements", "mal_de_gorge", "toux_seche"], "normale", "orl"),
    ("Angine", ["mal_de_gorge", "fievre", "difficulte_avaler"], "normale", "orl"),
    ("Pharyngite", ["mal_de_gorge", "toux_seche", "fatigue"], "normale", "orl"),
    ("Laryngite", ["voix_enrouee", "mal_de_gorge", "toux_seche"], "normale", "orl"),
    ("Sinusite", ["nez_bouche", "mal_de_tete", "douleur_faciale", "fievre"], "normale", "orl"),
    ("Otite_moyenne", ["oreille_douloureuse", "fievre", "fatigue", "perte_audition"], "normale", "orl"),
    ("Bronchite", ["toux_grasse", "fatigue", "essoufflement", "fievre"], "normale", "orl"),
    ("Pneumonie", ["fievre", "toux_grasse", "essoufflement", "douleur_thoracique"], "urgente", "orl"),
    ("Asthme_leger", ["respiration_sifflante", "essoufflement", "toux_seche"], "normale", "orl"),
    ("Allergie_saisonniere", ["eternuements", "nez_qui_coule", "demangeaisons", "yeux_rouges"], "normale", "orl"),
    ("Apnee_sommeil", ["fatigue", "insomnie", "ronflement", "somnolence"], "normale", "orl"),

    # ===== DIGESTIF (10) =====
    ("Gastro_enterite", ["diarrhee", "nausee", "vomissement", "douleur_abdominale", "fievre"], "normale", "digestif"),
    ("Intoxication_alimentaire", ["nausee", "vomissement", "diarrhee", "crampes_abdominales"], "normale", "digestif"),
    ("Reflux_gastro_oesophagien", ["brulures_estomac", "reflux", "ballonnements", "nausee"], "normale", "digestif"),
    ("Ulcere_estomac", ["brulures_estomac", "douleur_abdominale", "nausee", "perte_appetit"], "normale", "digestif"),
    ("Gastrite", ["brulures_estomac", "nausee", "douleur_abdominale"], "normale", "digestif"),
    ("Constipation_simple", ["constipation", "ballonnements", "douleur_abdominale"], "normale", "digestif"),
    ("Syndrome_intestin_irritable", ["ballonnements", "douleur_abdominale", "constipation", "diarrhee"], "normale", "digestif"),
    ("Hemorroides", ["hemorroides", "sang_selles", "douleur_anale"], "normale", "digestif"),
    ("Colite", ["douleur_abdominale", "diarrhee", "sang_selles"], "normale", "digestif"),
    ("Crise_hemorroidaire", ["hemorroides", "douleur_anale", "sang_selles"], "normale", "digestif"),

    # ===== NEURO / PSY (8) =====
    ("Migraine", ["mal_de_tete", "nausee", "photosensibilite", "vertiges"], "normale", "neuro"),
    ("Cephalee_de_tension", ["mal_de_tete", "raideur", "stress"], "normale", "neuro"),
    ("Insomnie_passagere", ["insomnie", "fatigue", "anxiete"], "normale", "neuro"),
    ("Anxiete_legere", ["anxiete", "insomnie", "fatigue", "palpitations"], "normale", "neuro"),
    ("Depression_legere", ["fatigue", "insomnie", "perte_appetit", "anxiete"], "normale", "neuro"),
    ("Vertige_positionnel", ["vertiges", "etourdissements", "nausee"], "normale", "neuro"),
    ("Nevralgie", ["douleur_nerveuse", "engourdissement", "picotements"], "normale", "neuro"),
    ("Crise_angoisse", ["anxiete", "palpitations", "essoufflement", "tremblements"], "urgente", "neuro"),

    # ===== URINAIRE (4) =====
    ("Cystite", ["brulures_urinaires", "envie_frequente", "douleur_abdominale"], "normale", "urinaire"),
    ("Infection_urinaire", ["brulures_urinaires", "envie_frequente", "fievre", "douleur_lombaire"], "normale", "urinaire"),
    ("Colique_nephretique", ["douleur_lombaire", "sang_urines", "nausee", "vomissement"], "urgente", "urinaire"),
    ("Prostatite", ["brulures_urinaires", "difficulte_uriner", "douleur_lombaire", "fievre"], "normale", "urinaire"),

    # ===== PEAU (5) =====
    ("Eczema", ["demangeaisons", "rougeurs_peau", "peau_seche"], "normale", "peau"),
    ("Urticaire", ["urticaire", "demangeaisons", "rougeurs_peau"], "normale", "peau"),
    ("Acne", ["boutons", "rougeurs_peau", "points_noirs"], "normale", "peau"),
    ("Mycose_cutanee", ["mycoses", "demangeaisons", "rougeurs_peau"], "normale", "peau"),
    ("Dermatite_atopique", ["eczema", "demangeaisons", "peau_seche"], "normale", "peau"),

    # ===== YEUX (2) =====
    ("Conjonctivite", ["yeux_rouges", "larmoiement", "demangeaisons", "douleur_oculaire"], "normale", "yeux"),
    ("Orgelet", ["douleur_oculaire", "rougeurs_peau", "gonflement_paupiere"], "normale", "yeux"),

    # ===== MUSCULO-SQUELETTIQUE (5) =====
    ("Lombalgie", ["mal_de_dos", "raideur", "douleur_musculaire"], "normale", "musculo"),
    ("Cervicalgie", ["douleur_cervicale", "raideur", "mal_de_tete"], "normale", "musculo"),
    ("Entorse", ["entorse", "douleur_articulaire", "gonflement_articulaire"], "normale", "musculo"),
    ("Arthrose", ["douleur_articulaire", "raideur", "gonflement_articulaire"], "normale", "musculo"),
    ("Tendinite", ["douleur_articulaire", "douleur_musculaire", "raideur"], "normale", "musculo"),

    # ===== AUTRES (5) =====
    ("Anemie_legere", ["fatigue", "vertiges", "paleur", "essoufflement"], "normale", "general"),
    ("Carence_vitamine_D", ["fatigue", "douleur_musculaire", "fatigue_musculaire"], "normale", "general"),
    ("Hemorragie_legere", ["saignement_nez", "saignement_gencives"], "normale", "autre"),
    ("Aphtose", ["aphtes", "douleur_buccale"], "normale", "autre"),
    ("Dent_de_sagesse", ["douleur_dentaire", "gonflement_articulaire", "fievre"], "normale", "autre"),
]

# Format : (nom, dci, ordonnance, categorie, description, contre_indications)
MEDICAMENTS = [
    # ===== ANTALGIQUES / AINS (6) =====
    ("Paracetamol", "Paracétamol", False, "Antalgique", "Antidouleur et antipyrétique", ["insuffisance hépatique"]),
    ("Ibuprofene", "Ibuprofène", False, "AINS", "Anti-inflammatoire non stéroïdien", ["ulcère", "grossesse 3e trimestre", "insuffisance rénale"]),
    ("Aspirine", "Acide acétylsalicylique", False, "Antalgique", "Antidouleur, antipyrétique, anti-inflammatoire", ["ulcère", "enfants < 16 ans", "grossesse"]),
    ("Diclofenac", "Diclofénac", True, "AINS", "Anti-inflammatoire puissant", ["ulcère", "insuffisance cardiaque"]),
    ("Naproxene", "Naproxène", True, "AINS", "Anti-inflammatoire", ["ulcère", "grossesse"]),
    ("Gel_ketoprofene", "Kétoprofène", False, "AINS topique", "Gel anti-inflammatoire local", []),

    # ===== TOUX / ORL (7) =====
    ("Sirop_toux_seche", "Dextrométhorphane", False, "Antitussif", "Calme la toux sèche", ["toux grasse"]),
    ("Sirop_toux_grasse", "Carbocistéine", False, "Mucolytique", "Fluidifie les sécrétions", ["ulcère gastrique"]),
    ("Pastilles_gorge", "Lidocaïne", False, "Antalgique local", "Soulage la gorge irritée", []),
    ("Spray_gorge", "Benzydamine", False, "Anti-inflammatoire local", "Soulage le mal de gorge", []),
    ("Spray_nasal", "Oxymétazoline", False, "Décongestionnant", "Débouche le nez", ["hypertension", "< 6 ans"]),
    ("Serum_physiologique", "Chlorure de sodium", False, "Lavage nasal", "Nettoie les fosses nasales", []),
    ("Gouttes_oreille", "Lidocaïne", False, "Antalgique local", "Soulage l'otite", ["perforation tympan"]),

    # ===== ALLERGIE (3) =====
    ("Cetirizine", "Cétirizine", False, "Antihistaminique", "Antiallergique non sédatif", ["insuffisance rénale"]),
    ("Loratadine", "Loratadine", False, "Antihistaminique", "Antiallergique", []),
    ("Azelastine_collyre", "Azélastine", False, "Collyre antiallergique", "Yeux irrités allergiques", []),

    # ===== DIGESTIF (12) =====
    ("Omeprazole", "Oméprazole", True, "Antiacide", "Réduit l'acidité gastrique", ["grossesse"]),
    ("Gaviscon", "Alginate de sodium", False, "Antiacide", "Soulage les brûlures d'estomac", []),
    ("Macrogol", "Macrogol", False, "Laxatif", "Facilite le transit", ["occlusion intestinale"]),
    ("Bisacodyl", "Bisacodyl", False, "Laxatif stimulant", "Laxatif rapide", ["occlusion", "enfants < 6 ans"]),
    ("Phloroglucinol", "Phloroglucinol", False, "Antispasmodique", "Calme les spasmes", []),
    ("Solution_rehydratation", "Sels de réhydratation", False, "Réhydratant", "Compense les pertes", []),
    ("Metoclopramide", "Métoclopramide", True, "Antiémétique", "Contre nausées/vomissements", ["occlusion"]),
    ("Loperamide", "Lopéramide", False, "Antidiarrhéique", "Ralentit le transit", ["diarrhée sanglante", "fievre"]),
    ("Smecta", "Diosmectite", False, "Antidiarrhéique", "Protège la muqueuse intestinale", []),
    ("Motilium", "Dompéridone", True, "Antiémétique", "Contre nausées", ["problèmes cardiaques"]),
    ("Vogalene", "Métopimazine", True, "Antiémétique", "Contre vomissements", ["glaucome"]),
    ("Fer", "Sulfate ferreux", False, "Complément", "Contre l'anémie", ["hémochromatose"]),

    # ===== VITAMINES / COMPLÉMENTS (5) =====
    ("Vitamine_C", "Acide ascorbique", False, "Vitamine", "Renforce les défenses", []),
    ("Vitamine_D", "Cholécalciférol", False, "Vitamine", "Fixe le calcium", ["hypercalcémie"]),
    ("Magnesium", "Magnésium", False, "Complément", "Contre la fatigue et les crampes", ["insuffisance rénale"]),
    ("Calcium", "Calcium", False, "Complément", "Renforce les os", ["hypercalcémie"]),
    ("Omega_3", "Oméga-3", False, "Complément", "Santé cardiovasculaire", []),

    # ===== ANTIBIOTIQUES (3) =====
    ("Amoxicilline", "Amoxicilline", True, "Antibiotique", "Antibiotique large spectre", ["allergie pénicilline"]),
    ("Azithromycine", "Azithromycine", True, "Antibiotique", "Antibiotique macrolide", ["allergie macrolides"]),
    ("Fucidique_acide", "Acide fusidique", True, "Antibiotique topique", "Infections cutanées", []),

    # ===== DERMATOLOGIE (7) =====
    ("Hydrocortisone", "Hydrocortisone", False, "Corticoïde", "Crème anti-inflammatoire", ["infection cutanée"]),
    ("Betamethasone", "Bétaméthasone", True, "Corticoïde", "Corticoïde puissant", ["infection cutanée", "grossesse"]),
    ("Clotrimazole", "Clotrimazole", False, "Antifongique", "Contre les mycoses", []),
    ("Miconazole", "Miconazole", False, "Antifongique", "Contre les mycoses", []),
    ("Aciclovir", "Aciclovir", False, "Antiviral", "Contre l'herpès", []),
    ("Betadine", "Povidone iodée", False, "Antiseptique", "Désinfecte les plaies", ["thyroïde", "allergie iode"]),
    ("Biafine", "Trolamine", False, "Cicatrisant", "Soigne les brûlures", []),

    # ===== YEUX (2) =====
    ("Collyre_antiseptique", "Chlorhexidine", False, "Collyre", "Désinfecte les yeux", []),
    ("Larmes_artificielles", "Carmellose", False, "Collyre", "Yeux secs", []),

    # ===== AUTRES (2) =====
    ("Patch_lidocaine", "Lidocaïne", False, "Antalgique", "Douleurs localisées", ["allergie lidocaïne"]),
    ("Aloe_vera", "Aloe vera", False, "Cicatrisant", "Apaise la peau", []),
]


# Format : maladie -> [medicaments]
ASSOCIATIONS = {
    "Grippe": ["Paracetamol", "Vitamine_C", "Repos"],
    "Rhume": ["Paracetamol", "Serum_physiologique", "Vitamine_C"],
    "Angine": ["Paracetamol", "Pastilles_gorge", "Spray_gorge"],
    "Pharyngite": ["Paracetamol", "Pastilles_gorge"],
    "Laryngite": ["Pastilles_gorge", "Sirop_toux_seche"],
    "Sinusite": ["Paracetamol", "Spray_nasal", "Serum_physiologique"],
    "Otite_moyenne": ["Paracetamol", "Ibuprofene", "Gouttes_oreille"],
    "Bronchite": ["Sirop_toux_grasse", "Paracetamol"],
    "Pneumonie": ["Amoxicilline"],  # urgence → médecin
    "Asthme_leger": ["Salbutamol"],
    "Allergie_saisonniere": ["Cetirizine", "Loratadine", "Azelastine_collyre"],
    "Apnee_sommeil": [],  # médecin
    "Gastro_enterite": ["Solution_rehydratation", "Smecta", "Paracetamol"],
    "Intoxication_alimentaire": ["Solution_rehydratation", "Smecta"],
    "Reflux_gastro_oesophagien": ["Gaviscon", "Omeprazole"],
    "Ulcere_estomac": ["Omeprazole"],
    "Gastrite": ["Gaviscon", "Omeprazole"],
    "Constipation_simple": ["Macrogol", "Bisacodyl"],
    "Syndrome_intestin_irritable": ["Phloroglucinol", "Smecta"],
    "Hemorroides": ["Hydrocortisone", "Paracetamol"],
    "Colite": ["Phloroglucinol"],
    "Crise_hemorroidaire": ["Hydrocortisone", "Paracetamol", "Ibuprofene"],
    "Migraine": ["Paracetamol", "Ibuprofene", "Aspirine"],
    "Cephalee_de_tension": ["Paracetamol", "Magnesium"],
    "Insomnie_passagere": ["Magnesium", "Vitamine_C"],
    "Anxiete_legere": ["Magnesium", "Omega_3"],
    "Depression_legere": ["Omega_3", "Vitamine_D"],
    "Vertige_positionnel": ["Phloroglucinol"],
    "Nevralgie": ["Paracetamol", "Ibuprofene"],
    "Crise_angoisse": [],  # médecin
    "Cystite": ["Solution_rehydratation", "Paracetamol"],
    "Infection_urinaire": ["Amoxicilline"],
    "Colique_nephretique": [],  # urgence
    "Prostatite": ["Amoxicilline"],
    "Eczema": ["Hydrocortisone", "Aloe_vera"],
    "Urticaire": ["Cetirizine", "Loratadine"],
    "Acne": ["Biafine"],
    "Mycose_cutanee": ["Clotrimazole", "Miconazole"],
    "Dermatite_atopique": ["Hydrocortisone", "Aloe_vera"],
    "Conjonctivite": ["Collyre_antiseptique", "Larmes_artificielles"],
    "Orgelet": ["Collyre_antiseptique"],
    "Lombalgie": ["Paracetamol", "Gel_ketoprofene", "Patch_lidocaine"],
    "Cervicalgie": ["Paracetamol", "Gel_ketoprofene"],
    "Entorse": ["Paracetamol", "Gel_ketoprofene"],
    "Arthrose": ["Paracetamol", "Gel_ketoprofene"],
    "Tendinite": ["Ibuprofene", "Gel_ketoprofene"],
    "Anemie_legere": ["Fer", "Vitamine_C"],
    "Carence_vitamine_D": ["Vitamine_D", "Calcium"],
    "Hemorragie_legere": ["Betadine"],
    "Aphtose": ["Biafine"],
    "Dent_de_sagesse": ["Paracetamol", "Ibuprofene"],
}


def main():
    # Construire les listes au format final
    symptomes_json = [
        {
            "nom": s[0],
            "synonymes": s[1],
            "gravite": s[2],
            "categorie": s[3],
        }
        for s in SYMPTOMES
    ]

    maladies_json = [
        {
            "nom": m[0],
            "symptomes": m[1],
            "gravite": m[2],
            "categorie": m[3],
        }
        for m in MALADIES
    ]

    medicaments_json = [
        {
            "nom": m[0],
            "dci": m[1],
            "ordonnance_requise": m[2],
            "categorie": m[3],
            "description": m[4],
            "contre_indications": m[5],
        }
        for m in MEDICAMENTS
    ]

    associations_json = [
        {"maladie": maladie, "medicaments": meds}
        for maladie, meds in ASSOCIATIONS.items()
    ]

    cas_graves = [
        {"symptome": "douleur_thoracique", "message": "Douleur thoracique détectée. Appelez immédiatement le 15 ou le 112."},
        {"symptome": "essoufflement", "message": "Difficulté respiratoire détectée. Consultez un médecin en urgence."},
        {"symptome": "palpitations", "message": "Palpitations détectées. Consultez un médecin rapidement."},
        {"symptome": "perte_connaissance", "message": "Perte de connaissance détectée. Appelez immédiatement le 15."},
        {"symptome": "convulsions", "message": "Convulsions détectées. Appelez le 15 immédiatement."},
        {"symptome": "toux_sang", "message": "Sang dans les crachats. Consultez un médecin en urgence."},
        {"symptome": "confusion", "message": "Confusion mentale. Consultez un médecin rapidement."},
        {"symptome": "sang_selles", "message": "Sang dans les selles. Consultez un médecin rapidement."},
    ]

    dataset = {
        "version": "2.0",
        "description": "Dataset médical enrichi pour Pharma Chatbot",
        "symptomes": symptomes_json,
        "maladies": maladies_json,
        "medicaments": medicaments_json,
        "associations": associations_json,
        "cas_graves": cas_graves,
    }

    output = Path("data/dataset_medical.json")
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("DATASET GÉNÉRÉ")
    print("=" * 60)
    print(f"  Symptômes     : {len(symptomes_json)}")
    print(f"  Maladies      : {len(maladies_json)}")
    print(f"  Médicaments   : {len(medicaments_json)}")
    print(f"  Associations  : {len(associations_json)}")
    print(f"  Cas graves    : {len(cas_graves)}")
    print(f"\nFichier écrit : {output}")
    print("=" * 60)
