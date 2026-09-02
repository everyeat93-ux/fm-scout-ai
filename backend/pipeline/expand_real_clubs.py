# -*- coding: utf-8 -*-
"""
FM Scout AI - Additional 100% Real World Football Squads
Covers:
- Serie A (Inter Milan, AC Milan, Juventus, Napoli, Atalanta, Roma, Lazio, Fiorentina, Torino, Bologna, Como, etc.)
- Ligue 1 (PSG, Marseille, Monaco, Lille, Lyon, Nice, Lens, Rennes, Brest, Reims, etc.)
- Bundesliga (Dortmund, Leipzig, Frankfurt, Stuttgart, Freiburg, Mainz, Wolfsburg, Gladbach, etc.)
- La Liga (Real Sociedad, Athletic Club, Girona, Villarreal, Real Betis, Sevilla, Valencia, Celta, Mallorca, Osasuna, etc.)
- Premier League (West Ham, Crystal Palace, Fulham, Bournemouth, Brentford, Everton, Forest, Leicester, Ipswich, Southampton)
- K-League 1 & 2 (Jeju, Daegu, Suwon FC, Suwon Samsung, Busan IPark, Seongnam, Seoul E-Land, Anyang, Bucheon, Gyeongnam, etc.)
- Eredivisie / Liga Portugal / MLS / Saudi / South America
"""

EXPANDED_REAL_SQUADS = [
    # === SERIE A ===
    ("Inter Milan", "Serie A", 1, "Italy", "IT", 94, [
        ("L. Martínez", "Lautaro Martínez", "라우타로 마르티네스", 27, "Argentina", "AR", "ST", "CF", "FW", "Right", 174, 110.0, 300.0, "세리에 A 득점왕 & 코파 아메리카 득점왕", "st_worldclass"),
        ("M. Thuram", "Marcus Thuram", "마르쿠스 튀람", 27, "France", "FR", "ST", "LW", "FW", "Right", 192, 65.0, 150.0, "피지컬 몬스터 & 다이내믹 포워드", "st_elite"),
        ("N. Barella", "Nicolò Barella", "니콜로 바렐라", 27, "Italy", "IT", "CM", "AM", "MF", "Right", 172, 80.0, 200.0, "지치지 않는 심장 & 박스투박스 에이스", "cm_worldclass"),
        ("H. Çalhanoğlu", "Hakan Çalhanoğlu", "하칸 찰하놀루", 30, "Turkey", "TR", "DM", "CM", "MF", "Right", 178, 45.0, 200.0, "세계 최고 레지스타 & 데드볼 마에스트로", "dm_worldclass"),
        ("H. Mkhitaryan", "Henrikh Mkhitaryan", "헨리크 미키타리안", 35, "Armenia", "AM", "CM", "AM", "MF", "Both", 177, 6.0, 120.0, "축구 지능 & 하프스페이스 연계", "cm_solid"),
        ("F. Dimarco", "Federico Dimarco", "페데리코 디마르코", 26, "Italy", "IT", "LWB", "LB", "DF", "Left", 175, 50.0, 120.0, "악마의 왼발 크로서 & 원더골 제조기", "fb_worldclass"),
        ("D. Dumfries", "Denzel Dumfries", "덴젤 둠프리스", 28, "Netherlands", "NL", "RWB", "RB", "DF", "Right", 188, 20.0, 90.0, "파워풀 직선 돌진 윙백", "fb_elite"),
        ("A. Bastoni", "Alessandro Bastoni", "알레산드로 바스토니", 25, "Italy", "IT", "CB", "DF", "DF", "Left", 190, 70.0, 160.0, "세계 최고 왼발 빌드업 센터백", "cb_worldclass"),
        ("B. Pavard", "Benjamin Pavard", "뱅자맹 파바르", 28, "France", "FR", "CB", "RB", "DF", "Right", 186, 50.0, 150.0, "스마트 멀티 디펜더 & 월드컵 위너", "cb_elite"),
        ("F. Acerbi", "Francesco Acerbi", "프란체스코 아체르비", 36, "Italy", "IT", "CB", "DF", "DF", "Left", 193, 3.5, 90.0, "노련한 홀란드 지우개 & 베테랑 리더", "cb_solid"),
        ("Y. Sommer", "Yann Sommer", "얀 좀머", 35, "Switzerland", "CH", "GK", "GK", "GK", "Right", 183, 5.0, 90.0, "철벽 반사신경 골키퍼", "gk_elite"),
        ("M. Taremi", "Mehdi Taremi", "메디 타레미", 32, "Iran", "IR", "ST", "CF", "FW", "Right", 187, 10.0, 90.0, "아시아 최고 타깃 피니셔", "st_solid"),
        ("D. Frattesi", "Davide Frattesi", "다비데 프라테시", 24, "Italy", "IT", "CM", "AM", "MF", "Right", 178, 35.0, 90.0, "박스 침투 슈퍼 서브 득점원", "cm_elite"),
        ("P. Zieliński", "Piotr Zieliński", "표트르 지엘린스키", 30, "Poland", "PL", "CM", "AM", "MF", "Both", 180, 22.0, 140.0, "양발 드리블 & 중원 테크니션", "cm_elite"),
        ("Y. Bisseck", "Yann Aurel Bisseck", "얀 비섹", 23, "Germany", "DE", "CB", "DF", "DF", "Right", 196, 25.0, 30.0, "초대형 피지컬 신성 센터백", "cb_wonderkid")
    ]),

    ("AC Milan", "Serie A", 1, "Italy", "IT", 91, [
        ("R. Leão", "Rafael Leão", "하파엘 레앙", 25, "Portugal", "PT", "W", "LW", "FW", "Right", 188, 90.0, 175.0, "세리에 A MVP & 압도적 가속 크랙", "winger_worldclass"),
        ("C. Pulisic", "Christian Pulisic", "크리스천 풀리식", 25, "United States", "US", "W", "RW", "FW", "Right", 178, 40.0, 110.0, "캡틴 아메리카 & 전술적 피니셔", "winger_elite"),
        ("Á. Morata", "Álvaro Morata", "알바로 모라타", 31, "Spain", "ES", "ST", "CF", "FW", "Right", 189, 16.0, 150.0, "유로 2024 우승 캡틴 스트라이커", "st_elite"),
        ("T. Reijnders", "Tijjani Reijnders", "티자니 레인더스", 26, "Netherlands", "NL", "CM", "AM", "MF", "Right", 185, 30.0, 55.0, "중원 전진 패서 & 네덜란드 주전", "cm_elite"),
        ("Y. Fofana", "Youssouf Fofana", "유수프 포파나", 25, "France", "FR", "DM", "CM", "MF", "Right", 185, 30.0, 90.0, "프랑스 국대 피지컬 미드필더", "dm_elite"),
        ("R. Loftus-Cheek", "Ruben Loftus-Cheek", "루벤 로프터스-치크", 28, "England", "GB-ENG", "AM", "CM", "MF", "Right", 191, 25.0, 110.0, "피지컬 전진 드리블러", "cm_solid"),
        ("T. Hernández", "Theo Hernández", "테오 에르난데스", 26, "France", "FR", "LB", "LWB", "DF", "Left", 184, 60.0, 130.0, "세계 최고 공격형 레프트백 기관차", "fb_worldclass"),
        ("F. Tomori", "Fikayo Tomori", "피카요 토모리", 26, "England", "GB-ENG", "CB", "DF", "DF", "Right", 185, 32.0, 90.0, "초고속 커버링 센터백", "cb_elite"),
        ("S. Pavlović", "Strahinja Pavlović", "스트라히냐 파블로비치", 23, "Serbia", "RS", "CB", "DF", "DF", "Left", 194, 25.0, 60.0, "괴물 투사형 왼발 센터백", "cb_elite"),
        ("M. Maignan", "Mike Maignan", "마이크 메냥", 29, "France", "FR", "GK", "GK", "GK", "Right", 191, 38.0, 100.0, "프랑스 No.1 매직 핸드 키퍼", "gk_worldclass"),
        ("T. Abraham", "Tammy Abraham", "태미 에이브러햄", 26, "England", "GB-ENG", "ST", "CF", "FW", "Right", 194, 25.0, 120.0, "장신 타깃 포워드", "st_solid"),
        ("S. Chukwueze", "Samuel Chukwueze", "사무엘 추쿠에제", 25, "Nigeria", "NG", "W", "RW", "FW", "Left", 172, 20.0, 90.0, "나이지리아 특급 드리블러", "winger_solid")
    ]),

    ("Juventus", "Serie A", 1, "Italy", "IT", 92, [
        ("D. Vlahović", "Dušan Vlahović", "두샨 블라호비치", 24, "Serbia", "RS", "ST", "CF", "FW", "Left", 190, 65.0, 300.0, "대포알 왼발 슈터 & 폭격기", "st_worldclass"),
        ("K. Yıldız", "Kenan Yıldız", "케난 일디즈", 19, "Turkey", "TR", "AM", "LW", "FW", "Right", 185, 40.0, 20.0, "델 피에로의 후계자 10번 원더키드", "am_wonderkid"),
        ("T. Koopmeiners", "Teun Koopmeiners", "퇸 코프메이너르스", 26, "Netherlands", "NL", "AM", "CM", "MF", "Left", 184, 55.0, 110.0, "세리에 A 최고 공격형 미드필더", "am_elite"),
        ("N. González", "Nicolás González", "니콜라스 곤살레스", 26, "Argentina", "AR", "W", "RW", "FW", "Left", 180, 35.0, 85.0, "코파 우승 아르헨티나 윙어", "winger_elite"),
        ("F. Conceição", "Francisco Conceição", "프란시스코 콘세이상", 21, "Portugal", "PT", "W", "RW", "FW", "Left", 170, 22.0, 35.0, "유로 스타 & 폭풍 드리블 크랙", "winger_wonderkid"),
        ("Douglas Luiz", "Douglas Luiz", "도글라스 루이스", 26, "Brazil", "BR", "CM", "DM", "MF", "Right", 177, 55.0, 130.0, "마스터 패서 & 데드볼 전담", "cm_elite"),
        ("K. Thuram", "Khéphren Thuram", "케프랑 튀람", 23, "France", "FR", "CM", "DM", "MF", "Right", 192, 35.0, 60.0, "거구의 롱스트라이드 드리블러", "cm_elite"),
        ("M. Locatelli", "Manuel Locatelli", "마누엘 로카텔리", 26, "Italy", "IT", "DM", "CM", "MF", "Right", 185, 28.0, 90.0, "유로 우승 딥라잉 플레이메이커", "dm_elite"),
        ("A. Cambiaso", "Andrea Cambiaso", "안드레아 캄비아소", 24, "Italy", "IT", "FB", "LB", "DF", "Both", 182, 30.0, 45.0, "양발 전술 인버티드 풀백", "fb_elite"),
        ("Bremer", "Gleison Bremer", "글레이송 브레메르", 27, "Brazil", "BR", "CB", "DF", "DF", "Right", 188, 60.0, 120.0, "세리에 A 최우수 수비수 & 괴물 스토퍼", "cb_worldclass"),
        ("F. Gatti", "Federico Gatti", "페데리코 가티", 26, "Italy", "IT", "CB", "DF", "DF", "Right", 190, 25.0, 40.0, "골 넣는 파이터 수비수", "cb_solid"),
        ("M. Di Gregorio", "Michele Di Gregorio", "미켈레 디 그레고리오", 27, "Italy", "IT", "GK", "GK", "GK", "Right", 187, 18.0, 50.0, "세리에 A 최우수 골키퍼", "gk_elite")
    ]),

    ("Napoli", "Serie A", 1, "Italy", "IT", 91, [
        ("K. Kvaratskhelia", "Khvicha Kvaratskhelia", "흐비차 크바라츠헬리아", 23, "Georgia", "GE", "W", "LW", "FW", "Both", 183, 80.0, 45.0, "크바라도나 & 멈출 수 없는 크랙", "winger_worldclass"),
        ("R. Lukaku", "Romelu Lukaku", "로멜루 루카쿠", 31, "Belgium", "BE", "ST", "CF", "FW", "Left", 191, 30.0, 150.0, "벨기에 역대 최다 득점 괴물 탱크", "st_elite"),
        ("S. McTominay", "Scott McTominay", "스콧 맥토미니", 27, "Scotland", "GB-SCT", "CM", "AM", "MF", "Right", 191, 32.0, 90.0, "스코틀랜드 폭격기 & 박스 침투 득점원", "cm_elite"),
        ("A. Z. Anguissa", "André-Frank Zambo Anguissa", "앙드레프랑크 잠보 앙귀사", 28, "Cameroon", "CM", "CM", "MF", "MF", "Right", 184, 27.0, 80.0, "중원 탈압박 탱크", "cm_elite"),
        ("S. Lobotka", "Stanislav Lobotka", "스타니슬라프 로보트카", 29, "Slovakia", "SK", "DM", "CM", "MF", "Right", 170, 28.0, 75.0, "나폴리의 모드리치 & 턴 마스터", "dm_elite"),
        ("M. Politano", "Matteo Politano", "마테오 폴리타노", 31, "Italy", "IT", "W", "RW", "FW", "Left", 171, 13.0, 75.0, "고감도 왼발 킥 윙어", "winger_solid"),
        ("David Neres", "David Neres", "다비드 네레스", 27, "Brazil", "BR", "W", "RW", "FW", "Left", 175, 28.0, 70.0, "폭풍 어시스트 삼바 크랙", "winger_elite"),
        ("G. Di Lorenzo", "Giovanni Di Lorenzo", "조반니 디 로렌초", 31, "Italy", "IT", "RB", "DF", "DF", "Right", 183, 15.0, 90.0, "나폴리 우승 캡틴 라이트백", "fb_elite"),
        ("A. Buongiorno", "Alessandro Buongiorno", "알레산드로 부온조르노", 25, "Italy", "IT", "CB", "DF", "DF", "Left", 190, 35.0, 60.0, "이탈리아 국대 주전 센터백", "cb_elite"),
        ("A. Rrahmani", "Amir Rrahmani", "아미르 라흐마니", 30, "Kosovo", "XK", "CB", "DF", "DF", "Right", 192, 15.0, 65.0, "코소보 캡틴 수비수", "cb_solid"),
        ("A. Meret", "Alex Meret", "알렉스 메렛", 27, "Italy", "IT", "GK", "GK", "GK", "Left", 190, 12.0, 45.0, "이탈리아 국대 골키퍼", "gk_solid")
    ]),

    ("Atalanta", "Serie A", 1, "Italy", "IT", 90, [
        ("A. Lookman", "Ademola Lookman", "아데몰라 루크먼", 26, "Nigeria", "NG", "W", "ST", "FW", "Right", 174, 40.0, 50.0, "유로파리그 결승 해트트릭 영웅", "winger_worldclass"),
        ("C. De Ketelaere", "Charles De Ketelaere", "샤를 드 케텔라에르", 23, "Belgium", "BE", "AM", "ST", "FW", "Left", 192, 35.0, 55.0, "벨기에 천재 공격수 & 어시스트 마스터", "am_elite"),
        ("M. Retegui", "Mateo Retegui", "마테오 레테기", 25, "Italy", "IT", "ST", "CF", "FW", "Right", 186, 28.0, 55.0, "세리에 A 득점 선두 & 폭격기", "st_elite"),
        ("M. Pašalić", "Mario Pašalić", "마리오 파샬리치", 29, "Croatia", "HR", "AM", "CM", "MF", "Right", 188, 13.0, 50.0, "박스 침투의 달인", "am_solid"),
        ("Éderson", "Éderson dos Santos", "에데르송", 25, "Brazil", "BR", "CM", "DM", "MF", "Right", 182, 40.0, 40.0, "브라질 국대 전천후 미드필더", "cm_elite"),
        ("M. de Roon", "Marten de Roon", "마르텐 더 론", 33, "Netherlands", "NL", "DM", "CM", "MF", "Right", 185, 8.0, 45.0, "아탈란타의 영원한 캡틴", "dm_solid"),
        ("D. Zappacosta", "Davide Zappacosta", "다비데 자파코스타", 32, "Italy", "IT", "RWB", "RB", "DF", "Right", 182, 6.0, 45.0, "베테랑 윙백", "fb_solid"),
        ("M. Ruggeri", "Matteo Ruggeri", "마테오 루제리", 22, "Italy", "IT", "LWB", "LB", "DF", "Left", 187, 20.0, 20.0, "택배 크로스 레프트 윙백", "fb_wonderkid"),
        ("I. Hien", "Isak Hien", "이사크 히엔", 25, "Sweden", "SE", "CB", "DF", "DF", "Right", 191, 20.0, 30.0, "스웨덴 괴물 피지컬 센터백", "cb_elite"),
        ("M. Carnesecchi", "Marco Carnesecchi", "마르코 카르네세키", 24, "Italy", "IT", "GK", "GK", "GK", "Right", 191, 16.0, 25.0, "이탈리아 차세대 넘버원 골키퍼", "gk_wonderkid")
    ]),

    # === LIGUE 1 ===
    ("Paris Saint-Germain", "Ligue 1", 1, "France", "FR", 94, [
        ("O. Dembélé", "Ousmane Dembélé", "우스만 뎀벨레", 27, "France", "FR", "W", "RW", "FW", "Both", 178, 60.0, 300.0, "양발 드리블 매직 & 기회 창출 머신", "winger_worldclass"),
        ("B. Barcola", "Bradley Barcola", "브래들리 바르콜라", 21, "France", "FR", "W", "LW", "FW", "Right", 186, 65.0, 100.0, "리그 1 득점 선두 & 폭풍 스프린터", "winger_worldclass"),
        ("K. I. Lee", "Lee Kang-in", "이강인", 23, "South Korea", "KR", "AM", "RW", "MF", "Left", 173, 25.0, 80.0, "탈압박 찬스메이커 & 왼발 플레이메이커", "am_elite"),
        ("Vitinha", "Vítor Machado Ferreira", "비티냐", 24, "Portugal", "PT", "CM", "DM", "MF", "Right", 172, 55.0, 120.0, "챔피언스리그 베스트 11 조율사", "cm_worldclass"),
        ("João Neves", "João Neves", "주앙 네베스", 19, "Portugal", "PT", "CM", "DM", "MF", "Right", 174, 60.0, 90.0, "유럽 최고 원더키드 미드필더 & 어시스트 1위", "cm_wonderkid"),
        ("W. Zaïre-Emery", "Warren Zaïre-Emery", "워렌 자이르-에메리", 18, "France", "FR", "CM", "DM", "MF", "Right", 178, 60.0, 100.0, "프랑스 최연소 국가대표 원더키드", "cm_wonderkid"),
        ("F. Ruiz", "Fabián Ruiz", "파비안 루이스", 28, "Spain", "ES", "CM", "AM", "MF", "Left", 189, 35.0, 180.0, "유로 2024 베스트 11 & 우승 주역", "cm_elite"),
        ("A. Hakimi", "Achraf Hakimi", "아슈라프 하키미", 25, "Morocco", "MA", "RB", "RWB", "DF", "Right", 181, 60.0, 240.0, "세계 최고 공격형 라이트백", "fb_worldclass"),
        ("N. Mendes", "Nuno Mendes", "누누 멘데스", 22, "Portugal", "PT", "LB", "LWB", "DF", "Left", 176, 55.0, 140.0, "폭발적 스피드 & 대인방어 레프트백", "fb_worldclass"),
        ("Marquinhos", "Marcos Aoás Corrêa", "마르퀴뇨스", 30, "Brazil", "BR", "CB", "DF", "DF", "Right", 183, 50.0, 240.0, "PSG 영원한 캡틴 & 빌드업 센터백", "cb_elite"),
        ("W. Pacho", "Willian Pacho", "윌리안 파초", 22, "Ecuador", "EC", "CB", "LB", "DF", "Left", 187, 40.0, 80.0, "단단한 왼발 피지컬 스토퍼", "cb_elite"),
        ("G. Donnarumma", "Gianluigi Donnarumma", "잔루이지 돈나룸마", 25, "Italy", "IT", "GK", "GK", "GK", "Right", 196, 40.0, 250.0, "유로 MVP 거인 골키퍼", "gk_worldclass"),
        ("G. Ramos", "Gonçalo Ramos", "곤살루 하무스", 23, "Portugal", "PT", "ST", "CF", "FW", "Right", 185, 50.0, 120.0, "월드컵 해트트릭 골잡이", "st_elite"),
        ("D. Doué", "Désiré Doué", "데지레 두에", 19, "France", "FR", "AM", "W", "MF", "Right", 181, 40.0, 60.0, "프랑스 올림픽 은메달 신성 크랙", "am_wonderkid")
    ]),

    ("Olympique de Marseille", "Ligue 1", 1, "France", "FR", 88, [
        ("M. Greenwood", "Mason Greenwood", "메이슨 그린우드", 22, "England", "GB-ENG", "W", "RW", "FW", "Both", 181, 35.0, 100.0, "리그 1 폭격 양발 원더 슈터", "winger_worldclass"),
        ("E. Wahi", "Elye Wahi", "엘리 와히", 21, "France", "FR", "ST", "CF", "FW", "Right", 184, 35.0, 60.0, "초고속 침투 스트라이커", "st_wonderkid"),
        ("P. Højbjerg", "Pierre-Emile Højbjerg", "피에르-에밀 호이비에르", 29, "Denmark", "DK", "DM", "CM", "MF", "Right", 185, 18.0, 100.0, "중원 사령관 & 덴마크 캡틴", "dm_elite"),
        ("A. Rabiot", "Adrien Rabiot", "아드리앙 라비오", 29, "France", "FR", "CM", "DM", "MF", "Left", 191, 35.0, 120.0, "프랑스 국대 엘리트 박스투박스", "cm_elite"),
        ("G. Kondogbia", "Geoffrey Kondogbia", "조프레 콩도그비아", 31, "Central African Republic", "CF", "DM", "CM", "MF", "Left", 188, 10.0, 75.0, "피지컬 진공청소기", "dm_solid"),
        ("Q. Merlin", "Quentin Merlin", "캉탱 메를랭", 22, "France", "FR", "LB", "DF", "DF", "Left", 173, 15.0, 30.0, "프랑스 U-21 주전 레프트백", "fb_wonderkid"),
        ("L. Balerdi", "Leonardo Balerdi", "레오나르도 발레르디", 25, "Argentina", "AR", "CB", "DF", "DF", "Right", 187, 20.0, 45.0, "마르세유 캡틴 센터백", "cb_solid"),
        ("G. Rulli", "Gerónimo Rulli", "헤로니모 룰리", 32, "Argentina", "AR", "GK", "GK", "GK", "Right", 187, 5.0, 40.0, "월드컵 우승 아르헨티나 골키퍼", "gk_solid")
    ]),

    ("AS Monaco", "Ligue 1", 1, "Monaco", "MC", 88, [
        ("E. Ben Seghir", "Eliesse Ben Seghir", "엘리에스 벤 세기르", 19, "Morocco", "MA", "AM", "LW", "MF", "Right", 178, 18.0, 20.0, "모나코의 황금재능 테크니션", "am_wonderkid"),
        ("M. Akliouche", "Maghnes Akliouche", "마그네스 아클리우슈", 22, "France", "FR", "AM", "RW", "MF", "Left", 183, 30.0, 35.0, "프랑스 올림픽 은메달 에이스", "am_wonderkid"),
        ("T. Minamino", "Takumi Minamino", "미나미노 타쿠미", 29, "Japan", "JP", "AM", "ST", "FW", "Right", 174, 20.0, 80.0, "일본 대표팀 캡틴 & 찬스메이커", "am_elite"),
        ("A. Golovin", "Aleksandr Golovin", "알렉산드르 골로빈", 28, "Russia", "RU", "AM", "CM", "MF", "Right", 180, 30.0, 85.0, "모나코의 10번 플레이메이커", "am_elite"),
        ("B. Embolo", "Breel Embolo", "브릴 엠볼로", 27, "Switzerland", "CH", "ST", "CF", "FW", "Right", 187, 12.0, 70.0, "스위스 국대 파워 스트라이커", "st_solid"),
        ("F. Balogun", "Folarin Balogun", "폴라린 발로건", 23, "United States", "US", "ST", "CF", "FW", "Right", 178, 30.0, 75.0, "미국 국대 주전 득점원", "st_elite"),
        ("D. Zakaria", "Denis Zakaria", "데니스 자카리아", 27, "Switzerland", "CH", "DM", "CB", "MF", "Right", 191, 28.0, 75.0, "모나코 캡틴 & 수비 앵커", "dm_elite"),
        ("Vanderson", "Vanderson de Oliveira", "반데르송", 23, "Brazil", "BR", "RB", "RWB", "DF", "Right", 180, 20.0, 35.0, "브라질 국대 라이트백", "fb_elite"),
        ("T. Kehrer", "Thilo Kehrer", "틸로 케러", 27, "Germany", "DE", "CB", "RB", "DF", "Right", 186, 12.0, 60.0, "독일 국대 출신 멀티 수비수", "cb_solid")
    ])
]

