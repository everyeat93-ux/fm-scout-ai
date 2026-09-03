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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 px-1">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#00ff88]/10 text-[#00ff88] text-xs font-mono font-medium border border-[#00ff88]/30">
            <Sparkles className="w-3.5 h-3.5 text-yellow-400" />
            {candidate.gem_score ? `가성비 진주 지수: ${candidate.gem_score}점` : '전술 프로필'}
          </span>
          <span className="text-xs text-gray-400 font-mono hidden sm:inline">
            {algorithm === 'cosine' ? '📐 Cosine 전술 비율' : '📏 Euclidean 체급 볼륨'}
          </span>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {onCompareDirectly && (
            <button
              onClick={() => onCompareDirectly(targetPlayer.id, player.id)}
              className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3 py-1.5 rounded bg-[#181832] hover:bg-[#202046] text-xs font-mono text-gray-200 border border-[#1f2240] transition-colors cursor-pointer"
            >
              <Layers className="w-3.5 h-3.5 text-[#00e5ff]" />
              <span>1v1 비교 대조</span>
            </button>
          )}

          <button
            onClick={handleSaveCard}
            disabled={isExporting}
            className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded bg-[#00ff88] hover:bg-[#00e577] text-black font-bold text-xs font-mono shadow-glow-neon transition-all active:scale-95 disabled:opacity-50 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isExporting ? '생성 중...' : exportSuccess ? '저장 완료!' : '리포트 카드 저장 (PNG)'}</span>
          </button>
        </div>
      </div>

      {/* Captured Report Card Component */}
      <div
        ref={cardRef}
        id="scout-report-card"
        className="tactical-box rounded-xl p-3.5 sm:p-5 bg-[#121226] border border-[#1f2240] shadow-2xl relative overflow-hidden"
      >
        {/* Card Header */}
        <div className="flex items-center justify-between border-b border-[#1f2240] pb-2.5 mb-3.5">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-[#00ff88] animate-ping opacity-75 shrink-0" />
            <h3 className="text-xs tracking-wider uppercase font-mono font-bold text-gray-300">
              [ AI 전술 스카우팅 정밀 분석 리포트 ]
            </h3>
          </div>
          <div className="text-[10px] font-mono text-gray-500 hidden sm:block">
            ENGINE: Wyscout Event Model v2.4 (CC BY 4.0)
          </div>
        </div>

        {/* AI Tactical One-Liner Briefing Banner */}
        {candidate?.ai_briefing && (
          <div className="mb-4 p-3 rounded-xl bg-gradient-to-r from-[#00ff88]/15 via-[#00e5ff]/10 to-[#121226] border border-[#00ff88]/30 flex items-start gap-2.5 shadow-md">
            <Sparkles className="w-4 h-4 text-[#00ff88] mt-0.5 shrink-0 animate-pulse" />
            <div className="min-w-0">
              <div className="text-[10px] font-mono font-bold text-[#00ff88] uppercase tracking-wider flex items-center gap-1.5">
                <span>AI SCOUT TACTICAL BRIEFING</span>
                <span className="px-1.5 py-0.2 rounded bg-[#00ff88]/20 text-[#00ff88] text-[9px]">실시간 전술 총평</span>
              </div>
              <div className="text-xs sm:text-sm text-gray-200 mt-1 font-sans leading-relaxed break-keep">
                {candidate.ai_briefing}
              </div>
            </div>
          </div>
        )}

        {/* Main Grid: Left Profile + Right Dual Radar */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4 sm:gap-5 items-center">
          {/* Left Column: Player Silhouette & Core Metadata */}
          <div className="md:col-span-6 flex flex-col gap-3 sm:gap-4">
            <div className="flex gap-3 sm:gap-4 items-start">
              {/* Privacy Silhouette Avatar */}
              <div className="w-16 h-20 sm:w-20 sm:h-24 rounded-lg bg-[#181832] border border-[#2a2e5c] flex flex-col items-center justify-center p-2 relative shrink-0 shadow-inner">
                <svg className="w-10 h-12 sm:w-12 sm:h-14 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
                </svg>
                <span className="absolute bottom-1 right-1 text-xs sm:text-sm drop-shadow">{flag}</span>
              </div>

              {/* Player Identity */}
              <div className="flex flex-col min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <h2 className="text-lg sm:text-xl font-bold text-white tracking-tight break-keep">
                    {player.name}
                  </h2>
                  {player.korean_name && (
                    <span className="text-xs sm:text-sm font-medium text-[#00ff88] break-keep">
                      ({player.korean_name})
                    </span>
                  )}
                  <span className="px-1.5 py-0.2 text-[10px] sm:text-xs font-mono font-bold rounded bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/30 shrink-0">
                    {player.primary_pos}
                  </span>
                </div>
                <div className="text-[11px] text-gray-400 font-mono mt-0.5 truncate">{player.full_name}</div>
                <div className="text-xs text-gray-300 font-medium mt-1 flex items-center gap-1.5 flex-wrap break-keep">
                  <span className="text-gray-300">{player.club}</span>
                  <span className="text-gray-600">•</span>
                  <span className="text-gray-400">{player.league}</span>
                </div>
                <div className="text-[11px] font-mono text-[#00ff88] mt-1 break-keep">
                  ROLE: {player.tactical_role}
                </div>
              </div>
            </div>

            {/* Quick Metrics 4-Box Grid (2x2 on Mobile, 4x1 on Desktop) */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-[#0d0d1e] p-2.5 rounded-lg border border-[#1f2240] text-center font-mono">
              <div className="p-1">
                <div className="text-[10px] text-gray-400 font-sans">나이 (AGE)</div>
                <div className="text-xs sm:text-sm font-bold text-white mt-0.5">{player.age}세</div>
              </div>
              <div className="p-1">
                <div className="text-[10px] text-gray-400 font-sans">주발 / 신장</div>
                <div className="text-xs sm:text-sm font-bold text-white mt-0.5">{player.foot} / {player.height_cm}cm</div>
              </div>
              <div className="p-1">
                <div className="text-[10px] text-gray-400 font-sans">시장 가치</div>
                <div className="text-xs sm:text-sm font-bold text-[#00ff88] mt-0.5">€{player.market_value_eur}M</div>
              </div>
              <div className="p-1">
                <div className="text-[10px] text-gray-400 font-sans">추정 주급</div>
                <div className="text-xs sm:text-sm font-bold text-gray-300 mt-0.5">€{player.wage_eur_pw}k/w</div>
              </div>
            </div>

            {/* Tactical Match Highlight Banner */}
            <div className="p-3 rounded-lg bg-gradient-to-r from-[#00ff88]/15 via-[#00e5ff]/10 to-transparent border border-[#00ff88]/30 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <div className="text-[10px] uppercase font-mono tracking-wider text-gray-300">
                  전술 일치도 (TACTICAL MATCH)
                </div>
                <div className="text-xs text-gray-300 mt-0.5 flex items-center gap-1.5 flex-wrap break-keep">
                  <span>vs <strong className="text-white">{targetPlayer.korean_name || targetPlayer.name}</strong></span>
                  {candidate?.cosine_pct !== undefined && candidate?.cosine_pct !== null && (
                    <span className="text-[10px] font-mono text-gray-300 bg-[#0a0a16] px-1.5 py-0.5 rounded border border-[#1f2240]">
                      스타일: <strong className="text-[#00ff88]">{safeFormat(candidate.cosine_pct)}%</strong> | 체급: <strong className="text-[#00e5ff]">{safeFormat(candidate.euclidean_pct)}%</strong>
                    </span>
                  )}
                </div>
              </div>
              <div className="sm:text-right">
                <div className="text-2xl font-mono font-extrabold text-[#00ff88] tracking-tight drop-shadow-[0_0_10px_rgba(0,255,136,0.4)]">
                  {safeFormat(similarityPct)}%
                </div>
              </div>
            </div>

            {/* 5 Tactical Pillar Badges */}
            <div className="flex flex-wrap gap-1.5 items-center">
              <div className="text-[10px] font-mono text-gray-400 mr-1 shrink-0 font-bold">능력치:</div>
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
          <div className="md:col-span-6 flex flex-col items-center justify-center p-2 sm:p-3 rounded-xl bg-[#0e0e22]/80 border border-[#1f2240]">
            <div className="text-[11px] font-mono text-gray-400 mb-1 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#00ff88]"></span>
              전술 레이더 대조 (Target vs Scouted)
            </div>
            <RadarChartCanvas
              targetScores={targetScores}
              candidateScores={candScores}
              targetName={targetPlayer.korean_name || targetPlayer.name}
              candidateName={player.korean_name || player.name}
              size={260}
            />
          </div>
        </div>

        {/* Detailed Per-90 Factual Stats Comparison Table */}
        <div className="mt-4 pt-3.5 border-t border-[#1f2240]">
          <div className="text-xs font-mono font-semibold text-gray-300 mb-2.5 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Crosshair className="w-3.5 h-3.5 text-[#00ff88]" />
              [ 90분당 핵심 전술 스탯 직접 대조 ]
            </span>
            <span className="text-[10px] text-gray-400 hidden sm:inline">9대 영역 Wyscout 데이터 기반</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {/* Stat 1: Key Passes */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-[#00e5ff] font-sans font-semibold">기회 창출 (Key Passes)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.key_passes}</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.key_passes}</span>
              </div>
            </div>

            {/* Stat 2: Progressive Passes */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-[#00e5ff] font-sans font-semibold">전진 패스 (Prog Passes)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.progressive_passes}</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.progressive_passes}</span>
              </div>
            </div>

            {/* Stat 3: Pass Completion % */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-[#00e5ff] font-sans font-semibold">패스 성공률 (Pass Acc)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.pass_completion_pct}%</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.pass_completion_pct}%</span>
              </div>
            </div>

            {/* Stat 4: Dribbles Completed */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-amber-400 font-sans font-semibold">드리블 성공 (Dribbles)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.dribbles_completed}</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.dribbles_completed}</span>
              </div>
            </div>

            {/* Stat 5: Shots & xG */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-rose-400 font-sans font-semibold">슈팅 & xG (Shots)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.shots} <span className="text-[10px] text-rose-300">({player.xg})</span></span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.shots}</span>
              </div>
            </div>

            {/* Stat 6: Tackles & Interceptions */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-indigo-400 font-sans font-semibold">태클+가로채기 (Tkl+Int)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{safeFormat(safeNum(player.tackles_won) + safeNum(player.interceptions))}</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {safeFormat(safeNum(targetPlayer.tackles_won) + safeNum(targetPlayer.interceptions))}</span>
              </div>
            </div>

            {/* Stat 7: Ground Duels */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-emerald-400 font-sans font-semibold">지상 경합 승리 (Duels)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.ground_duels_won}</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.ground_duels_won}</span>
              </div>
            </div>

            {/* Stat 8: Aerial Won % */}
            <div className="bg-[#0e0e22] p-2 sm:p-2.5 rounded-lg border border-[#1f2240] font-mono text-xs">
              <div className="text-[10px] text-emerald-400 font-sans font-semibold">공중볼 승률 (Aerial %)</div>
              <div className="flex items-baseline justify-between mt-1">
                <span className="text-white font-bold text-xs sm:text-sm">{player.aerial_won_pct}%</span>
                <span className="text-[10px] sm:text-[11px] text-gray-400">기준 {targetPlayer.aerial_won_pct}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Card Footer: Generated by FM Scout AI */}
        <div className="mt-3.5 pt-2.5 border-t border-[#1f2240] flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-[10px] font-mono text-gray-400">
          <div>Generated by <span className="text-[#00ff88] font-bold">FM Scout AI (FC Finder)</span></div>
          <div>CC BY 4.0 Wyscout Nature Sci Data / StatsBomb Open Data Model</div>
        </div>
      </div>
    </div>
  );
}
