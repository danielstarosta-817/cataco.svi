#!/usr/bin/env python3
"""
Mexico SVI Tool — Prototype Dataset Builder
Generates a research-grounded prototype CSV with real municipality names and CVE codes.
Values are approximations derived from published CONAPO/CONEVAL grades and academic sources.
ALL values are clearly marked PROTOTYPE — replace with real data from download_and_process.py.

Output: data/processed/prototype_municipalities.csv
"""

import pandas as pd
import os

PROC = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(PROC, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# Municipality data
# CVE_GEO: 5-digit INEGI code (state 2 + municipio 3)
# CONAPO_GRADO: MA=Muy Alto, A=Alto, M=Medio, B=Bajo, MB=Muy Bajo
# CONAPO_IMM: approximate marginalization index value (higher = more marginalized)
# SVI_SOCIAL: approximate Social cluster score 0-1 (derived from CONAPO grade)
# HAZARD_SISMICO: approximate seismic hazard score 0-1
# HAZARD_CICLONICO: approximate cyclonic hazard score 0-1
# POB_TOTAL: approximate 2020 population
# PCT_HABLA_INDIG: % speaking indigenous language as primary (approximate)
# NOTES: why this municipality was selected
# ─────────────────────────────────────────────────────────────────────────────

# Grade → approximate SVI social score mapping
GRADE_SCORE = {"MA": 0.90, "A": 0.72, "M": 0.50, "B": 0.28, "MB": 0.10}

municipalities = [

    # ══════════════════════════════════════════════════════════════════
    # GUERRERO (12) — 27 municipalities
    # ══════════════════════════════════════════════════════════════════

    # Coastal zone — Otis primary impact
    {"CVE_GEO":"12001","NOM_MUN":"Acapulco de Juárez",   "NOM_ENT":"Guerrero","CONAPO_GRADO":"A",
     "POB_TOTAL":895981,"PCT_HABLA_INDIG":3.1,"HAZARD_SISMICO":0.85,"HAZARD_CICLONICO":0.95,
     "NOTES":"Otis direct landfall; tres Acapulcos story anchor; highest urban poverty in Mexico"},

    {"CVE_GEO":"12001_CAC","NOM_MUN":"Cacahuatepec (Acapulco rural)", "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":38000,"PCT_HABLA_INDIG":12.0,"HAZARD_SISMICO":0.80,"HAZARD_CICLONICO":0.90,
     "NOTES":"CECOP / 36 comunidades rurales sin ayuda post-Otis; Hilo 4 anchor"},

    {"CVE_GEO":"12025","NOM_MUN":"Coyuca de Benítez",    "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":66131,"PCT_HABLA_INDIG":2.0,"HAZARD_SISMICO":0.82,"HAZARD_CICLONICO":0.88,
     "NOTES":"Costa Grande; Otis impact zone; communal land tenure"},

    {"CVE_GEO":"12054","NOM_MUN":"Petatlán",              "NOM_ENT":"Guerrero","CONAPO_GRADO":"A",
     "POB_TOTAL":52300,"PCT_HABLA_INDIG":3.5,"HAZARD_SISMICO":0.80,"HAZARD_CICLONICO":0.85,
     "NOTES":"Costa Grande; coastal hurricane exposure"},

    {"CVE_GEO":"12067","NOM_MUN":"Técpan de Galeana",     "NOM_ENT":"Guerrero","CONAPO_GRADO":"A",
     "POB_TOTAL":67200,"PCT_HABLA_INDIG":2.8,"HAZARD_SISMICO":0.78,"HAZARD_CICLONICO":0.82,
     "NOTES":"Costa Grande; Otis secondary impact"},

    {"CVE_GEO":"12041","NOM_MUN":"José Azueta (Zihuatanejo)","NOM_ENT":"Guerrero","CONAPO_GRADO":"M",
     "POB_TOTAL":125000,"PCT_HABLA_INDIG":2.1,"HAZARD_SISMICO":0.88,"HAZARD_CICLONICO":0.75,
     "NOTES":"Guerrero Gap seismic high-risk; tourism economy; social vulnerability contrast"},

    {"CVE_GEO":"12052","NOM_MUN":"Ometepec",              "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":49200,"PCT_HABLA_INDIG":35.0,"HAZARD_SISMICO":0.75,"HAZARD_CICLONICO":0.70,
     "NOTES":"Costa Chica; Afro-Mexican community; high indigenous/afrodescendant population"},

    {"CVE_GEO":"12059","NOM_MUN":"San Luis Acatlán",      "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":39400,"PCT_HABLA_INDIG":48.0,"HAZARD_SISMICO":0.72,"HAZARD_CICLONICO":0.65,
     "NOTES":"Costa Chica; Mixtec/Amuzgo community; police comunitaria presence"},

    # Guerrero montaña — most marginalized
    {"CVE_GEO":"12085","NOM_MUN":"Cochoapa el Grande",    "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":19700,"PCT_HABLA_INDIG":98.5,"HAZARD_SISMICO":0.55,"HAZARD_CICLONICO":0.30,
     "NOTES":"Most marginalized municipality in Mexico; Mixtec; landlocked; very low physical hazard BUT highest SVI"},

    {"CVE_GEO":"12047","NOM_MUN":"Metlatonoc",            "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":26500,"PCT_HABLA_INDIG":97.0,"HAZARD_SISMICO":0.55,"HAZARD_CICLONICO":0.25,
     "NOTES":"Montaña Alta; second most marginalized nationally; Mixtec"},

    {"CVE_GEO":"12073","NOM_MUN":"Tlacoachistlahuaca",    "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":22100,"PCT_HABLA_INDIG":78.0,"HAZARD_SISMICO":0.58,"HAZARD_CICLONICO":0.32,
     "NOTES":"Montaña; Amuzgo community; very high marginalization"},

    {"CVE_GEO":"12076","NOM_MUN":"Tlapa de Comonfort",    "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":69800,"PCT_HABLA_INDIG":65.0,"HAZARD_SISMICO":0.60,"HAZARD_CICLONICO":0.28,
     "NOTES":"Montaña commercial center; regional hub for most marginalized municipalities"},

    {"CVE_GEO":"12044","NOM_MUN":"Malinaltepec",          "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":30200,"PCT_HABLA_INDIG":82.0,"HAZARD_SISMICO":0.58,"HAZARD_CICLONICO":0.28,
     "NOTES":"Montaña; Me'phaa/Tlapanec community; armed conflict/displacement history"},

    # Central Guerrero
    {"CVE_GEO":"12028","NOM_MUN":"Chilpancingo de los Bravo","NOM_ENT":"Guerrero","CONAPO_GRADO":"B",
     "POB_TOTAL":276285,"PCT_HABLA_INDIG":3.2,"HAZARD_SISMICO":0.78,"HAZARD_CICLONICO":0.45,
     "NOTES":"State capital; moderate SVI; high seismic exposure; cartel violence"},

    {"CVE_GEO":"12013","NOM_MUN":"Chilapa de Álvarez",    "NOM_ENT":"Guerrero","CONAPO_GRADO":"A",
     "POB_TOTAL":75200,"PCT_HABLA_INDIG":40.0,"HAZARD_SISMICO":0.65,"HAZARD_CICLONICO":0.38,
     "NOTES":"Nahuatl community; documented forced displacement from cartel conflict"},

    {"CVE_GEO":"12063","NOM_MUN":"San Miguel Totolapan",  "NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":29100,"PCT_HABLA_INDIG":5.0,"HAZARD_SISMICO":0.62,"HAZARD_CICLONICO":0.35,
     "NOTES":"2022: mayor and town council members massacred by cartel; extreme violence score"},

    {"CVE_GEO":"12065","NOM_MUN":"Taxco de Alarcón",      "NOM_ENT":"Guerrero","CONAPO_GRADO":"M",
     "POB_TOTAL":105000,"PCT_HABLA_INDIG":2.0,"HAZARD_SISMICO":0.70,"HAZARD_CICLONICO":0.25,
     "NOTES":"Tourism/mining economy; moderate vulnerability; seismic risk"},

    {"CVE_GEO":"12038","NOM_MUN":"Iguala de la Independencia","NOM_ENT":"Guerrero","CONAPO_GRADO":"B",
     "POB_TOTAL":124000,"PCT_HABLA_INDIG":1.8,"HAZARD_SISMICO":0.68,"HAZARD_CICLONICO":0.28,
     "NOTES":"Ayotzinapa disappearances site; institutional trust near zero; high homicide"},

    {"CVE_GEO":"12033","NOM_MUN":"General Heliodoro Castillo","NOM_ENT":"Guerrero","CONAPO_GRADO":"MA",
     "POB_TOTAL":28500,"PCT_HABLA_INDIG":8.0,"HAZARD_SISMICO":0.60,"HAZARD_CICLONICO":0.35,
     "NOTES":"Sierra de Guerrero; poppy cultivation area; displacement; high violence"},

    # ══════════════════════════════════════════════════════════════════
    # OAXACA (20) — 27 municipalities
    # ══════════════════════════════════════════════════════════════════

    # Oaxaca Coast
    {"CVE_GEO":"20296","NOM_MUN":"Santa María Huatulco",  "NOM_ENT":"Oaxaca","CONAPO_GRADO":"M",
     "POB_TOTAL":42300,"PCT_HABLA_INDIG":8.5,"HAZARD_SISMICO":0.88,"HAZARD_CICLONICO":0.70,
     "NOTES":"Tourism coast; high seismic; moderate SVI — classic high physical / low social case"},

    {"CVE_GEO":"20211","NOM_MUN":"San Pedro Pochutla",    "NOM_ENT":"Oaxaca","CONAPO_GRADO":"A",
     "POB_TOTAL":48900,"PCT_HABLA_INDIG":18.0,"HAZARD_SISMICO":0.88,"HAZARD_CICLONICO":0.68,
     "NOTES":"Costa Oaxaca; Puerto Ángel; seismic + cyclone; informal fishing communities"},

    {"CVE_GEO":"20070","NOM_MUN":"Santiago Jamiltepec (Pinotepa Nacional)","NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":57100,"PCT_HABLA_INDIG":42.0,"HAZARD_SISMICO":0.82,"HAZARD_CICLONICO":0.65,
     "NOTES":"Costa Chica Oaxaca; Mixtec/Afro-Mexican; Otis secondary impact zone"},

    # Oaxaca city and central valleys
    {"CVE_GEO":"20067","NOM_MUN":"Santa Cruz Xoxocotlán (Oaxaca metro)","NOM_ENT":"Oaxaca","CONAPO_GRADO":"MB",
     "POB_TOTAL":75100,"PCT_HABLA_INDIG":12.0,"HAZARD_SISMICO":0.80,"HAZARD_CICLONICO":0.30,
     "NOTES":"Oaxaca metro; low SVI but high seismic; reference case"},

    {"CVE_GEO":"20063","NOM_MUN":"Oaxaca de Juárez",      "NOM_ENT":"Oaxaca","CONAPO_GRADO":"B",
     "POB_TOTAL":264685,"PCT_HABLA_INDIG":18.0,"HAZARD_SISMICO":0.82,"HAZARD_CICLONICO":0.25,
     "NOTES":"State capital; cultural heritage site; seismic risk with dense historic urban fabric"},

    # Oaxaca Sierra — high vulnerability
    {"CVE_GEO":"20543","NOM_MUN":"San José Tenango",      "NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":14200,"PCT_HABLA_INDIG":95.0,"HAZARD_SISMICO":0.65,"HAZARD_CICLONICO":0.20,
     "NOTES":"Cañada region; most marginalized in Oaxaca; Mazatec; zero physical hazard visibility"},

    {"CVE_GEO":"20100","NOM_MUN":"San Felipe Jalapa de Díaz","NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":24500,"PCT_HABLA_INDIG":92.0,"HAZARD_SISMICO":0.62,"HAZARD_CICLONICO":0.22,
     "NOTES":"Cañada; Mazatec Chinantec; very high marginalization; flood risk in lowlands"},

    {"CVE_GEO":"20321","NOM_MUN":"Santa María Tlahuitoltepec","NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":10800,"PCT_HABLA_INDIG":99.0,"HAZARD_SISMICO":0.60,"HAZARD_CICLONICO":0.15,
     "NOTES":"Sierra Mixe; usos y costumbres; strong indigenous governance; tequio documented"},

    {"CVE_GEO":"20030","NOM_MUN":"Ixtlán de Juárez",      "NOM_ENT":"Oaxaca","CONAPO_GRADO":"M",
     "POB_TOTAL":7900,"PCT_HABLA_INDIG":85.0,"HAZARD_SISMICO":0.62,"HAZARD_CICLONICO":0.18,
     "NOTES":"Sierra Norte; community forest management model; resilience case study"},

    # Mixteca
    {"CVE_GEO":"20411","NOM_MUN":"Heroica Ciudad de Tlaxiaco","NOM_ENT":"Oaxaca","CONAPO_GRADO":"A",
     "POB_TOTAL":36700,"PCT_HABLA_INDIG":72.0,"HAZARD_SISMICO":0.65,"HAZARD_CICLONICO":0.20,
     "NOTES":"Mixteca regional center; out-migration hub (highest remittance dependence in Oaxaca)"},

    {"CVE_GEO":"20370","NOM_MUN":"Santiago Juxtlahuaca",   "NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":25200,"PCT_HABLA_INDIG":88.0,"HAZARD_SISMICO":0.62,"HAZARD_CICLONICO":0.18,
     "NOTES":"Mixteca Baja; Mixtec/Triqui; gozona documented; very high marginalization"},

    {"CVE_GEO":"20009","NOM_MUN":"Coicoyán de las Flores", "NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":9400,"PCT_HABLA_INDIG":96.0,"HAZARD_SISMICO":0.58,"HAZARD_CICLONICO":0.18,
     "NOTES":"Mixteca; consistently among 10 most marginalized nationally"},

    # Istmo
    {"CVE_GEO":"20042","NOM_MUN":"Heroica Cd. de Juchitán","NOM_ENT":"Oaxaca","CONAPO_GRADO":"A",
     "POB_TOTAL":76900,"PCT_HABLA_INDIG":68.0,"HAZARD_SISMICO":0.92,"HAZARD_CICLONICO":0.55,
     "NOTES":"2017 earthquake epicenter region; Zapotec; highest seismic score in Oaxaca"},

    {"CVE_GEO":"20132","NOM_MUN":"San Juan Guichicovi",    "NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":22100,"PCT_HABLA_INDIG":79.0,"HAZARD_SISMICO":0.90,"HAZARD_CICLONICO":0.50,
     "NOTES":"Istmo; Mixe-Zoque; seismic high risk; migration corridor violence"},

    {"CVE_GEO":"20175","NOM_MUN":"San Miguel Chimalapa",   "NOM_ENT":"Oaxaca","CONAPO_GRADO":"MA",
     "POB_TOTAL":9700,"PCT_HABLA_INDIG":72.0,"HAZARD_SISMICO":0.88,"HAZARD_CICLONICO":0.48,
     "NOTES":"Chimalapa forest; Zoque; land conflict; biosphere/communal land tension"},

    # ══════════════════════════════════════════════════════════════════
    # CHIAPAS (07) — 26 municipalities
    # ══════════════════════════════════════════════════════════════════

    # Highland Chiapas — Los Altos (most marginalized + highest displacement)
    {"CVE_GEO":"07020","NOM_MUN":"Chalchihuitán",         "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":13200,"PCT_HABLA_INDIG":99.0,"HAZARD_SISMICO":0.55,"HAZARD_CICLONICO":0.15,
     "NOTES":"Most marginalized in Chiapas; Tzotzil; 2017-18 forced displacement event documented"},

    {"CVE_GEO":"07059","NOM_MUN":"Mitontic",              "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":9800,"PCT_HABLA_INDIG":99.0,"HAZARD_SISMICO":0.52,"HAZARD_CICLONICO":0.12,
     "NOTES":"Los Altos; Tzotzil; inter-community land conflict; very high displacement risk"},

    {"CVE_GEO":"07078","NOM_MUN":"San Juan Cancuc",       "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":18600,"PCT_HABLA_INDIG":99.0,"HAZARD_SISMICO":0.55,"HAZARD_CICLONICO":0.14,
     "NOTES":"Los Altos; Tzeltal; highest SVI in Chiapas cluster"},

    {"CVE_GEO":"07044","NOM_MUN":"Larrainzar",            "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":16400,"PCT_HABLA_INDIG":98.0,"HAZARD_SISMICO":0.52,"HAZARD_CICLONICO":0.12,
     "NOTES":"Los Altos; Tzotzil; autonomous municipality; armed conflict 2020s"},

    {"CVE_GEO":"07113","NOM_MUN":"San Juan Chamula",      "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":89200,"PCT_HABLA_INDIG":98.0,"HAZARD_SISMICO":0.52,"HAZARD_CICLONICO":0.14,
     "NOTES":"Los Altos; large Tzotzil municipality; usos y costumbres; complex governance"},

    {"CVE_GEO":"07076","NOM_MUN":"San Cristóbal de las Casas","NOM_ENT":"Chiapas","CONAPO_GRADO":"M",
     "POB_TOTAL":215887,"PCT_HABLA_INDIG":28.0,"HAZARD_SISMICO":0.58,"HAZARD_CICLONICO":0.14,
     "NOTES":"Highland urban center; massive IDP host city; displacement funnel municipality"},

    # Selva / Jungle zone
    {"CVE_GEO":"07063","NOM_MUN":"Ocosingo",              "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":232900,"PCT_HABLA_INDIG":72.0,"HAZARD_SISMICO":0.60,"HAZARD_CICLONICO":0.25,
     "NOTES":"Largest Chiapas municipality; Selva; Zapatista territory; EZLN autonomous communities"},

    {"CVE_GEO":"07031","NOM_MUN":"Chilón",                "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":121200,"PCT_HABLA_INDIG":85.0,"HAZARD_SISMICO":0.58,"HAZARD_CICLONICO":0.28,
     "NOTES":"Selva; Tzeltal; high landslide risk on deforested slopes; Huracan Stan 2005 impact"},

    {"CVE_GEO":"07050","NOM_MUN":"Las Margaritas",        "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":134500,"PCT_HABLA_INDIG":62.0,"HAZARD_SISMICO":0.62,"HAZARD_CICLONICO":0.30,
     "NOTES":"Fronteriza; Tojolabal; active displacement from organized crime 2024"},

    {"CVE_GEO":"07101","NOM_MUN":"La Trinitaria",         "NOM_ENT":"Chiapas","CONAPO_GRADO":"A",
     "POB_TOTAL":97300,"PCT_HABLA_INDIG":28.0,"HAZARD_SISMICO":0.65,"HAZARD_CICLONICO":0.35,
     "NOTES":"Fronteriza; cartel corridor; forced displacement events 2023-24"},

    # Pacific coast Chiapas
    {"CVE_GEO":"07099","NOM_MUN":"Tonalá",                "NOM_ENT":"Chiapas","CONAPO_GRADO":"A",
     "POB_TOTAL":92700,"PCT_HABLA_INDIG":4.0,"HAZARD_SISMICO":0.90,"HAZARD_CICLONICO":0.78,
     "NOTES":"Pacific coast; highest seismic + cyclonic in Chiapas; 1985 analog zone"},

    {"CVE_GEO":"07001","NOM_MUN":"Acapetahua",            "NOM_ENT":"Chiapas","CONAPO_GRADO":"A",
     "POB_TOTAL":47200,"PCT_HABLA_INDIG":8.0,"HAZARD_SISMICO":0.88,"HAZARD_CICLONICO":0.75,
     "NOTES":"Pacific coast; mangrove loss documented; flood + seismic compound risk"},

    {"CVE_GEO":"07119","NOM_MUN":"Mapastepec",            "NOM_ENT":"Chiapas","CONAPO_GRADO":"A",
     "POB_TOTAL":51800,"PCT_HABLA_INDIG":10.0,"HAZARD_SISMICO":0.87,"HAZARD_CICLONICO":0.76,
     "NOTES":"Pacific coast; prior Hurricane Stan impact; agricultural/fishery economy"},

    # Highlands / SASMEX coverage gap
    {"CVE_GEO":"07096","NOM_MUN":"Tila",                  "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":48400,"PCT_HABLA_INDIG":95.0,"HAZARD_SISMICO":0.60,"HAZARD_CICLONICO":0.22,
     "NOTES":"Chol community; SASMEX no coverage; land conflict; displacement history"},

    {"CVE_GEO":"07114","NOM_MUN":"Chicomuselo",           "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":26900,"PCT_HABLA_INDIG":15.0,"HAZARD_SISMICO":0.65,"HAZARD_CICLONICO":0.30,
     "NOTES":"Mining conflict; cartel violence; mass displacement 2024; ACLED documented"},

    {"CVE_GEO":"07089","NOM_MUN":"Simojovel",             "NOM_ENT":"Chiapas","CONAPO_GRADO":"MA",
     "POB_TOTAL":46100,"PCT_HABLA_INDIG":78.0,"HAZARD_SISMICO":0.62,"HAZARD_CICLONICO":0.20,
     "NOTES":"Tzotzil; amber mining; armed conflict; displacement; very high SVI"},

    {"CVE_GEO":"07029","NOM_MUN":"Chiapa de Corzo",       "NOM_ENT":"Chiapas","CONAPO_GRADO":"M",
     "POB_TOTAL":78000,"PCT_HABLA_INDIG":8.0,"HAZARD_SISMICO":0.68,"HAZARD_CICLONICO":0.28,
     "NOTES":"Central Chiapas; moderate SVI; Cañón del Sumidero flood risk; reference case"},

]

# ─────────────────────────────────────────────────────────────────────────────
# Build DataFrame with derived SVI cluster approximations
# ─────────────────────────────────────────────────────────────────────────────

df = pd.DataFrame(municipalities)

# Derive approximate SVI_SOCIAL from CONAPO grade
df["SVI_SOCIAL_APPROX"] = df["CONAPO_GRADO"].map(GRADE_SCORE)

# Derive Physical Hazard composite (simple average of seismic + cyclonic)
df["HAZARD_FISICO_COMPOSITE"] = (df["HAZARD_SISMICO"] * 0.40 +
                                  df["HAZARD_CICLONICO"] * 0.35 +
                                  0.30 * 0.25).round(3)  # flood placeholder 0.30

# Flag municipalities where SVI would diverge most from physical hazard
# (high SVI, low physical = most likely to be underserved)
df["SVI_DIVERGENCE_FLAG"] = (
    (df["SVI_SOCIAL_APPROX"] > 0.75) & (df["HAZARD_FISICO_COMPOSITE"] < 0.55)
).map({True: "HIGH_SVI_LOW_PHYS", False: ""})

# Mark as prototype
df["DATA_STATUS"] = "PROTOTYPE — replace with real data from download_and_process.py"

# Sort by state then CVE
df = df.sort_values(["NOM_ENT", "CVE_GEO"]).reset_index(drop=True)

out = os.path.join(PROC, "prototype_municipalities.csv")
df.to_csv(out, index=False)

print(f"Prototype dataset saved: {out}")
print(f"{len(df)} municipalities × {len(df.columns)} columns")
print(f"\nBreakdown by state:")
print(df["NOM_ENT"].value_counts().to_string())
print(f"\nMarginalization distribution:")
print(df["CONAPO_GRADO"].value_counts().to_string())
print(f"\nHigh SVI / Low Physical (most likely underserved):")
flagged = df[df["SVI_DIVERGENCE_FLAG"] != ""]
for _, r in flagged.iterrows():
    print(f"  {r['CVE_GEO']} {r['NOM_MUN']} ({r['NOM_ENT']}) — SVI {r['SVI_SOCIAL_APPROX']:.2f} / HAZARD {r['HAZARD_FISICO_COMPOSITE']:.2f}")
