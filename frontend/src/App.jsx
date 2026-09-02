import React, { useState, useEffect } from 'react';
import { 
  Activity, Search, Compass, Shield, Sparkles, Layers, Sliders, 
  Download, HelpCircle, ArrowRight, CheckCircle2, User, Trophy, Eye, BookOpen
} from 'lucide-react';
import TargetSelector from './components/TargetSelector';
import FilterControls from './components/FilterControls';
import ScoutReportCard from './components/ScoutReportCard';
import ComparisonArena from './components/ComparisonArena';
import LegalModal from './components/LegalModal';
import MetricGuideModal from './components/MetricGuideModal';

const countryFlags = {
  "South Korea": "🇰🇷",
  "Japan": "🇯🇵",
  "Norway": "🇳🇴",
  "Belgium": "🇧🇪",
  "Germany": "🇩🇪",
  "Netherlands": "🇳🇱",
  "Israel": "🇮🇱",
  "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
  "France": "🇫🇷",
  "Sweden": "🇸🇪",
  "Slovenia": "🇸🇮",
  "Togo": "🇹🇬",
  "Spain": "🇪🇸",
  "Uruguay": "🇺🇾",
  "Argentina": "🇦🇷",
  "United States": "🇺🇸",
  "Egypt": "🇪🇬",
  "Gambia": "🇬🇲",
  "Canada": "🇨🇦",
  "Portugal": "🇵🇹",
  "Morocco": "🇲🇦",
  "Croatia": "🇭🇷",
  "Denmark": "🇩🇰",
  "Italy": "🇮🇹",
  "Brazil": "🇧🇷",
  "Georgia": "🇬🇪",
  "Colombia": "🇨🇴",
  "Hungary": "🇭🇺",
  "Ghana": "🇬🇭",
  "Ecuador": "🇪🇨",
  "Senegal": "🇸🇳",
  "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
  "Mali": "🇲🇱",
  "Cameroon": "🇨🇲",
  "Turkey": "🇹🇷",
  "Switzerland": "🇨🇭",
  "Poland": "🇵🇱",
  "Serbia": "🇷🇸",
  "Nigeria": "🇳🇬",
  "Guinea": "🇬🇳",
  "Ivory Coast": "🇨🇮",
  "Greece": "🇬🇷",
  "Saudi Arabia": "🇸🇦"
};

const getGradeBadgeClass = (grade) => {
  switch (grade) {
    case 'SSS': return 'grade-badge-sss';
    case 'SS': return 'grade-badge-ss';
    case 'S': return 'grade-badge-s';
    case 'A': return 'grade-badge-a';
    case 'B': return 'grade-badge-b';
    case 'C': return 'grade-badge-c';
    case 'D': return 'grade-badge-d';
    default: return 'grade-badge-f';
  }
};

export default function App() {
  const [players, setPlayers] = useState([]);
  const [archetypes, setArchetypes] = useState([]);
  const [targetPlayerId, setTargetPlayerId] = useState("p_odegaard");
  const [targetPlayer, setTargetPlayer] = useState(null);
  
  // Similarity Engine Settings
  const [algorithm, setAlgorithm] = useState("hybrid");
  const [hybridBalance, setHybridBalance] = useState(0.5);
  const [sequentialCutoff, setSequentialCutoff] = useState(80.0);
  const [positionMatch, setPositionMatch] = useState("group");
  const [maxMarketValue, setMaxMarketValue] = useState(null);
  const [maxAge, setMaxAge] = useState(null);
  const [leagueTier, setLeagueTier] = useState(null);
  const [customWeights, setCustomWeights] = useState({
    vision: 1.0,
    striking: 1.0,
    dribble: 1.0,
    defense: 1.0,
    physical: 1.0
  });

  // Results State
  const [scoutResults, setScoutResults] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [loading, setLoading] = useState(false);

  // UI Modes
  const [isCompareArenaOpen, setIsCompareArenaOpen] = useState(false);
  const [comparePlayerAId, setComparePlayerAId] = useState("p_son");
  const [comparePlayerBId, setComparePlayerBId] = useState("p_stengs");
  const [isLegalModalOpen, setIsLegalModalOpen] = useState(false);
  const [isMetricGuideOpen, setIsMetricGuideOpen] = useState(false);

  // Initial Fetch: Players & Archetypes
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [playersRes, archRes] = await Promise.all([
          fetch('/api/players?limit=15000'),
          fetch('/api/archetypes')
        ]);
        const pData = await playersRes.json();
        const aData = await archRes.json();
        setPlayers(pData.players || []);
        setArchetypes(aData.archetypes || []);
      } catch (err) {
        console.error("Initial load error:", err);
      }
    };
    fetchInitialData();
  }, []);

  // Fetch Target Player and Run Similarity Search
  const runScouting = useCallback(async () => {
    if (!targetPlayerId) return;
    setLoading(true);
    try {
      const res = await fetch('/api/scout/similar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_player_id: targetPlayerId,
          algorithm,
          hybrid_balance: hybridBalance,
          sequential_cutoff: sequentialCutoff,
          position_match: positionMatch,
          max_age: maxAge,
          max_market_value: maxMarketValue,
          league_tier: leagueTier,
          limit: 20,
          custom_weights: customWeights
        })
      });

      const data = await res.json();
      if (data.target_player) {
        setTargetPlayer(data.target_player);
        setScoutResults(data.results || []);
        if (data.results && data.results.length > 0) {
          setSelectedCandidate(data.results[0]);
        } else {
          setSelectedCandidate(null);
        }
      }
    } catch (err) {
      console.error("Scouting search error:", err);
    } finally {
      setLoading(false);
    }
  }, [targetPlayerId, algorithm, hybridBalance, sequentialCutoff, positionMatch, maxMarketValue, maxAge, leagueTier, customWeights]);

  useEffect(() => {
    runScouting();
  }, [runScouting]);

  const handleResetFilters = () => {
    setAlgorithm("hybrid");
    setHybridBalance(0.5);
    setSequentialCutoff(80.0);
    setPositionMatch("group");
    setMaxMarketValue(null);
    setMaxAge(null);
    setLeagueTier(null);
    setCustomWeights({ vision: 1.0, striking: 1.0, dribble: 1.0, defense: 1.0, physical: 1.0 });
  };

  const handleOpen1v1Compare = (pA, pB) => {
    setComparePlayerAId(pA || targetPlayerId);
    setComparePlayerBId(pB || (selectedCandidate?.player?.id || "p_stengs"));
    setIsCompareArenaOpen(true);
  };

  return (
    <div className="min-h-screen bg-[#0a0a16] text-[#e2e8f0] flex flex-col font-sans">
      {/* Top Tactical Navigation Bar */}
      <header className="sticky top-0 z-40 bg-[#0a0a16]/90 backdrop-blur-md border-b border-[#1f2240] px-4 lg:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo & Subtitle */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[#00ff88] to-[#00e5ff] p-0.5 shadow-glow-neon">
              <div className="w-full h-full bg-[#0a0a16] rounded-[7px] flex items-center justify-center">
                <Activity className="w-5 h-5 text-[#00ff88]" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono font-extrabold text-base tracking-tight text-white">
                  FM SCOUT <span className="text-[#00ff88]">AI</span>
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#181832] text-[#00e5ff] border border-[#2a2e5c]">
                  FC FINDER v2.4
                </span>
              </div>
              <p className="text-[10px] font-mono text-gray-400">
                Wyscout / Metrica Nexus Tactical Engine • Zero-Cost Static Architecture
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setIsMetricGuideOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#00ff88]/10 hover:bg-[#00ff88]/20 text-[#00ff88] text-xs font-mono font-medium border border-[#00ff88]/30 transition-all shadow-glow-neon"
            >
              <BookOpen className="w-3.5 h-3.5" />
              전술 지표 가이드
            </button>

            <button
              onClick={() => setIsCompareArenaOpen(!isCompareArenaOpen)}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-mono transition-all ${
                isCompareArenaOpen
                  ? 'bg-[#00e5ff] text-black font-bold shadow-glow-cyan'
                  : 'bg-[#121226] text-gray-300 border border-[#1f2240] hover:border-[#2a2e5c]'
              }`}
            >
              <Layers className="w-3.5 h-3.5 text-[#00e5ff]" />
              1v1 비교 아레나
            </button>

            <button
              onClick={() => setIsLegalModalOpen(true)}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#121226] hover:bg-[#181832] text-gray-400 hover:text-white text-xs font-mono border border-[#1f2240] transition-colors"
            >
              <Shield className="w-3.5 h-3.5 text-gray-400" />
              라이선스
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 flex-1 flex flex-col gap-6">
        {/* 1v1 Compare Arena View (if opened) */}
        {isCompareArenaOpen ? (
          <ComparisonArena
            players={players}
            initialPlayerAId={comparePlayerAId}
            initialPlayerBId={comparePlayerBId}
            onClose={() => setIsCompareArenaOpen(false)}
          />
        ) : (
          <>
            {/* Target Player Selector & Presets */}
            <TargetSelector
              players={players}
              selectedTargetId={targetPlayerId}
              onSelectTarget={setTargetPlayerId}
              archetypes={archetypes}
            />

            {/* Tactical Filter Controls Panel */}
            <FilterControls
              algorithm={algorithm}
              setAlgorithm={setAlgorithm}
              hybridBalance={hybridBalance}
              setHybridBalance={setHybridBalance}
              sequentialCutoff={sequentialCutoff}
              setSequentialCutoff={setSequentialCutoff}
              positionMatch={positionMatch}
              setPositionMatch={setPositionMatch}
              maxMarketValue={maxMarketValue}
              setMaxMarketValue={setMaxMarketValue}
              maxAge={maxAge}
              setMaxAge={setMaxAge}
              leagueTier={leagueTier}
              setLeagueTier={setLeagueTier}
              customWeights={customWeights}
              setCustomWeights={setCustomWeights}
              onResetFilters={handleResetFilters}
              onRunScouting={runScouting}
              loading={loading}
            />

            {/* Dashboard Workspace */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* Left Column (7 cols): Hero Scout Report Card */}
              <div className="lg:col-span-7 flex flex-col gap-4">
                {selectedCandidate && targetPlayer ? (
                  <ScoutReportCard
                    candidate={selectedCandidate}
                    targetPlayer={targetPlayer}
                    similarityPct={selectedCandidate.similarity_pct}
                    algorithm={algorithm}
                    onCompareDirectly={handleOpen1v1Compare}
                  />
                ) : (
                  <div className="p-12 text-center rounded-xl bg-[#121226] border border-[#1f2240] text-gray-400 font-mono text-xs">
                    {loading ? '전술 유사도 계산 중...' : '조건에 맞는 선수가 없습니다. 필터 조건을 완화해보세요.'}
                  </div>
                )}
              </div>

              {/* Right Column (5 cols): Candidates Scouting Board */}
              <div className="lg:col-span-5 flex flex-col gap-3">
                <div className="flex items-center justify-between px-1">
                  <div className="text-xs font-mono font-bold text-gray-300 flex items-center gap-2">
                    <Trophy className="w-3.5 h-3.5 text-yellow-400" />
                    유사 선수 랭킹 ({scoutResults.length}명)
                  </div>
                  <span className="text-[11px] font-mono text-gray-400">
                    정렬: 유사도 높은 순
                  </span>
                </div>

                <div className="space-y-2.5 max-h-[750px] overflow-y-auto pr-1">
                  {loading ? (
                    <div className="p-12 text-center rounded-xl bg-[#121226] border border-[#00ff88]/30 text-gray-300 font-mono text-xs flex flex-col items-center justify-center gap-3 shadow-glow-neon animate-pulse">
                      <RefreshCw className="w-7 h-7 text-[#00ff88] animate-spin" />
                      <div className="text-white font-bold">11,685명 글로벌 선수 풀 스카우팅 연산 중...</div>
                      <div className="text-[11px] text-gray-400">코사인 전술 스타일 + 유클리드 퍼포먼스 체급 계산 중</div>
                    </div>
                  ) : scoutResults.length === 0 ? (
                    <div className="p-8 text-center rounded-xl bg-[#121226] border border-[#1f2240] text-gray-400 font-mono text-xs">
                      조건에 일치하는 선수가 없습니다. 필터 조건을 완화해보세요.
                    </div>
                  ) : (
                    scoutResults.map((item, idx) => {
                      const p = item.player;
                      const isSelected = selectedCandidate?.player?.id === p.id;
                      const flag = countryFlags[p.nationality] || "🌐";
                      const isTopGem = item.gem_score && item.gem_score > 90;

                    return (
                      <div
                        key={p.id}
                        onClick={() => setSelectedCandidate(item)}
                        className={`p-3.5 rounded-xl transition-all cursor-pointer border ${
                          isSelected
                            ? 'bg-[#161633] border-[#00ff88] shadow-glow-neon'
                            : 'bg-[#121226] border-[#1f2240] hover:border-[#2a2e5c] hover:bg-[#15152c]'
                        }`}
                      >
                        <div className="flex items-start justify-between gap-2">
                          {/* Player Basic Info */}
                          <div className="flex items-center gap-3">
                            <span className="text-lg">{flag}</span>
                            <div>
                              <div className="flex items-center gap-1.5">
                                <span className="font-bold text-white text-sm tracking-tight">{p.name}</span>
                                {p.korean_name && (
                                  <span className="text-[#00ff88] text-xs font-sans font-medium">({p.korean_name})</span>
                                )}
                                <span className="px-1.5 py-0.2 rounded bg-[#00e5ff]/15 text-[#00e5ff] text-[10px] font-mono font-bold">
                                  {p.primary_pos}
                                </span>
                                {isTopGem && (
                                  <span className="px-1.5 py-0.2 rounded bg-yellow-400/20 text-yellow-300 text-[10px] font-mono flex items-center gap-0.5">
                                    <Sparkles className="w-2.5 h-2.5" /> 진주
                                  </span>
                                )}
                              </div>
                              <div className="text-xs text-gray-400 font-mono mt-0.5">
                                {p.club} • {p.league} • {p.age}세
                              </div>
                            </div>
                          </div>

                          {/* Match % & Gem Score */}
                          <div className="text-right">
                            <div className="text-base font-extrabold font-mono text-[#00ff88]">
                              {item.similarity_pct.toFixed(1)}%
                            </div>
                            <div className="text-[10px] font-mono text-gray-400">
                              스타일 <span className="text-[#00ff88]">{item.cosine_pct?.toFixed(0)}%</span> • 체급 <span className="text-[#00e5ff]">{item.euclidean_pct?.toFixed(0)}%</span>
                            </div>
                          </div>
                        </div>

                        {/* Tactical 5-Pillar Mini Badges Bar */}
                        <div className="mt-2.5 pt-2 border-t border-[#1f2240]/60 flex items-center justify-between text-[10px] font-mono">
                          <div className="flex items-center gap-1 text-gray-400">
                            <span>V:{p.vision_grade}</span>
                            <span>•</span>
                            <span>S:{p.striking_grade}</span>
                            <span>•</span>
                            <span>D:{p.dribble_grade}</span>
                            <span>•</span>
                            <span>Df:{p.defense_grade}</span>
                            <span>•</span>
                            <span>P:{p.physical_grade}</span>
                          </div>

                          <div className="flex items-center gap-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleOpen1v1Compare(targetPlayerId, p.id);
                              }}
                              className="text-gray-400 hover:text-[#00e5ff] text-[10px] flex items-center gap-0.5"
                            >
                              1v1 대조 <ArrowRight className="w-2.5 h-2.5" />
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer & License Attribution Bar */}
      <footer className="border-t border-[#1f2240] bg-[#0a0a16] py-5 px-4 lg:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-xs font-mono text-gray-400">
          <div>
            경기 전술 이벤트 통계는 Luca Pappalardo 등이 Nature Scientific Data(2019) 저널에 배포한 Wyscout Open Dataset(CC BY 4.0) 및 StatsBomb Open Data를 기반으로 역산되었습니다.
          </div>
          <div className="flex items-center gap-4 shrink-0">
            <button onClick={() => setIsLegalModalOpen(true)} className="hover:text-white underline">
              법적 고지 & 라이선스
            </button>
            <span className="text-[#00ff88]">FM Scout AI © 2026</span>
          </div>
        </div>
      </footer>

      {/* Legal & Compliance Modal */}
      <LegalModal
        isOpen={isLegalModalOpen}
        onClose={() => setIsLegalModalOpen(false)}
      />

      {/* Metric Guide & Tactical Glossary Modal */}
      <MetricGuideModal
        isOpen={isMetricGuideOpen}
        onClose={() => setIsMetricGuideOpen(false)}
      />
    </div>
  );
}
