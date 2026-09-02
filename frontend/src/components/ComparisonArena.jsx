import React, { useState, useEffect } from 'react';
import { Layers, ArrowLeftRight, User, Shield, Zap, Award, Sparkles, Check, ChevronRight } from 'lucide-react';
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
  "Georgia": "🇬🇪"
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

export default function ComparisonArena({
  players = [],
  initialPlayerAId,
  initialPlayerBId,
  onClose
}) {
  const [playerAId, setPlayerAId] = useState(initialPlayerAId || players[0]?.id || "p_odegaard");
  const [playerBId, setPlayerBId] = useState(initialPlayerBId || players[1]?.id || "p_stengs");
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);

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

  const radarScoresA = pA ? [pA.vision_score, pA.striking_score, pA.dribble_score, pA.defense_score, pA.physical_score] : [50,50,50,50,50];
  const radarScoresB = pB ? [pB.vision_score, pB.striking_score, pB.dribble_score, pB.defense_score, pB.physical_score] : [50,50,50,50,50];

  return (
    <div className="flex flex-col gap-5 p-5 rounded-xl bg-[#121226] border border-[#1f2240] shadow-2xl">
      {/* Arena Header */}
      <div className="flex items-center justify-between border-b border-[#1f2240] pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-[#00e5ff]/15 text-[#00e5ff] border border-[#00e5ff]/30">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white font-mono tracking-tight flex items-center gap-2">
              [ 1v1 TACTICAL HEAD-TO-HEAD ARENA ]
            </h2>
            <p className="text-xs text-gray-400 font-mono">두 선수의 전술 레이더 오버레이 및 세부 스탯 1:1 정밀 대조</p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="px-3 py-1.5 rounded-lg bg-[#1a1a38] hover:bg-[#222248] text-xs font-mono text-gray-300 border border-[#2a2e5c]"
        >
          스카우팅 리스트로 복귀 ✕
        </button>
      </div>

      {/* Selectors Bar */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Player A Selector */}
        <div className="p-3 rounded-lg bg-[#0a0a16] border border-[#2a2e5c]">
          <div className="text-[11px] font-mono text-gray-400 mb-1 flex items-center gap-1.5">
            <span className="w-2.5 h-0.5 border-t-2 border-dashed border-white inline-block"></span>
            PLAYER A (기준 / 화이트)
          </div>
          <select
            value={playerAId}
            onChange={(e) => setPlayerAId(e.target.value)}
            className="w-full bg-[#121226] text-white font-mono text-xs p-2 rounded border border-[#1f2240] focus:border-[#00ff88] focus:outline-none"
          >
            {players.map(p => (
              <option key={p.id} value={p.id}>
                {p.name} {p.korean_name ? `(${p.korean_name})` : ''} - {p.club} ({p.primary_pos}, €{p.market_value_eur}M)
              </option>
            ))}
          </select>
        </div>

        {/* Player B Selector */}
        <div className="p-3 rounded-lg bg-[#0a0a16] border border-[#2a2e5c]">
          <div className="text-[11px] font-mono text-[#00ff88] mb-1 flex items-center gap-1.5">
            <span className="w-2.5 h-2 bg-[#00ff88]/30 border border-[#00ff88] rounded-sm inline-block shadow-glow-neon"></span>
            PLAYER B (대조 / 네온그린)
          </div>
          <select
            value={playerBId}
            onChange={(e) => setPlayerBId(e.target.value)}
            className="w-full bg-[#121226] text-white font-mono text-xs p-2 rounded border border-[#1f2240] focus:border-[#00ff88] focus:outline-none"
          >
            {players.map(p => (
              <option key={p.id} value={p.id}>
                {p.name} {p.korean_name ? `(${p.korean_name})` : ''} - {p.club} ({p.primary_pos}, €{p.market_value_eur}M)
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Comparison Metrics Header Banner */}
      {comparisonData && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="p-3 rounded-lg bg-[#00ff88]/10 border border-[#00ff88]/30 flex items-center justify-between font-mono">
            <div>
              <div className="text-[10px] text-gray-400">COSINE SIMILARITY (플레이스타일 비율)</div>
              <div className="text-xs text-gray-300 font-medium">전술 행동 패턴 방향 일치도</div>
            </div>
            <div className="text-2xl font-bold text-[#00ff88]">
              {comparisonData.cosine_similarity}%
            </div>
          </div>

          <div className="p-3 rounded-lg bg-[#00e5ff]/10 border border-[#00e5ff]/30 flex items-center justify-between font-mono">
            <div>
              <div className="text-[10px] text-gray-400">EUCLIDEAN SIMILARITY (절대 볼륨)</div>
              <div className="text-xs text-gray-300 font-medium">물리적 스탯 거리: {comparisonData.euclidean_distance}</div>
            </div>
            <div className="text-2xl font-bold text-[#00e5ff]">
              {comparisonData.euclidean_similarity}%
            </div>
          </div>
        </div>
      )}

      {/* Main Grid: Radar Chart + Head to Head Stat Diff Table */}
      {pA && pB && (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5 items-start">
          {/* Left Column: Overlay Radar Chart */}
          <div className="md:col-span-5 flex flex-col items-center justify-center p-4 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
            <RadarChartCanvas
              targetScores={radarScoresA}
              candidateScores={radarScoresB}
              targetName={pA.name}
              candidateName={pB.name}
              size={300}
            />
          </div>

          {/* Right Column: Detailed Metric by Metric Comparison */}
          <div className="md:col-span-7 flex flex-col gap-3">
            {/* 5 Tactical Pillars Summary */}
            <div className="p-3 rounded-lg bg-[#0a0a16] border border-[#1f2240]">
              <div className="text-xs font-mono font-bold text-gray-300 mb-2">5대 핵심 전술 능력 지표 대조</div>
              <div className="space-y-2 font-mono text-xs">
                {comparisonData.radar_data.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-1.5 rounded bg-[#121226]">
                    <span className="w-28 text-gray-400">{item.metric}</span>
                    <div className="flex items-center gap-2">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] ${getGradeBadgeClass(item.gradeA)}`}>
                        {item.playerA} ({item.gradeA})
                      </span>
                      <span className="text-gray-500">vs</span>
                      <span className={`px-1.5 py-0.5 rounded text-[10px] ${getGradeBadgeClass(item.gradeB)}`}>
                        {item.playerB} ({item.gradeB})
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Per 90 Detailed Stats Table */}
            <div className="p-3 rounded-lg bg-[#0a0a16] border border-[#1f2240]">
              <div className="text-xs font-mono font-bold text-gray-300 mb-2">
                Per-90 경기당 사실 데이터 (Factual Stats)
              </div>
              <div className="max-h-64 overflow-y-auto space-y-1 pr-1 font-mono text-xs">
                {comparisonData.detailed_stats.map((stat, idx) => {
                  const valA = parseFloat(stat.a);
                  const valB = parseFloat(stat.b);
                  const aWins = valA > valB;
                  const bWins = valB > valA;
                  return (
                    <div key={idx} className="flex items-center justify-between p-1.5 rounded hover:bg-[#181832] transition-colors border-b border-[#1f2240]/40">
                      <span className="text-gray-400 text-[11px]">{stat.name}</span>
                      <div className="flex items-center gap-4 text-[11px]">
                        <span className={`font-bold ${aWins ? 'text-white underline decoration-white/40' : 'text-gray-400'}`}>
                          {valA}{stat.unit}
                        </span>
                        <span className="text-gray-600">|</span>
                        <span className={`font-bold ${bWins ? 'text-[#00ff88] underline decoration-[#00ff88]/40' : 'text-gray-400'}`}>
                          {valB}{stat.unit}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
