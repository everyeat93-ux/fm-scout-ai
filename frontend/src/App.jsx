import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  Activity, Search, Compass, Shield, Sparkles, Layers, Sliders, 
  Download, HelpCircle, ArrowRight, CheckCircle2, User, Trophy, Eye, BookOpen, RefreshCw, Target, Star
} from 'lucide-react';
import TargetSelector from './components/TargetSelector';
import FilterControls from './components/FilterControls';
import ScoutReportCard from './components/ScoutReportCard';
import ComparisonArena from './components/ComparisonArena';
import LegalModal from './components/LegalModal';
import MetricGuideModal from './components/MetricGuideModal';
import ShortlistModal from './components/ShortlistModal';

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
  const [targetPlayerId, setTargetPlayerId] = useState("p_son");
  const [targetPlayer, setTargetPlayer] = useState(null);
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  
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
  const [quickFilter, setQuickFilter] = useState("all"); // 'all', 'gems', 'u23', 'top5', 'kleague'
  const [mobileTab, setMobileTab] = useState("candidates"); // 'target', 'candidates', 'report', 'arena'

  // Shortlist Bookmarks State (with LocalStorage persistence)
  const [bookmarkedPlayerIds, setBookmarkedPlayerIds] = useState(() => {
    try {
      const saved = localStorage.getItem('fm_scout_bookmarks');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });
  const [isShortlistOpen, setIsShortlistOpen] = useState(false);

  const toggleBookmark = useCallback((playerId) => {
    setBookmarkedPlayerIds((prev) => {
      const next = prev.includes(playerId)
        ? prev.filter((id) => id !== playerId)
        : [...prev, playerId];
      try {
        localStorage.setItem('fm_scout_bookmarks', JSON.stringify(next));
      } catch (e) {}
      return next;
    });
  }, []);

  const clearAllBookmarks = useCallback(() => {
    setBookmarkedPlayerIds([]);
    try {
      localStorage.removeItem('fm_scout_bookmarks');
    } catch (e) {}
  }, []);

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
          fetch('/api/players?limit=200'),
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
        const results = data.results || [];
        setScoutResults(results);
        if (results && results.length > 0) {
          setSelectedCandidate(results[0]);
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

  // Dynamic 1-Click Quick Filtering
  const filteredScoutResults = useMemo(() => {
    if (quickFilter === 'gems') {
      return scoutResults.filter(r => (r.player.market_value_eur <= 25) || (r.gem_score && r.gem_score >= 80));
    }
    if (quickFilter === 'u23') {
      return scoutResults.filter(r => r.player.age <= 23);
    }
    if (quickFilter === 'top5') {
      return scoutResults.filter(r => ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1'].includes(r.player.league));
    }
    if (quickFilter === 'kleague') {
      return scoutResults.filter(r => (r.player.league && r.player.league.includes('K-League')) || r.player.nationality === 'South Korea');
    }
    return scoutResults;
  }, [scoutResults, quickFilter]);

  const handleResetFilters = () => {
    setAlgorithm("hybrid");
    setHybridBalance(0.5);
    setSequentialCutoff(80.0);
    setPositionMatch("group");
    setMaxMarketValue(null);
    setMaxAge(null);
    setLeagueTier(null);
    setQuickFilter("all");
    setCustomWeights({ vision: 1.0, striking: 1.0, dribble: 1.0, defense: 1.0, physical: 1.0 });
  };

  const handleSelectCandidate = (item) => {
    setSelectedCandidate(item);
    setMobileTab('report'); // Seamlessly switches view to report on mobile
  };

  const handleOpen1v1Compare = (pA, pB) => {
    setComparePlayerAId(pA || targetPlayerId);
    setComparePlayerBId(pB || (selectedCandidate?.player?.id || "p_stengs"));
    setIsCompareArenaOpen(true);
    setMobileTab('arena');
  };

  return (
    <div className="min-h-screen bg-[#0a0a16] text-[#e2e8f0] flex flex-col font-sans">
      {/* Top Tactical Navigation Bar */}
      <header className="sticky top-0 z-40 bg-[#0a0a16]/95 backdrop-blur-md border-b border-[#1f2240] px-3 sm:px-6 lg:px-8 py-2.5 sm:py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-2">
          {/* Logo & Subtitle */}
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-gradient-to-br from-[#00ff88] to-[#00e5ff] p-0.5 shadow-glow-neon shrink-0">
              <div className="w-full h-full bg-[#0a0a16] rounded-[6px] sm:rounded-[7px] flex items-center justify-center">
                <Activity className="w-4 h-4 sm:w-5 sm:h-5 text-[#00ff88]" />
              </div>
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="font-mono font-extrabold text-sm sm:text-base tracking-tight text-white whitespace-nowrap">
                  FM SCOUT <span className="text-[#00ff88]">AI</span>
                </span>
                <span className="px-1.5 py-0.2 rounded text-[9px] sm:text-[10px] font-mono font-bold bg-[#181832] text-[#00e5ff] border border-[#2a2e5c] shrink-0">
                  v2.4
                </span>
              </div>
              <p className="text-[10px] font-mono text-gray-400 hidden sm:block truncate">
                Wyscout / Metrica Nexus Tactical Engine • 100% Real Football Database
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
            <button
              onClick={() => setIsShortlistOpen(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-400/10 hover:bg-amber-400/20 text-amber-300 text-[11px] sm:text-xs font-mono font-medium border border-amber-400/30 transition-all shadow-glow-neon whitespace-nowrap cursor-pointer"
            >
              <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
              <span>쇼트리스트 ({bookmarkedPlayerIds.length})</span>
            </button>

            <button
              onClick={() => setIsMetricGuideOpen(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#00ff88]/10 hover:bg-[#00ff88]/20 text-[#00ff88] text-[11px] sm:text-xs font-mono font-medium border border-[#00ff88]/30 transition-all shadow-glow-neon whitespace-nowrap cursor-pointer"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">전술 가이드</span>
            </button>

            <button
              onClick={() => setIsCompareArenaOpen(!isCompareArenaOpen)}
              className={`flex items-center gap-1 px-2.5 sm:px-3.5 py-1.5 rounded-lg text-[11px] sm:text-xs font-mono transition-all whitespace-nowrap cursor-pointer ${
                isCompareArenaOpen
                  ? 'bg-[#00e5ff] text-black font-bold shadow-glow-cyan'
                  : 'bg-[#121226] text-gray-300 border border-[#1f2240] hover:border-[#2a2e5c]'
              }`}
            >
              <Layers className="w-3.5 h-3.5 text-[#00e5ff]" />
              <span className="hidden sm:inline">1v1 비교 아레나</span>
              <span className="sm:hidden">1v1 비교</span>
            </button>

            <button
              onClick={() => setIsLegalModalOpen(true)}
              className="flex items-center gap-1 px-2 py-1.5 rounded-lg bg-[#121226] hover:bg-[#181832] text-gray-400 hover:text-white text-[11px] sm:text-xs font-mono border border-[#1f2240] transition-colors whitespace-nowrap cursor-pointer"
            >
              <Shield className="w-3.5 h-3.5 text-gray-400" />
              <span className="hidden sm:inline">라이선스</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 flex-1 flex flex-col gap-4 sm:gap-6 pb-20 sm:pb-6">
        {/* 1v1 Compare Arena View (if opened) */}
        {isCompareArenaOpen ? (
          <ComparisonArena
            players={players}
            initialPlayerAId={comparePlayerAId}
            initialPlayerBId={comparePlayerBId}
            onClose={() => {
              setIsCompareArenaOpen(false);
              setMobileTab('candidates');
            }}
          />
        ) : (
          <>
            {/* Target Player Selector & Presets (Always on Desktop, shown on Mobile if tab is 'target' or default) */}
            <div className={`flex flex-col gap-4 ${mobileTab === 'target' ? 'block' : 'hidden sm:block'}`}>
              <TargetSelector
                players={players}
                selectedTargetId={targetPlayerId}
                targetPlayer={targetPlayer}
                onSelectTarget={(id) => {
                  setTargetPlayerId(id);
                  setMobileTab('candidates');
                }}
                archetypes={archetypes}
              />

              {/* Collapsible Filter Toggle Bar */}
              <div className="flex items-center justify-between">
                <button
                  onClick={() => setShowFilterPanel(!showFilterPanel)}
                  className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#121226] hover:bg-[#1a1a38] border border-[#1f2240] hover:border-[#00ff88]/50 text-xs font-mono text-gray-200 transition-all cursor-pointer shadow-md"
                >
                  <Sliders className="w-3.5 h-3.5 text-[#00ff88]" />
                  <span className="font-bold">
                    {showFilterPanel ? '▲ 세부 검색 필터 닫기' : '▼ 세부 필터 & AI 가중치 설정'}
                  </span>
                </button>

                <div className="text-[11px] font-mono text-gray-400 hidden sm:block">
                  ⚡ 100% 현역 실데이터 AI 전술 스카우팅 엔진
                </div>
              </div>

              {/* Tactical Filter Controls Panel */}
              {showFilterPanel && (
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
              )}
            </div>

            {/* 1-Second One-Click Quick Filter Chips Bar */}
            <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
              <span className="text-[11px] font-mono text-gray-400 shrink-0 mr-1 hidden sm:inline">⚡ 퀵 필터:</span>
              
              <button
                onClick={() => setQuickFilter('all')}
                className={`px-3 py-1.5 rounded-full text-xs font-mono font-medium transition-all shrink-0 cursor-pointer ${
                  quickFilter === 'all'
                    ? 'bg-[#00ff88] text-black font-bold shadow-glow-neon'
                    : 'bg-[#121226] text-gray-300 border border-[#1f2240] hover:border-[#00ff88]/40'
                }`}
              >
                ✨ 전체 ({scoutResults.length})
              </button>

              <button
                onClick={() => setQuickFilter('gems')}
                className={`px-3 py-1.5 rounded-full text-xs font-mono font-medium transition-all shrink-0 flex items-center gap-1 cursor-pointer ${
                  quickFilter === 'gems'
                    ? 'bg-amber-400 text-black font-bold shadow-glow-neon'
                    : 'bg-[#121226] text-amber-300 border border-amber-500/30 hover:border-amber-400/60'
                }`}
              >
                <Sparkles className="w-3 h-3 text-amber-400" />
                <span>💎 가성비 진주 (≤€25M)</span>
              </button>

              <button
                onClick={() => setQuickFilter('u23')}
                className={`px-3 py-1.5 rounded-full text-xs font-mono font-medium transition-all shrink-0 flex items-center gap-1 cursor-pointer ${
                  quickFilter === 'u23'
                    ? 'bg-[#00e5ff] text-black font-bold shadow-glow-cyan'
                    : 'bg-[#121226] text-[#00e5ff] border border-[#00e5ff]/30 hover:border-[#00e5ff]/60'
                }`}
              >
                <span>🌟 U-23 특급 유망주</span>
              </button>

              <button
                onClick={() => setQuickFilter('top5')}
                className={`px-3 py-1.5 rounded-full text-xs font-mono font-medium transition-all shrink-0 cursor-pointer ${
                  quickFilter === 'top5'
                    ? 'bg-purple-500 text-white font-bold shadow-lg'
                    : 'bg-[#121226] text-purple-300 border border-purple-500/30 hover:border-purple-400/60'
                }`}
              >
                <span>🇪🇺 유럽 5대 리그</span>
              </button>

              <button
                onClick={() => setQuickFilter('kleague')}
                className={`px-3 py-1.5 rounded-full text-xs font-mono font-medium transition-all shrink-0 cursor-pointer ${
                  quickFilter === 'kleague'
                    ? 'bg-rose-500 text-white font-bold shadow-lg'
                    : 'bg-[#121226] text-rose-300 border border-rose-500/30 hover:border-rose-400/60'
                }`}
              >
                <span>🇰🇷 K리그 보석</span>
              </button>
            </div>

            {/* Dashboard Workspace */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* Left Column (7 cols): Hero Scout Report Card */}
              <div className={`lg:col-span-7 flex flex-col gap-4 ${mobileTab === 'report' ? 'block' : 'hidden sm:block'}`}>
                {selectedCandidate && targetPlayer ? (
                  <ScoutReportCard
                    candidate={selectedCandidate}
                    targetPlayer={targetPlayer}
                    similarityPct={selectedCandidate.similarity_pct}
                    algorithm={algorithm}
                    onCompareDirectly={handleOpen1v1Compare}
                    isBookmarked={bookmarkedPlayerIds.includes(selectedCandidate?.player?.id)}
                    onToggleBookmark={toggleBookmark}
                  />
                ) : (
                  <div className="p-12 text-center rounded-xl bg-[#121226] border border-[#1f2240] text-gray-400 font-mono text-xs">
                    {loading ? '전술 유사도 계산 중...' : '조건에 맞는 선수가 없습니다. 필터 조건을 완화해보세요.'}
                  </div>
                )}
              </div>

              {/* Right Column (5 cols): Candidates Scouting Board */}
              <div className={`lg:col-span-5 flex flex-col gap-3 ${mobileTab === 'candidates' ? 'block' : 'hidden sm:block'}`}>
                <div className="flex items-center justify-between px-1">
                  <div className="text-xs font-mono font-bold text-gray-300 flex items-center gap-2">
                    <Trophy className="w-3.5 h-3.5 text-yellow-400" />
                    유사 선수 랭킹 ({filteredScoutResults.length}명)
                  </div>
                  <span className="text-[11px] font-mono text-gray-400">
                    정렬: 유사도 높은 순
                  </span>
                </div>

                <div className="space-y-2.5 max-h-[750px] overflow-y-auto pr-1">
                  {loading ? (
                    <div className="p-10 text-center rounded-xl bg-[#121226] border border-[#00ff88]/30 text-gray-300 font-mono text-xs flex flex-col items-center justify-center gap-3 shadow-glow-neon animate-pulse">
                      <RefreshCw className="w-7 h-7 text-[#00ff88] animate-spin" />
                      <div className="text-white font-bold text-sm">실시간 AI 전술 스카우팅 연산 중...</div>
                      <div className="text-[11px] text-gray-400">코사인 전술 스타일 + 유클리드 퍼포먼스 체급 종합 계산 중</div>
                    </div>
                  ) : filteredScoutResults.length === 0 ? (
                    <div className="p-8 text-center rounded-xl bg-[#121226] border border-[#1f2240] text-gray-400 font-mono text-xs">
                      조건에 일치하는 선수가 없습니다. 퀵 필터를 '전체'로 변경해보세요.
                    </div>
                  ) : (
                    filteredScoutResults.map((item) => {
                      const p = item.player;
                      const isSelected = selectedCandidate?.player?.id === p.id;
                      const isBookmarked = bookmarkedPlayerIds.includes(p.id);
                      const flag = countryFlags[p.nationality] || "🌐";
                      const isTopGem = item.gem_score && item.gem_score > 90;

                      return (
                        <div
                          key={p.id}
                          onClick={() => handleSelectCandidate(item)}
                          className={`p-3 sm:p-3.5 rounded-xl transition-all cursor-pointer border ${
                            isSelected
                              ? 'bg-[#161633] border-[#00ff88] shadow-glow-neon ring-1 ring-[#00ff88]/50'
                              : 'bg-[#121226] border-[#1f2240] hover:border-[#2a2e5c] hover:bg-[#15152c]'
                          }`}
                        >
                          {/* Card Top: Identity & Match Score */}
                          <div className="flex items-start justify-between gap-2.5">
                            {/* Player Basic Info */}
                            <div className="flex items-start gap-2.5 min-w-0 flex-1">
                              <span className="text-base sm:text-lg shrink-0 mt-0.5">{flag}</span>
                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="font-bold text-white text-xs sm:text-sm tracking-tight break-keep">
                                    {p.korean_name || p.name}
                                  </span>
                                  {p.korean_name && (
                                    <span className="text-gray-400 text-[11px] font-mono shrink-0">
                                      ({p.name})
                                    </span>
                                  )}
                                  <span className="px-1.5 py-0.2 rounded bg-[#00e5ff]/20 text-[#00e5ff] text-[10px] font-mono font-bold shrink-0">
                                    {p.primary_pos}
                                  </span>
                                  {isTopGem && (
                                    <span className="px-1.5 py-0.2 rounded bg-amber-400/20 text-amber-300 text-[10px] font-mono flex items-center gap-0.5 shrink-0 whitespace-nowrap">
                                      <Sparkles className="w-2.5 h-2.5" /> 진주
                                    </span>
                                  )}
                                  {item.manager_fit?.best_fit && (
                                    <span className="px-1.5 py-0.2 rounded bg-amber-400/10 text-amber-300 text-[10px] font-mono border border-amber-400/30 flex items-center gap-0.5 shrink-0 whitespace-nowrap">
                                      👑 {item.manager_fit.best_fit.name.split(' ')[0]} {item.manager_fit.best_fit.score}점
                                    </span>
                                  )}
                                </div>
                                <div className="text-[11px] text-gray-400 font-mono mt-0.5 flex items-center gap-1.5 flex-wrap break-keep">
                                  <span className="text-gray-300 font-medium">{p.club}</span>
                                  <span className="text-gray-600">•</span>
                                  <span>{p.league}</span>
                                  <span className="text-gray-600">•</span>
                                  <span>{p.age}세</span>
                                  <span className="text-gray-600">•</span>
                                  <span className="text-[#00ff88] font-bold">€{p.market_value_eur}M</span>
                                </div>
                              </div>
                            </div>

                            {/* Match % & Sub-Metrics */}
                            <div className="text-right shrink-0">
                              <div className="text-base sm:text-lg font-extrabold font-mono text-[#00ff88] tracking-tight">
                                {(Number(item.similarity_pct) || 0).toFixed(1)}%
                              </div>
                              <div className="text-[10px] font-mono text-gray-400 whitespace-nowrap">
                                스타일 <span className="text-[#00ff88]">{(Number(item.cosine_pct) || 0).toFixed(0)}%</span> • 체급 <span className="text-[#00e5ff]">{(Number(item.euclidean_pct) || 0).toFixed(0)}%</span>
                              </div>
                            </div>
                          </div>

                          {/* AI Scout Narrative Briefing Pill */}
                          {item.ai_briefing && (
                            <div className="mt-2 text-[11px] text-gray-300 bg-[#0a0a16] px-2.5 py-1.5 rounded-lg border border-[#1f2240] flex items-start gap-1.5 break-keep">
                              <span className="text-[#00ff88] font-mono font-bold text-[10px] shrink-0 mt-0.5">🤖 AI 코멘트</span>
                              <span className="leading-snug text-gray-300 line-clamp-2">{item.ai_briefing}</span>
                            </div>
                          )}

                          {/* Tactical 5-Pillar Clean Badges Bar */}
                          <div className="mt-2.5 pt-2 border-t border-[#1f2240]/70 flex items-center justify-between gap-2 flex-wrap text-[10px] font-mono">
                            <div className="flex items-center gap-1 flex-wrap text-gray-300">
                              <span className="px-1.5 py-0.5 rounded bg-[#0a0a16] border border-[#1f2240]">🪄 패스 {p.vision_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-[#0a0a16] border border-[#1f2240]">⚽ 슈팅 {p.striking_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-[#0a0a16] border border-[#1f2240]">⚡ 드리블 {p.dribble_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-[#0a0a16] border border-[#1f2240]">🛡️ 수비 {p.defense_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-[#0a0a16] border border-[#1f2240]">💪 경합 {p.physical_grade}</span>
                            </div>

                            <div className="flex items-center gap-1.5 ml-auto">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  toggleBookmark(p.id);
                                }}
                                className={`px-2 py-0.5 rounded text-[10px] font-mono border flex items-center gap-1 shrink-0 transition-colors cursor-pointer ${
                                  isBookmarked
                                    ? 'bg-amber-400/20 text-amber-300 border-amber-400 shadow-glow-neon'
                                    : 'bg-[#0a0a16] hover:bg-[#181832] text-gray-400 border-[#1f2240]'
                                }`}
                                title="관심 선수 쇼트리스트에 담기"
                              >
                                <Star className={`w-2.5 h-2.5 ${isBookmarked ? 'fill-amber-400 text-amber-400' : ''}`} />
                                <span>{isBookmarked ? '찜함' : '찜'}</span>
                              </button>

                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleOpen1v1Compare(targetPlayerId, p.id);
                                }}
                                className="px-2 py-0.5 rounded bg-[#00e5ff]/10 hover:bg-[#00e5ff]/20 text-[#00e5ff] text-[10px] font-mono border border-[#00e5ff]/30 flex items-center gap-1 shrink-0 transition-colors cursor-pointer"
                              >
                                <span>1v1 비교</span>
                                <ArrowRight className="w-2.5 h-2.5" />
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

      {/* Floating Mobile Bottom Navigation Bar */}
      <nav className="sm:hidden fixed bottom-0 left-0 right-0 z-50 bg-[#0a0a16]/95 backdrop-blur-xl border-t border-[#1f2240] px-3 py-2 flex items-center justify-around shadow-2xl">
        <button
          onClick={() => {
            setIsCompareArenaOpen(false);
            setMobileTab('target');
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            mobileTab === 'target' && !isCompareArenaOpen ? 'text-[#00ff88] font-bold' : 'text-gray-400'
          }`}
        >
          <Target className="w-4 h-4" />
          <span>타겟</span>
        </button>

        <button
          onClick={() => {
            setIsCompareArenaOpen(false);
            setMobileTab('candidates');
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            mobileTab === 'candidates' && !isCompareArenaOpen ? 'text-[#00ff88] font-bold' : 'text-gray-400'
          }`}
        >
          <Trophy className="w-4 h-4" />
          <span>랭킹</span>
        </button>

        <button
          onClick={() => {
            setIsCompareArenaOpen(false);
            setMobileTab('report');
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            mobileTab === 'report' && !isCompareArenaOpen ? 'text-[#00e5ff] font-bold' : 'text-gray-400'
          }`}
        >
          <Activity className="w-4 h-4" />
          <span>리포트</span>
        </button>

        <button
          onClick={() => setIsShortlistOpen(true)}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            bookmarkedPlayerIds.length > 0 ? 'text-amber-300 font-bold' : 'text-gray-400'
          }`}
        >
          <Star className={`w-4 h-4 ${bookmarkedPlayerIds.length > 0 ? 'fill-amber-400 text-amber-400' : ''}`} />
          <span>찜 ({bookmarkedPlayerIds.length})</span>
        </button>

        <button
          onClick={() => {
            handleOpen1v1Compare(targetPlayerId, selectedCandidate?.player?.id);
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            isCompareArenaOpen ? 'text-[#00e5ff] font-bold' : 'text-gray-400'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>1v1</span>
        </button>
      </nav>

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

      {/* Shortlist Modal */}
      <ShortlistModal
        isOpen={isShortlistOpen}
        onClose={() => setIsShortlistOpen(false)}
        bookmarkedPlayerIds={bookmarkedPlayerIds}
        allPlayers={players}
        onRemoveBookmark={toggleBookmark}
        onClearAllBookmarks={clearAllBookmarks}
        onSelectAsTarget={(id) => {
          setTargetPlayerId(id);
          setMobileTab('candidates');
        }}
        onOpen1v1Compare={handleOpen1v1Compare}
        targetPlayerId={targetPlayerId}
      />

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
