import React, { useRef, useState } from 'react';
import html2canvas from 'html2canvas';
import { 
  Download, Sparkles, Trophy, Star, Shield, Award, 
  Layers, ChevronDown, ChevronUp, Crosshair, ArrowRight
} from 'lucide-react';
import RadarChartCanvas from './RadarChartCanvas';
import PitchZoneMap from './PitchZoneMap';

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
  "Greece": "🇬🇷"
};

const getClubTheme = (clubName = "") => {
  const c = clubName.toLowerCase();
  if (c.includes("paris") || c.includes("psg")) return { bg: "#004170", text: "#ffffff", accent: "#da291c", name: "PSG" };
  if (c.includes("sporting")) return { bg: "#008057", text: "#ffffff", accent: "#ffffff", name: "Sporting CP" };
  if (c.includes("tottenham")) return { bg: "#132257", text: "#ffffff", accent: "#ffffff", name: "Tottenham" };
  if (c.includes("real madrid")) return { bg: "#0c2340", text: "#f59e0b", accent: "#eeeee4", name: "Real Madrid" };
  if (c.includes("manchester city")) return { bg: "#6cabdd", text: "#1c2c5b", accent: "#ffffff", name: "Man City" };
  if (c.includes("arsenal")) return { bg: "#ef0107", text: "#ffffff", accent: "#063672", name: "Arsenal" };
  if (c.includes("bayern") || c.includes("munich")) return { bg: "#dc052d", text: "#ffffff", accent: "#0066b2", name: "Bayern" };
  if (c.includes("liverpool")) return { bg: "#c8102e", text: "#fcd34d", accent: "#00b2a9", name: "Liverpool" };
  if (c.includes("barcelona")) return { bg: "#004d98", text: "#edbb00", accent: "#a50044", name: "Barcelona" };
  if (c.includes("chelsea")) return { bg: "#034694", text: "#ffffff", accent: "#dba111", name: "Chelsea" };
  if (c.includes("dortmund")) return { bg: "#fde100", text: "#000000", accent: "#000000", name: "Dortmund" };
  return { bg: "#1e293b", text: "#f59e0b", accent: "#ffffff", name: clubName || "Pro Club" };
};

const getPlayerNumber = (player) => {
  if (player.shirt_number) return player.shirt_number;
  if (player.number) return player.number;
  const name = (player.name || "").toLowerCase();
  if (name.includes("son") || name.includes("손흥민")) return 7;
  if (name.includes("lee kang") || name.includes("이강인") || name.includes("k. i. lee")) return 19;
  if (name.includes("haaland") || name.includes("홀란드")) return 9;
  if (name.includes("salah") || name.includes("살라")) return 11;
  if (name.includes("mbappe") || name.includes("음바페")) return 9;
  if (name.includes("kim min") || name.includes("김민재")) return 3;
  if (name.includes("messi") || name.includes("메시")) return 10;
  if (name.includes("ronaldo") || name.includes("호날두")) return 7;
  if (name.includes("musiala")) return 42;
  if (name.includes("wirtz")) return 10;

  if (player.primary_pos?.includes("ST") || player.primary_pos?.includes("CF")) return 9;
  if (player.primary_pos?.includes("LW") || player.primary_pos?.includes("LM")) return 7;
  if (player.primary_pos?.includes("RW") || player.primary_pos?.includes("RM")) return 11;
  if (player.primary_pos?.includes("CAM") || player.primary_pos?.includes("AM")) return 10;
  if (player.primary_pos?.includes("CM")) return 8;
  if (player.primary_pos?.includes("CDM") || player.primary_pos?.includes("DM")) return 6;
  if (player.primary_pos?.includes("CB")) return 4;
  if (player.primary_pos?.includes("LB")) return 3;
  if (player.primary_pos?.includes("RB")) return 2;
  return 10;
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
  onCompareDirectly,
  isBookmarked = false,
  onToggleBookmark
}) {
  const cardRef = useRef(null);
  const [isExporting, setIsExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);
  const [showDetailedStats, setShowDetailedStats] = useState(false);

  if (!candidate || !targetPlayer) return null;

  const player = candidate.player || candidate;
  const flag = countryFlags[player.nationality] || "🌐";
  const clubTheme = getClubTheme(player.club);
  const playerNum = getPlayerNumber(player);

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

  // Capture Card in High-Resolution Image
  const handleSaveCard = async () => {
    if (!cardRef.current || isExporting) return;
    setIsExporting(true);

    try {
      const element = cardRef.current;
      const canvas = await html2canvas(element, {
        useCORS: true,
        scale: 2,
        backgroundColor: '#ffffff',
        logging: false
      });

      const link = document.createElement('a');
      const filename = `FM_ScoutCard_${player.name.replace(/[^a-zA-Z0-9]/g, '_')}.png`;
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
      {/* Top Action Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 px-1">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-50 text-emerald-800 text-xs font-mono font-bold border border-emerald-200 shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            {candidate.gem_score ? `가성비 진주 지수: ${candidate.gem_score}점` : '정밀 스카우팅 인포그래픽 카드'}
          </span>
          <span className="text-xs text-gray-500 font-mono hidden sm:inline">
            {algorithm === 'cosine' ? '📐 Cosine 전술 비율' : '📏 Euclidean 체급 볼륨'}
          </span>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {onToggleBookmark && (
            <button
              onClick={() => onToggleBookmark(player.id)}
              className={`flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold border transition-all cursor-pointer shadow-xs ${
                isBookmarked ? 'bg-amber-100 border-amber-400 text-amber-900' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Star className={`w-3.5 h-3.5 ${isBookmarked ? 'fill-amber-500 text-amber-500' : ''}`} />
              <span>{isBookmarked ? '찜 완료' : '관심 찜'}</span>
            </button>
          )}

          {onCompareDirectly && (
            <button
              onClick={() => onCompareDirectly(targetPlayer.id, player.id)}
              className="flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-gray-50 text-xs font-mono font-bold text-gray-800 border border-gray-300 transition-colors cursor-pointer shadow-xs"
            >
              <Layers className="w-3.5 h-3.5 text-purple-600" />
              <span>1v1 비교</span>
            </button>
          )}

          <button
            onClick={handleSaveCard}
            disabled={isExporting}
            className="flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-gray-900 hover:bg-gray-800 text-white font-bold text-xs font-mono shadow-sm transition-all active:scale-95 disabled:opacity-50 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            <span>{isExporting ? '생성 중...' : exportSuccess ? '저장 완료!' : '카드 이미지 저장 (PNG)'}</span>
          </button>
        </div>
      </div>

      {/* 
        PREMIUM RE-LAB INFOGRAPHIC CARD
        Clean Off-White Base, High Contrast Typography, Ultra-Crisp Grid System
      */}
      <div
        ref={cardRef}
        id="scout-report-card"
        style={{
          backgroundColor: '#ffffff',
          color: '#0f172a'
        }}
        className="rounded-2xl border-2 border-gray-900 p-3 sm:p-5 shadow-[0_12px_28px_rgba(0,0,0,0.15)] relative select-none w-full max-w-2xl mx-auto overflow-hidden bg-white"
      >
        {/* ========================================================
            1. TOP HEADER: [Position Badge] | [Names] | [Shirt Number]
            ======================================================== */}
        <div className="flex items-center justify-between border-b-2 border-gray-900 pb-2.5 mb-2.5">
          {/* Left: Solid Position Box (Re-lab 'F' Style) */}
          <div className="w-11 h-11 bg-white border-2 border-gray-900 rounded flex flex-col items-center justify-center shadow-[2px_2px_0px_#000000] shrink-0">
            <span className="text-xl font-black font-sans leading-none text-gray-950">
              {player.primary_pos || 'AM'}
            </span>
            <span className="text-[9px] font-bold text-gray-500 mt-0.5">{flag}</span>
          </div>

          {/* Center: Dual-Language Names & Club */}
          <div className="flex flex-col items-center justify-center text-center px-2 flex-1 min-w-0">
            <div className="text-[11px] font-bold text-gray-500 tracking-wider truncate max-w-full font-sans">
              {player.korean_name ? `${player.korean_name} (${player.name})` : player.name} • {player.club}
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-gray-950 tracking-tight font-sans truncate max-w-full">
              {player.name}
            </h1>
          </div>

          {/* Right: Team Color Shirt Number Box (Re-lab '30' Style) */}
          <div
            className="w-11 h-11 border-2 border-gray-900 rounded flex items-center justify-center shadow-[2px_2px_0px_#000000] shrink-0"
            style={{ backgroundColor: clubTheme.bg, color: clubTheme.text }}
          >
            <span className="text-2xl font-black font-sans leading-none">
              {playerNum}
            </span>
          </div>
        </div>

        {/* ========================================================
            2. STARS & TIER RATING
            ======================================================== */}
        <div className="flex items-center justify-center gap-1 mb-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <span key={i} className="text-base leading-none text-amber-400 fill-amber-400 drop-shadow-xs">
              ★
            </span>
          ))}
          <span className="text-[10px] font-mono font-bold text-gray-500 ml-1">
            —— {player.tier_grade || 'S'}-TIER SCOUT
          </span>
        </div>

        {/* ========================================================
            3. CENTER SHOWCASE: [Badges] | [Player Kit Graphic] | [Trophies]
            ======================================================== */}
        <div className="grid grid-cols-12 gap-2 items-center mb-2.5 px-1">
          {/* Left Column: Re-lab Style Season Badges */}
          <div className="col-span-3 flex flex-col gap-1.5 z-10">
            <div className="border border-gray-900 bg-white rounded shadow-[1.5px_1.5px_0px_#000000] text-center overflow-hidden">
              <div className="bg-gray-100 text-[8px] font-mono font-bold text-gray-700 py-0.5 border-b border-gray-300">
                2024-25
              </div>
              <div className="text-[10px] font-black text-gray-950 py-1 px-0.5 truncate font-sans">
                LIGA BEST XI
              </div>
            </div>

            <div className="border border-gray-900 bg-white rounded shadow-[1.5px_1.5px_0px_#000000] text-center overflow-hidden">
              <div className="bg-gray-100 text-[8px] font-mono font-bold text-gray-700 py-0.5 border-b border-gray-300">
                TACTICAL
              </div>
              <div className="text-[9px] font-black text-purple-900 py-1 px-0.5 truncate font-sans">
                {player.tactical_role || '찬스 메이커'}
              </div>
            </div>

            <div className="border border-gray-900 bg-white rounded shadow-[1.5px_1.5px_0px_#000000] text-center overflow-hidden">
              <div className="bg-gray-100 text-[8px] font-mono font-bold text-gray-700 py-0.5 border-b border-gray-300">
                PHYSICAL
              </div>
              <div className="text-[10px] font-black text-gray-950 py-1 px-0.5 truncate font-sans">
                {player.foot || 'Left'} • {player.height_cm}cm
              </div>
            </div>
          </div>

          {/* Center Column: High-Quality Vector Football Jersey Shield */}
          <div className="col-span-6 flex flex-col items-center justify-center relative">
            <div className="relative w-36 sm:w-40 h-36 sm:h-40 flex items-center justify-center">
              <svg viewBox="0 0 160 160" className="w-full h-full drop-shadow-sm">
                <defs>
                  <radialGradient id="shieldGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stopColor="#f8fafc" />
                    <stop offset="100%" stopColor="#e2e8f0" />
                  </radialGradient>
                  <linearGradient id="kitGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor={clubTheme.bg} />
                    <stop offset="100%" stopColor="#0f172a" />
                  </linearGradient>
                </defs>

                {/* Outer Shield Frame */}
                <path
                  d="M 80 8 L 142 26 L 136 112 C 136 138 80 154 80 154 C 80 154 24 138 24 112 L 18 26 Z"
                  fill="url(#shieldGlow)"
                  stroke="#0f172a"
                  strokeWidth="2.5"
                />

                {/* Inner Decorative Dashed Line */}
                <path
                  d="M 80 14 L 136 30 L 130 108 C 130 130 80 145 80 145 C 80 145 30 130 30 108 L 24 30 Z"
                  fill="none"
                  stroke="#94a3b8"
                  strokeWidth="1"
                  strokeDasharray="3,2"
                />

                {/* Pro Football Jersey */}
                {/* Collar */}
                <path d="M 68 38 L 80 50 L 92 38 Z" fill="#ffffff" stroke="#0f172a" strokeWidth="1.5" />

                {/* Jersey Torso */}
                <path
                  d="M 52 38 L 68 38 L 80 50 L 92 38 L 108 38 L 114 96 L 46 96 Z"
                  fill="url(#kitGrad)"
                  stroke="#0f172a"
                  strokeWidth="1.8"
                />

                {/* Sleeves */}
                <path d="M 52 38 L 36 62 L 46 68 L 56 48 Z" fill={clubTheme.bg} stroke="#0f172a" strokeWidth="1.5" />
                <path d="M 108 38 L 124 62 L 114 68 L 104 48 Z" fill={clubTheme.bg} stroke="#0f172a" strokeWidth="1.5" />

                {/* Kit Stripes */}
                <line x1="72" y1="50" x2="70" y2="96" stroke="#ffffff" strokeWidth="2.5" opacity="0.3" />
                <line x1="88" y1="50" x2="90" y2="96" stroke="#ffffff" strokeWidth="2.5" opacity="0.3" />

                {/* Shirt Number */}
                <text
                  x="80"
                  y="78"
                  textAnchor="middle"
                  fontSize="24"
                  fontWeight="900"
                  fontFamily="sans-serif"
                  fill={clubTheme.text}
                  stroke="#000000"
                  strokeWidth="0.6"
                >
                  {playerNum}
                </text>

                {/* Player Name Tag on Jersey */}
                <text
                  x="80"
                  y="90"
                  textAnchor="middle"
                  fontSize="7"
                  fontWeight="800"
                  fontFamily="sans-serif"
                  fill={clubTheme.text}
                  letterSpacing="0.8"
                >
                  {player.name.toUpperCase()}
                </text>

                {/* Football Ball Icon at Base */}
                <g transform="translate(68, 110)">
                  <circle cx="12" cy="12" r="10" fill="#ffffff" stroke="#0f172a" strokeWidth="1.5" />
                  <polygon points="12,6 15,9 14,13 10,13 9,9" fill="#0f172a" />
                  <line x1="12" y1="6" x2="12" y2="2" stroke="#0f172a" strokeWidth="1" />
                  <line x1="15" y1="9" x2="19" y2="7" stroke="#0f172a" strokeWidth="1" />
                  <line x1="14" y1="13" x2="18" y2="16" stroke="#0f172a" strokeWidth="1" />
                  <line x1="10" y1="13" x2="6" y2="16" stroke="#0f172a" strokeWidth="1" />
                  <line x1="9" y1="9" x2="5" y2="7" stroke="#0f172a" strokeWidth="1" />
                </g>
              </svg>
            </div>
          </div>

          {/* Right Column: Re-lab Trophies & Tactical Match Stamp */}
          <div className="col-span-3 flex flex-col items-center gap-1.5 z-10">
            {/* Dual Trophies (Golden Boot + Ballon d'Or) */}
            <div className="flex items-center justify-center gap-1 w-full">
              <div className="flex flex-col items-center">
                <div className="w-8 h-9 border border-gray-900 bg-amber-50 rounded flex items-center justify-center shadow-[1px_1px_0px_#000000]">
                  <Trophy className="w-4 h-4 text-amber-500 fill-amber-400" />
                </div>
                <span className="text-[7px] font-mono font-bold text-gray-500 mt-0.5">2023-24</span>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-8 h-9 border border-gray-900 bg-amber-50 rounded flex items-center justify-center shadow-[1px_1px_0px_#000000]">
                  <Award className="w-4 h-4 text-amber-500 fill-amber-400" />
                </div>
                <span className="text-[7px] font-mono font-bold text-gray-500 mt-0.5">2022-23</span>
              </div>
            </div>

            {/* Tactical Match Stamp Seal */}
            <div className="w-full border-2 border-rose-800 bg-rose-50 rounded-lg p-1.5 text-center shadow-[1px_1px_0px_#991b1b]">
              <div className="text-[8px] font-mono font-black text-rose-800 uppercase tracking-tighter">
                전술 매칭률
              </div>
              <div className="text-base sm:text-lg font-black font-mono text-rose-700 leading-none mt-0.5">
                {safeFormat(similarityPct)}%
              </div>
              <div className="text-[7px] font-mono text-gray-600 truncate mt-0.5">
                vs {targetPlayer.name}
              </div>
            </div>
          </div>
        </div>

        {/* ========================================================
            4. HORIZONTAL SOLID DIVIDER
            ======================================================== */}
        <div className="border-t-2 border-gray-900 my-2"></div>

        {/* ========================================================
            5. BOTTOM 3-COLUMN DATA MODULE (FIXED 3 COLUMNS)
            Directly replicates the iconic Re-lab 3-Box Layout:
            [Basic Profile] | [Radar Chart] | [Attack Zone]
            ======================================================== */}
        <div className="grid grid-cols-3 gap-1.5 sm:gap-3 items-center w-full overflow-hidden">
          {/* Column 1: Basic Profile (基本資料) */}
          <div className="col-span-1 flex flex-col justify-center border-r-2 border-gray-900 pr-1.5 sm:pr-2 min-w-0">
            <div className="text-[9px] sm:text-[10px] font-bold text-gray-800 uppercase tracking-wider mb-1 border-b border-gray-300 pb-0.5 truncate">
              기본자료 [基本資料]
            </div>

            <div className="space-y-0.5 sm:space-y-1 font-sans text-[9px] sm:text-[10px]">
              {/* Age */}
              <div className="flex items-baseline justify-between border-b border-gray-200 pb-0.5">
                <span className="text-gray-500 font-bold">연령</span>
                <div className="flex items-baseline gap-0.5">
                  <span className="text-xs sm:text-base font-black text-gray-950 font-mono">{player.age}</span>
                  <span className="text-[7px] sm:text-[8px] text-gray-500 font-bold">yrs</span>
                </div>
              </div>

              {/* Weight */}
              <div className="flex items-baseline justify-between border-b border-gray-200 pb-0.5">
                <span className="text-gray-500 font-bold">체중</span>
                <div className="flex items-baseline gap-0.5">
                  <span className="text-xs sm:text-base font-black text-gray-950 font-mono">{player.weight_kg || '78'}</span>
                  <span className="text-[7px] sm:text-[8px] text-gray-500 font-bold">kg</span>
                </div>
              </div>

              {/* Height */}
              <div className="flex items-baseline justify-between border-b border-gray-200 pb-0.5">
                <span className="text-gray-500 font-bold">신장</span>
                <div className="flex items-baseline gap-0.5">
                  <span className="text-xs sm:text-base font-black text-gray-950 font-mono">{player.height_cm}</span>
                  <span className="text-[7px] sm:text-[8px] text-gray-500 font-bold">cm</span>
                </div>
              </div>

              {/* Market Value */}
              <div className="flex items-baseline justify-between">
                <span className="text-gray-500 font-bold">가치</span>
                <div className="flex items-baseline gap-0.5">
                  <span className="text-xs sm:text-base font-black text-emerald-700 font-mono">€{player.market_value_eur}</span>
                  <span className="text-[7px] sm:text-[8px] text-emerald-700 font-bold">M</span>
                </div>
              </div>
            </div>
          </div>

          {/* Column 2: Dual Tactical Radar (전술 대조) */}
          <div className="col-span-1 flex flex-col items-center justify-center px-0.5 border-r-2 border-gray-900 pr-1.5 sm:pr-2 min-w-0">
            <RadarChartCanvas
              targetScores={targetScores}
              candidateScores={candScores}
              targetName={targetPlayer.name}
              candidateName={player.name}
              size={150}
            />
          </div>

          {/* Column 3: Mini Pitch Attack Zone (주요 공격 구역) */}
          <div className="col-span-1 flex flex-col items-center justify-center min-w-0">
            <PitchZoneMap position={player.primary_pos} role={player.tactical_role} />
          </div>
        </div>

        {/* ========================================================
            6. RE-LAB BRANDING FOOTER & EXPANDABLE DRAWER
            ======================================================== */}
        <div className="mt-2.5 pt-1.5 border-t-2 border-gray-900 flex items-center justify-between text-[9px] font-mono text-gray-600">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full border border-gray-900 bg-red-600 flex items-center justify-center text-white font-black text-[6px]">
              ⚯
            </div>
            <span className="font-black text-gray-900 tracking-wider">FootScout AI</span>
            <span className="text-gray-400 hidden sm:inline">| Authentic Card</span>
          </div>

          <button
            onClick={() => setShowDetailedStats(!showDetailedStats)}
            className="flex items-center gap-1 text-[9px] font-bold text-gray-700 hover:text-black cursor-pointer bg-gray-100 hover:bg-gray-200 px-2 py-0.5 rounded border border-gray-300 transition-colors"
          >
            <span>상세 전술 스탯 {showDetailedStats ? '접기 ▲' : '펼치기 ▼'}</span>
          </button>

          <div className="text-gray-500 font-medium hidden sm:block">
            Wyscout Event Model
          </div>
        </div>

        {/* ========================================================
            7. EXPANDABLE ADVANCED STATS DRAWER (Clean Editorial Box)
            ======================================================== */}
        {showDetailedStats && (
          <div className="mt-2.5 pt-2.5 border-t border-gray-300 space-y-2.5 font-sans">
            {/* AI Tactical One-Liner */}
            {candidate?.ai_briefing && (
              <div className="p-2.5 rounded-lg bg-amber-50 border border-amber-300 text-xs text-gray-900 leading-relaxed font-medium">
                <span className="font-bold text-amber-900 mr-1.5">[AI 총평]</span>
                {candidate.ai_briefing}
              </div>
            )}

            {/* 5 Master Managers Tactical Fit */}
            {candidate?.manager_fit && (
              <div className="bg-gray-50 p-2 rounded-lg border border-gray-300">
                <div className="text-[10px] font-bold text-gray-700 mb-1 flex items-center justify-between">
                  <span>세계 5대 명장 감독 전술 시스템 적합도</span>
                  {candidate.manager_fit.best_fit && (
                    <span className="text-amber-800 font-black">
                      👑 {candidate.manager_fit.best_fit.name} 최적합 ({candidate.manager_fit.best_fit.score}점)
                    </span>
                  )}
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-1 text-center font-mono">
                  {candidate.manager_fit.managers.map((mgr) => {
                    const isBest = candidate.manager_fit.best_fit?.id === mgr.id;
                    return (
                      <div
                        key={mgr.id}
                        className={`p-1 rounded border text-xs ${
                          isBest ? 'bg-amber-100 border-amber-400 font-black text-amber-950' : 'bg-white border-gray-200 text-gray-800'
                        }`}
                      >
                        <div className="text-[9px] truncate font-sans text-gray-600">{mgr.name}</div>
                        <div className="text-xs font-bold mt-0.5">{mgr.score}점</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Per-90 Factual Stats Grid */}
            <div className="bg-gray-50 p-2 rounded-lg border border-gray-300">
              <div className="text-[10px] font-bold text-gray-700 mb-1">
                90분당 핵심 스탯 대조 (후보 vs {targetPlayer.name})
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-1.5 text-xs font-mono">
                <div className="bg-white p-1.5 rounded border border-gray-200 flex justify-between items-center">
                  <span className="text-[9px] text-gray-500 font-sans">기회 창출</span>
                  <span className="font-bold text-gray-900">{player.key_passes} <span className="text-[9px] text-gray-400">({targetPlayer.key_passes})</span></span>
                </div>
                <div className="bg-white p-1.5 rounded border border-gray-200 flex justify-between items-center">
                  <span className="text-[9px] text-gray-500 font-sans">전진 패스</span>
                  <span className="font-bold text-gray-900">{player.progressive_passes} <span className="text-[9px] text-gray-400">({targetPlayer.progressive_passes})</span></span>
                </div>
                <div className="bg-white p-1.5 rounded border border-gray-200 flex justify-between items-center">
                  <span className="text-[9px] text-gray-500 font-sans">패스 성공률</span>
                  <span className="font-bold text-gray-900">{player.pass_completion_pct}% <span className="text-[9px] text-gray-400">({targetPlayer.pass_completion_pct}%)</span></span>
                </div>
                <div className="bg-white p-1.5 rounded border border-gray-200 flex justify-between items-center">
                  <span className="text-[9px] text-gray-500 font-sans">드리블 성공</span>
                  <span className="font-bold text-gray-900">{player.dribbles_completed} <span className="text-[9px] text-gray-400">({targetPlayer.dribbles_completed})</span></span>
                </div>
                <div className="bg-white p-1.5 rounded border border-gray-200 flex justify-between items-center">
                  <span className="text-[9px] text-gray-500 font-sans">슈팅</span>
                  <span className="font-bold text-gray-900">{player.shots} <span className="text-[9px] text-gray-400">({targetPlayer.shots})</span></span>
                </div>
                <div className="bg-white p-1.5 rounded border border-gray-200 flex justify-between items-center">
                  <span className="text-[9px] text-gray-500 font-sans">가치</span>
                  <span className="font-bold text-emerald-700">€{player.market_value_eur}M</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
