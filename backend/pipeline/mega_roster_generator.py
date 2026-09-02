"""
FM Scout AI (FC Finder) - Mega World Roster Generator (10,000+ Players)
Generates complete squads across 400+ world clubs spanning 25 global leagues:
- Premier League, Championship, League One
- La Liga, La Liga 2
- Serie A, Serie B
- Bundesliga, 2. Bundesliga
- Ligue 1, Ligue 2
- Eredivisie, Liga Portugal, Belgian Pro League, Scottish Premiership
- Swiss Super League, Austrian Bundesliga, Turkish Süper Lig, Danish Superliga
- K-League 1 & K-League 2, J-League 1 & J-League 2
- Brazil Serie A, Argentina Primera Division
- MLS, Saudi Pro League
"""
import random
from typing import List, Dict, Any

CLUBS_DATABASE = [
    # === 1. PREMIER LEAGUE (20 Clubs) ===
    {"club": "London Red", "real": "Arsenal", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 95},
    {"club": "Manchester Blue", "real": "Manchester City", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 96},
    {"club": "Liverpool Red", "real": "Liverpool", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 95},
    {"club": "London White", "real": "Tottenham Hotspur", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 90},
    {"club": "West London Blue", "real": "Chelsea", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 91},
    {"club": "Manchester Red", "real": "Manchester United", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 92},
    {"club": "Birmingham Claret", "real": "Aston Villa", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 88},
    {"club": "Newcastle Black-White", "real": "Newcastle United", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 89},
    {"club": "Brighton Seagulls", "real": "Brighton & Hove Albion", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 85},
    {"club": "East London Claret", "real": "West Ham United", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 86},
    {"club": "South London Eagles", "real": "Crystal Palace", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 84},
    {"club": "Fulham White", "real": "Fulham", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 83},
    {"club": "Bournemouth Red-Black", "real": "Bournemouth", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 82},
    {"club": "Brentford Red", "real": "Brentford", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 82},
    {"club": "Wolverhampton Gold", "real": "Wolverhampton Wanderers", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 83},
    {"club": "Everton Blue", "real": "Everton", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 84},
    {"club": "Nottingham Red", "real": "Nottingham Forest", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 82},
    {"club": "Leicester Blue", "real": "Leicester City", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 83},
    {"club": "Ipswich Blue", "real": "Ipswich Town", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 79},
    {"club": "Southampton Red-White", "real": "Southampton", "league": "Premier League", "tier": 1, "nat": "England", "code": "GB-ENG", "rep": 80},

    # === 2. LA LIGA (20 Clubs) ===
    {"club": "Madrid White", "real": "Real Madrid", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 97},
    {"club": "Catalan Blue", "real": "FC Barcelona", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 96},
    {"club": "Madrid Red", "real": "Atlético Madrid", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 92},
    {"club": "San Sebastián Blue", "real": "Real Sociedad", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 88},
    {"club": "Bilbao Red", "real": "Athletic Club", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 88},
    {"club": "Girona Red", "real": "Girona FC", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 87},
    {"club": "Sevilla White", "real": "Sevilla FC", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 86},
    {"club": "Betis Green", "real": "Real Betis", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 86},
    {"club": "Villarreal Yellow", "real": "Villarreal CF", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 86},
    {"club": "Valencia White", "real": "Valencia CF", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 85},
    {"club": "Osasuna Red", "real": "CA Osasuna", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 82},
    {"club": "Celta Sky Blue", "real": "Celta Vigo", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 82},
    {"club": "Mallorca Red", "real": "RCD Mallorca", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 81},
    {"club": "Rayo White-Red", "real": "Rayo Vallecano", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 80},
    {"club": "Las Palmas Yellow", "real": "UD Las Palmas", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 80},
    {"club": "Alavés Blue-White", "real": "Deportivo Alavés", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 79},
    {"club": "Getafe Blue", "real": "Getafe CF", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 80},
    {"club": "Espanyol Blue-White", "real": "RCD Espanyol", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 80},
    {"club": "Leganés Blue-White", "real": "CD Leganés", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 78},
    {"club": "Valladolid Violet", "real": "Real Valladolid", "league": "La Liga", "tier": 1, "nat": "Spain", "code": "ES", "rep": 78},

    # === 3. SERIE A (20 Clubs) ===
    {"club": "Milan Blue-Black", "real": "Inter Milan", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 94},
    {"club": "Milan Red-Black", "real": "AC Milan", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 92},
    {"club": "Turin Black-White", "real": "Juventus", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 93},
    {"club": "Napoli Sky Blue", "real": "SSC Napoli", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 90},
    {"club": "Bergamo Black-Blue", "real": "Atalanta", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 89},
    {"club": "Roma Red", "real": "AS Roma", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 88},
    {"club": "Lazio Sky Blue", "real": "SS Lazio", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 87},
    {"club": "Florence Purple", "real": "Fiorentina", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 86},
    {"club": "Bologna Red-Blue", "real": "Bologna FC", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 85},
    {"club": "Turin Maroon", "real": "Torino FC", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 83},
    {"club": "Monza Red-White", "real": "AC Monza", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 81},
    {"club": "Genoa Red-Blue", "real": "Genoa CFC", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 81},
    {"club": "Udinese Black-White", "real": "Udinese Calcio", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 80},
    {"club": "Parma Yellow-Blue", "real": "Parma Calcio", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 80},
    {"club": "Cagliari Red-Blue", "real": "Cagliari Calcio", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 79},
    {"club": "Empoli Blue", "real": "Empoli FC", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 79},
    {"club": "Verona Yellow-Blue", "real": "Hellas Verona", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 79},
    {"club": "Como Blue", "real": "Como 1907", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 80},
    {"club": "Lecce Yellow-Red", "real": "US Lecce", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 78},
    {"club": "Venezia Orange-Black", "real": "Venezia FC", "league": "Serie A", "tier": 1, "nat": "Italy", "code": "IT", "rep": 78},

    # === 4. BUNDESLIGA (18 Clubs) ===
    {"club": "München Rot", "real": "Bayern Munich", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 96},
    {"club": "Leverkusen", "real": "Bayer 04 Leverkusen", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 94},
    {"club": "Dortmund Yellow", "real": "Borussia Dortmund", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 92},
    {"club": "Leipzig Red", "real": "RB Leipzig", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 90},
    {"club": "Stuttgart White", "real": "VfB Stuttgart", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 87},
    {"club": "Frankfurt Black-Red", "real": "Eintracht Frankfurt", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 86},
    {"club": "Hoffenheim Blue", "real": "TSG Hoffenheim", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 83},
    {"club": "Freiburg Red", "real": "SC Freiburg", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 84},
    {"club": "Bremen Green", "real": "Werder Bremen", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 82},
    {"club": "Wolfsburg Green", "real": "VfL Wolfsburg", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 83},
    {"club": "Augsburg Red-Green", "real": "FC Augsburg", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 80},
    {"club": "Heidenheim Red-Blue", "real": "1. FC Heidenheim", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 80},
    {"club": "Gladbach Black-Green", "real": "Borussia Mönchengladbach", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 82},
    {"club": "Union Berlin Red", "real": "1. FC Union Berlin", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 81},
    {"club": "Mainz Red", "real": "1. FSV Mainz 05", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 81},
    {"club": "Bochum Blue", "real": "VfL Bochum", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 78},
    {"club": "St. Pauli Brown", "real": "FC St. Pauli", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 79},
    {"club": "Kiel Blue", "real": "Holstein Kiel", "league": "Bundesliga", "tier": 1, "nat": "Germany", "code": "DE", "rep": 77},

    # === 5. LIGUE 1 (18 Clubs) ===
    {"club": "Paris Blue", "real": "Paris Saint-Germain", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 95},
    {"club": "Monaco Red-White", "real": "AS Monaco", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 89},
    {"club": "Brest Red", "real": "Stade Brestois 29", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 85},
    {"club": "Lille Red-Blue", "real": "LOSC Lille", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 87},
    {"club": "Nice Red-Black", "real": "OGC Nice", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 86},
    {"club": "Lyon White", "real": "Olympique Lyonnais", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 87},
    {"club": "Lens Blood-Gold", "real": "RC Lens", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 85},
    {"club": "Marseille Sky Blue", "real": "Olympique de Marseille", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 88},
    {"club": "Rennes Red-Black", "real": "Stade Rennais FC", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 84},
    {"club": "Toulouse Violet", "real": "Toulouse FC", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 81},
    {"club": "Reims Red-White", "real": "Stade de Reims", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 81},
    {"club": "Montpellier Orange", "real": "Montpellier HSC", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 80},
    {"club": "Strasbourg Blue", "real": "RC Strasbourg", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 81},
    {"club": "Nantes Yellow", "real": "FC Nantes", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 80},
    {"club": "Le Havre Sky Blue", "real": "Le Havre AC", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 78},
    {"club": "Auxerre White-Blue", "real": "AJ Auxerre", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 78},
    {"club": "Angers Black-White", "real": "Angers SCO", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 77},
    {"club": "Saint-Étienne Green", "real": "AS Saint-Étienne", "league": "Ligue 1", "tier": 1, "nat": "France", "code": "FR", "rep": 78},

    # === 6. EREDIVISIE (18 Clubs) ===
    {"club": "Eindhoven Red", "real": "PSV Eindhoven", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 86},
    {"club": "Rotterdam White", "real": "Feyenoord", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 85},
    {"club": "Amsterdam Red-White", "real": "AFC Ajax", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 86},
    {"club": "Twente Red", "real": "FC Twente", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 81},
    {"club": "Alkmaar Red-White", "real": "AZ Alkmaar", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 82},
    {"club": "Utrecht Red-White", "real": "FC Utrecht", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 78},
    {"club": "Go Ahead Yellow-Red", "real": "Go Ahead Eagles", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 76},
    {"club": "Nijmegen Red-Green", "real": "NEC Nijmegen", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 76},
    {"club": "Heerenveen Blue-White", "real": "SC Heerenveen", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 76},
    {"club": "Sparta Red-White", "real": "Sparta Rotterdam", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 75},
    {"club": "Zwolle Blue", "real": "PEC Zwolle", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 74},
    {"club": "Sittard Yellow", "real": "Fortuna Sittard", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 74},
    {"club": "Almere Black-Red", "real": "Almere City FC", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 73},
    {"club": "Heracles Black-White", "real": "Heracles Almelo", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 73},
    {"club": "Breda Yellow", "real": "NAC Breda", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 74},
    {"club": "Willem Tricolor", "real": "Willem II", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 74},
    {"club": "Groningen Green-White", "real": "FC Groningen", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 75},
    {"club": "Waalwijk Yellow-Blue", "real": "RKC Waalwijk", "league": "Eredivisie", "tier": 2, "nat": "Netherlands", "code": "NL", "rep": 72},

    # === 7. LIGA PORTUGAL (18 Clubs) ===
    {"club": "Lisbon Green", "real": "Sporting CP", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 88},
    {"club": "Lisbon Red", "real": "SL Benfica", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 88},
    {"club": "Porto Blue", "real": "FC Porto", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 87},
    {"club": "Braga Red", "real": "SC Braga", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 83},
    {"club": "Guimarães White-Black", "real": "Vitória de Guimarães", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 80},
    {"club": "Moreirense Green-White", "real": "Moreirense FC", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 76},
    {"club": "Arouca Yellow", "real": "FC Arouca", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 76},
    {"club": "Famalicao Blue-White", "real": "FC Famalicão", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 77},
    {"club": "Rio Ave Green-White", "real": "Rio Ave FC", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 76},
    {"club": "Gil Vicente Red", "real": "Gil Vicente FC", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 75},
    {"club": "Estoril Yellow-Blue", "real": "Estoril Praia", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 76},
    {"club": "Boavista Black-White", "real": "Boavista FC", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 75},
    {"club": "Casa Pia Black", "real": "Casa Pia AC", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 74},
    {"club": "Farense Black-White", "real": "SC Farense", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 74},
    {"club": "Nacional Black-White", "real": "CD Nacional", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 73},
    {"club": "Santa Clara Red", "real": "CD Santa Clara", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 74},
    {"club": "AVS Red-White", "real": "AVS Futebol SAD", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 73},
    {"club": "Estrela Tricolor", "real": "CF Estrela da Amadora", "league": "Liga Portugal", "tier": 2, "nat": "Portugal", "code": "PT", "rep": 73},

    # === 8. EFL CHAMPIONSHIP (24 Clubs) ===
    {"club": "Leeds White", "real": "Leeds United", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 82},
    {"club": "Burnley Claret", "real": "Burnley FC", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 81},
    {"club": "Sheffield Red-White", "real": "Sheffield United", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 80},
    {"club": "Sunderland Red-White", "real": "Sunderland AFC", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 80},
    {"club": "Middlesbrough Red", "real": "Middlesbrough FC", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 79},
    {"club": "Norwich Yellow", "real": "Norwich City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 79},
    {"club": "West Brom Navy", "real": "West Bromwich Albion", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 79},
    {"club": "Watford Yellow", "real": "Watford FC", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 78},
    {"club": "Coventry Sky Blue", "real": "Coventry City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 78},
    {"club": "Hull Amber-Black", "real": "Hull City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 77},
    {"club": "Bristol Red", "real": "Bristol City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 76},
    {"club": "Blackburn Blue-White", "real": "Blackburn Rovers", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 77},
    {"club": "Preston White", "real": "Preston North End", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 75},
    {"club": "Swansea White", "real": "Swansea City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 76},
    {"club": "QPR Blue-White", "real": "Queens Park Rangers", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 76},
    {"club": "Luton Orange", "real": "Luton Town", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 79},
    {"club": "Stoke Red", "real": "Stoke City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 76},
    {"club": "Millwall Blue", "real": "Millwall FC", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 75},
    {"club": "Derby White-Black", "real": "Derby County", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 75},
    {"club": "Portsmouth Blue", "real": "Portsmouth FC", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 74},
    {"club": "Plymouth Green", "real": "Plymouth Argyle", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 74},
    {"club": "Cardiff Blue", "real": "Cardiff City", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 75},
    {"club": "Oxford Yellow", "real": "Oxford United", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 73},
    {"club": "Sheffield Blue-White", "real": "Sheffield Wednesday", "league": "Championship", "tier": 2, "nat": "England", "code": "GB-ENG", "rep": 75},

    # === 9. BELGIAN PRO LEAGUE (16 Clubs) ===
    {"club": "Brugge Blue-Black", "real": "Club Brugge", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 81},
    {"club": "Union Yellow-Blue", "real": "Royale Union Saint-Gilloise", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 81},
    {"club": "Anderlecht Purple", "real": "RSC Anderlecht", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 80},
    {"club": "Genk Blue", "real": "KRC Genk", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 80},
    {"club": "Gent Blue-White", "real": "KAA Gent", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 79},
    {"club": "Antwerp Red-White", "real": "Royal Antwerp FC", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 79},
    {"club": "Cercle Green-Black", "real": "Cercle Brugge", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 77},
    {"club": "Mechelen Yellow-Red", "real": "KV Mechelen", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 75},
    {"club": "Sint-Truiden Yellow", "real": "Sint-Truidense VV", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 74},
    {"club": "Westerlo Yellow-Blue", "real": "KVC Westerlo", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 74},
    {"club": "Standard Red", "real": "Standard Liège", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 76},
    {"club": "Charleroi Black-White", "real": "Sporting Charleroi", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 74},
    {"club": "Leuven White", "real": "OH Leuven", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 73},
    {"club": "Kortrijk Red", "real": "KV Kortrijk", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 72},
    {"club": "Dender Blue-Black", "real": "FCV Dender EH", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 71},
    {"club": "Beerschot Purple", "real": "K Beerschot VA", "league": "Belgian Pro League", "tier": 3, "nat": "Belgium", "code": "BE", "rep": 71},

    # === 10. TURKISH SÜPER LIG (16 Clubs) ===
    {"club": "Galatasaray Yellow-Red", "real": "Galatasaray SK", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 84},
    {"club": "Fenerbahce Yellow-Navy", "real": "Fenerbahçe SK", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 84},
    {"club": "Besiktas Black-White", "real": "Beşiktaş JK", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 82},
    {"club": "Trabzonspor Claret-Blue", "real": "Trabzonspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 80},
    {"club": "Basaksehir Orange", "real": "İstanbul Başakşehir", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 78},
    {"club": "Samsun Red-White", "real": "Samsunspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 75},
    {"club": "Eyup Violet-Yellow", "real": "Eyüpspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 74},
    {"club": "Sivas Red-White", "real": "Sivasspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 74},
    {"club": "Antalya Red-White", "real": "Antalyaspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 74},
    {"club": "Goztepe Yellow-Red", "real": "Göztepe SK", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 74},
    {"club": "Kasimpasa Navy", "real": "Kasımpaşa SK", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 74},
    {"club": "Rizespor Green-Blue", "real": "Çaykur Rizespor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 73},
    {"club": "Alanya Orange-Green", "real": "Alanyaspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 73},
    {"club": "Gaziantep Red-Black", "real": "Gaziantep FK", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 72},
    {"club": "Konya Green-White", "real": "Konyaspor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 73},
    {"club": "Kayseri Yellow-Red", "real": "Kayserispor", "league": "Süper Lig", "tier": 2, "nat": "Turkey", "code": "TR", "rep": 72},

    # === 11. SCOTTISH PREMIERSHIP & AUSTRIAN & SWISS (20 Clubs) ===
    {"club": "Celtic Green-White", "real": "Celtic FC", "league": "Scottish Premiership", "tier": 2, "nat": "Scotland", "code": "GB-SCT", "rep": 82},
    {"club": "Rangers Blue", "real": "Rangers FC", "league": "Scottish Premiership", "tier": 2, "nat": "Scotland", "code": "GB-SCT", "rep": 81},
    {"club": "Aberdeen Red", "real": "Aberdeen FC", "league": "Scottish Premiership", "tier": 2, "nat": "Scotland", "code": "GB-SCT", "rep": 76},
    {"club": "Hearts Maroon", "real": "Heart of Midlothian", "league": "Scottish Premiership", "tier": 2, "nat": "Scotland", "code": "GB-SCT", "rep": 75},
    {"club": "Hibernian Green", "real": "Hibernian FC", "league": "Scottish Premiership", "tier": 2, "nat": "Scotland", "code": "GB-SCT", "rep": 74},
    {"club": "Salzburg Red", "real": "FC Red Bull Salzburg", "league": "Austrian Bundesliga", "tier": 2, "nat": "Austria", "code": "AT", "rep": 83},
    {"club": "Graz Black-White", "real": "SK Sturm Graz", "league": "Austrian Bundesliga", "tier": 2, "nat": "Austria", "code": "AT", "rep": 80},
    {"club": "LASK Black-White", "real": "LASK", "league": "Austrian Bundesliga", "tier": 2, "nat": "Austria", "code": "AT", "rep": 77},
    {"club": "Rapid Green-White", "real": "SK Rapid Wien", "league": "Austrian Bundesliga", "tier": 2, "nat": "Austria", "code": "AT", "rep": 77},
    {"club": "Austria Wien Violet", "real": "FK Austria Wien", "league": "Austrian Bundesliga", "tier": 2, "nat": "Austria", "code": "AT", "rep": 76},
    {"club": "Young Boys Yellow-Black", "real": "BSC Young Boys", "league": "Swiss Super League", "tier": 2, "nat": "Switzerland", "code": "CH", "rep": 80},
    {"club": "Basel Red-Blue", "real": "FC Basel", "league": "Swiss Super League", "tier": 2, "nat": "Switzerland", "code": "CH", "rep": 79},
    {"club": "Servette Garnet", "real": "Servette FC", "league": "Swiss Super League", "tier": 2, "nat": "Switzerland", "code": "CH", "rep": 77},
    {"club": "Zurich White", "real": "FC Zürich", "league": "Swiss Super League", "tier": 2, "nat": "Switzerland", "code": "CH", "rep": 77},
    {"club": "Lugano Black-White", "real": "FC Lugano", "league": "Swiss Super League", "tier": 2, "nat": "Switzerland", "code": "CH", "rep": 76},
    {"club": "St. Gallen Green-White", "real": "FC St. Gallen", "league": "Swiss Super League", "tier": 2, "nat": "Switzerland", "code": "CH", "rep": 75},
    {"club": "Copenhagen White", "real": "FC Copenhagen", "league": "Danish Superliga", "tier": 2, "nat": "Denmark", "code": "DK", "rep": 80},
    {"club": "Midtjylland Black-Red", "real": "FC Midtjylland", "league": "Danish Superliga", "tier": 2, "nat": "Denmark", "code": "DK", "rep": 79},
    {"club": "Brondby Yellow-Blue", "real": "Brøndby IF", "league": "Danish Superliga", "tier": 2, "nat": "Denmark", "code": "DK", "rep": 78},
    {"club": "Nordsjaelland Red", "real": "FC Nordsjælland", "league": "Danish Superliga", "tier": 2, "nat": "Denmark", "code": "DK", "rep": 77},

    # === 12. K-LEAGUE 1 & K-LEAGUE 2 (25 Clubs) ===
    {"club": "Ulsan Blue", "real": "Ulsan HD FC", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 77},
    {"club": "Jeonbuk Green", "real": "Jeonbuk Hyundai Motors", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 77},
    {"club": "Seoul Red-Black", "real": "FC Seoul", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 76},
    {"club": "Pohang Red-Black", "real": "Pohang Steelers", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 75},
    {"club": "Gwangju Yellow", "real": "Gwangju FC", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 74},
    {"club": "Gangwon Orange", "real": "Gangwon FC", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 74},
    {"club": "Jeju Orange", "real": "Jeju United", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 73},
    {"club": "Daejeon Purple-Green", "real": "Daejeon Hana Citizen", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 73},
    {"club": "Incheon Blue-Black", "real": "Incheon United", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 73},
    {"club": "Suwon FC Red-Blue", "real": "Suwon FC", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 72},
    {"club": "Daegu Sky Blue", "real": "Daegu FC", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 73},
    {"club": "Gimcheon Army Red", "real": "Gimcheon Sangmu", "league": "K-League 1", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 74},
    {"club": "Suwon Blue-Wings", "real": "Suwon Samsung Bluewings", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 73},
    {"club": "Busan Red", "real": "Busan IPark", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 72},
    {"club": "Seoul E-Land Leopard", "real": "Seoul E-Land FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 72},
    {"club": "Anyang Violet", "real": "FC Anyang", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 72},
    {"club": "Bucheon Red-Black", "real": "Bucheon FC 1995", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 71},
    {"club": "Seongnam Black", "real": "Seongnam FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 71},
    {"club": "Jeonnam Yellow", "real": "Jeonnam Dragons", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 71},
    {"club": "Asan Yellow-Blue", "real": "Chungnam Asan FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 70},
    {"club": "Gyeongnam Rose", "real": "Gyeongnam FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 70},
    {"club": "Gimpo Gold-Navy", "real": "Gimpo FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 70},
    {"club": "Cheongju Blue", "real": "Chungbuk Cheongju FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 69},
    {"club": "Cheonan Red-White", "real": "Cheonan City FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 68},
    {"club": "Ansan Green", "real": "Ansan Greeners FC", "league": "K-League 2", "tier": 3, "nat": "South Korea", "code": "KR", "rep": 68},

    # === 13. J-LEAGUE 1 & 2 (20 Clubs) ===
    {"club": "Kobe Crimson", "real": "Vissel Kobe", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 76},
    {"club": "Yokohama Tricolor", "real": "Yokohama F. Marinos", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 76},
    {"club": "Hiroshima Violet", "real": "Sanfrecce Hiroshima", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 76},
    {"club": "Machida Blue", "real": "FC Machida Zelvia", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 75},
    {"club": "Kashima Antlers Red", "real": "Kashima Antlers", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 75},
    {"club": "Gamba Blue-Black", "real": "Gamba Osaka", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 74},
    {"club": "Cerezo Cherry-Pink", "real": "Cerezo Osaka", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 74},
    {"club": "Tokyo Blue-Red", "real": "FC Tokyo", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 74},
    {"club": "Kawasaki Sky Blue", "real": "Kawasaki Frontale", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 75},
    {"club": "Urawa Red", "real": "Urawa Red Diamonds", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 75},
    {"club": "Nagoya Red-Yellow", "real": "Nagoya Grampus", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 74},
    {"club": "Niigata Orange-Blue", "real": "Albirex Niigata", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 73},
    {"club": "Kashiwa Yellow", "real": "Kashiwa Reysol", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 73},
    {"club": "Fukuoka Navy-Silver", "real": "Avispa Fukuoka", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 73},
    {"club": "Verdy Green", "real": "Tokyo Verdy", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 73},
    {"club": "Kyoto Purple", "real": "Kyoto Sanga FC", "league": "J-League 1", "tier": 3, "nat": "Japan", "code": "JP", "rep": 72},
    {"club": "Shimizu Orange", "real": "Shimizu S-Pulse", "league": "J-League 2", "tier": 3, "nat": "Japan", "code": "JP", "rep": 73},
    {"club": "Yokohama Blue", "real": "Yokohama FC", "league": "J-League 2", "tier": 3, "nat": "Japan", "code": "JP", "rep": 72},
    {"club": "Nagasaki Blue-Orange", "real": "V-Varen Nagasaki", "league": "J-League 2", "tier": 3, "nat": "Japan", "code": "JP", "rep": 72},
    {"club": "Yamagata Blue-White", "real": "Montedio Yamagata", "league": "J-League 2", "tier": 3, "nat": "Japan", "code": "JP", "rep": 71},

    # === 14. BRAZIL SERIE A & ARGENTINA (26 Clubs) ===
    {"club": "Botafogo Black-White", "real": "Botafogo", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 83},
    {"club": "Palmeiras Green", "real": "Palmeiras", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 84},
    {"club": "Flamengo Red-Black", "real": "Flamengo", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 84},
    {"club": "Fortaleza Tricolor", "real": "Fortaleza EC", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 79},
    {"club": "Internacional Red", "real": "SC Internacional", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 80},
    {"club": "São Paulo Tricolor", "real": "São Paulo FC", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 81},
    {"club": "Cruzeiro Blue", "real": "Cruzeiro EC", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 80},
    {"club": "Vasco Black-White", "real": "Vasco da Gama", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 79},
    {"club": "Atlético Mineiro Black-White", "real": "Atlético Mineiro", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 81},
    {"club": "Fluminense Tricolor", "real": "Fluminense FC", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 80},
    {"club": "Grêmio Tricolor", "real": "Grêmio FBPA", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 80},
    {"club": "Corinthians Black-White", "real": "Corinthians", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 80},
    {"club": "Athletico Red-Black", "real": "Athletico Paranaense", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 78},
    {"club": "Santos White", "real": "Santos FC", "league": "Brasileirão", "tier": 2, "nat": "Brazil", "code": "BR", "rep": 80},
    {"club": "River Red-White", "real": "River Plate", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 84},
    {"club": "Boca Blue-Gold", "real": "Boca Juniors", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 84},
    {"club": "Vélez Blue-White", "real": "Vélez Sarsfield", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 80},
    {"club": "Huracán White-Red", "real": "Huracán", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 78},
    {"club": "Talleres Blue-White", "real": "Talleres de Córdoba", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 79},
    {"club": "Racing Sky Blue-White", "real": "Racing Club", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 81},
    {"club": "Independiente Red", "real": "CA Independiente", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 79},
    {"club": "Estudiantes Red-White", "real": "Estudiantes de La Plata", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 79},
    {"club": "San Lorenzo Blue-Red", "real": "San Lorenzo", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 78},
    {"club": "Rosario Yellow-Blue", "real": "Rosario Central", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 78},
    {"club": "Newell's Red-Black", "real": "Newell's Old Boys", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 77},
    {"club": "Lanús Garnet", "real": "Club Atlético Lanús", "league": "Liga Argentina", "tier": 2, "nat": "Argentina", "code": "AR", "rep": 77},

    # === 15. MLS & SAUDI PRO LEAGUE (28 Clubs) ===
    {"club": "Miami Pink", "real": "Inter Miami CF", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 82},
    {"club": "LA Black-Gold", "real": "Los Angeles FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 79},
    {"club": "LA Galaxy White", "real": "LA Galaxy", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 79},
    {"club": "Columbus Yellow-Black", "real": "Columbus Crew", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 79},
    {"club": "Cincinnati Orange-Blue", "real": "FC Cincinnati", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 78},
    {"club": "Salt Lake Claret-Cobalt", "real": "Real Salt Lake", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 76},
    {"club": "Seattle Sounders Green", "real": "Seattle Sounders FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 77},
    {"club": "Houston Orange", "real": "Houston Dynamo FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 76},
    {"club": "Minnesota Black-Blue", "real": "Minnesota United FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 75},
    {"club": "Portland Green-Gold", "real": "Portland Timbers", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 76},
    {"club": "Vancouver White-Blue", "real": "Vancouver Whitecaps FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 75},
    {"club": "New York Red", "real": "New York Red Bulls", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 77},
    {"club": "NYCFC Sky Blue", "real": "New York City FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 77},
    {"club": "Philadelphia Navy-Gold", "real": "Philadelphia Union", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 76},
    {"club": "Atlanta Red-Black", "real": "Atlanta United FC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 77},
    {"club": "Orlando Purple", "real": "Orlando City SC", "league": "MLS", "tier": 2, "nat": "United States", "code": "US", "rep": 76},
    {"club": "Riyadh Blue", "real": "Al-Hilal SFC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 85},
    {"club": "Riyadh Yellow", "real": "Al-Nassr FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 84},
    {"club": "Jeddah Yellow-Black", "real": "Al-Ittihad Club", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 83},
    {"club": "Jeddah Green-White", "real": "Al-Ahli Saudi FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 82},
    {"club": "Khobar Red-Yellow", "real": "Al-Qadsiah FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 79},
    {"club": "Riyadh White-Black", "real": "Al-Shabab FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 78},
    {"club": "Dammam Green-Red", "real": "Al-Ettifaq FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 78},
    {"club": "Buraidah Yellow-Blue", "real": "Al-Taawoun FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 76},
    {"club": "Ahsa Blue-Green", "real": "Al-Fateh SC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 75},
    {"club": "Majmaah Orange-Blue", "real": "Al-Fayha FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 74},
    {"club": "Saihat Yellow-Blue", "real": "Al-Khaleej Club", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 74},
    {"club": "Khamis Mushait Red", "real": "Damac FC", "league": "Saudi Pro League", "tier": 2, "nat": "Saudi Arabia", "code": "SA", "rep": 74}
]

NATIONALITY_POOLS = {
    "South Korea": {
        "code": "KR",
        "first": ["민재", "흥민", "강인", "희찬", "준호", "민혁", "영우", "재성", "인범", "규성", "현규", "지성", "승호", "선범", "태환", "영권", "우영", "현석", "진호", "상호", "동원", "동경", "범근", "승우", "성용", "청용", "태욱", "재익", "지수", "진우", "한빈", "기희", "태희", "상우", "명주", "교원", "세진", "성욱", "준수", "원상", "유현", "세훈", "준홍", "강현", "민우", "승민", "도혁", "건희", "현호", "재원"],
        "last": ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍", "배", "백", "설", "엄", "양", "손", "구", "차", "기", "이청", "하", "허", "전", "문", "유", "남", "노", "원", "우", "변", "탁", "도", "주", "나", "마"]
    },
    "England": {
        "code": "GB-ENG",
        "first": ["Harry", "Jude", "Phil", "Bukayo", "Declan", "Cole", "Ollie", "Anthony", "Eberechi", "Kobbie", "Morgan", "Levi", "Curtis", "Adam", "Jacob", "Jack", "James", "Marcus", "Trent", "John", "Ben", "Mason", "Jarrod", "Harvey", "Emile", "Joe", "Sam", "Luke", "Callum", "Lewis", "Dominic", "Tino", "Alex", "Dan", "Max", "Archie", "George", "Noni", "Ethan", "Taylor"],
        "last": ["Kane", "Bellingham", "Foden", "Saka", "Rice", "Palmer", "Watkins", "Gordon", "Eze", "Mainoo", "Rogers", "Colwill", "Jones", "Wharton", "Greaves", "Grealish", "Maddison", "Rashford", "White", "Stones", "Pickford", "Bowen", "Elliott", "Smith", "Alexander", "Walker", "Trippier", "Barnes", "Pope", "Livramento", "Hall", "Guéhi", "Konsa", "Burn", "Dunk", "Solanke", "Madueke", "Nwaneri", "Gray"]
    },
    "Spain": {
        "code": "ES",
        "first": ["Lamine", "Rodri", "Pedri", "Gavi", "Nico", "Dani", "Alejandro", "Pau", "Martín", "Ferran", "Mikel", "Brais", "Cristhian", "Álvaro", "David", "Marc", "Sergio", "Lucas", "Iago", "Borja", "Ander", "Unai", "Robin", "Yeremy", "Alex", "Pablo", "Marcos", "Carlos", "Gerard", "Raúl", "Samu", "Dean", "Cristhian", "Aitor", "Hugo", "Jon", "Beñat", "Oihan", "Diego", "Adrián"],
        "last": ["Yamal", "Hernández", "González", "Páez", "Williams", "Olmo", "Grimaldo", "Cubarsí", "Zubimendi", "Torres", "Merino", "Méndez", "Mosquera", "Morata", "Raya", "Casadó", "García", "Vázquez", "Aspas", "Iglesias", "Herrera", "Simón", "Le Normand", "Pino", "Baena", "Navas", "Ruiz", "Soler", "Omorodion", "Huijsen", "Sancet", "Vivian", "Galarreta", "Paredes", "Duro", "Guerra", "Pepelu", "López"]
    },
    "France": {
        "code": "FR",
        "first": ["Kylian", "William", "Antoine", "Aurélien", "Eduardo", "Bradley", "Warren", "Michael", "Christopher", "Marcus", "Ibrahima", "Dayot", "Theo", "Lucas", "Ousmane", "Rayan", "Manu", "Olivier", "Adrien", "Jules", "Brice", "Kingsley", "Youssouf", "Axel", "Malo", "Jean", "Castello", "Leny", "Maxence", "Enzo", "Désiré", "Magne", "Kouadio", "Randal", "Mathys", "Elye", "Képhren", "Guillaume", "Moussa"],
        "last": ["Mbappé", "Saliba", "Griezmann", "Tchouaméni", "Camavinga", "Barcola", "Zaïre-Emery", "Olise", "Nkunku", "Thuram", "Konaté", "Upamecano", "Hernández", "Digne", "Dembélé", "Cherki", "Koné", "Boscagli", "Rabiot", "Koundé", "Samba", "Coman", "Fofana", "Disasi", "Gusto", "Mateta", "Lukeba", "Yoro", "Doué", "Kolo Muani", "Tel", "Wahi", "Caqueret", "Restes", "Diouf", "Kalimuendo", "Badé", "Akliouche"]
    },
    "Germany": {
        "code": "DE",
        "first": ["Florian", "Jamal", "Kai", "Leroy", "Serge", "Joshua", "Aleksandar", "Antonio", "Nico", "Karim", "Julian", "Maximilian", "Jonathan", "Waldemar", "David", "Kevin", "Pascal", "Robin", "Robert", "Chris", "Brajan", "Tom", "Jan", "Lukas", "Paul", "Lars", "Timo", "Leon", "Denis", "Finn", "Noah", "Can", "Felix", "Niklas", "Angelo", "Jamie", "Atakan", "Merlin", "Rocco", "Keke"],
        "last": ["Wirtz", "Musiala", "Havertz", "Sané", "Gnabry", "Kimmich", "Pavlović", "Rüdiger", "Schlotterbeck", "Adeyemi", "Brandt", "Beier", "Tah", "Anton", "Raum", "Schade", "Groß", "Koch", "Andrich", "Führich", "Gruda", "Bischof", "Thielmann", "Klostermann", "Wanner", "Nmecha", "Werner", "Goretzka", "Stiller", "Leweling", "Karazor", "Mainka", "Dinkçi", "Reitz", "Krauß", "Röhl", "Topp", "Tietz"]
    },
    "Brazil": {
        "code": "BR",
        "first": ["Vinícius", "Rodrygo", "Raphinha", "Gabriel", "Bruno", "Savinho", "Endrick", "Richarlison", "Lucas", "Douglas", "Ederson", "Alisson", "Gleison", "Wenderson", "Marcos", "Danilo", "Carlos", "Matheus", "Vitor", "Andreas", "Joao", "Murillo", "Igor", "Yan", "Bento", "Luiz", "Felipe", "Estêvão", "Gerson", "Luiz", "Beraldo", "Abner", "Vanderson", "André", "Joelinton", "Evanilson", "Paulinho", "Pepê", "Wesley"],
        "last": ["Júnior", "Goes", "Belloli", "Magalhães", "Guimarães", "Moreira", "Felipe", "Andrade", "Paquetá", "Luiz", "Moraes", "Becker", "Bremer", "Galeno", "Corrêa", "Silva", "Augusto", "Cunha", "Roque", "Pereira", "Gomes", "Santiago", "Jesus", "Couto", "Krepski", "Martinelli", "Henrique", "Willian", "Trindade", "Henrique", "Galdames", "Nascimento", "Ribeiro", "Cardoso", "Alves", "Barbosa"]
    },
    "Argentina": {
        "code": "AR",
        "first": ["Lionel", "Julián", "Lautaro", "Alexis", "Enzo", "Rodrigo", "Cristian", "Lisandro", "Alejandro", "Emiliano", "Alan", "Thiago", "Exequiel", "Nahuel", "Gonzalo", "Nicolás", "Guido", "Valentín", "Facundo", "Matías", "Claudio", "Franco", "Lucas", "Máximo", "Nehuén", "Federico", "Joaquín", "Santiago", "Ignacio", "Giuliano", "Valentín", "Kevin", "Ezequiel", "Braian", "Juan", "Pedro", "Bruno", "Geronimo"],
        "last": ["Messi", "Álvarez", "Martínez", "Mac Allister", "Fernández", "De Paul", "Romero", "Garnacho", "Varela", "Almada", "Palacios", "Molina", "Montiel", "González", "Rodríguez", "Carboni", "Buonanotte", "Soulé", "Echeverri", "Armani", "Ocampos", "Perrone", "Pérez", "Beltrán", "Redondo", "Castro", "Miramón", "Simeone", "Barco", "Zenón", "Fernández", "Medina", "Aguirre", "Rulli", "Benítez"]
    },
    "Netherlands": {
        "code": "NL",
        "first": ["Virgil", "Frenkie", "Cody", "Ryan", "Jurriën", "Jeremie", "Calvin", "Joey", "Sem", "Micky", "Teun", "Xavi", "Brian", "Kenneth", "Jorrel", "Nathan", "Stefan", "Denzel", "Tijjani", "Mats", "Bart", "Ian", "Quinten", "Joshua", "Wout", "Noa", "Jerdy", "Lutsharel", "Quilindschy", "Guus", "Mika", "Ruben", "Emanuel", "Luciano", "Givairo", "Kjell", "Dirk", "Youri", "Jan"],
        "last": ["van Dijk", "de Jong", "Gakpo", "Gravenberch", "Timber", "Frimpong", "Stengs", "Veerman", "Steijn", "van de Ven", "Koopmeiners", "Simons", "Brobbey", "Taylor", "Hato", "Aké", "de Vrij", "Dumfries", "Reijnders", "Wieffer", "Verbruggen", "Maatsen", "Zirkzee", "Weghorst", "Lang", "Schouten", "Til", "Godts", "van Bommel", "Emegha", "Valente", "Read", "Scherpen", "Proper", "Baas"]
    },
    "Italy": {
        "code": "IT",
        "first": ["Nicolò", "Federico", "Alessandro", "Destiny", "Guglielmo", "Gianluigi", "Lorenzo", "Davide", "Bryan", "Giacomo", "Mateo", "Riccardo", "Gianluca", "Samuele", "Michael", "Andrea", "Manuel", "Mattia", "Matteo", "Moise", "Cesare", "Tommaso", "Giorgio", "Giovanni", "Francesco", "Sandro", "Daniel", "Edoardo", "Niccolò", "Fabiano", "Diego", "Jacopo", "Marco", "Lorenzo", "Roberto"],
        "last": ["Barella", "Dimarco", "Bastoni", "Udogie", "Vicario", "Donnarumma", "Pellegrini", "Frattesi", "Cristante", "Raspadori", "Retegui", "Calafiori", "Scamacca", "Ricci", "Folorunsho", "Cambiaso", "Locatelli", "Zaccagni", "Darmian", "Kean", "Casadei", "Baldanzi", "Scalvini", "Di Lorenzo", "Acerbi", "Tonali", "Maldini", "Bove", "Pisilli", "Parisi", "Coppola", "Fazzini", "Carnesecchi", "Luperto"]
    },
    "Portugal": {
        "code": "PT",
        "first": ["Cristiano", "Bruno", "Bernardo", "Rafael", "João", "Rúben", "Gonçalo", "Francisco", "Diogo", "Nuno", "Vitinha", "Pedro", "Otávio", "Matheus", "Renato", "Florentino", "Tiago", "Fábio", "José", "António", "Nélson", "Rui", "Chiquinho", "Dany", "Geovany", "Rodrigo", "Tomás", "Eduardo", "Mateus", "Samuel", "Martim", "Dário", "Gustavo", "Afonso", "Vasco", "Heriberto"],
        "last": ["Ronaldo", "Fernandes", "Silva", "Leão", "Neves", "Dias", "Inácio", "Trincão", "Costa", "Mendes", "Ferreira", "Neto", "Monteiro", "Nunes", "Sanches", "Luís", "Dantas", "Vieira", "Sá", "Ramos", "Semedo", "Cancelo", "Patrício", "Mota", "Carvalho", "Quenda", "Mora", "Araújo", "Quaresma", "Fernandes", "Soares", "Fernandes", "Essugo", "Sá", "Moreira", "Sousa"]
    },
    "Japan": {
        "code": "JP",
        "first": ["Kaoru", "Takefusa", "Wataru", "Ritsu", "Takumi", "Takehiro", "Hiroki", "Daichi", "Ayase", "Koki", "Reo", "Hidemasa", "Ao", "Ko", "Shogo", "Zion", "Keito", "Yukinari", "Daizen", "Junya", "Yuta", "Kosei", "Taisei", "Ryoya", "Joel", "Kota", "Seiya", "Shunsuke", "Hayao", "Kodai", "Yuki", "Mao", "Sota", "Ken", "Taishi", "Ryotaro", "Kuryu", "Shinnosuke", "Haruki"],
        "last": ["Mitoma", "Kubo", "Endo", "Doan", "Minamino", "Tomiyasu", "Ito", "Kamada", "Ueda", "Ogawa", "Hatate", "Morita", "Tanaka", "Itakura", "Taniguchi", "Suzuki", "Nakamura", "Sugawara", "Maeda", "Nakayama", "Tani", "Miyashiro", "Morishita", "Fujita", "Takai", "Maikuma", "Mito", "Kawabe", "Sano", "Soma", "Hosoya", "Kitagawa", "Matsuki", "Iwashita", "Araki", "Ohashi", "Seki"]
    }
}

ARCHETYPE_TEMPLATES = {
    "striker_poacher": {
        "role": "Clinical Box Poacher & Finisher",
        "pos": "ST", "sec": "CF", "group": "FW",
        "base": {"kp": 1.1, "prog_p": 1.7, "pass_acc": 74.0, "passes_att": 19.0, "through_balls": 0.20, "crosses_box": 0.2, "shots": 3.8, "box_shots": 3.3, "sot_pct": 47.0, "xg": 0.70, "npxg": 0.62, "goals": 0.72, "dribbles": 1.2, "dribble_pct": 51.0, "carry_dist": 140.0, "fouls_drawn": 1.9, "prog_carries": 2.4, "interceptions": 0.3, "tackles_won": 0.6, "clearances": 0.8, "blocks": 0.4, "recoveries": 2.6, "aerial_pct": 54.0, "ground_duels": 5.1, "aerial_duels": 2.2, "pressures": 13.5}
    },
    "striker_target": {
        "role": "Aerial Target Forward & Post Player",
        "pos": "ST", "sec": "CF", "group": "FW",
        "base": {"kp": 1.3, "prog_p": 2.2, "pass_acc": 72.0, "passes_att": 22.0, "through_balls": 0.22, "crosses_box": 0.3, "shots": 3.4, "box_shots": 2.9, "sot_pct": 45.0, "xg": 0.62, "npxg": 0.54, "goals": 0.60, "dribbles": 1.5, "dribble_pct": 52.0, "carry_dist": 160.0, "fouls_drawn": 2.5, "prog_carries": 2.8, "interceptions": 0.4, "tackles_won": 0.8, "clearances": 1.2, "blocks": 0.5, "recoveries": 3.2, "aerial_pct": 66.0, "ground_duels": 6.8, "aerial_duels": 3.8, "pressures": 16.0}
    },
    "striker_mobile": {
        "role": "High-Mobility Channel Slasher",
        "pos": "ST", "sec": "LW", "group": "FW",
        "base": {"kp": 1.8, "prog_p": 3.2, "pass_acc": 79.0, "passes_att": 28.0, "through_balls": 0.40, "crosses_box": 0.8, "shots": 3.2, "box_shots": 2.4, "sot_pct": 44.0, "xg": 0.54, "npxg": 0.48, "goals": 0.52, "dribbles": 2.4, "dribble_pct": 57.0, "carry_dist": 220.0, "fouls_drawn": 2.2, "prog_carries": 4.2, "interceptions": 0.5, "tackles_won": 1.2, "clearances": 0.6, "blocks": 0.5, "recoveries": 3.8, "aerial_pct": 46.0, "ground_duels": 5.8, "aerial_duels": 1.4, "pressures": 18.0}
    },
    "winger_inverted": {
        "role": "Inside Forward & Goalscoring Slasher",
        "pos": "W", "sec": "RW", "group": "FW",
        "base": {"kp": 2.6, "prog_p": 4.4, "pass_acc": 81.0, "passes_att": 38.0, "through_balls": 0.62, "crosses_box": 1.6, "shots": 3.2, "box_shots": 2.4, "sot_pct": 42.0, "xg": 0.48, "npxg": 0.44, "goals": 0.44, "dribbles": 3.6, "dribble_pct": 60.0, "carry_dist": 275.0, "fouls_drawn": 2.6, "prog_carries": 6.0, "interceptions": 0.6, "tackles_won": 1.5, "clearances": 0.4, "blocks": 0.6, "recoveries": 4.8, "aerial_pct": 36.0, "ground_duels": 6.0, "aerial_duels": 0.5, "pressures": 18.0}
    },
    "winger_dribbler": {
        "role": "1v1 Isolation Pure Dribbler",
        "pos": "W", "sec": "LW", "group": "FW",
        "base": {"kp": 2.2, "prog_p": 3.6, "pass_acc": 78.5, "passes_att": 32.0, "through_balls": 0.42, "crosses_box": 1.5, "shots": 2.6, "box_shots": 1.8, "sot_pct": 39.0, "xg": 0.35, "npxg": 0.35, "goals": 0.30, "dribbles": 4.4, "dribble_pct": 64.0, "carry_dist": 310.0, "fouls_drawn": 2.8, "prog_carries": 7.2, "interceptions": 0.5, "tackles_won": 1.3, "clearances": 0.3, "blocks": 0.4, "recoveries": 4.5, "aerial_pct": 30.0, "ground_duels": 6.2, "aerial_duels": 0.4, "pressures": 16.5}
    },
    "playmaker_10": {
        "role": "Advanced Creative 10 & Pocket Master",
        "pos": "AM", "sec": "CM", "group": "MF",
        "base": {"kp": 3.3, "prog_p": 6.5, "pass_acc": 85.5, "passes_att": 56.0, "through_balls": 0.90, "crosses_box": 1.4, "shots": 2.5, "box_shots": 1.5, "sot_pct": 38.0, "xg": 0.34, "npxg": 0.34, "goals": 0.30, "dribbles": 2.6, "dribble_pct": 63.0, "carry_dist": 245.0, "fouls_drawn": 2.2, "prog_carries": 4.6, "interceptions": 0.8, "tackles_won": 1.5, "clearances": 0.4, "blocks": 0.7, "recoveries": 5.6, "aerial_pct": 38.0, "ground_duels": 5.6, "aerial_duels": 0.5, "pressures": 19.0}
    },
    "midfield_b2b": {
        "role": "Box-to-Box Dynamic Engine",
        "pos": "CM", "sec": "AM", "group": "MF",
        "base": {"kp": 2.0, "prog_p": 6.2, "pass_acc": 87.5, "passes_att": 64.0, "through_balls": 0.50, "crosses_box": 0.8, "shots": 1.8, "box_shots": 0.7, "sot_pct": 34.0, "xg": 0.18, "npxg": 0.18, "goals": 0.16, "dribbles": 1.9, "dribble_pct": 65.0, "carry_dist": 235.0, "fouls_drawn": 2.0, "prog_carries": 3.8, "interceptions": 1.3, "tackles_won": 2.4, "clearances": 1.1, "blocks": 1.0, "recoveries": 7.4, "aerial_pct": 54.0, "ground_duels": 6.8, "aerial_duels": 1.3, "pressures": 23.0}
    },
    "midfield_pivot": {
        "role": "Deep-Lying Regista & Metronome",
        "pos": "DM", "sec": "CM", "group": "MF",
        "base": {"kp": 1.6, "prog_p": 8.0, "pass_acc": 91.5, "passes_att": 82.0, "through_balls": 0.52, "crosses_box": 0.4, "shots": 1.1, "box_shots": 0.3, "sot_pct": 30.0, "xg": 0.10, "npxg": 0.10, "goals": 0.08, "dribbles": 1.2, "dribble_pct": 72.0, "carry_dist": 210.0, "fouls_drawn": 1.8, "prog_carries": 2.6, "interceptions": 1.5, "tackles_won": 2.6, "clearances": 1.5, "blocks": 1.2, "recoveries": 8.0, "aerial_pct": 60.0, "ground_duels": 6.6, "aerial_duels": 1.8, "pressures": 20.0}
    },
    "midfield_destroyer": {
        "role": "Aggressive Ball-Winning Screen",
        "pos": "DM", "sec": "CM", "group": "MF",
        "base": {"kp": 0.9, "prog_p": 5.2, "pass_acc": 87.0, "passes_att": 58.0, "through_balls": 0.22, "crosses_box": 0.2, "shots": 0.7, "box_shots": 0.3, "sot_pct": 26.0, "xg": 0.06, "npxg": 0.06, "goals": 0.04, "dribbles": 0.9, "dribble_pct": 62.0, "carry_dist": 160.0, "fouls_drawn": 1.9, "prog_carries": 1.8, "interceptions": 1.9, "tackles_won": 3.6, "clearances": 2.1, "blocks": 1.5, "recoveries": 8.6, "aerial_pct": 62.0, "ground_duels": 8.0, "aerial_duels": 2.2, "pressures": 26.0}
    },
    "fullback_attacking": {
        "role": "High-Paced Overlapping Wingback",
        "pos": "FB", "sec": "LWB", "group": "DF",
        "base": {"kp": 2.2, "prog_p": 5.8, "pass_acc": 82.5, "passes_att": 60.0, "through_balls": 0.45, "crosses_box": 2.0, "shots": 1.3, "box_shots": 0.5, "sot_pct": 32.0, "xg": 0.12, "npxg": 0.12, "goals": 0.10, "dribbles": 2.4, "dribble_pct": 62.0, "carry_dist": 280.0, "fouls_drawn": 2.0, "prog_carries": 5.0, "interceptions": 1.4, "tackles_won": 2.4, "clearances": 1.8, "blocks": 0.9, "recoveries": 6.5, "aerial_pct": 48.0, "ground_duels": 6.2, "aerial_duels": 1.1, "pressures": 18.0}
    },
    "centerback_stopper": {
        "role": "Aggressive High-Line Stopper",
        "pos": "CB", "sec": "DF", "group": "DF",
        "base": {"kp": 0.3, "prog_p": 4.2, "pass_acc": 91.0, "passes_att": 72.0, "through_balls": 0.15, "crosses_box": 0.05, "shots": 0.5, "box_shots": 0.5, "sot_pct": 30.0, "xg": 0.06, "npxg": 0.06, "goals": 0.05, "dribbles": 0.4, "dribble_pct": 75.0, "carry_dist": 175.0, "fouls_drawn": 0.8, "prog_carries": 1.2, "interceptions": 1.7, "tackles_won": 2.5, "clearances": 4.2, "blocks": 1.6, "recoveries": 7.4, "aerial_pct": 70.0, "ground_duels": 6.5, "aerial_duels": 3.5, "pressures": 12.0}
    },
    "centerback_ballplaying": {
        "role": "Ball-Playing Diagonal Passer CB",
        "pos": "CB", "sec": "LB", "group": "DF",
        "base": {"kp": 0.7, "prog_p": 6.2, "pass_acc": 93.0, "passes_att": 84.0, "through_balls": 0.35, "crosses_box": 0.10, "shots": 0.6, "box_shots": 0.5, "sot_pct": 32.0, "xg": 0.07, "npxg": 0.07, "goals": 0.06, "dribbles": 0.6, "dribble_pct": 78.0, "carry_dist": 210.0, "fouls_drawn": 0.8, "prog_carries": 1.9, "interceptions": 1.4, "tackles_won": 2.1, "clearances": 3.4, "blocks": 1.2, "recoveries": 6.9, "aerial_pct": 64.0, "ground_duels": 5.6, "aerial_duels": 2.3, "pressures": 10.5}
    }
}

def generate_mega_dataset() -> List[Dict[str, Any]]:
    """
    Generates 10,000+ realistic player profiles with Wyscout per-90 metrics,
    Korean names, authentic tactical stats, and market values across 400+ clubs.
    """
    rng = random.Random(2026)
    players = []
    pid_counter = 1000

    squad_archetypes = [
        "striker_poacher", "striker_target", "striker_mobile", "striker_mobile",
        "winger_inverted", "winger_inverted", "winger_dribbler", "winger_dribbler",
        "playmaker_10", "playmaker_10", "midfield_b2b", "midfield_b2b", "midfield_b2b",
        "midfield_pivot", "midfield_pivot", "midfield_destroyer", "midfield_destroyer",
        "fullback_attacking", "fullback_attacking", "fullback_attacking", "fullback_attacking",
        "centerback_stopper", "centerback_stopper", "centerback_stopper",
        "centerback_ballplaying", "centerback_ballplaying"
    ]

    nat_keys = list(NATIONALITY_POOLS.keys())

    for club_info in CLUBS_DATABASE:
        club_name = club_info["club"]
        real_club = club_info["real"]
        league = club_info["league"]
        tier = club_info["tier"]
        home_nat = club_info["nat"]
        rep = club_info["rep"]

        # Number of players to generate per club (35 to 40 players covering 1st team + B-team / U21 prospects)
        squad_size = rng.randint(35, 40)

        for i in range(squad_size):
            arch_key = squad_archetypes[i % len(squad_archetypes)]
            arch_data = ARCHETYPE_TEMPLATES[arch_key]

            # Determine player nationality: 55% home nation, 45% international
            if rng.random() < 0.55:
                p_nat = home_nat
            else:
                p_nat = rng.choice(nat_keys)

            nat_data = NATIONALITY_POOLS.get(p_nat, NATIONALITY_POOLS["England"])
            first_name = rng.choice(nat_data["first"])
            last_name = rng.choice(nat_data["last"])
            nat_code = nat_data["code"]

            if p_nat == "South Korea":
                full_name = f"{last_name} {first_name}"
                korean_name = f"{last_name}{first_name}"
                short_name = f"{first_name[0]}. {first_name[1]}. {last_name}" if len(first_name) >= 2 else f"{first_name[0]}. {last_name}"
            else:
                full_name = f"{first_name} {last_name}"
                korean_name = f"{first_name} {last_name}"
                short_name = f"{first_name[0]}. {last_name}"

            pid = f"p_db_{pid_counter}"
            pid_counter += 1

            age = rng.randint(17, 34)
            foot = rng.choices(["Right", "Left", "Both"], weights=[65, 27, 8])[0]
            height = rng.randint(170, 196) if arch_data["group"] != "FW" else rng.randint(174, 198)

            # Quality multiplier based on club reputation and age
            quality_factor = (rep / 100.0) * rng.uniform(0.85, 1.15)
            
            # Market Value (EUR Millions)
            if quality_factor > 0.96 and age <= 25:
                market_val = round(rng.uniform(35.0, 120.0), 1)
                wage = round(rng.uniform(100.0, 320.0), 1)
            elif quality_factor > 0.88:
                market_val = round(rng.uniform(15.0, 50.0), 1)
                wage = round(rng.uniform(45.0, 150.0), 1)
            elif quality_factor > 0.78:
                market_val = round(rng.uniform(4.0, 18.0), 1)
                wage = round(rng.uniform(15.0, 55.0), 1)
            else:
                market_val = round(rng.uniform(0.5, 5.0), 1)
                wage = round(rng.uniform(3.0, 18.0), 1)

            # Per-90 stats based on archetype + quality jitter
            base_stats = arch_data["base"]
            player_stats = {}
            for sk, sv in base_stats.items():
                stat_jitter = quality_factor * rng.uniform(0.90, 1.10)
                if isinstance(sv, float):
                    player_stats[sk] = round(sv * stat_jitter, 2)
                else:
                    player_stats[sk] = int(sv * stat_jitter)

            players.append({
                "id": pid,
                "name": short_name,
                "full_name": full_name,
                "korean_name": korean_name,
                "age": age,
                "nationality": p_nat,
                "nat_code": nat_code,
                "club": real_club,
                "league": league,
                "league_tier": tier,
                "primary_pos": arch_data["pos"],
                "secondary_pos": arch_data["sec"],
                "pos_group": arch_data["group"],
                "foot": foot,
                "height_cm": height,
                "market_value_eur": market_val,
                "wage_eur_pw": wage,
                "contract_until": 2026 + rng.randint(0, 5),
                "tactical_role": arch_data["role"],
                "stats": {
                    "matches": rng.randint(18, 36),
                    "minutes": rng.randint(1400, 3100),
                    **player_stats
                }
            })

    return players
