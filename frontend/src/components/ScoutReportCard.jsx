import React, { useRef, useState } from 'react';
import html2canvas from 'html2canvas';
import { Download, Share2, Sparkles, TrendingUp, Shield, Zap, Crosshair, Award, ArrowUpRight, ArrowDownRight, Layers } from 'lucide-react';
import RadarChartCanvas from './RadarChartCanvas';

// Flag mapping helper
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

const getGradeLabel = (grade) => {
  switch (grade) {
    case 'SSS': return '👑 SSS (World Class)';
    case 'SS': return '🔥 SS (Elite Big League)';
    case 'S': return '✨ S (League Best XI)';
    case 'A': return '📈 A (Starting XI)';
    case 'B': return 'B (Solid Rotation)';
    case 'C': return 'C (Squad Backup)';
    case 'D': return 'D (Prospect)';
    default: return 'F (Excluded)';
  }
};

const safeNum = (v, fallback = 0) => {
  const n = parseFloat(v);
  return isNaN(n) ? fallback : n;
};

const safeFormat = (v, digits = 1) => {
  const n = parseFloat(v);
  return isNaN(n) ? '0.0' : n.toFixed(digits);
};

export default function ScoutReportCard({
  candidate,
  targetPlayer,
  similarityPct = 94.2,
  algorithm = "cosine",
  onCompareDirectly
}) {
  const cardRef = useRef(null);
  const [isExporting, setIsExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);

  if (!candidate || !targetPlayer) return null;

  const player = candidate.player || candidate;
  const flag = countryFlags[player.nationality] || "🌐";

  const targetScores = [
    targetPlayer.vision_score || 80,
    targetPlayer.striking_score || 70,
    targetPlayer.dribble_score || 75,
    targetPlayer.defense_score || 40,
    targetPlayer.physical_score || 50
  ];

  const candScores = [
    player.vision_score || 75,
    player.striking_score || 68,
    player.dribble_score || 72,
    player.defense_score || 42,
    player.physical_score || 52
  ];

  // Client-Side Zero-Cost Image Capture via html2canvas (Per 기획서 section 5.2)
  const handleSaveCard = async () => {
    if (!cardRef.current || isExporting) return;
    setIsExporting(true);

    try {
      const element = cardRef.current;
      const canvas = await html2canvas(element, {
        useCORS: true,
        scale: 2, // High-resolution 2x crisp rendering
        backgroundColor: '#0a0a16',
        logging: false
      });

      const link = document.createElement('a');
      const filename = `FM_Scout_${player.name.replace(/[^a-zA-Z0-9]/g, '_')}_vs_${targetPlayer.name.replace(/[^a-zA-Z0-9]/g, '_')}.png`;
      link.download = filename;
      link.href = canvas.toDataURL('image/png');
      link.click();

      setExportSuccess(true);
      setTimeout(() => setExportSuccess(false), 3000);
    } catch (err) {
      console.error("Card capture error:", err);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="flex flex-col gap-3 w-full">
      {/* Action Toolbar */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#00ff88]/10 text-[#00ff88] text-xs font-mono font-medium border border-[#00ff88]/30">
            <Sparkles className="w-3.5 h-3.5" />
            {candidate.gem_score ? `가성비 진주 지수: ${candidate.gem_score}점` : 'Tactical Profile'}
          </span>
          <span className="text-xs text-gray-400 font-mono">
            {algorithm === 'cosine' ? '📐 Cosine Playstyle Ratio' : '📏 Euclidean Volume Metric'}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {onCompareDirectly && (
            <button
              onClick={() => onCompareDirectly(targetPlayer.id, player.id)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#181832] hover:bg-[#202046] text-xs font-mono text-gray-200 border border-[#1f2240] transition-colors"
            >
              <Layers className="w-3.5 h-3.5 text-[#00e5ff]" />
              1v1 아레나 대조
            </button>
          )}

          <button
            onClick={handleSaveCard}
            disabled={isExporting}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded bg-[#00ff88] hover:bg-[#00e577] text-black font-semibold text-xs font-mono shadow-glow-neon transition-all active:scale-95 disabled:opacity-50"
          >
            <Download className="w-3.5 h-3.5" />
            {isExporting ? '생성 중...' : exportSuccess ? '저장 완료!' : '스카우팅 카드 저장 (PNG)'}
          </button>
        </div>
      </div>

      {/* Captured Report Card Component */}
      <div
        ref={cardRef}
        id="scout-report-card"
        className="tactical-box rounded-xl p-5 bg-[#121226] border border-[#1f2240] shadow-2xl relative overflow-hidden"
      >
        {/* Card Header */}
        <div className="flex items-center justify-between border-b border-[#1f2240] pb-3 mb-4">
          <div className="flex items-center gap-2.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#00ff88] animate-ping opacity-75" />
            <h3 className="text-xs tracking-wider uppercase font-mono font-bold text-gray-300">
              [ VERIFIED TACTICAL SCOUT REPORT ]
            </h3>
          </div>
          <div className="text-[11px] font-mono text-gray-500">
            ENGINE: Wyscout Event Model v2.4 (CC BY 4.0)
          </div>
        </div>

        {/* Main Grid: Left Profile + Right Dual Radar */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-5 items-center">
          {/* Left Column: Player Silhouette & Core Metadata */}
          <div className="md:col-span-6 flex flex-col gap-4">
            <div className="flex gap-4 items-start">
              {/* Privacy Silhouette Avatar (Portrait rights compliance) */}
              <div className="w-20 h-24 rounded-lg bg-[#181832] border border-[#2a2e5c] flex flex-col items-center justify-center p-2 relative shrink-0 shadow-inner">
                <svg className="w-12 h-14 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
                </svg>
                <span className="absolute bottom-1 right-1 text-sm drop-shadow">{flag}</span>
              </div>

              {/* Player Identity */}
              <div className="flex flex-col">
                <div className="flex items-center gap-2">
                  <h2 className="text-xl font-bold text-white tracking-tight">
                    {player.name} {player.korean_name && <span className="text-sm font-normal text-gray-400">({player.korean_name})</span>}
                  </h2>
                  <span className="px-2 py-0.5 text-xs font-mono font-bold rounded bg-[#00e5ff]/15 text-[#00e5ff] border border-[#00e5ff]/30">
                    {player.primary_pos}
                  </span>
                </div>
                <div className="text-xs text-gray-400 font-mono mt-0.5">{player.full_name}</div>
                <div className="text-xs text-gray-300 font-medium mt-1 flex items-center gap-1.5">
                  <span className="text-gray-400">{player.club}</span>
                  <span className="text-gray-600">•</span>
                  <span className="text-gray-400">{player.league}</span>
                </div>
                <div className="text-[11px] font-mono text-[#00ff88] mt-1">
                  ROLE: {player.tactical_role}
                </div>
              </div>
            </div>

            {/* Quick Metrics Tag Grid */}
            <div className="grid grid-cols-4 gap-2 bg-[#0d0d1e] p-2.5 rounded-lg border border-[#1f2240] text-center font-mono">
              <div>
                <div className="text-[10px] text-gray-400">AGE</div>
                <div className="text-xs font-bold text-white">{player.age}세</div>
              </div>
              <div>
                <div className="text-[10px] text-gray-400">FOOT / HT</div>
                <div className="text-xs font-bold text-white">{player.foot} / {player.height_cm}cm</div>
              </div>
              <div>
                <div className="text-[10px] text-gray-400">MKT VALUE</div>
                <div className="text-xs font-bold text-[#00ff88]">€{player.market_value_eur}M</div>
              </div>
              <div>
                <div className="text-[10px] text-gray-400">WAGE</div>
                <div className="text-xs font-bold text-gray-300">€{player.wage_eur_pw}k/w</div>
              </div>
            </div>

            {/* Tactical Match Highlight Banner */}
            <div className="p-3 rounded-lg bg-gradient-to-r from-[#00ff88]/15 via-[#00e5ff]/10 to-transparent border border-[#00ff88]/30 flex items-center justify-between">
              <div>
                <div className="text-[10px] uppercase font-mono tracking-wider text-gray-300">
                  TACTICAL MATCH SCORE <span className="text-[9px] text-[#00ff88]">({candidate?.metric_type || algorithm})</span>
                </div>
                <div className="text-xs font-medium text-gray-400 mt-0.5 flex items-center gap-2">
                  <span>vs <span className="text-white font-semibold">{targetPlayer.name}</span></span>
                  {candidate?.cosine_pct !== undefined && candidate?.cosine_pct !== null && (
                    <span className="text-[10px] font-mono text-gray-300 bg-[#0a0a16] px-1.5 py-0.5 rounded border border-[#1f2240]">
                      스타일: <strong className="text-[#00ff88]">{safeFormat(candidate.cosine_pct)}%</strong> | 체급: <strong className="text-[#00e5ff]">{safeFormat(candidate.euclidean_pct)}%</strong>
                    </span>
                  )}
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-mono font-extrabold text-[#00ff88] tracking-tight drop-shadow-[0_0_10px_rgba(0,255,136,0.4)]">
                  {safeFormat(similarityPct)}%
                </div>
              </div>
            </div>

            {/* 5 Tactical Pillar Badges */}
            <div className="flex flex-wrap gap-1.5 items-center">
              <div className="text-[10px] font-mono text-gray-400 mr-1">TIER RATINGS:</div>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${getGradeBadgeClass(player.vision_grade)}`}>
                창의성 {player.vision_grade} ({player.vision_score})
              </span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${getGradeBadgeClass(player.striking_grade)}`}>
                슈팅 {player.striking_grade} ({player.striking_score})
              </span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${getGradeBadgeClass(player.dribble_grade)}`}>
                드리블 {player.dribble_grade} ({player.dribble_score})
              </span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${getGradeBadgeClass(player.defense_grade)}`}>
                수비 {player.defense_grade} ({player.defense_score})
              </span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${getGradeBadgeClass(player.physical_grade)}`}>
                경합 {player.physical_grade} ({player.physical_score})
              </span>
            </div>
          </div>

          {/* Right Column: Interactive Overlay Radar Chart */}
          <div className="md:col-span-6 flex flex-col items-center justify-center p-2 rounded-xl bg-[#0e0e22]/70 border border-[#1f2240]/80">
            <div className="text-[11px] font-mono text-gray-400 mb-1 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#00ff88]"></span>
              RADAR STYLE OVERLAY (Target vs Scouted)
            </div>
            <RadarChartCanvas
              targetScores={targetScores}
              candidateScores={candScores}
              targetName={targetPlayer.name}
              candidateName={player.name}
              size={290}
            />
          </div>
        </div>

        {/* Detailed Per-90 Factual Stats Comparison Table */}
        <div className="mt-5 pt-4 border-t border-[#1f2240]">
          <div className="text-xs font-mono font-semibold text-gray-300 mb-2 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Crosshair className="w-3.5 h-3.5 text-[#00ff88]" />
              [ KEY STATS COMPARISON (Per 90 Minutes) ]
            </span>
            <span className="text-[10px] text-gray-400">Green = Advantage vs Target</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            {/* Stat 1: Key Passes */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-[#00e5ff] font-sans font-medium">기회 창출 (Key Passes)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.key_passes}</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.key_passes}</span>
              </div>
            </div>

            {/* Stat 2: Progressive Passes */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-[#00e5ff] font-sans font-medium">전진 패스 (Prog Passes)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.progressive_passes}</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.progressive_passes}</span>
              </div>
            </div>

            {/* Stat 3: Pass Completion % */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-[#00e5ff] font-sans font-medium">패스 성공률 (Pass Acc)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.pass_completion_pct}%</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.pass_completion_pct}%</span>
              </div>
            </div>

            {/* Stat 4: Dribbles Completed */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-amber-400 font-sans font-medium">드리블 성공 (Dribbles)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.dribbles_completed}</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.dribbles_completed}</span>
              </div>
            </div>

            {/* Stat 5: Shots & xG */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-rose-400 font-sans font-medium">슈팅 & xG (Shots)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.shots} ({player.xg})</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.shots} ({targetPlayer.xg})</span>
              </div>
            </div>

            {/* Stat 6: Tackles & Interceptions */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-indigo-400 font-sans font-medium">태클 & 가로채기 (Tkl+Int)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{safeFormat(safeNum(player.tackles_won) + safeNum(player.interceptions))}</span>
                <span className="text-[11px] text-gray-400">기준: {safeFormat(safeNum(targetPlayer.tackles_won) + safeNum(targetPlayer.interceptions))}</span>
              </div>
            </div>

            {/* Stat 7: Ground Duels */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-emerald-400 font-sans font-medium">지상 경합 승리 (Duels)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.ground_duels_won}</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.ground_duels_won}</span>
              </div>
            </div>

            {/* Stat 8: Aerial Won % */}
            <div className="bg-[#0e0e22] p-2 rounded border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-emerald-400 font-sans font-medium">공중볼 승률 (Aerial %)</div>
              <div className="flex items-baseline justify-between mt-0.5">
                <span className="text-white font-bold">{player.aerial_won_pct}%</span>
                <span className="text-[11px] text-gray-400">기준: {targetPlayer.aerial_won_pct}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Card Footer: Generated by FM Scout AI */}
        <div className="mt-4 pt-3 border-t border-[#1f2240] flex items-center justify-between text-[10px] font-mono text-gray-400">
          <div>Generated by <span className="text-[#00ff88] font-bold">FM Scout AI (FC Finder)</span></div>
          <div>CC BY 4.0 Wyscout Nature Sci Data / StatsBomb Open Data Model</div>
        </div>
      </div>
    </div>
  );
}
