import React, { useState, useEffect, useMemo } from 'react';
import { 
  Layers, ArrowLeftRight, User, Shield, Zap, Award, Sparkles, Check, 
  ChevronRight, Search, X, Trophy, Activity, Target, Flame
} from 'lucide-react';
import RadarChartCanvas from './RadarChartCanvas';

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

const RIVALRY_PRESETS = [
  { label: "손흥민 vs 살라", a: "p_son", b: "p_salah", desc: "EPL 득점왕 윙어 대결" },
  { label: "홀란드 vs 음바페", a: "p_haaland", b: "p_mbappe", desc: "차세대 발롱도르 괴물 대결" },
  { label: "이강인 vs 쿠보", a: "p_lee_kangin", b: "p_kubo", desc: "한일 최고의 왼발 테크니션" },
  { label: "김민재 vs 반다이크", a: "p_kim_minjae", b: "p_van_dijk", desc: "유럽 최정상 센터백 벽 대결" },
  { label: "로드리 vs 라이스", a: "p_rodri", b: "p_rice", desc: "세계 최고 6번 수미 대결" },
  { label: "비니시우스 vs 야말", a: "p_vinicius", b: "p_yamal", desc: "엘클라시코 측면 크랙 대결" }
];

export default function ComparisonArena({
  players = [],
  initialPlayerAId,
  initialPlayerBId,
  onClose
}) {
  const [playerAId, setPlayerAId] = useState(initialPlayerAId || "p_son");
  const [playerBId, setPlayerBId] = useState(initialPlayerBId || "p_salah");
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Search Modal State
  const [searchTargetSlot, setSearchTargetSlot] = useState(null); // 'A' or 'B'
  const [searchQuery, setSearchQuery] = useState("");
  const [posFilter, setPosFilter] = useState("ALL"); // 'ALL', 'FW', 'MF', 'DF', 'GK'

  const fetchComparison = async () => {
    if (!playerAId || !playerBId) return;
    setLoading(true);
    try {
      const res = await fetch('/api/scout/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_a_id: playerAId, player_b_id: playerBId })
      });
      const data = await res.json();
      setComparisonData(data);
    } catch (err) {
      console.error("Comparison fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComparison();
  }, [playerAId, playerBId]);

  const pA = comparisonData?.player_a;
  const pB = comparisonData?.player_b;

  const flagA = pA ? countryFlags[pA.nationality] || "🌐" : "🌐";
  const flagB = pB ? countryFlags[pB.nationality] || "🌐" : "🌐";

  const radarScoresA = pA ? [pA.vision_score, pA.striking_score, pA.dribble_score, pA.defense_score, pA.physical_score] : [50,50,50,50,50];
  const radarScoresB = pB ? [pB.vision_score, pB.striking_score, pB.dribble_score, pB.defense_score, pB.physical_score] : [50,50,50,50,50];

  // Swap Player A and Player B
  const handleSwapPlayers = () => {
    const temp = playerAId;
    setPlayerAId(playerBId);
    setPlayerBId(temp);
  };

  // Filtered Players for Search Modal
  const modalFilteredPlayers = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    return players.filter(p => {
      // Position filter
      if (posFilter !== "ALL" && p.pos_group !== posFilter && p.primary_pos !== posFilter) {
        return false;
      }
      if (!q) return true;
      const kor = (p.korean_name || "").toLowerCase();
      const eng = (p.name || "").toLowerCase();
      const full = (p.full_name || "").toLowerCase();
      const club = (p.club || "").toLowerCase();
      const league = (p.league || "").toLowerCase();
      return kor.includes(q) || eng.includes(q) || full.includes(q) || club.includes(q) || league.includes(q);
    });
  }, [players, searchQuery, posFilter]);

  const handleSelectPlayerFromModal = (selectedId) => {
    if (searchTargetSlot === 'A') {
      setPlayerAId(selectedId);
    } else if (searchTargetSlot === 'B') {
      setPlayerBId(selectedId);
    }
    setSearchTargetSlot(null);
    setSearchQuery("");
  };

  return (
    <div className="flex flex-col gap-5 p-4 sm:p-6 rounded-2xl bg-[#121226] border border-[#1f2240] shadow-2xl relative">
      {/* Arena Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#1f2240] pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-[#00e5ff]/20 to-[#00ff88]/20 border border-[#00e5ff]/30 text-[#00e5ff] shadow-glow-cyan shrink-0">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base sm:text-lg font-bold text-white font-mono tracking-tight flex items-center gap-2">
              <span>1v1 TACTICAL HEAD-TO-HEAD ARENA</span>
              <span className="px-2 py-0.5 rounded text-[10px] bg-[#181832] text-[#00ff88] border border-[#00ff88]/30">LIVE 대조</span>
            </h2>
            <p className="text-xs text-gray-400 font-mono">두 선수의 전술 레이더 오버레이 및 9대 핵심 스탯 1:1 정밀 대조</p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="self-start sm:self-auto px-3.5 py-1.5 rounded-xl bg-[#181832] hover:bg-[#222248] text-xs font-mono text-gray-300 border border-[#2a2e5c] transition-colors cursor-pointer"
        >
          스카우팅 보드로 복귀 ✕
        </button>
      </div>

      {/* Trending Rivalry Battles 1-Click Quick Presets */}
      <div className="flex flex-col gap-1.5">
        <div className="text-[11px] font-mono text-gray-400 flex items-center gap-1.5 px-1">
          <Flame className="w-3.5 h-3.5 text-amber-400" />
          <span className="font-bold text-gray-300">인기 라이벌 더비 퀵 매치:</span>
          <span className="text-[10px] text-gray-500 hidden sm:inline">원클릭으로 두 선수를 즉시 1v1 아레나에 로드합니다.</span>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
          {RIVALRY_PRESETS.map((preset, idx) => {
            const isActive = (playerAId === preset.a && playerBId === preset.b) || (playerAId === preset.b && playerBId === preset.a);
            return (
              <button
                key={idx}
                onClick={() => {
                  setPlayerAId(preset.a);
                  setPlayerBId(preset.b);
                }}
                className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
                  isActive
                    ? 'bg-gradient-to-r from-[#00e5ff] to-[#00ff88] text-black font-extrabold shadow-glow-cyan'
                    : 'bg-[#0a0a16] text-gray-300 border border-[#1f2240] hover:border-[#00e5ff]/50 hover:bg-[#15152c]'
                }`}
              >
                <span>⚔️</span>
                <span>{preset.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Hero VS Match Arena (Player A vs Player B Cards) */}
      <div className="grid grid-cols-1 lg:grid-cols-11 gap-4 items-center">
        {/* Player A Card (Cyan Theme) */}
        <div className="lg:col-span-5 p-4 rounded-xl bg-[#0a0a16] border border-[#00e5ff]/40 shadow-glow-cyan flex flex-col gap-3 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/40">
              PLAYER A (기준 / CYAN)
            </span>
            <button
              onClick={() => {
                setSearchTargetSlot('A');
                setSearchQuery("");
              }}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#181832] hover:bg-[#202046] text-[#00e5ff] text-xs font-mono border border-[#00e5ff]/30 transition-colors cursor-pointer"
            >
              <Search className="w-3 h-3" />
              <span>선수 변경</span>
            </button>
          </div>

          {pA ? (
            <div className="flex items-start gap-3">
              <div className="w-14 h-16 sm:w-16 sm:h-20 rounded-lg bg-[#121226] border border-[#2a2e5c] flex flex-col items-center justify-center relative shrink-0 shadow-inner">
                <User className="w-8 h-10 text-cyan-400/80" />
                <span className="absolute bottom-1 right-1 text-xs">{flagA}</span>
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <h3 className="text-base sm:text-lg font-bold text-white tracking-tight break-keep">
                    {pA.korean_name || pA.name}
                  </h3>
                  {pA.korean_name && (
                    <span className="text-xs text-gray-400 font-mono">({pA.name})</span>
                  )}
                  <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-[#00e5ff]/20 text-[#00e5ff]">
                    {pA.primary_pos}
                  </span>
                </div>
                <div className="text-xs text-gray-300 font-mono mt-0.5 break-keep">
                  {pA.club} • {pA.league} • {pA.age}세
                </div>
                <div className="text-[11px] text-[#00e5ff] font-mono mt-0.5 font-bold">
                  시장가치: €{pA.market_value_eur}M (약 {(pA.market_value_eur * 14.8).toFixed(0)}억원)
                </div>
                <div className="flex items-center gap-1 flex-wrap text-[10px] font-mono mt-2 text-gray-300">
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">🪄 패스 {pA.vision_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">⚽ 슈팅 {pA.striking_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">⚡ 드리블 {pA.dribble_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">🛡️ 수비 {pA.defense_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">💪 경합 {pA.physical_grade}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center text-gray-400 font-mono text-xs">선수를 선택해주세요.</div>
          )}
        </div>

        {/* Center Swap & VS Hub */}
        <div className="lg:col-span-1 flex flex-row lg:flex-col items-center justify-center gap-2 py-1">
          <button
            onClick={handleSwapPlayers}
            className="p-2.5 rounded-full bg-[#181832] hover:bg-[#222248] text-gray-300 hover:text-white border border-[#2a2e5c] shadow-lg transition-all active:scale-90 cursor-pointer"
            title="선수 위치 맞바꾸기"
          >
            <ArrowLeftRight className="w-4 h-4 text-[#00e5ff]" />
          </button>
          <div className="font-extrabold text-sm font-mono tracking-widest text-gray-500">VS</div>
        </div>

        {/* Player B Card (Neon Green Theme) */}
        <div className="lg:col-span-5 p-4 rounded-xl bg-[#0a0a16] border border-[#00ff88]/40 shadow-glow-neon flex flex-col gap-3 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#00ff88]/20 text-[#00ff88] border border-[#00ff88]/40">
              PLAYER B (대조 / NEON GREEN)
            </span>
            <button
              onClick={() => {
                setSearchTargetSlot('B');
                setSearchQuery("");
              }}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#181832] hover:bg-[#202046] text-[#00ff88] text-xs font-mono border border-[#00ff88]/30 transition-colors cursor-pointer"
            >
              <Search className="w-3 h-3" />
              <span>선수 변경</span>
            </button>
          </div>

          {pB ? (
            <div className="flex items-start gap-3">
              <div className="w-14 h-16 sm:w-16 sm:h-20 rounded-lg bg-[#121226] border border-[#2a2e5c] flex flex-col items-center justify-center relative shrink-0 shadow-inner">
                <User className="w-8 h-10 text-emerald-400/80" />
                <span className="absolute bottom-1 right-1 text-xs">{flagB}</span>
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <h3 className="text-base sm:text-lg font-bold text-white tracking-tight break-keep">
                    {pB.korean_name || pB.name}
                  </h3>
                  {pB.korean_name && (
                    <span className="text-xs text-gray-400 font-mono">({pB.name})</span>
                  )}
                  <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-[#00ff88]/20 text-[#00ff88]">
                    {pB.primary_pos}
                  </span>
                </div>
                <div className="text-xs text-gray-300 font-mono mt-0.5 break-keep">
                  {pB.club} • {pB.league} • {pB.age}세
                </div>
                <div className="text-[11px] text-[#00ff88] font-mono mt-0.5 font-bold">
                  시장가치: €{pB.market_value_eur}M (약 {(pB.market_value_eur * 14.8).toFixed(0)}억원)
                </div>
                <div className="flex items-center gap-1 flex-wrap text-[10px] font-mono mt-2 text-gray-300">
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">🪄 패스 {pB.vision_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">⚽ 슈팅 {pB.striking_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">⚡ 드리블 {pB.dribble_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">🛡️ 수비 {pB.defense_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">💪 경합 {pB.physical_grade}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center text-gray-400 font-mono text-xs">선수를 선택해주세요.</div>
          )}
        </div>
      </div>

      {/* Tactical Similarity Overall Outcome Banner */}
      {comparisonData && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="p-3.5 rounded-xl bg-gradient-to-r from-[#00e5ff]/15 via-[#00e5ff]/5 to-transparent border border-[#00e5ff]/30 flex items-center justify-between font-mono">
            <div>
              <div className="text-[10px] text-gray-300 uppercase tracking-wider">COSINE PLAYSTYLE MATCH</div>
              <div className="text-xs text-gray-400 mt-0.5">플레이스타일 & 전술 패턴 일치율</div>
            </div>
            <div className="text-2xl font-bold text-[#00e5ff] drop-shadow-md">
              {comparisonData.cosine_similarity}%
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-gradient-to-r from-[#00ff88]/15 via-[#00ff88]/5 to-transparent border border-[#00ff88]/30 flex items-center justify-between font-mono">
            <div>
              <div className="text-[10px] text-gray-300 uppercase tracking-wider">EUCLIDEAN VOLUME SIMILARITY</div>
              <div className="text-xs text-gray-400 mt-0.5">물리적 퍼포먼스 체급 일치율</div>
            </div>
            <div className="text-2xl font-bold text-[#00ff88] drop-shadow-md">
              {comparisonData.euclidean_similarity}%
            </div>
          </div>
        </div>
      )}

      {/* Main Grid: Radar Chart + Head-to-Head Advantage Bar Table */}
      {pA && pB && (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5 items-start">
          {/* Left Column: Overlay Radar Chart */}
          <div className="md:col-span-5 flex flex-col items-center justify-center p-4 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
            <div className="text-xs font-mono text-gray-300 mb-2 flex items-center gap-3">
              <span className="flex items-center gap-1 text-[#00e5ff]">
                <span className="w-2.5 h-2.5 rounded-full bg-[#00e5ff]"></span>
                {pA.korean_name || pA.name}
              </span>
              <span className="text-gray-500">vs</span>
              <span className="flex items-center gap-1 text-[#00ff88]">
                <span className="w-2.5 h-2.5 rounded-full bg-[#00ff88]"></span>
                {pB.korean_name || pB.name}
              </span>
            </div>

            <RadarChartCanvas
              targetScores={radarScoresA}
              candidateScores={radarScoresB}
              targetName={pA.korean_name || pA.name}
              candidateName={pB.korean_name || pB.name}
              size={270}
            />
          </div>

          {/* Right Column: Key 90-Minute Stats Advantage Differential Table */}
          <div className="md:col-span-7 flex flex-col gap-3">
            <div className="p-3.5 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
              <div className="flex items-center justify-between text-xs font-mono font-bold text-gray-300 mb-3 border-b border-[#1f2240] pb-2">
                <span className="text-[#00e5ff] flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-[#00e5ff]" />
                  {pA.korean_name || pA.name}
                </span>
                <span className="text-gray-400 font-sans font-medium text-[11px]">[ 90분당 핵심 스탯 직접 비교 ]</span>
                <span className="text-[#00ff88] flex items-center gap-1">
                  {pB.korean_name || pB.name}
                  <span className="w-2 h-2 rounded-full bg-[#00ff88]" />
                </span>
              </div>

              <div className="space-y-2.5 font-mono text-xs">
                {comparisonData.detailed_stats && comparisonData.detailed_stats.map((stat, idx) => {
                  const valA = parseFloat(stat.a) || 0;
                  const valB = parseFloat(stat.b) || 0;
                  const sum = valA + valB;
                  const pctA = sum > 0 ? (valA / sum) * 100 : 50;
                  const pctB = sum > 0 ? (valB / sum) * 100 : 50;
                  const aWins = valA > valB;
                  const bWins = valB > valA;

                  return (
                    <div key={idx} className="p-2 rounded-lg bg-[#121226] border border-[#1f2240]/60 flex flex-col gap-1.5">
                      {/* Metric Name & Values */}
                      <div className="flex items-center justify-between text-xs">
                        <span className={`font-bold ${aWins ? 'text-[#00e5ff] drop-shadow-sm font-extrabold' : 'text-gray-400'}`}>
                          {aWins && '👑 '}{valA}{stat.unit}
                        </span>

                        <span className="text-gray-300 font-sans text-[11px] font-medium break-keep text-center px-1">
                          {stat.name}
                        </span>

                        <span className={`font-bold ${bWins ? 'text-[#00ff88] drop-shadow-sm font-extrabold' : 'text-gray-400'}`}>
                          {valB}{stat.unit}{bWins && ' 👑'}
                        </span>
                      </div>

                      {/* Visual Advantage Gauge Bar */}
                      <div className="w-full h-1.5 bg-[#0a0a16] rounded-full overflow-hidden flex">
                        <div
                          style={{ width: `${pctA}%` }}
                          className={`h-full transition-all ${
                            aWins ? 'bg-[#00e5ff] shadow-glow-cyan' : 'bg-gray-600'
                          }`}
                        />
                        <div
                          style={{ width: `${pctB}%` }}
                          className={`h-full transition-all ${
                            bWins ? 'bg-[#00ff88] shadow-glow-neon' : 'bg-gray-600'
                          }`}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Interactive Player Search & Select Modal */}
      {searchTargetSlot && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
          <div className="bg-[#121226] border border-[#00ff88]/40 rounded-2xl w-full max-w-xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="p-4 border-b border-[#1f2240] flex items-center justify-between bg-[#0a0a16]">
              <div className="flex items-center gap-2">
                <Search className="w-4 h-4 text-[#00ff88]" />
                <h3 className="text-sm font-bold text-white font-mono">
                  [ {searchTargetSlot === 'A' ? 'PLAYER A (기준)' : 'PLAYER B (대조)'} 선수 검색 및 선택 ]
                </h3>
              </div>
              <button
                onClick={() => setSearchTargetSlot(null)}
                className="p-1 rounded-lg hover:bg-[#181832] text-gray-400 hover:text-white transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Search Input & Position Filter */}
            <div className="p-3.5 border-b border-[#1f2240] bg-[#0d0d1e] flex flex-col gap-2.5">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="선수 이름 (손흥민, 살라, 홀란드, 음바페...), 클럽명, 리그 검색..."
                  autoFocus
                  className="w-full bg-[#181832] border border-[#2a2e5c] focus:border-[#00ff88] rounded-xl pl-9 pr-8 py-2 text-xs font-mono text-white placeholder-gray-500 focus:outline-none"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="absolute right-2.5 top-2.5 text-gray-400 hover:text-white"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>

              {/* Position Filter Pills */}
              <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
                {["ALL", "FW", "MF", "DF", "GK"].map((pos) => (
                  <button
                    key={pos}
                    onClick={() => setPosFilter(pos)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-mono transition-all shrink-0 cursor-pointer ${
                      posFilter === pos
                        ? 'bg-[#00ff88] text-black font-bold'
                        : 'bg-[#181832] text-gray-400 hover:text-white border border-[#2a2e5c]'
                    }`}
                  >
                    {pos === "ALL" ? "전체" : pos}
                  </button>
                ))}
              </div>
            </div>

            {/* Search Results List */}
            <div className="p-3 overflow-y-auto max-h-96 space-y-1.5 divide-y divide-[#1f2240]/40">
              {modalFilteredPlayers.length === 0 ? (
                <div className="p-8 text-center text-gray-400 font-mono text-xs">
                  검색 결과가 없습니다.
                </div>
              ) : (
                modalFilteredPlayers.slice(0, 50).map((player) => {
                  const flag = countryFlags[player.nationality] || "🌐";
                  const isCurrent = (searchTargetSlot === 'A' ? playerAId : playerBId) === player.id;
                  return (
                    <div
                      key={player.id}
                      onClick={() => handleSelectPlayerFromModal(player.id)}
                      className={`pt-1.5 first:pt-0 p-2.5 rounded-xl transition-all cursor-pointer flex items-center justify-between gap-2 ${
                        isCurrent
                          ? 'bg-[#00ff88]/20 border border-[#00ff88] text-white'
                          : 'hover:bg-[#181832] border border-transparent'
                      }`}
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <span className="text-base shrink-0">{flag}</span>
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5 flex-wrap">
                            <span className="font-bold text-white text-xs sm:text-sm tracking-tight break-keep">
                              {player.korean_name || player.name}
                            </span>
                            {player.korean_name && (
                              <span className="text-gray-400 text-[11px] font-mono">
                                ({player.name})
                              </span>
                            )}
                            <span className="px-1.5 py-0.2 rounded bg-[#00e5ff]/20 text-[#00e5ff] text-[10px] font-mono font-bold">
                              {player.primary_pos}
                            </span>
                          </div>
                          <div className="text-[11px] text-gray-400 font-mono mt-0.5 break-keep">
                            {player.club} • {player.league} • {player.age}세
                          </div>
                        </div>
                      </div>

                      <div className="text-right shrink-0">
                        <div className="text-xs font-bold font-mono text-[#00ff88]">
                          €{player.market_value_eur}M
                        </div>
                        <div className="text-[10px] font-mono text-gray-500">
                          {player.foot}발
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
