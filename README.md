# ⚽ FM Scout AI (FC Finder)
> **Wyscout 전술 분석관 테마 기반 AI 선수 스카우팅 & 유사 선수 비교 서비스**
> 비용 0원(완전 무료)의 오프라인 정적 SQLite 아키텍처 & 클라이언트 사이드 HTML5 Canvas 렌더링

---

## 📌 1. 프로젝트 개요 (Overview)
- **서비스명**: FM Scout AI (FC Finder)
- **타깃 사용자**: FM(Football Manager) 게이머, 스포츠 통계 분석가, 인게임 전술 데이터 덕후
- **핵심 가치 제안**: 실시간 유료 API 구독 비용을 0원으로 통제하면서, 공인 오픈 축구 데이터셋을 결합하여 **"내가 원하는 타깃 선수와 90% 이상 유사한 전술적 역할을 수행하는 하위 리그의 가성비 유망주"**를 발굴하는 초정밀 시뮬레이터.
- **디자인 테마**: Wyscout / Metrica Nexus 스타일의 다크 하이테크 대시보드 (`#0a0a16`, `#00ff88` 네온 그린, `#00e5ff` 사이버 사이언).

---

## 📐 2. 핵심 알고리즘 및 수학적 수식

### 2.1 1단계: 타깃 포지션 전처리 필터링 (Target Filtering)
축구 도메인 관점의 왜곡을 방지하기 위해 1차적으로 포지션 군집화(MF / FW / DF) 또는 세부 포지션 엄격 일치 필터링을 수행합니다.

### 2.2 2단계: Per-90 Min-Max 정규화 (Normalization)
선수별 출전 시간 편차를 제거하기 위해 모든 지표를 **경기당 평균(Per 90)**으로 변환한 뒤 $0 \sim 100$ 백분위 스코어로 정규화합니다.
$$\text{Normalized } X_i = \frac{X_i - \min(X)}{\max(X) - \min(X)} \times 100$$

### 2.3 3단계: 유사도 매칭 알고리즘
- **① 코사인 유사도 (Cosine Similarity)** - *플레이 스타일 비율 중심 매칭 (가성비 진주 발굴)*
  $$\text{Cosine Similarity}(A, B) = \frac{\sum_{i=1}^{n} a_i b_i}{\sqrt{\sum_{i=1}^{n} a_i^2} \sqrt{\sum_{i=1}^{n} b_i^2}}$$
- **② 유클리드 거리 (Euclidean Distance)** - *절대 퍼포먼스 볼륨 중심 매칭 (완성형 대체자 탐색)*
  $$\text{Distance}(A, B) = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}, \quad \text{Similarity (\%)} = \left( 1 - \frac{\text{Distance}}{\text{Max Distance}} \right) \times 100$$

---

## 🏆 3. 커스텀 5대 전술 능력치 및 F ~ SSS 등급제

| 5대 전술 지표 | 세부 산출 지표 (Wyscout / FBref 사실 데이터) | 가중치 비중 |
| :--- | :--- | :--- |
| **창의성 (Vision)** | 기회 창출(Key Passes), 전진 패스(Prog Passes), 패스 성공률(Pass Acc %) | 40% / 40% / 20% |
| **슈팅 (Striking)** | 경기당 슈팅 수, 박스 내 슈팅(Box Shots), 유효 슈팅 비율(SOT %) | 30% / 50% / 20% |
| **드리블 (Dribble)** | 드리블 성공(Dribbles Completed), 전진 운반 거리(Carry Dist), 피파울 빈도 | 40% / 40% / 20% |
| **수비력 (Defense)** | 가로채기(Interceptions), 태클 성공(Tackles Won), 걷어내기(Clearances) | 35% / 35% / 30% |
| **경합력 (Physical)** | 공중볼 경합 성공률(Aerial Won %), 지상 볼 경합 성공(Ground Duels Won) | 50% / 50% |

### 등급 매핑 룰 (F ~ SSS)
- $\ge 95$: 👑 **SSS** (월드클래스)
- $90 \le \text{Score} < 95$: 🔥 **SS** (빅리그 최정상급)
- $85 \le \text{Score} < 90$: ✨ **S** (리그 베스트 11급)
- $80 \le \text{Score} < 85$: 📈 **A** (빅리그 주전급)
- $70 \le \text{Score} < 80$: **B** (준수한 로테이션)
- $60 \le \text{Score} < 70$: **C** (평범한 백업)
- $50 \le \text{Score} < 60$: **D** (개발 유망주)
- $< 50$: **F** (평가 제외 / 표본 부족)

---

## 🖼️ 4. 클라이언트 사이드 2x PNG 저장 기능 (html2canvas)
서버에 이미지 렌더러(Puppeteer 등)를 두지 않고, 사용자 브라우저/모바일 CPU에서 `html2canvas`로 2배 고해상도 PNG 스카우팅 카드를 직접 캡처 및 다운로드하여 서버 비용을 완전한 0원으로 유지합니다.

---

## ⚖️ 5. 오픈 데이터 라이선스 및 지적재산권 준수
1. **Wyscout Open Dataset (CC BY 4.0)**:
   > "경기 전술 이벤트 통계는 Luca Pappalardo 등이 Nature Scientific Data(2019) 저널에 배포한 Wyscout Open Dataset(CC BY 4.0)을 기반으로 역산되었습니다."
2. **StatsBomb Open Data**: 전술 공간 지표 및 xG 모델 가이드라인 준수.
3. **선수 초상권 보호**: 실제 얼굴 사진 대신 국기 이모지(🇳🇱, 🇳🇴 등) 및 실루엣 아바타 적용.
4. **클럽 상표권 우회**: 범용 및 약식 구단명 표기.

---

## 🚀 6. 실행 방법 (Quick Start)

### 1) 원클릭 앱 실행
```bash
python start_app.py
```
브라우저에서 **`http://localhost:8000`** 접속.

### 2) 개발 모드로 실행
- **백엔드**:
  ```bash
  cd backend
  python -m uvicorn main:app --reload --port 8000
  ```
- **프론트엔드 (HMR)**:
  ```bash
  cd frontend
  npm run dev
  ```
