import React from 'react';

/**
 * Re-lab Infographic High-Contrast Dual Radar Chart
 * Solves label ambiguity and delivers crystal-clear corner stat badges.
 */
export default function RadarChartCanvas({
  targetScores = [80, 80, 80, 80, 80],
  candidateScores = [75, 75, 75, 75, 75],
  targetName = "Target",
  candidateName = "Candidate",
  size = 200,
  showLegend = true,
  labels = [
    { label: "창의성", key: "vision" },
    { label: "슈팅", key: "striking" },
    { label: "드리블", key: "dribble" },
    { label: "수비", key: "defense" },
    { label: "피지컬", key: "physical" }
  ]
}) {
  // Use normalized 200x200 coordinate space for robust responsive scaling
  const V_SIZE = 200;
  const center = 100;
  const radius = 60; // Leaves 40px margin around perimeter for text badges
  const numAxes = labels.length;
  const angleStep = (Math.PI * 2) / numAxes;
  const startAngle = -Math.PI / 2;

  const getCoordinates = (index, value, customRadius = radius) => {
    const angle = startAngle + index * angleStep;
    const safeVal = (typeof value === 'number' && !isNaN(value)) ? Math.max(0, Math.min(100, value)) : 50;
    const r = (safeVal / 100) * customRadius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle)
    };
  };

  const getPolygonPoints = (scores) => {
    const validScores = (scores || [50, 50, 50, 50, 50]).map(v => (typeof v === 'number' && !isNaN(v) ? Math.max(0, Math.min(100, v)) : 50));
    return validScores
      .map((score, i) => {
        const pt = getCoordinates(i, score);
        return `${pt.x},${pt.y}`;
      })
      .join(" ");
  };

  const gridLevels = [25, 50, 75, 100];

  return (
    <div className="flex flex-col items-center justify-center relative select-none w-full max-w-[160px] sm:max-w-[200px]">
      {/* Legend Indicator with distinct roles */}
      {showLegend && (
        <div className="flex items-center justify-center gap-2 sm:gap-3 mb-1 text-[9px] sm:text-[10px] font-sans font-bold flex-wrap">
          <div className="flex items-center gap-1 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 inline-block"></span>
            <span className="text-amber-900 truncate max-w-[70px] sm:max-w-[90px]">기준: {targetName}</span>
          </div>
          <div className="flex items-center gap-1 bg-purple-50 px-1.5 py-0.5 rounded border border-purple-200">
            <span className="w-1.5 h-1.5 rounded-full bg-purple-600 inline-block"></span>
            <span className="text-purple-900 font-extrabold truncate max-w-[70px] sm:max-w-[90px]">추천: {candidateName}</span>
          </div>
        </div>
      )}

      <svg
        viewBox={`0 0 ${V_SIZE} ${V_SIZE}`}
        className="w-full h-auto overflow-visible"
        style={{ maxWidth: `${size}px` }}
      >
        <defs>
          {/* Candidate Purple Gradient */}
          <linearGradient id="relabPurpleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.55" />
            <stop offset="100%" stopColor="#6366f1" stopOpacity="0.3" />
          </linearGradient>

          {/* Target Amber Gradient */}
          <linearGradient id="relabAmberGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#d97706" stopOpacity="0.1" />
          </linearGradient>
        </defs>

        {/* Concentric Grid Web */}
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
              fill={lvl % 50 === 0 ? "rgba(241, 245, 249, 0.7)" : "transparent"}
              stroke={lvl === 100 ? "#94a3b8" : "#cbd5e1"}
              strokeWidth={lvl === 100 ? "1.2" : "0.7"}
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
              stroke="#cbd5e1"
              strokeWidth="0.8"
            />
          );
        })}

        {/* Target Player Polygon (Amber Dashed) */}
        {targetScores && (
          <g>
            <polygon
              points={getPolygonPoints(targetScores)}
              fill="url(#relabAmberGrad)"
              stroke="#d97706"
              strokeWidth="1.6"
              strokeDasharray="3,2"
            />
            {targetScores.map((score, i) => {
              const pt = getCoordinates(i, score);
              return (
                <circle
                  key={`target-pt-${i}`}
                  cx={pt.x}
                  cy={pt.y}
                  r="2"
                  fill="#f59e0b"
                  stroke="#ffffff"
                  strokeWidth="0.8"
                />
              );
            })}
          </g>
        )}

        {/* Candidate Player Polygon (Purple Solid) */}
        {candidateScores && (
          <g>
            <polygon
              points={getPolygonPoints(candidateScores)}
              fill="url(#relabPurpleGrad)"
              stroke="#6d28d9"
              strokeWidth="2.2"
            />
            {candidateScores.map((score, i) => {
              const pt = getCoordinates(i, score);
              return (
                <circle
                  key={`cand-pt-${i}`}
                  cx={pt.x}
                  cy={pt.y}
                  r="3"
                  fill="#7c3aed"
                  stroke="#ffffff"
                  strokeWidth="1.2"
                />
              );
            })}
          </g>
        )}

        {/* Corner Stat Badges (Re-lab Corner Ratios) */}
        {labels.map((item, i) => {
          // Calculate label center with controlled radius
          const labelDist = radius + 18;
          const labelPt = getCoordinates(i, 100, labelDist);
          const isTop = i === 0;
          const isBottom = i === 2 || i === 3;
          const isRight = i === 1;
          const isLeft = i === 4;

          let textAnchor = "middle";
          let dx = 0;
          if (isRight) { textAnchor = "start"; dx = 2; }
          if (isLeft) { textAnchor = "end"; dx = -2; }

          const candVal = candidateScores ? Math.round(candidateScores[i]) : 0;
          const targetVal = targetScores ? Math.round(targetScores[i]) : 0;

          return (
            <g key={`label-${i}`} transform={`translate(${labelPt.x + dx}, ${labelPt.y})`}>
              <text
                textAnchor={textAnchor}
                fontSize="9"
                fontWeight="800"
                fontFamily="sans-serif"
                fill="#0f172a"
                dy={isTop ? "-7" : isBottom ? "9" : "-1"}
              >
                {item.label}
              </text>
              <text
                textAnchor={textAnchor}
                fontSize="8.5"
                fontWeight="800"
                fontFamily="monospace"
                fill="#6d28d9"
                dy={isTop ? "4" : isBottom ? "19" : "9"}
              >
                {candVal}
                <tspan fill="#b45309" fontWeight="700">/{targetVal}</tspan>
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
