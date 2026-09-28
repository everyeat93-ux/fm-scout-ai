import React, { useState, useEffect, useMemo } from 'react';
import { 
  Layers, ArrowLeftRight, User, Shield, Zap, Award, Sparkles, Check, 
  ChevronRight, Search, X, Trophy, Activity, Target, Flame
} from 'lucide-react';
import RadarChartCanvas from './RadarChartCanvas';
import { API_BASE } from '../apiConfig';

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
      const res = await fetch(`${API_BASE}/api/scout/compare`, {
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
    <div className="flex flex-col gap-5 p-4 sm:p-6 rounded-2xl bg-white border-2 border-gray-900 shadow-md relative text-gray-900 select-none">
      {/* Arena Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-200 pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-purple-100 border border-purple-200 text-purple-700 shadow-xs shrink-0">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base sm:text-lg font-black text-gray-950 font-sans tracking-tight flex items-center gap-2">
              <span>1v1 TACTICAL HEAD-TO-HEAD ARENA</span>
              <span className="px-2 py-0.5 rounded text-[10px] bg-purple-100 text-purple-800 border border-purple-300 font-bold font-mono">LIVE 대조</span>
            </h2>
            <p className="text-xs text-gray-500 font-mono">두 선수의 전술 레이더 오버레이 및 9대 핵심 스탯 1:1 정밀 대조</p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="self-start sm:self-auto px-3.5 py-1.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-xs font-mono font-bold text-gray-700 border border-gray-300 transition-colors cursor-pointer shadow-xs"
        >
          스카우팅 보드로 복귀 ✕
        </button>
      </div>

      {/* Trending Rivalry Battles 1-Click Quick Presets */}
      <div className="flex flex-col gap-1.5">
        <div className="text-[11px] font-mono text-gray-600 flex items-center gap-1.5 px-1">
          <Flame className="w-3.5 h-3.5 text-amber-500" />
          <span className="font-bold text-gray-800">인기 라이벌 더비 퀵 매치:</span>
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
                className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 flex items-center gap-1.5 cursor-pointer whitespace-nowrap border ${
                  isActive
                    ? 'bg-gray-900 border-gray-900 text-white font-bold shadow-sm'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 shadow-xs'
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
        {/* Player A Card */}
        <div className="lg:col-span-5 p-4 rounded-xl bg-purple-50/40 border-2 border-purple-600 shadow-sm flex flex-col gap-3 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-100 text-purple-900 border border-purple-300">
              PLAYER A (PURPLE)
            </span>
            <button
              onClick={() => {
                setSearchTargetSlot('A');
                setSearchQuery("");
              }}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white hover:bg-purple-50 text-purple-700 text-xs font-mono font-bold border border-purple-300 transition-colors cursor-pointer shadow-xs"
            >
              <Search className="w-3.5 h-3.5" />
              <span>선수 변경</span>
            </button>
          </div>

          {pA ? (
            <div className="flex items-start gap-3">
              <div className="w-14 h-16 sm:w-16 sm:h-20 rounded-lg bg-white border-2 border-purple-300 flex flex-col items-center justify-center relative shrink-0 shadow-xs">
                <User className="w-8 h-10 text-purple-600" />
                <span className="absolute bottom-1 right-1 text-xs">{flagA}</span>
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <h3 className="text-base sm:text-lg font-black text-gray-950 tracking-tight break-keep">
                    {pA.korean_name || pA.name}
                  </h3>
                  {pA.korean_name && (
                    <span className="text-xs text-gray-500 font-mono">({pA.name})</span>
                  )}
                  <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-purple-100 text-purple-900 border border-purple-200">
                    {pA.primary_pos}
                  </span>
                </div>
                <div className="text-xs text-gray-600 font-mono mt-0.5 break-keep">
                  {pA.club} • {pA.league} • {pA.age}세
                </div>
                <div className="text-xs text-purple-700 font-mono mt-0.5 font-bold">
                  시장가치: €{pA.market_value_eur}M
                </div>
                <div className="flex items-center gap-1 flex-wrap text-[10px] font-mono mt-2 text-gray-700">
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">🪄 패스 {pA.vision_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">⚽ 슈팅 {pA.striking_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">⚡ 드리블 {pA.dribble_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">🛡️ 수비 {pA.defense_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">💪 경합 {pA.physical_grade}</span>
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
            className="p-2.5 rounded-full bg-white hover:bg-gray-100 text-gray-800 border-2 border-gray-900 shadow-sm transition-all active:scale-90 cursor-pointer"
            title="선수 위치 맞바꾸기"
          >
            <ArrowLeftRight className="w-4 h-4 text-purple-700" />
          </button>
          <div className="font-extrabold text-sm font-mono tracking-widest text-gray-500">VS</div>
        </div>

        {/* Player B Card */}
        <div className="lg:col-span-5 p-4 rounded-xl bg-amber-50/40 border-2 border-amber-500 shadow-sm flex flex-col gap-3 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-100 text-amber-900 border border-amber-300">
              PLAYER B (AMBER)
            </span>
            <button
              onClick={() => {
                setSearchTargetSlot('B');
                setSearchQuery("");
              }}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white hover:bg-amber-50 text-amber-900 text-xs font-mono font-bold border border-amber-300 transition-colors cursor-pointer shadow-xs"
            >
              <Search className="w-3.5 h-3.5" />
              <span>선수 변경</span>
            </button>
          </div>

          {pB ? (
            <div className="flex items-start gap-3">
              <div className="w-14 h-16 sm:w-16 sm:h-20 rounded-lg bg-white border-2 border-amber-300 flex flex-col items-center justify-center relative shrink-0 shadow-xs">
                <User className="w-8 h-10 text-amber-500" />
                <span className="absolute bottom-1 right-1 text-xs">{flagB}</span>
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <h3 className="text-base sm:text-lg font-black text-gray-950 tracking-tight break-keep">
                    {pB.korean_name || pB.name}
                  </h3>
                  {pB.korean_name && (
                    <span className="text-xs text-gray-500 font-mono">({pB.name})</span>
                  )}
                  <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-amber-100 text-amber-900 border border-amber-200">
                    {pB.primary_pos}
                  </span>
                </div>
                <div className="text-xs text-gray-600 font-mono mt-0.5 break-keep">
                  {pB.club} • {pB.league} • {pB.age}세
                </div>
                <div className="text-xs text-amber-900 font-mono mt-0.5 font-bold">
                  시장가치: €{pB.market_value_eur}M
                </div>
                <div className="flex items-center gap-1 flex-wrap text-[10px] font-mono mt-2 text-gray-700">
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">🪄 패스 {pB.vision_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">⚽ 슈팅 {pB.striking_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">⚡ 드리블 {pB.dribble_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">🛡️ 수비 {pB.defense_grade}</span>
                  <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">💪 경합 {pB.physical_grade}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center text-gray-400 font-mono text-xs">선수를 선택해주세요.</div>
          )}
        </div>
      </div>

      {/* Tactical Similarity Overall Outcome Banner (Clean Light Theme) */}
      {comparisonData && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="p-3.5 rounded-xl bg-purple-50/70 border-2 border-purple-200 flex items-center justify-between font-mono shadow-xs">
            <div>
              <div className="text-[10px] text-purple-900 font-bold uppercase tracking-wider">COSINE PLAYSTYLE MATCH</div>
              <div className="text-xs text-gray-600 font-sans mt-0.5 font-medium">플레이스타일 & 전술 패턴 일치율</div>
            </div>
            <div className="text-2xl sm:text-3xl font-black text-purple-700 font-mono">
              {comparisonData.cosine_similarity}%
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-emerald-50/70 border-2 border-emerald-200 flex items-center justify-between font-mono shadow-xs">
            <div>
              <div className="text-[10px] text-emerald-900 font-bold uppercase tracking-wider">EUCLIDEAN VOLUME SIMILARITY</div>
              <div className="text-xs text-gray-600 font-sans mt-0.5 font-medium">물리적 퍼포먼스 체급 일치율</div>
            </div>
            <div className="text-2xl sm:text-3xl font-black text-emerald-700 font-mono">
              {comparisonData.euclidean_similarity}%
            </div>
          </div>
        </div>
      )}

      {/* Main Grid: Radar Chart + Head-to-Head Advantage Bar Table (Clean White Theme) */}
      {pA && pB && (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5 items-start">
          {/* Left Column: Overlay Radar Chart */}
          <div className="md:col-span-5 flex flex-col items-center justify-center p-4 rounded-xl bg-white border-2 border-gray-900 shadow-sm">
            <div className="text-xs font-mono text-gray-800 mb-2 flex items-center gap-3 font-bold">
              <span className="flex items-center gap-1.5 text-purple-700">
                <span className="w-2.5 h-2.5 rounded-full bg-purple-600"></span>
                {pA.korean_name || pA.name}
              </span>
              <span className="text-gray-400">vs</span>
              <span className="flex items-center gap-1.5 text-amber-700">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                {pB.korean_name || pB.name}
              </span>
            </div>

            <RadarChartCanvas
              targetScores={radarScoresA}
              candidateScores={radarScoresB}
              targetName={pA.korean_name || pA.name}
              candidateName={pB.korean_name || pB.name}
              size={240}
            />
          </div>

          {/* Right Column: Key 90-Minute Stats Advantage Differential Table */}
          <div className="md:col-span-7 flex flex-col gap-3">
            <div className="p-4 rounded-xl bg-white border-2 border-gray-900 shadow-sm">
              <div className="flex items-center justify-between text-xs font-mono font-bold text-gray-900 mb-3 border-b border-gray-200 pb-2.5">
                <span className="text-purple-700 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-purple-600" />
                  {pA.korean_name || pA.name}
                </span>
                <span className="text-gray-600 font-sans font-bold text-[11px]">[ 90분당 핵심 스탯 직접 비교 ]</span>
                <span className="text-amber-800 flex items-center gap-1.5">
                  {pB.korean_name || pB.name}
                  <span className="w-2 h-2 rounded-full bg-amber-500" />
                </span>
              </div>

              <div className="space-y-2 font-mono text-xs">
                {comparisonData.detailed_stats && comparisonData.detailed_stats.map((stat, idx) => {
                  const valA = parseFloat(stat.a) || 0;
                  const valB = parseFloat(stat.b) || 0;
                  const sum = valA + valB;
                  const pctA = sum > 0 ? (valA / sum) * 100 : 50;
                  const pctB = sum > 0 ? (valB / sum) * 100 : 50;
                  const aWins = valA > valB;
                  const bWins = valB > valA;

                  return (
                    <div key={idx} className="p-2.5 rounded-xl bg-gray-50 border border-gray-200 hover:bg-purple-50/30 transition-colors flex flex-col gap-1.5">
                      {/* Metric Name & Values */}
                      <div className="flex items-center justify-between text-xs">
                        <span className={`font-mono font-bold ${aWins ? 'text-purple-700 font-black' : 'text-gray-500'}`}>
                          {aWins && '👑 '}{valA}{stat.unit}
                        </span>

                        <span className="text-gray-900 font-sans text-xs font-bold break-keep text-center px-1">
                          {stat.name}
                        </span>

                        <span className={`font-mono font-bold ${bWins ? 'text-amber-700 font-black' : 'text-gray-500'}`}>
                          {valB}{stat.unit}{bWins && ' 👑'}
                        </span>
                      </div>

                      {/* Visual Advantage Gauge Bar */}
                      <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden flex">
                        <div
                          style={{ width: `${pctA}%` }}
                          className={`h-full transition-all ${
                            aWins ? 'bg-purple-600' : 'bg-gray-300'
                          }`}
                        />
                        <div
                          style={{ width: `${pctB}%` }}
                          className={`h-full transition-all ${
                            bWins ? 'bg-amber-500' : 'bg-gray-300'
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

      {/* Interactive Player Search & Select Modal (Clean White Theme) */}
      {searchTargetSlot && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/50 backdrop-blur-sm animate-fadeIn">
          <div className="bg-white border-2 border-gray-900 rounded-2xl w-full max-w-xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden text-gray-900">
            {/* Modal Header */}
            <div className="p-4 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <div className="flex items-center gap-2">
                <Search className="w-4 h-4 text-purple-600" />
                <h3 className="text-sm font-bold text-gray-950 font-mono">
                  [ {searchTargetSlot === 'A' ? 'PLAYER A (기준)' : 'PLAYER B (대조)'} 선수 검색 및 선택 ]
                </h3>
              </div>
              <button
                onClick={() => setSearchTargetSlot(null)}
                className="p-1 rounded-lg hover:bg-gray-200 text-gray-500 hover:text-gray-900 transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Search Input & Position Filter */}
            <div className="p-3.5 border-b border-gray-200 bg-white flex flex-col gap-2.5">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="선수 이름 (손흥민, 살라, 홀란드, 음바페...), 클럽명, 리그 검색..."
                  autoFocus
                  className="w-full bg-gray-50 border border-gray-300 focus:border-purple-600 rounded-xl pl-9 pr-8 py-2 text-xs font-mono text-gray-900 placeholder-gray-400 focus:outline-none"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="absolute right-2.5 top-2.5 text-gray-400 hover:text-gray-700"
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
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-mono transition-all shrink-0 cursor-pointer border ${
                      posFilter === pos
                        ? 'bg-gray-900 text-white font-bold border-gray-900'
                        : 'bg-white text-gray-700 hover:bg-gray-100 border-gray-300'
                    }`}
                  >
                    {pos === "ALL" ? "전체" : pos}
                  </button>
                ))}
              </div>
            </div>

            {/* Search Results List */}
            <div className="p-3 overflow-y-auto max-h-96 space-y-1.5 divide-y divide-gray-100">
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
                      className={`pt-1.5 first:pt-0 p-2.5 rounded-xl transition-all cursor-pointer flex items-center justify-between gap-2 border ${
                        isCurrent
                          ? 'bg-purple-100/70 border-purple-400 text-gray-950 font-bold'
                          : 'hover:bg-gray-50 border-transparent text-gray-800'
                      }`}
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <span className="text-base shrink-0">{flag}</span>
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5 flex-wrap">
                            <span className="font-bold text-gray-950 text-xs sm:text-sm tracking-tight break-keep">
                              {player.korean_name || player.name}
                            </span>
                            {player.korean_name && (
                              <span className="text-gray-500 text-[11px] font-mono">
                                ({player.name})
                              </span>
                            )}
                            <span className="px-1.5 py-0.2 rounded bg-purple-100 text-purple-900 text-[10px] font-mono font-bold">
                              {player.primary_pos}
                            </span>
                          </div>
                          <div className="text-[11px] text-gray-500 font-mono mt-0.5 break-keep">
                            {player.club} • {player.league} • {player.age}세
                          </div>
                        </div>
                      </div>

                      <div className="text-right shrink-0">
                        <div className="text-xs font-bold font-mono text-purple-700">
                          €{player.market_value_eur}M
                        </div>
                        <div className="text-[10px] font-mono text-gray-400">
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
