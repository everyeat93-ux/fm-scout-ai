import React from 'react';

/**
 * Authentic Football Half-Pitch Tactical Heatmap
 * Replaces crude blocks with a professional Wyscout / FotMob style smoothed tactical heatmap.
 */
export default function PitchZoneMap({ position = "ST", role = "Target Man" }) {
  const pos = (position || "").toUpperCase();

  // Position-based realistic tactical hotspots (normalized coords: 0-120 x, 0-90 y)
  const getHeatmapHotspots = (p) => {
    if (p.includes("ST") || p.includes("CF")) {
      return {
        title: "박스 중앙 타격 & 포처 존",
        sub: "골문 앞 6야드 및 박스 안 집중 (88%)",
        accentColor: "#ef4444",
        spots: [
          { cx: 60, cy: 22, r: 24, opacity: 0.85, color: "#dc2626" }, // Central poacher spot
          { cx: 60, cy: 35, r: 18, opacity: 0.7, color: "#ea580c" },  // Penalty spot area
          { cx: 50, cy: 26, r: 16, opacity: 0.55, color: "#f59e0b" }, // Left cut
          { cx: 70, cy: 26, r: 16, opacity: 0.55, color: "#f59e0b" }  // Right cut
        ]
      };
    }
    if (p.includes("LW") || p.includes("LM")) {
      return {
        title: "좌측 하프스페이스 & 컷인",
        sub: "좌측 측면 돌파 및 박스 안 컷인 (84%)",
        accentColor: "#ec4899",
        spots: [
          { cx: 24, cy: 32, r: 22, opacity: 0.85, color: "#dc2626" }, // Left flank wide
          { cx: 40, cy: 25, r: 20, opacity: 0.75, color: "#ea580c" }, // Half-space cut-in
          { cx: 52, cy: 22, r: 16, opacity: 0.55, color: "#f59e0b" }  // Box penetration
        ]
      };
    }
    if (p.includes("RW") || p.includes("RM")) {
      return {
        title: "우측 하프스페이스 & 컷인",
        sub: "우측 측면 돌파 및 박스 안 컷인 (84%)",
        accentColor: "#ec4899",
        spots: [
          { cx: 96, cy: 32, r: 22, opacity: 0.85, color: "#dc2626" }, // Right flank wide
          { cx: 80, cy: 25, r: 20, opacity: 0.75, color: "#ea580c" }, // Half-space cut-in
          { cx: 68, cy: 22, r: 16, opacity: 0.55, color: "#f59e0b" }  // Box penetration
        ]
      };
    }
    if (p.includes("AM") || p.includes("CAM")) {
      return {
        title: "Zone 14 & 파이널 서드 창출",
        sub: "아크 정면 및 좌우 하프스페이스 조율 (91%)",
        accentColor: "#8b5cf6",
        spots: [
          { cx: 60, cy: 40, r: 24, opacity: 0.85, color: "#dc2626" }, // Zone 14 (D-box)
          { cx: 42, cy: 34, r: 18, opacity: 0.65, color: "#ea580c" }, // Left channel
          { cx: 78, cy: 34, r: 18, opacity: 0.65, color: "#ea580c" }, // Right channel
          { cx: 60, cy: 24, r: 14, opacity: 0.5, color: "#f59e0b" }   // Box entry
        ]
      };
    }
    if (p.includes("CM") || p.includes("DM")) {
      return {
        title: "중원 장악 & 빌드업 허브",
        sub: "하프라인 전진 및 2선 볼 배급 (86%)",
        accentColor: "#3b82f6",
        spots: [
          { cx: 60, cy: 62, r: 26, opacity: 0.8, color: "#dc2626" },
          { cx: 45, cy: 52, r: 20, opacity: 0.65, color: "#ea580c" },
          { cx: 75, cy: 52, r: 20, opacity: 0.65, color: "#ea580c" }
        ]
      };
    }
    // Defense / Default
    return {
      title: "후방 빌드업 & 저지선",
      sub: "최후방 라인 보호 및 롱패스 (82%)",
      accentColor: "#10b981",
      spots: [
        { cx: 60, cy: 68, r: 28, opacity: 0.8, color: "#dc2626" },
        { cx: 40, cy: 62, r: 20, opacity: 0.6, color: "#ea580c" },
        { cx: 80, cy: 62, r: 20, opacity: 0.6, color: "#ea580c" }
      ]
    };
  };

  const heatmap = getHeatmapHotspots(pos);

  return (
    <div className="flex flex-col items-center justify-center w-full select-none">
      {/* Header */}
      <div className="w-full flex items-center justify-between pb-1 mb-1 border-b border-gray-200 px-0.5">
        <span className="text-[10px] font-bold text-gray-800 tracking-tight flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-600 animate-pulse"></span>
          활동 히트맵 [HEATMAP]
        </span>
        <span className="text-[8px] font-mono font-extrabold text-rose-700 bg-rose-50 px-1 py-0.2 rounded border border-rose-200">
          {pos}
        </span>
      </div>

      {/* Authentic Mini Football Pitch with Gaussian Blur Heatmap */}
      <div className="relative w-full max-w-[155px] aspect-[4/3] bg-[#f4fbf7] border border-gray-900 rounded-lg p-1 shadow-xs overflow-hidden">
        <svg viewBox="0 0 120 90" className="w-full h-full" fill="none">
          <defs>
            {/* Heatmap Soft Blur Filter */}
            <filter id="heatBlur" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="7" result="blur" />
              <feColorMatrix
                type="matrix"
                values="1 0 0 0 0
                        0 1 0 0 0
                        0 0 1 0 0
                        0 0 0 18 -6"
                result="contrast"
              />
              <feComposite in="SourceGraphic" in2="contrast" operator="over" />
            </filter>

            {/* Subtle Pitch Grass Stripes Pattern */}
            <pattern id="pitchGrass" width="120" height="15" patternUnits="userSpaceOnUse">
              <rect width="120" height="7.5" fill="#f8fcf9" />
              <rect y="7.5" width="120" height="7.5" fill="#edf7f2" />
            </pattern>
          </defs>

          {/* Grass Background */}
          <rect x="2" y="2" width="116" height="86" rx="2" fill="url(#pitchGrass)" />

          {/* Realistic Pitch Tactical Markings */}
          {/* Outer Boundary */}
          <rect x="2" y="2" width="116" height="86" rx="2" stroke="#94a3b8" strokeWidth="1" />

          {/* Halfway Line */}
          <line x1="2" y1="88" x2="118" y2="88" stroke="#94a3b8" strokeWidth="1" />
          {/* Center Circle Arc */}
          <path d="M 45 88 A 15 15 0 0 1 75 88" stroke="#94a3b8" strokeWidth="1" />
          <circle cx="60" cy="88" r="1.5" fill="#94a3b8" />

          {/* Penalty Area (Box) */}
          <rect x="27" y="2" width="66" height="38" stroke="#94a3b8" strokeWidth="1" />

          {/* Goal Area (6-yard box) */}
          <rect x="42" y="2" width="36" height="13" stroke="#94a3b8" strokeWidth="0.8" />

          {/* Penalty Spot */}
          <circle cx="60" cy="27" r="1.2" fill="#94a3b8" />

          {/* Penalty D-Arc */}
          <path d="M 46 40 A 14 14 0 0 0 74 40" stroke="#94a3b8" strokeWidth="0.9" strokeDasharray="2,1.5" />

          {/* Corner Flags Arcs */}
          <path d="M 2 7 A 5 5 0 0 0 7 2" stroke="#94a3b8" strokeWidth="0.8" />
          <path d="M 113 2 A 5 5 0 0 0 118 7" stroke="#94a3b8" strokeWidth="0.8" />

          {/* Goal Post Frame at Top */}
          <rect x="47" y="0" width="26" height="2" fill="#0f172a" />

          {/* Smoothed Glow Heatmap Layer */}
          <g filter="url(#heatBlur)">
            {heatmap.spots.map((s, idx) => (
              <circle
                key={idx}
                cx={s.cx}
                cy={s.cy}
                r={s.r}
                fill={s.color}
                fillOpacity={s.opacity}
              />
            ))}
          </g>

          {/* Core Intensity Rings (Tactical Focal Dots) */}
          <circle cx={heatmap.spots[0].cx} cy={heatmap.spots[0].cy} r="4" fill="#dc2626" opacity="0.9" />
          <circle cx={heatmap.spots[0].cx} cy={heatmap.spots[0].cy} r="1.5" fill="#ffffff" />

          {/* Direction Indicator */}
          <g opacity="0.5">
            <line x1="60" y1="78" x2="60" y2="52" stroke="#475569" strokeWidth="1.2" strokeDasharray="2,2" />
            <polygon points="60,47 57,53 63,53" fill="#475569" />
          </g>
        </svg>

        {/* Small Bottom Tag */}
        <div className="absolute bottom-1 right-1 text-[7px] font-mono font-black text-gray-600 bg-white/90 px-1 py-0.2 rounded border border-gray-300">
          ATTACK ▲
        </div>
      </div>

      {/* Label and Activity Ratio */}
      <div className="text-[10px] font-extrabold text-gray-950 mt-1 truncate max-w-[155px] text-center font-sans">
        {heatmap.title}
      </div>
      <div className="text-[8px] text-gray-500 font-medium truncate max-w-[155px] text-center">
        {heatmap.sub}
      </div>
    </div>
  );
}
