import React from 'react';

/**
 * High-tech Tactical Radar Overlay Chart
 * Renders dual radar polygons:
 * - Target Player: Translucent dashed white line
 * - Scouted Candidate: Glowing Neon Green solid line with gradient fill
 */
export default function RadarChartCanvas({
  targetScores = [80, 80, 80, 80, 80],
  candidateScores = [75, 75, 75, 75, 75],
  targetName = "Target Player",
  candidateName = "Candidate",
  size = 320,
  showLegend = true,
  labels = [
    { label: "창의성 & 패스", sub: "Vision", key: "vision" },
    { label: "슈팅 & xG", sub: "Striking", key: "striking" },
    { label: "온볼 & 운반", sub: "Dribble", key: "dribble" },
    { label: "수비 엔진", sub: "Defense", key: "defense" },
    { label: "피지컬 경합", sub: "Physical", key: "physical" }
  ]
}) {
  const center = size / 2;
  const radius = (size / 2) - 48; // Padding for outer text labels
  const numAxes = labels.length;
  const angleStep = (Math.PI * 2) / numAxes;
  // Rotate so that the first axis points straight up (-PI/2)
  const startAngle = -Math.PI / 2;

  // Function to get (x, y) coordinates for a given index and value (0-100)
  const getCoordinates = (index, value) => {
    const angle = startAngle + index * angleStep;
    const r = (value / 100) * radius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle)
    };
  };

  // Generate polygon points string
  const getPolygonPoints = (scores) => {
    return scores
      .map((score, i) => {
        const pt = getCoordinates(i, score);
        return `${pt.x},${pt.y}`;
      })
      .join(" ");
  };

  const gridLevels = [20, 40, 60, 80, 100];

  return (
    <div className="flex flex-col items-center justify-center relative select-none">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="overflow-visible drop-shadow-[0_0_15px_rgba(0,0,0,0.8)]"
      >
        <defs>
          {/* Candidate Polygon Gradient */}
          <linearGradient id="neonGreenGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00ff88" stopOpacity="0.45" />
            <stop offset="100%" stopColor="#00e5ff" stopOpacity="0.25" />
          </linearGradient>
          
          {/* Target Polygon Gradient */}
          <radialGradient id="targetWhiteGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.15" />
            <stop offset="100%" stopColor="#ffffff" stopOpacity="0.05" />
          </radialGradient>

          {/* Glow Filter */}
          <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Concentric Grid Polygons */}
        {gridLevels.map((lvl) => {
          const pts = labels
            .map((_, i) => {
              const pt = getCoordinates(i, lvl);
              return `${pt.x},${pt.y}`;
            })
            .join(" ");
          return (
            <polygon
              key={`grid-${lvl}`}
              points={pts}
              fill="transparent"
              stroke="#1f2240"
              strokeWidth={lvl === 100 ? "1.5" : "1"}
              strokeDasharray={lvl === 100 ? "none" : "2,2"}
            />
          );
        })}

        {/* Radial Axis Lines */}
        {labels.map((_, i) => {
          const pt = getCoordinates(i, 100);
          return (
            <line
              key={`axis-${i}`}
              x1={center}
              y1={center}
              x2={pt.x}
              y2={pt.y}
              stroke="#1f2240"
              strokeWidth="1"
            />
          );
        })}

        {/* Target Player Polygon (Translucent White Dashed) */}
        {targetScores && (
          <g className="transition-all duration-500 ease-out">
            <polygon
              points={getPolygonPoints(targetScores)}
              fill="url(#targetWhiteGradient)"
              stroke="#ffffff"
              strokeWidth="1.8"
              strokeDasharray="4,3"
              strokeOpacity="0.8"
            />
            {targetScores.map((score, i) => {
              const pt = getCoordinates(i, score);
              return (
                <circle
                  key={`target-pt-${i}`}
                  cx={pt.x}
                  cy={pt.y}
                  r="3"
                  fill="#ffffff"
                  stroke="#0a0a16"
                  strokeWidth="1.5"
                  opacity="0.85"
                />
              );
            })}
          </g>
        )}

        {/* Candidate Player Polygon (Glowing Neon Green Solid) */}
        {candidateScores && (
          <g className="transition-all duration-500 ease-out">
            <polygon
              points={getPolygonPoints(candidateScores)}
              fill="url(#neonGreenGradient)"
              stroke="#00ff88"
              strokeWidth="2.5"
              filter="url(#neonGlow)"
            />
            {candidateScores.map((score, i) => {
              const pt = getCoordinates(i, score);
              return (
                <g key={`cand-pt-${i}`}>
                  <circle
                    cx={pt.x}
                    cy={pt.y}
                    r="4"
                    fill="#00ff88"
                    stroke="#0a0a16"
                    strokeWidth="1.5"
                    className="animate-pulse"
                  />
                  <circle
                    cx={pt.x}
                    cy={pt.y}
                    r="1.5"
                    fill="#ffffff"
                  />
                </g>
              );
            })}
          </g>
        )}

        {/* Axis Labels & Values */}
        {labels.map((item, i) => {
          const labelPt = getCoordinates(i, 120);
          const isTop = i === 0;
          const isBottom = i === 2 || i === 3;
          const isRight = i === 1;
          const isLeft = i === 4;

          let textAnchor = "middle";
          if (isRight) textAnchor = "start";
          if (isLeft) textAnchor = "end";

          const candVal = candidateScores ? candidateScores[i] : 0;
          const targetVal = targetScores ? targetScores[i] : 0;

          return (
            <g key={`label-${i}`} transform={`translate(${labelPt.x}, ${labelPt.y})`}>
              <text
                textAnchor={textAnchor}
                className="text-[11px] font-semibold fill-gray-300 tracking-tight"
                dy={isTop ? "-8" : isBottom ? "14" : "0"}
              >
                {item.label}
              </text>
              <text
                textAnchor={textAnchor}
                className="text-[10px] font-mono fill-[#00ff88] font-bold"
                dy={isTop ? "4" : isBottom ? "26" : "14"}
              >
                {candVal.toFixed(0)} <tspan className="fill-gray-400 font-normal">/ {targetVal.toFixed(0)}</tspan>
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend Indicator */}
      {showLegend && (
        <div className="flex items-center gap-6 mt-4 text-xs font-mono">
          <div className="flex items-center gap-2">
            <span className="w-3.5 h-0.5 border-t-2 border-dashed border-white inline-block"></span>
            <span className="text-gray-300">{targetName}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3.5 h-2 bg-[#00ff88]/30 border border-[#00ff88] rounded-sm inline-block shadow-glow-neon"></span>
            <span className="text-[#00ff88] font-semibold">{candidateName}</span>
          </div>
        </div>
      )}
    </div>
  );
}
