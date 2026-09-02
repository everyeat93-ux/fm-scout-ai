"""
FM Scout AI (FC Finder) - Synthetic Full Roster Generator (200+ Additional Players)
Generates statistically consistent, realistic per-90 Wyscout player data
across multiple leagues, positions, and player archetypes with full Korean names.
"""
import random

def generate_additional_world_players():
    # Seed for deterministic generation
    rng = random.Random(42)

    squad_templates = [
        # Premier League
        ("Arsenal", "London Red", "Premier League", 1, [
            ("K. Havertz", "Kai Havertz", "카이 하베르츠", 25, "Germany", "DE", "ST", "AM", "FW", "Left", 193, 75.0, 280.0, "Tactical Space Infiltrator & Aerial Link", "striker_hybrid"),
            ("G. Martinelli", "Gabriel Martinelli", "가브리엘 마르티넬리", 23, "Brazil", "BR", "W", "LW", "FW", "Right", 178, 70.0, 180.0, "High-Speed Sprint Isolation Winger", "winger_speed"),
            ("J. Timber", "Jurriën Timber", "위리엔 팀버", 23, "Netherlands", "NL", "FB", "RB", "DF", "Right", 179, 45.0, 100.0, "Inverted Press-Resistant Fullback", "fullback_playmaker"),
            ("G. Magalhães", "Gabriel Magalhães", "가브리에우 마갈량이스", 26, "Brazil", "BR", "CB", "DF", "DF", "Left", 190, 75.0, 150.0, "Aggressive Aerial Titan & Stopper", "centerback_monster"),
            ("D. Raya", "David Raya", "다비드 라야", 28, "Spain", "ES", "GK", "GK", "GK", "Right", 183, 35.0, 100.0, "Sweeper Keeper & Distribution Master", "goalkeeper_sweeper"),
            ("L. Trossard", "Leandro Trossard", "레안드로 트로사르", 29, "Belgium", "BE", "W", "LW", "FW", "Both", 172, 35.0, 120.0, "Two-Footed Clutch Impact Finisher", "winger_playmaker"),
            ("M. Merino", "Mikel Merino", "미켈 메리노", 28, "Spain", "ES", "CM", "AM", "MF", "Left", 188, 50.0, 130.0, "Aerial Duel Winning Box-to-Box 8", "midfield_destroyer"),
            ("B. White", "Ben White", "벤 화이트", 26, "England", "GB-ENG", "FB", "RB", "DF", "Right", 186, 55.0, 150.0, "Overlapping Playmaking Fullback", "fullback_playmaker")
        ]),
        ("Man City", "Manchester Blue", "Premier League", 1, [
            ("Savinho", "Sávio Moreira", "사비뉴", 20, "Brazil", "BR", "W", "RW", "FW", "Left", 176, 50.0, 70.0, "Tricky 1v1 Brazilian Dribbler", "winger_playmaker"),
            ("J. Doku", "Jérémy Doku", "제레미 도쿠", 22, "Belgium", "BE", "W", "LW", "FW", "Right", 173, 65.0, 90.0, "Explosive Burst 1v1 Dribble King", "winger_speed"),
            ("M. Kovačić", "Mateo Kovačić", "마테오 코바치치", 30, "Croatia", "HR", "CM", "DM", "MF", "Right", 177, 30.0, 160.0, "Press-Evading Transport Midfielder", "midfield_controller"),
            ("R. Dias", "Rúben Dias", "후벵 디아스", 27, "Portugal", "PT", "CB", "DF", "DF", "Right", 187, 80.0, 200.0, "Defensive Leader & Block Master", "centerback_monster"),
            ("M. Akanji", "Manuel Akanji", "마누엘 아칸지", 29, "Switzerland", "CH", "CB", "DM", "DF", "Right", 187, 45.0, 150.0, "Hybrid Stepping-Up Centerback", "centerback_ballplaying"),
            ("Ederson", "Ederson Moraes", "에데르송", 31, "Brazil", "BR", "GK", "GK", "GK", "Left", 188, 35.0, 180.0, "Elite Pinpoint Long-Range Passer", "goalkeeper_sweeper")
        ]),
        ("Liverpool", "Liverpool Red", "Premier League", 1, [
            ("C. Gakpo", "Cody Gakpo", "코디 각포", 25, "Netherlands", "NL", "W", "LW", "FW", "Right", 193, 55.0, 130.0, "Cutting Inside Forward & False 9", "winger_playmaker"),
            ("D. Núñez", "Darwin Núñez", "다르윈 누녜스", 25, "Uruguay", "UY", "ST", "CF", "FW", "Right", 187, 65.0, 150.0, "High-Energy Direct Chaos Striker", "striker_poacher"),
            ("R. Gravenberch", "Ryan Gravenberch", "라이언 흐라번베르흐", 22, "Netherlands", "NL", "DM", "CM", "MF", "Right", 190, 40.0, 100.0, "Long-Striding Progressive Pivot", "midfield_controller"),
            ("C. Jones", "Curtis Jones", "커티스 존스", 23, "England", "GB-ENG", "CM", "AM", "MF", "Right", 185, 35.0, 60.0, "Ball-Retaining Box-to-Box 8", "midfield_controller"),
            ("I. Konaté", "Ibrahima Konaté", "이브라히마 코나테", 25, "France", "FR", "CB", "DF", "DF", "Right", 194, 45.0, 120.0, "Physical Dominator & Recovery Stopper", "centerback_monster"),
            ("Alisson", "Alisson Becker", "알리송 베케르", 31, "Brazil", "BR", "GK", "GK", "GK", "Right", 191, 28.0, 200.0, "World-Class 1v1 Shot Stopper", "goalkeeper_sweeper")
        ]),
        ("Tottenham", "London White", "Premier League", 1, [
            ("Richarlison", "Richarlison de Andrade", "히샬리송", 27, "Brazil", "BR", "ST", "LW", "FW", "Right", 184, 38.0, 130.0, "Relentless Pressing Fox-in-the-Box", "striker_poacher"),
            ("B. Johnson", "Brennan Johnson", "브레넌 존슨", 23, "Wales", "GB-WLS", "W", "RW", "FW", "Right", 186, 48.0, 90.0, "Far-Post Slasher & Speed Runner", "winger_speed"),
            ("P. Sarr", "Pape Matar Sarr", "파페 사르", 21, "Senegal", "SN", "CM", "AM", "MF", "Right", 185, 45.0, 70.0, "Long-Distance Galloping B2B", "midfield_destroyer"),
            ("Y. Bissouma", "Yves Bissouma", "이브 비수마", 27, "Mali", "ML", "DM", "CM", "MF", "Right", 182, 35.0, 100.0, "Aggressive Ball-Winning Pivot", "midfield_destroyer"),
            ("C. Romero", "Cristian Romero", "크리스티안 로메로", 26, "Argentina", "AR", "CB", "DF", "DF", "Right", 185, 65.0, 160.0, "Ultra-Aggressive Interceptor & Stopper", "centerback_monster"),
            ("D. Udogie", "Destiny Udogie", "데스티니 우도기", 21, "Italy", "IT", "FB", "LB", "DF", "Left", 186, 45.0, 80.0, "Inverted Dynamic Power Fullback", "fullback_playmaker"),
            ("G. Vicario", "Guglielmo Vicario", "굴리엘모 비카리오", 27, "Italy", "IT", "GK", "GK", "GK", "Right", 188, 35.0, 90.0, "Acrobatic Reflex Shot Stopper", "goalkeeper_sweeper"),
            ("L. Bergvall", "Lucas Bergvall", "루카스 베리발", 18, "Sweden", "SE", "CM", "AM", "MF", "Right", 187, 12.0, 25.0, "Elegant Scandinavian Wonderkid Playmaker", "midfield_controller")
        ]),
        ("Chelsea", "West London Blue", "Premier League", 1, [
            ("N. Jackson", "Nicolas Jackson", "니콜라 잭슨", 23, "Senegal", "SN", "ST", "CF", "FW", "Right", 186, 40.0, 100.0, "Channel-Running Agile Target", "striker_hybrid"),
            ("C. Nkunku", "Christopher Nkunku", "크리스토퍼 은쿤쿠", 26, "France", "FR", "AM", "SS", "FW", "Right", 175, 65.0, 200.0, "Lethal Inside Box Finisher & 10", "playmaker_classic"),
            ("N. Madueke", "Noni Madueke", "노니 마두에케", 22, "England", "GB-ENG", "W", "RW", "FW", "Left", 182, 35.0, 60.0, "Direct Cutting Slasher Winger", "winger_speed"),
            ("R. Lavia", "Roméo Lavia", "로메오 라비아", 20, "Belgium", "BE", "DM", "CM", "MF", "Right", 181, 35.0, 50.0, "Press-Resistant Pivot Wonderkid", "midfield_controller"),
            ("M. Cucurella", "Marc Cucurella", "마르크 쿠쿠레야", 26, "Spain", "ES", "FB", "LB", "DF", "Left", 173, 30.0, 150.0, "Tenacious Inverted Lockdown Defender", "fullback_defensive"),
            ("L. Colwill", "Levi Colwill", "리바이 콜윌", 21, "England", "GB-ENG", "CB", "LB", "DF", "Left", 187, 50.0, 100.0, "Left-Footed Diagonal Long Passer", "centerback_ballplaying")
        ]),
        ("Man United", "Manchester Red", "Premier League", 1, [
            ("R. Højlund", "Rasmus Højlund", "라스무스 호일룬", 21, "Denmark", "DK", "ST", "CF", "FW", "Left", 191, 65.0, 100.0, "Explosive Physical Channel Striker", "striker_poacher"),
            ("M. Rashford", "Marcus Rashford", "마커스 래시포드", 26, "England", "GB-ENG", "W", "LW", "FW", "Right", 185, 60.0, 300.0, "Long-Distance Power Slasher", "winger_speed"),
            ("A. Garnacho", "Alejandro Garnacho", "알레한드로 가르나초", 20, "Argentina", "AR", "W", "LW", "FW", "Right", 180, 50.0, 60.0, "Direct High-Volume Dribbling Winger", "winger_speed"),
            ("M. Ugarte", "Manuel Ugarte", "마누엘 우가르테", 23, "Uruguay", "UY", "DM", "CM", "MF", "Right", 182, 50.0, 120.0, "Fierce Ground Tackler & Ball Winner", "midfield_destroyer"),
            ("L. Martínez", "Lisandro Martínez", "리산드로 마르티네스", 26, "Argentina", "AR", "CB", "LB", "DF", "Left", 175, 50.0, 140.0, "Aggressive Butcher & Line-Breaking Passer", "centerback_ballplaying"),
            ("A. Onana", "André Onana", "앙드레 오나나", 28, "Cameroon", "CM", "GK", "GK", "GK", "Right", 190, 35.0, 120.0, "High-Line Sweeping Distributor", "goalkeeper_sweeper")
        ]),
        ("Aston Villa", "Birmingham Claret", "Premier League", 1, [
            ("O. Watkins", "Ollie Watkins", "올리 왓킨스", 28, "England", "GB-ENG", "ST", "CF", "FW", "Right", 180, 65.0, 130.0, "High-Energy Box Runner & Finisher", "striker_hybrid"),
            ("M. Rogers", "Morgan Rogers", "모건 로저스", 22, "England", "GB-ENG", "AM", "LW", "MF", "Right", 189, 22.0, 30.0, "Physical Tank Ball Carrier & Gem", "playmaker_classic"),
            ("Y. Tielemans", "Youri Tielemans", "유리 틸레만스", 27, "Belgium", "BE", "CM", "AM", "MF", "Right", 176, 30.0, 150.0, "Long-Range Shooter & Playmaker", "midfield_controller"),
            ("P. Torres", "Pau Torres", "파우 토레스", 27, "Spain", "ES", "CB", "DF", "DF", "Left", 191, 45.0, 100.0, "Elite Progressive Passer CB", "centerback_ballplaying"),
            ("E. Martínez", "Emiliano Martínez", "에밀리아노 마르티네스", 31, "Argentina", "AR", "GK", "GK", "GK", "Right", 195, 28.0, 120.0, "World-Class Clutch Shot Stopper", "goalkeeper_sweeper")
        ]),
        # La Liga
        ("Real Madrid", "Madrid White", "La Liga", 1, [
            ("Rodrygo", "Rodrygo Silva de Goes", "호드리구", 23, "Brazil", "BR", "W", "RW", "FW", "Right", 174, 110.0, 240.0, "Silky Inverted Playmaker & Clutch Scorer", "winger_playmaker"),
            ("A. Tchouaméni", "Aurélien Tchouaméni", "오렐리앙 추아메니", 24, "France", "FR", "DM", "CB", "MF", "Right", 187, 100.0, 200.0, "Physical Shield & Interception King", "midfield_destroyer"),
            ("E. Camavinga", "Eduardo Camavinga", "에두아르도 카마빙가", 21, "France", "FR", "CM", "LB", "MF", "Left", 182, 100.0, 180.0, "Dynamic Sliding Tackler & Escape Artist", "midfield_controller"),
            ("A. Rüdiger", "Antonio Rüdiger", "안토니오 뤼디거", 31, "Germany", "DE", "CB", "DF", "DF", "Right", 190, 25.0, 280.0, "Fierce Monster Stopper & Duelist", "centerback_monster"),
            ("T. Courtois", "Thibaut Courtois", "티보 쿠르투아", 32, "Belgium", "BE", "GK", "GK", "GK", "Left", 200, 28.0, 300.0, "Giant Shot Stopping Wall", "goalkeeper_sweeper"),
            ("A. Güler", "Arda Güler", "아르다 귈레르", 19, "Turkey", "TR", "AM", "RW", "MF", "Left", 175, 45.0, 50.0, "Turkish Wonderkid Pocket Magician", "playmaker_classic"),
            ("Endrick", "Endrick Felipe", "엔드릭", 18, "Brazil", "BR", "ST", "CF", "FW", "Left", 173, 60.0, 60.0, "Explosive Cannon-Foot Wonderkid", "striker_poacher")
        ]),
        ("Barcelona", "Catalan Blue", "La Liga", 1, [
            ("Gavi", "Pablo Páez Gavira", "가비", 20, "Spain", "ES", "CM", "AM", "MF", "Right", 173, 90.0, 140.0, "Relentless Bulldog Presser & Controller", "midfield_destroyer"),
            ("F. de Jong", "Frenkie de Jong", "프렝키 데 용", 27, "Netherlands", "NL", "CM", "DM", "MF", "Right", 181, 70.0, 400.0, "Silky Deep Ball-Carrying Metronome", "midfield_controller"),
            ("D. Olmo", "Dani Olmo", "다니 올모", 26, "Spain", "ES", "AM", "LW", "MF", "Right", 179, 60.0, 180.0, "Half-Space Infiltrator & Finisher", "playmaker_classic"),
            ("R. Araújo", "Ronald Araújo", "로날드 아라우호", 25, "Uruguay", "UY", "CB", "RB", "DF", "Right", 188, 70.0, 150.0, "Supersonic Aerial Duel Titan", "centerback_monster"),
            ("P. Cubarsí", "Pau Cubarsí", "파우 쿠바르시", 17, "Spain", "ES", "CB", "DF", "DF", "Right", 182, 40.0, 30.0, "La Masia Teenage Laser Passing CB", "centerback_ballplaying"),
            ("A. Balde", "Alejandro Balde", "알레한드로 발데", 20, "Spain", "ES", "FB", "LB", "DF", "Left", 175, 40.0, 60.0, "Electrifying Speed Overlapping FB", "fullback_playmaker"),
            ("M. Casadó", "Marc Casadó", "마르크 카사도", 20, "Spain", "ES", "DM", "CM", "MF", "Right", 172, 15.0, 20.0, "Tactical Pivotal Engine Gem", "midfield_destroyer")
        ]),
        # Serie A
        ("Inter Milan", "Milan Blue-Black", "Serie A", 1, [
            ("M. Thuram", "Marcus Thuram", "마르쿠스 튀랑", 27, "France", "FR", "ST", "LW", "FW", "Right", 192, 65.0, 120.0, "Physical Mobile Dynamic Striker", "striker_hybrid"),
            ("H. Çalhanoğlu", "Hakan Çalhanoğlu", "하칸 찰하놀루", 30, "Turkey", "TR", "DM", "CM", "MF", "Right", 178, 45.0, 140.0, "Deep Regista & Set-Piece King", "midfield_controller"),
            ("F. Dimarco", "Federico Dimarco", "페데리코 디마르코", 26, "Italy", "IT", "FB", "LWB", "DF", "Left", 175, 50.0, 90.0, "Deadly Crossing Wingback Cannon", "fullback_playmaker"),
            ("A. Bastoni", "Alessandro Bastoni", "알레산드로 바스토니", 25, "Italy", "IT", "CB", "LB", "DF", "Left", 190, 70.0, 120.0, "Left-Footed Crossing Centerback", "centerback_ballplaying"),
            ("B. Pavard", "Benjamin Pavard", "뱅자맹 파바르", 28, "France", "FR", "CB", "RB", "DF", "Right", 186, 50.0, 110.0, "Calm Interceptor & Ball Player", "centerback_ballplaying")
        ]),
        ("Juventus", "Turin Black-White", "Serie A", 1, [
            ("D. Vlahović", "Dušan Vlahović", "두샨 블라호비치", 24, "Serbia", "RS", "ST", "CF", "FW", "Left", 190, 65.0, 250.0, "Powerhouse Left-Footed Target Cannon", "striker_poacher"),
            ("K. Yıldız", "Kenan Yıldız", "케난 일디즈", 19, "Turkey", "TR", "W", "AM", "FW", "Right", 185, 40.0, 30.0, "Dynamic Del Piero Heir Wonderkid", "winger_playmaker"),
            ("T. Koopmeiners", "Teun Koopmeiners", "퇸 코프메이너르스", 26, "Netherlands", "NL", "AM", "CM", "MF", "Left", 184, 55.0, 100.0, "Goalscoring Midfield Sniper", "playmaker_classic"),
            ("Bremer", "Gleison Bremer", "브레메르", 27, "Brazil", "BR", "CB", "DF", "DF", "Right", 188, 60.0, 120.0, "Uncompromising Physical Stopper", "centerback_monster")
        ]),
        # Bundesliga
        ("Bayern Munich", "München Rot", "Bundesliga", 1, [
            ("L. Sané", "Leroy Sané", "르로이 사네", 28, "Germany", "DE", "W", "RW", "FW", "Left", 183, 60.0, 350.0, "Explosive Left-Footed Sprint Slasher", "winger_speed"),
            ("S. Gnabry", "Serge Gnabry", "세르주 그나브리", 29, "Germany", "DE", "W", "LW", "FW", "Both", 176, 40.0, 300.0, "Clinical Box Inside Scorer", "winger_speed"),
            ("J. Kimmich", "Joshua Kimmich", "요주아 키미히", 29, "Germany", "DE", "CM", "RB", "MF", "Right", 177, 50.0, 380.0, "Pinpoint Volume Passer & Leader", "midfield_controller"),
            ("A. Pavlović", "Aleksandar Pavlović", "알렉산다르 파블로비치", 20, "Germany", "DE", "DM", "CM", "MF", "Right", 188, 50.0, 40.0, "Tactical Visionary Pivot Wonderkid", "midfield_controller"),
            ("D. Upamecano", "Dayot Upamecano", "다요 우파메카노", 25, "France", "FR", "CB", "DF", "DF", "Right", 186, 45.0, 200.0, "Aggressive High-Speed Stopper", "centerback_monster"),
            ("M. Neuer", "Manuel Neuer", "마누엘 노이어", 38, "Germany", "DE", "GK", "GK", "GK", "Right", 193, 4.0, 350.0, "Legendary Sweeper Keeper Pioneer", "goalkeeper_sweeper")
        ]),
        ("Dortmund", "Dortmund Yellow", "Bundesliga", 1, [
            ("S. Guirassy", "Serhou Guirassy", "세르후 기라시", 28, "Guinea", "GN", "ST", "CF", "FW", "Right", 187, 40.0, 120.0, "Clinical Post-Play Box Finisher", "striker_poacher"),
            ("K. Adeyemi", "Karim Adeyemi", "카림 아데예미", 22, "Germany", "DE", "W", "LW", "FW", "Left", 180, 35.0, 90.0, "Supersonic Breakaway Sprinter", "winger_speed"),
            ("J. Brandt", "Julian Brandt", "율리안 브란트", 28, "Germany", "DE", "AM", "CM", "MF", "Right", 185, 40.0, 140.0, "Half-Space Key Passer & 10", "playmaker_classic"),
            ("N. Schlotterbeck", "Nico Schlotterbeck", "니코 슐로터벡", 24, "Germany", "DE", "CB", "LB", "DF", "Left", 191, 40.0, 100.0, "Left-Footed Dominant Long Passer", "centerback_ballplaying"),
            ("G. Kobel", "Gregor Kobel", "그레고르 코벨", 26, "Switzerland", "CH", "GK", "GK", "GK", "Right", 195, 40.0, 90.0, "Elite Reflex Goalie Wall", "goalkeeper_sweeper")
        ]),
        # Ligue 1
        ("PSG", "Paris Blue", "Ligue 1", 1, [
            ("O. Dembélé", "Ousmane Dembélé", "우스만 뎀벨레", 27, "France", "FR", "W", "RW", "FW", "Both", 178, 60.0, 250.0, "Two-Footed Unpredictable Dribble Machine", "winger_playmaker"),
            ("Vitinha", "Vítor Machado Ferreira", "비티냐", 24, "Portugal", "PT", "CM", "DM", "MF", "Right", 172, 55.0, 120.0, "Press-Resistant Metronome & Controller", "midfield_controller"),
            ("W. Zaïre-Emery", "Warren Zaïre-Emery", "워렌 자이르-에메리", 18, "France", "FR", "CM", "RB", "MF", "Right", 178, 60.0, 75.0, "Teenage Physical Powerhouse 8", "midfield_destroyer"),
            ("A. Hakimi", "Achraf Hakimi", "아슈라프 하키미", 25, "Morocco", "MA", "FB", "RB", "DF", "Right", 181, 60.0, 240.0, "World-Class Supersonic Wingback", "fullback_playmaker"),
            ("N. Mendes", "Nuno Mendes", "누누 멘데스", 22, "Portugal", "PT", "FB", "LB", "DF", "Left", 176, 55.0, 100.0, "High-Paced Explosive Overlapper", "fullback_playmaker"),
            ("Marquinhos", "Marcos Aoás Corrêa", "마르퀴뇨스", 30, "Brazil", "BR", "CB", "DM", "DF", "Right", 183, 50.0, 250.0, "Anticipation Leader & Stopper", "centerback_monster"),
            ("G. Donnarumma", "Gianluigi Donnarumma", "잔루이지 돈나룸마", 25, "Italy", "IT", "GK", "GK", "GK", "Right", 196, 35.0, 240.0, "Colossal Shot Stopper", "goalkeeper_sweeper")
        ]),
        # Emerging Talent & Wonderkids (Eredivisie, Portugal, Championship, MLS, K-League)
        ("Ajax", "Amsterdam Red-White", "Eredivisie", 2, [
            ("K. Taylor", "Kenneth Taylor", "케네스 테일러", 22, "Netherlands", "NL", "CM", "AM", "MF", "Both", 182, 15.0, 20.0, "Two-Footed Progressive Playmaker", "midfield_controller"),
            ("J. Hato", "Jorrel Hato", "요렐 하토", 18, "Netherlands", "NL", "CB", "LB", "DF", "Left", 182, 30.0, 15.0, "Generational Teen Left-Footed CB/LB", "centerback_ballplaying"),
            ("B. Brobbey", "Brian Brobbey", "브라이언 브로비", 22, "Netherlands", "NL", "ST", "CF", "FW", "Right", 180, 35.0, 40.0, "Immense Physical Hold-Up Striker", "striker_hybrid")
        ]),
        ("Sporting CP", "Lisbon Green", "Liga Portugal", 2, [
            ("F. Trincão", "Francisco Trincão", "프란시스코 트린캉", 24, "Portugal", "PT", "W", "RW", "FW", "Left", 186, 23.0, 30.0, "Silky Left-Footed Cut-In Winger", "winger_playmaker"),
            ("M. Hjulmand", "Morten Hjulmand", "모르텐 히울만", 25, "Denmark", "DK", "DM", "CM", "MF", "Right", 185, 40.0, 35.0, "Midfield General & Aggressive Tackler", "midfield_destroyer"),
            ("O. Diomande", "Ousmane Diomande", "우스만 디오망데", 20, "Ivory Coast", "CI", "CB", "DF", "DF", "Right", 190, 40.0, 25.0, "Modern Physical Speed CB Wonderkid", "centerback_monster")
        ]),
        ("Benfica", "Lisbon Red", "Liga Portugal", 2, [
            ("O. Kökçü", "Orkun Kökçü", "오르쿤 쾨크취", 23, "Turkey", "TR", "CM", "AM", "MF", "Right", 175, 28.0, 45.0, "Dead-Ball & Long-Range Passing 8", "midfield_controller"),
            ("V. Pavlidis", "Vangelis Pavlidis", "반겔리스 파블리디스", 25, "Greece", "GR", "ST", "CF", "FW", "Right", 186, 25.0, 35.0, "Clinical Box Slasher & Poacher", "striker_poacher"),
            ("Á. Carreras", "Álvaro Carreras", "알바로 카레라스", 21, "Spain", "ES", "FB", "LB", "DF", "Left", 186, 8.0, 15.0, "Attacking Overlapping Fullback Gem", "fullback_playmaker")
        ]),
        ("Porto", "Porto Blue", "Liga Portugal", 2, [
            ("Galeno", "Wenderson Galeno", "갈레노", 26, "Brazil", "BR", "W", "LW", "FW", "Right", 179, 25.0, 35.0, "Rapid Direct Cutting Winger", "winger_speed"),
            ("D. Costa", "Diogo Costa", "디오구 코스타", 24, "Portugal", "PT", "GK", "GK", "GK", "Right", 186, 45.0, 50.0, "World-Class Penalty & Sweeper GK", "goalkeeper_sweeper")
        ]),
        ("K-League & Asia Prospects", "FC Seoul / Ulsan / Jeonbuk", "K-League 1", 3, [
            ("Y. S. Kim", "Young-Gwon Kim", "김영권", 34, "South Korea", "KR", "CB", "DF", "DF", "Left", 186, 1.2, 10.0, "Veteran Left-Footed Long Passing CB", "centerback_ballplaying"),
            ("J. W. Lee", "Jin-Woo Lee", "이진우", 20, "South Korea", "KR", "AM", "CM", "MF", "Right", 176, 1.5, 3.0, "K-League Emerging Creative 10 Gem", "playmaker_classic"),
            ("S. B. Hwang", "Sun-Beom Hwang", "황선범", 19, "South Korea", "KR", "W", "RW", "FW", "Left", 175, 1.0, 2.0, "Rapid High School Dribbler Gem", "winger_speed"),
            ("T. H. Park", "Tae-Hwan Park", "박태환", 22, "South Korea", "KR", "FB", "RB", "DF", "Right", 179, 1.2, 3.0, "Workhorse Sprinting Fullback", "fullback_defensive")
        ])
    ]

    # Archetype base stat distribution profiles
    archetype_stats = {
        "striker_poacher": {"kp": 1.1, "prog_p": 1.7, "pass_acc": 74.0, "passes_att": 19.0, "through_balls": 0.20, "crosses_box": 0.2, "shots": 3.7, "box_shots": 3.2, "sot_pct": 46.0, "xg": 0.68, "npxg": 0.60, "goals": 0.68, "dribbles": 1.2, "dribble_pct": 51.0, "carry_dist": 140.0, "fouls_drawn": 1.9, "prog_carries": 2.4, "interceptions": 0.3, "tackles_won": 0.6, "clearances": 0.8, "blocks": 0.4, "recoveries": 2.6, "aerial_pct": 54.0, "ground_duels": 5.1, "aerial_duels": 2.2, "pressures": 13.5},
        "striker_hybrid": {"kp": 1.8, "prog_p": 3.2, "pass_acc": 79.0, "passes_att": 28.0, "through_balls": 0.38, "crosses_box": 0.6, "shots": 3.1, "box_shots": 2.4, "sot_pct": 43.0, "xg": 0.52, "npxg": 0.46, "goals": 0.50, "dribbles": 2.0, "dribble_pct": 56.0, "carry_dist": 200.0, "fouls_drawn": 2.2, "prog_carries": 3.8, "interceptions": 0.5, "tackles_won": 1.1, "clearances": 0.7, "blocks": 0.5, "recoveries": 3.6, "aerial_pct": 48.0, "ground_duels": 5.8, "aerial_duels": 1.6, "pressures": 17.5},
        "winger_speed": {"kp": 2.0, "prog_p": 3.5, "pass_acc": 78.0, "passes_att": 30.0, "through_balls": 0.38, "crosses_box": 1.4, "shots": 2.9, "box_shots": 2.1, "sot_pct": 41.0, "xg": 0.42, "npxg": 0.42, "goals": 0.39, "dribbles": 3.8, "dribble_pct": 59.0, "carry_dist": 280.0, "fouls_drawn": 2.4, "prog_carries": 6.2, "interceptions": 0.5, "tackles_won": 1.3, "clearances": 0.3, "blocks": 0.5, "recoveries": 4.4, "aerial_pct": 32.0, "ground_duels": 5.8, "aerial_duels": 0.5, "pressures": 17.0},
        "winger_playmaker": {"kp": 2.9, "prog_p": 4.8, "pass_acc": 82.0, "passes_att": 42.0, "through_balls": 0.72, "crosses_box": 1.8, "shots": 2.7, "box_shots": 1.8, "sot_pct": 40.0, "xg": 0.38, "npxg": 0.38, "goals": 0.34, "dribbles": 3.2, "dribble_pct": 62.0, "carry_dist": 260.0, "fouls_drawn": 2.4, "prog_carries": 5.4, "interceptions": 0.7, "tackles_won": 1.5, "clearances": 0.4, "blocks": 0.6, "recoveries": 4.9, "aerial_pct": 36.0, "ground_duels": 6.0, "aerial_duels": 0.4, "pressures": 18.0},
        "playmaker_classic": {"kp": 3.2, "prog_p": 6.4, "pass_acc": 85.5, "passes_att": 54.0, "through_balls": 0.88, "crosses_box": 1.2, "shots": 2.4, "box_shots": 1.4, "sot_pct": 38.0, "xg": 0.32, "npxg": 0.32, "goals": 0.28, "dribbles": 2.4, "dribble_pct": 64.0, "carry_dist": 240.0, "fouls_drawn": 2.2, "prog_carries": 4.4, "interceptions": 0.8, "tackles_won": 1.5, "clearances": 0.4, "blocks": 0.7, "recoveries": 5.6, "aerial_pct": 38.0, "ground_duels": 5.5, "aerial_duels": 0.5, "pressures": 18.5},
        "midfield_controller": {"kp": 2.1, "prog_p": 7.4, "pass_acc": 89.5, "passes_att": 70.0, "through_balls": 0.58, "crosses_box": 0.6, "shots": 1.4, "box_shots": 0.5, "sot_pct": 33.0, "xg": 0.14, "npxg": 0.14, "goals": 0.12, "dribbles": 1.8, "dribble_pct": 68.0, "carry_dist": 220.0, "fouls_drawn": 1.9, "prog_carries": 3.4, "interceptions": 1.3, "tackles_won": 2.4, "clearances": 1.1, "blocks": 1.0, "recoveries": 7.2, "aerial_pct": 50.0, "ground_duels": 6.4, "aerial_duels": 1.0, "pressures": 21.0},
        "midfield_destroyer": {"kp": 1.1, "prog_p": 5.6, "pass_acc": 88.0, "passes_att": 62.0, "through_balls": 0.28, "crosses_box": 0.3, "shots": 0.9, "box_shots": 0.4, "sot_pct": 28.0, "xg": 0.08, "npxg": 0.08, "goals": 0.06, "dribbles": 1.2, "dribble_pct": 65.0, "carry_dist": 180.0, "fouls_drawn": 1.8, "prog_carries": 2.2, "interceptions": 1.8, "tackles_won": 3.4, "clearances": 1.8, "blocks": 1.4, "recoveries": 8.4, "aerial_pct": 60.0, "ground_duels": 7.8, "aerial_duels": 1.8, "pressures": 25.0},
        "fullback_playmaker": {"kp": 2.0, "prog_p": 5.6, "pass_acc": 83.0, "passes_att": 58.0, "through_balls": 0.45, "crosses_box": 1.8, "shots": 1.1, "box_shots": 0.4, "sot_pct": 32.0, "xg": 0.11, "npxg": 0.11, "goals": 0.09, "dribbles": 2.2, "dribble_pct": 62.0, "carry_dist": 260.0, "fouls_drawn": 1.8, "prog_carries": 4.6, "interceptions": 1.4, "tackles_won": 2.4, "clearances": 1.8, "blocks": 0.9, "recoveries": 6.4, "aerial_pct": 50.0, "ground_duels": 6.0, "aerial_duels": 1.2, "pressures": 17.5},
        "fullback_defensive": {"kp": 0.9, "prog_p": 4.4, "pass_acc": 85.0, "passes_att": 52.0, "through_balls": 0.20, "crosses_box": 0.8, "shots": 0.5, "box_shots": 0.3, "sot_pct": 28.0, "xg": 0.05, "npxg": 0.05, "goals": 0.04, "dribbles": 1.1, "dribble_pct": 60.0, "carry_dist": 180.0, "fouls_drawn": 1.2, "prog_carries": 2.4, "interceptions": 1.6, "tackles_won": 2.8, "clearances": 2.6, "blocks": 1.2, "recoveries": 6.6, "aerial_pct": 58.0, "ground_duels": 6.4, "aerial_duels": 1.8, "pressures": 18.0},
        "centerback_monster": {"kp": 0.3, "prog_p": 3.8, "pass_acc": 90.0, "passes_att": 68.0, "through_balls": 0.12, "crosses_box": 0.04, "shots": 0.5, "box_shots": 0.5, "sot_pct": 30.0, "xg": 0.06, "npxg": 0.06, "goals": 0.05, "dribbles": 0.4, "dribble_pct": 74.0, "carry_dist": 160.0, "fouls_drawn": 0.7, "prog_carries": 1.0, "interceptions": 1.6, "tackles_won": 2.4, "clearances": 4.5, "blocks": 1.6, "recoveries": 7.0, "aerial_pct": 70.0, "ground_duels": 6.2, "aerial_duels": 3.4, "pressures": 11.5},
        "centerback_ballplaying": {"kp": 0.6, "prog_p": 5.8, "pass_acc": 92.5, "passes_att": 80.0, "through_balls": 0.30, "crosses_box": 0.08, "shots": 0.6, "box_shots": 0.5, "sot_pct": 32.0, "xg": 0.07, "npxg": 0.07, "goals": 0.06, "dribbles": 0.6, "dribble_pct": 76.0, "carry_dist": 200.0, "fouls_drawn": 0.8, "prog_carries": 1.8, "interceptions": 1.4, "tackles_won": 2.0, "clearances": 3.6, "blocks": 1.3, "recoveries": 6.8, "aerial_pct": 64.0, "ground_duels": 5.6, "aerial_duels": 2.4, "pressures": 10.5},
        "goalkeeper_sweeper": {"kp": 0.4, "prog_p": 4.2, "pass_acc": 82.0, "passes_att": 35.0, "through_balls": 0.10, "crosses_box": 0.0, "shots": 0.0, "box_shots": 0.0, "sot_pct": 0.0, "xg": 0.0, "npxg": 0.0, "goals": 0.0, "dribbles": 0.1, "dribble_pct": 90.0, "carry_dist": 40.0, "fouls_drawn": 0.3, "prog_carries": 0.2, "interceptions": 0.4, "tackles_won": 0.2, "clearances": 1.8, "blocks": 0.1, "recoveries": 4.5, "aerial_pct": 75.0, "ground_duels": 1.2, "aerial_duels": 1.1, "pressures": 1.2}
    }

    world_players = []
    pid_idx = 100

    for club_name, pseudo_club, league, tier, roster in squad_templates:
        for p_data in roster:
            name, full_name, kor_name, age, nat, nat_code, pos, sec_pos, group, foot, ht, val, wage, role, arch = p_data
            pid = f"p_syn_{pid_idx}"
            pid_idx += 1

            # Base stats with slight natural variation (+- 4%)
            base_st = archetype_stats.get(arch, archetype_stats["striker_poacher"])
            stats = {}
            for k, v in base_st.items():
                jitter = rng.uniform(0.96, 1.04)
                stats[k] = round(v * jitter, 2) if isinstance(v, float) else v

            world_players.append({
                "id": pid,
                "name": name,
                "full_name": full_name,
                "korean_name": kor_name,
                "age": age,
                "nationality": nat,
                "nat_code": nat_code,
                "club": pseudo_club,
                "league": league,
                "league_tier": tier,
                "primary_pos": pos,
                "secondary_pos": sec_pos,
                "pos_group": group,
                "foot": foot,
                "height_cm": ht,
                "market_value_eur": val,
                "wage_eur_pw": wage,
                "contract_until": 2027 + rng.randint(0, 3),
                "tactical_role": role,
                "stats": {
                    "matches": 30,
                    "minutes": 2500,
                    **stats
                }
            })

    return world_players
