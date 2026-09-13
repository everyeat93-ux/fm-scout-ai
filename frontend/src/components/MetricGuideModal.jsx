import React, { useState } from 'react';
import { BookOpen, X, Sparkles, Target, Compass, Shield, Zap, TrendingUp, Layers, HelpCircle, CheckCircle2 } from 'lucide-react';

export default function MetricGuideModal({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('pillars');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white border-2 border-gray-900 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden text-gray-900">
        
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-purple-100 border border-purple-200 text-purple-700">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-black text-gray-950 font-mono tracking-tight flex items-center gap-2">
                [ 전술 지표 및 FM 스카우팅 가이드 ]
              </h2>
              <p className="text-xs text-gray-500 font-mono">
                Wyscout 실데이터 기반 5대 전술 축, 9대 세부 스탯, AI 유사도 수식 설명서
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-500 hover:text-gray-900 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 bg-white px-5 gap-2 overflow-x-auto">
          {[
            { id: 'pillars', label: '5대 전술 능력치 축', icon: Compass },
            { id: 'per90', label: '90분당(Per-90) 세부 스탯', icon: Zap },
            { id: 'algorithms', label: 'AI 유사도 알고리즘', icon: Layers },
            { id: 'gem', label: '가성비 진주 지수(Gem)', icon: Sparkles },
            { id: 'grades', label: 'F ~ SSS 등급 체계', icon: Target },
          ].map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-3 px-3.5 text-xs font-mono font-bold border-b-2 transition-all whitespace-nowrap cursor-pointer ${
                  isActive
                    ? 'border-purple-600 text-purple-700 bg-purple-50/50'
                    : 'border-transparent text-gray-500 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-5 custom-scrollbar text-xs leading-relaxed font-sans">
          
          {/* TAB 1: 5 PILLARS */}
          {activeTab === 'pillars' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-purple-50/60 border border-purple-200">
                <p className="text-gray-800 font-medium">
                  FM Scout AI는 단순 종합 점수(OVR) 대신 선수의 전술적 역할을 5가지 핵심 축으로 정규화하여 
                  <span className="text-purple-700 font-bold"> 레이더 차트</span>와 
                  <span className="text-amber-800 font-bold"> 전술 티어(Grade)</span>를 평가합니다.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                {/* 1. Vision & Pass */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-purple-700 font-bold font-mono">
                    <Compass className="w-4 h-4" />
                    1. 창의성 & 패스 (Vision & Pass)
                  </div>
                  <p className="text-gray-600">
                    상대 수비 라인을 무너뜨리는 기회 창출력과 빌드업 기여도를 측정합니다.
                  </p>
                  <div className="text-[11px] font-mono text-gray-800 bg-white p-2 rounded border border-gray-200">
                    💡 <span className="text-purple-700 font-bold">반영 산식:</span> 키패스 40% + 전진 패스 40% + 패스 성공률 20%
                  </div>
                  <div className="text-[11px] text-gray-500">
                    • 대표 역할: 플레이메이커, 딥라잉 플레이메이커, 찬스 크리에이터
                  </div>
                </div>

                {/* 2. Striking & xG */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-rose-600 font-bold font-mono">
                    <Target className="w-4 h-4" />
                    2. 슈팅 & 득점력 (Striking & xG)
                  </div>
                  <p className="text-gray-600">
                    박스 안팎에서의 결정력, 슈팅 정확도 및 통계적 기대 득점(xG)을 종합 평가합니다.
                  </p>
                  <div className="text-[11px] font-mono text-gray-800 bg-white p-2 rounded border border-gray-200">
                    💡 <span className="text-rose-600 font-bold">반영 산식:</span> 박스 내 슈팅 50% + 90분당 슈팅 수 30% + 유효 슈팅률 20%
                  </div>
                  <div className="text-[11px] text-gray-500">
                    • 대표 역할: 포처, 타깃 포워드, 인사이드 포워드, 골게터
                  </div>
                </div>

                {/* 3. Dribble & Carry */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-amber-700 font-bold font-mono">
                    <Zap className="w-4 h-4" />
                    3. 온볼 & 볼 운반 (On-ball & Carry)
                  </div>
                  <p className="text-gray-600">
                    1v1 돌파력, 압박을 뚫고 상대 진영으로 볼을 전진시키는 능력 및 파울 유도력입니다.
                  </p>
                  <div className="text-[11px] font-mono text-gray-800 bg-white p-2 rounded border border-gray-200">
                    💡 <span className="text-amber-700 font-bold">반영 산식:</span> 드리블 성공 40% + 전진 운반 거리(m) 40% + 피파울 20%
                  </div>
                  <div className="text-[11px] text-gray-500">
                    • 대표 역할: 크랙형 윙어, 볼 캐리어, 탈압박 미드필더
                  </div>
                </div>

                {/* 4. Defensive Engine */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-blue-700 font-bold font-mono">
                    <Shield className="w-4 h-4" />
                    4. 수비 엔진 (Defensive Engine)
                  </div>
                  <p className="text-gray-600">
                    상대 공격 흐름을 차단하는 태클, 가로채기 및 위험 지역 걷어내기 수치입니다.
                  </p>
                  <div className="text-[11px] font-mono text-gray-800 bg-white p-2 rounded border border-gray-200">
                    💡 <span className="text-blue-700 font-bold">반영 산식:</span> 가로채기 35% + 태클 성공 35% + 걷어내기 30%
                  </div>
                  <div className="text-[11px] text-gray-500">
                    • 대표 역할: 볼위닝 미드필더, 앵커맨, 스토퍼 센터백, 락다운 풀백
                  </div>
                </div>

                {/* 5. Physical Duels */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2 md:col-span-2">
                  <div className="flex items-center gap-2 text-emerald-700 font-bold font-mono">
                    <TrendingUp className="w-4 h-4" />
                    5. 피지컬 경합 (Physical Duels)
                  </div>
                  <p className="text-gray-600">
                    세트피스 및 인게임 상황에서 지상/공중볼 경합을 이겨내고 소유권을 확보하는 피지컬 지배력입니다.
                  </p>
                  <div className="text-[11px] font-mono text-gray-800 bg-white p-2 rounded border border-gray-200">
                    💡 <span className="text-emerald-700 font-bold">반영 산식:</span> 공중볼 경합 승률(%) 50% + 지상 경합 성공 수 50%
                  </div>
                  <div className="text-[11px] text-gray-500">
                    • 대표 역할: 포스트 플레이어, 공중전 장악 센터백, 박스투박스
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: PER-90 STATS */}
          {activeTab === 'per90' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-blue-50/60 border border-blue-200">
                <p className="text-gray-800 font-medium">
                  출전 시간에 따른 왜곡을 방지하기 위해 모든 데이터는 
                  <span className="text-blue-800 font-bold font-mono"> Per-90 (90분 환산값)</span>을 기준으로 분석합니다.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  { name: "Key Passes (KP/90)", kor: "기회 창출 패스", desc: "동료의 슈팅으로 직접 연결된 결정적인 패스 횟수입니다." },
                  { name: "Prog. Passes (ProgP/90)", kor: "전진 패스 성공", desc: "상대 진영으로 최소 10m 이상 전진시킨 빌드업 패스입니다." },
                  { name: "Expected Goals (xG/90)", kor: "기대 득점값", desc: "슈팅 위치, 각도, 수비수 압박을 고려한 통계적 득점 확률 합계입니다." },
                  { name: "Shots on Target % (SOT%)", kor: "유효 슈팅 비율", desc: "전체 슈팅 중 골문 안으로 향한 슈팅의 비율(%)입니다." },
                  { name: "Prog. Carries (ProgC/90)", kor: "전진 볼 운반", desc: "상대 골문 방향으로 10m 이상 단독으로 볼을 몰고 간 횟수입니다." },
                  { name: "Carrying Dist (Carry/90)", kor: "총 볼 운반 거리", desc: "90분 동안 볼을 직접 컨트롤하며 전진 이동시킨 거리(미터)입니다." },
                  { name: "Tackles Won (Tkl/90)", kor: "태클 성공 횟수", desc: "상대 소유권을 빼앗거나 볼을 밖으로 쳐낸 태클 횟수입니다." },
                  { name: "Interceptions (Int/90)", kor: "가로채기 (인터셉트)", desc: "상대의 패스 경로를 예측하여 공을 가로챈 횟수입니다." },
                  { name: "Aerial Won % (Aerial%)", kor: "공중볼 경합 승률", desc: "헤더 경합 시 공중볼을 따낸 백분율(%)입니다." },
                  { name: "Pressures / Recoveries", kor: "압박 및 리커버리", desc: "볼을 잃어버린 직후 다시 빼앗아온 루즈볼 회수 횟수입니다." },
                ].map((st, i) => (
                  <div key={i} className="p-3 rounded-lg bg-gray-50 border border-gray-200">
                    <div className="flex items-center justify-between font-mono mb-1">
                      <span className="font-bold text-gray-950 text-xs">{st.kor}</span>
                      <span className="text-purple-700 font-bold text-[11px]">{st.name}</span>
                    </div>
                    <p className="text-[11px] text-gray-600">{st.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: ALGORITHMS */}
          {activeTab === 'algorithms' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-purple-50/60 border border-purple-200">
                <h3 className="font-bold text-purple-950 mb-1 font-mono">[ 4대 AI 스카우팅 알고리즘 & 앙상블 수식 가이드 ]</h3>
                <p className="text-gray-700">
                  코사인(스타일)과 유클리드(체급)의 장점을 결합하여 가장 정밀한 대체자를 발굴할 수 있습니다.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* 1. Hybrid Ensemble */}
                <div className="p-4 rounded-xl bg-purple-50/40 border-2 border-purple-500 flex flex-col gap-2 shadow-sm">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-purple-900 font-mono text-sm flex items-center gap-1">
                      🎯 하이브리드 앙상블 (Hybrid Ensemble)
                    </span>
                    <span className="px-2 py-0.5 rounded bg-purple-100 text-purple-800 text-[10px] font-mono font-bold">추천 디폴트</span>
                  </div>
                  <p className="text-gray-700 text-[11px]">
                    <span className="text-purple-700 font-bold">스타일(코사인)과 체급(유클리드)을 가중 합산</span>하여, 
                    플레이 형태도 닮았으면서 실제 경기 생산량도 근접한 이상적인 도플갱어를 발굴합니다.
                  </p>
                  <div className="bg-white p-2.5 rounded border border-purple-200 text-[11px] text-purple-900 font-mono font-bold">
                    수식: Final = (w_cos × Cosine) + (w_euc × Euclidean)
                  </div>
                  <div className="text-gray-600 text-[11px] bg-white p-2.5 rounded border border-gray-200">
                    💡 <strong className="text-gray-900">특징:</strong> 슬라이더를 통해 스타일 중심(예: 70:30) 또는 체급 중심(예: 30:70)으로 자유롭게 가중치 밸런스를 조절할 수 있습니다.
                  </div>
                </div>

                {/* 2. Sequential Scouting */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-gray-900 font-mono text-sm">🔄 2단계 순차 스카우팅 (Sequential)</span>
                    <span className="px-2 py-0.5 rounded bg-gray-200 text-gray-800 text-[10px] font-mono font-bold">2-Stage</span>
                  </div>
                  <p className="text-gray-700 text-[11px]">
                    <span className="text-purple-700 font-bold">1단계에서 전술 스타일 커트라인(예: 80% 이상)</span>을 통과한 후보군만 1차 선별한 후, 
                    <span className="text-gray-950 font-bold">2단계에서 실제 퍼포먼스 체급(유클리드 거리)</span>이 가장 우수한 순으로 최종 랭킹합니다.
                  </p>
                  <div className="bg-white p-2.5 rounded border border-gray-200 text-[11px] text-gray-800 font-mono">
                    파이프라인: Filter(Cosine ≥ Cutoff) ➔ RankBy(Euclidean)
                  </div>
                  <div className="text-gray-600 text-[11px] bg-white p-2.5 rounded border border-gray-200">
                    🎯 <strong className="text-gray-900">추천 용도:</strong> 전술 적합성이 완전히 검증된 상태에서 체급이 가장 높은 즉시 전력감을 찾을 때 최적입니다.
                  </div>
                </div>

                {/* 3. Cosine Similarity */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-gray-900 font-mono text-sm">① 코사인 유사도 (Cosine)</span>
                    <span className="px-2 py-0.5 rounded bg-gray-200 text-gray-800 text-[10px] font-mono">스타일 비율</span>
                  </div>
                  <p className="text-gray-700 text-[11px]">
                    선수의 능력치 간의 <span className="text-gray-950 font-bold">비율과 전술 패턴(방향성)</span>을 분석합니다.
                  </p>
                  <div className="bg-white p-2.5 rounded border border-gray-200 text-[11px] text-gray-600 font-mono">
                    수식: cos(θ) = (A · B) / (||A|| ||B||)
                  </div>
                  <div className="text-gray-600 text-[11px] bg-white p-2.5 rounded border border-gray-200">
                    🎯 <strong className="text-gray-900">추천 용도:</strong> 하위 리그에서 전술적 움직임이 동일한 <span className="text-emerald-700 font-bold">가성비 유망주/원석</span>을 발굴할 때 적합합니다.
                  </div>
                </div>

                {/* 4. Euclidean Distance */}
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 flex flex-col gap-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-gray-900 font-mono text-sm">② 유클리드 거리 (Euclidean)</span>
                    <span className="px-2 py-0.5 rounded bg-gray-200 text-gray-800 text-[10px] font-mono">절대 볼륨</span>
                  </div>
                  <p className="text-gray-700 text-[11px]">
                    선수가 실제로 경기당 기록한 <span className="text-gray-950 font-bold">스탯의 절대적 크기와 피지컬 체급</span>을 계산합니다.
                  </p>
                  <div className="bg-white p-2.5 rounded border border-gray-200 text-[11px] text-gray-600 font-mono">
                    수식: dist = sqrt(Σ (Ai - Bi)²)
                  </div>
                  <div className="text-gray-600 text-[11px] bg-white p-2.5 rounded border border-gray-200">
                    🎯 <strong className="text-gray-900">추천 용도:</strong> 실제 경기 생산량과 스탯 볼륨이 동급인 <span className="text-blue-700 font-bold">완성형 주전급 대체자</span>를 찾을 때 적합합니다.
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: GEM SCORE */}
          {activeTab === 'gem' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200">
                <h3 className="font-bold text-amber-950 mb-1 font-mono flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-amber-600" /> 가성비 진주 지수 (Gem Index Score)
                </h3>
                <p className="text-gray-700">
                  타깃 선수와 유사하면서도, 이적료가 저렴하고 성장 잠재력이 높은 
                  <span className="text-amber-900 font-bold"> 'FM식 꿀영입 유망주'</span>를 한눈에 알아볼 수 있도록 계산된 복합 지수입니다.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-3">
                <div className="text-xs font-mono font-bold text-gray-900">
                  📐 진주 지수 산출 알고리즘 가중치:
                </div>
                <div className="space-y-2 text-[11px]">
                  <div className="flex items-center justify-between p-2 rounded bg-white border border-gray-200">
                    <span className="text-gray-700">1. 타깃 선수와의 전술 유사도 (Similarity Match)</span>
                    <span className="text-purple-700 font-mono font-bold">50% 반영</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-white border border-gray-200">
                    <span className="text-gray-700">2. 시장 가치 가성비 (저렴한 몸값일수록 높은 점수)</span>
                    <span className="text-amber-700 font-mono font-bold">30% 반영</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-white border border-gray-200">
                    <span className="text-gray-700">3. 나이 보너스 (23세 이하 유망주일수록 추가 가산점)</span>
                    <span className="text-blue-700 font-mono font-bold">20% 반영</span>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-[11px]">
                  ✨ <strong>스카우트 팁:</strong> 진주 지수 90점 이상인 선수는 
                  <span className="text-amber-700 font-bold"> [진주] </span> 배지가 부여되며, 
                  하위 리그에서 빅클럽으로 스텝업할 수 있는 강력 추천 영입 대상입니다.
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: GRADES */}
          {activeTab === 'grades' && (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-gray-100 border border-gray-200">
                <h3 className="font-bold text-gray-950 mb-1 font-mono">[ F ~ SSS 전술 등급표 기준 ]</h3>
                <p className="text-gray-600">
                  유럽 5대 리그 및 주요 리그 전체 선수들의 정규화된 데이터 백분위를 바탕으로 부여되는 실전 티어입니다.
                </p>
              </div>

              <div className="space-y-2">
                {[
                  { grade: "SSS", label: "월드클래스 (World Class)", score: "95점 이상", desc: "세계 축구 최정상, 발롱도르 컨텐더 수준의 압도적인 지배력", color: "text-amber-900 border-amber-400 bg-amber-100" },
                  { grade: "SS", label: "엘리트 빅리그 (Elite Big League)", score: "90 ~ 94점", desc: "챔피언스리그 8강 이상 빅클럽의 핵심 에이스 및 주전", color: "text-purple-900 border-purple-400 bg-purple-100" },
                  { grade: "S", label: "리그 베스트 XI (League Best XI)", score: "85 ~ 89점", desc: "리그 정상급 퍼포먼스를 보여주는 최상위권 주축 선수", color: "text-emerald-900 border-emerald-400 bg-emerald-100" },
                  { grade: "A", label: "빅리그 주전급 (Big League Starter)", score: "80 ~ 84점", desc: "유럽 5대 리그 상위권 구단에서 안정적으로 선발 출전 가능한 기량", color: "text-blue-900 border-blue-400 bg-blue-100" },
                  { grade: "B", label: "견고한 로테이션 (Solid Rotation)", score: "70 ~ 79점", desc: "전술적 역할을 충실히 수행하는 실속파 로테이션 및 준주전", color: "text-teal-900 border-teal-400 bg-teal-100" },
                  { grade: "C", label: "스쿼드 백업 (Squad Backup)", score: "60 ~ 69점", desc: "리그 백업 자원 또는 하위 리그 주전급 수준", color: "text-gray-700 border-gray-300 bg-gray-100" },
                  { grade: "D", label: "육성형 유망주 (Development Prospect)", score: "50 ~ 59점", desc: "출전 시간이 더 필요하며 성장이 기대되는 신예 유망주", color: "text-orange-900 border-orange-400 bg-orange-100" },
                  { grade: "F", label: "평가 제외 (Excluded / Low Sample)", score: "50점 미만", desc: "출전 표본 부족 또는 해당 전술 역할에 적합하지 않음", color: "text-gray-500 border-gray-300 bg-gray-100" },
                ].map((g, i) => (
                  <div key={i} className="flex items-center gap-3 p-2.5 rounded-xl bg-gray-50 border border-gray-200">
                    <span className={`w-12 text-center py-1 rounded font-mono font-black text-xs border ${g.color}`}>
                      {g.grade}
                    </span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-gray-950 text-xs">{g.label}</span>
                        <span className="text-[10px] font-mono text-gray-500 font-bold">({g.score})</span>
                      </div>
                      <p className="text-[11px] text-gray-600 mt-0.5">{g.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 bg-gray-50 flex items-center justify-between text-xs font-mono text-gray-500">
          <span>데이터 모델: Wyscout v2.4 (CC BY 4.0 Open License)</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-gray-900 text-white font-bold hover:bg-gray-800 transition-colors cursor-pointer"
          >
            확인 완료
          </button>
        </div>

      </div>
    </div>
  );
}
