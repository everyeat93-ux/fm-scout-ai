import React, { useState, useEffect } from 'react';
import { Search, User, Sparkles, Filter, ChevronDown } from 'lucide-react';

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

export default function TargetSelector({
  players = [],
  selectedTargetId,
  onSelectTarget,
  archetypes = []
}) {
  const [searchQuery, setSearchQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const selectedPlayer = players.find(p => p.id === selectedTargetId) || players[0];

  const filteredPlayers = players.filter(p => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      p.name.toLowerCase().includes(q) ||
      p.full_name?.toLowerCase().includes(q) ||
      p.korean_name?.toLowerCase().includes(q) ||
      p.club.toLowerCase().includes(q) ||
      p.primary_pos.toLowerCase().includes(q)
    );
  });

  return (
    <div className="flex flex-col gap-3">
      {/* Target Player Selection Bar */}
      <div className="relative">
        <div className="flex items-center justify-between gap-3 p-3.5 rounded-xl bg-[#121226] border border-[#1f2240] hover:border-[#2a2e5c] transition-all">
          <div className="flex items-center gap-3">
            {/* Silhouette Avatar */}
            <div className="w-11 h-11 rounded-lg bg-[#181832] border border-[#2a2e5c] flex items-center justify-center relative shrink-0">
              <User className="w-6 h-6 text-gray-400" />
              <span className="absolute -bottom-1 -right-1 text-xs">
                {selectedPlayer ? countryFlags[selectedPlayer.nationality] : '🌐'}
              </span>
            </div>

            {/* Target Player Info */}
            {selectedPlayer ? (
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-[#00ff88]">TARGET BENCHMARK:</span>
                  <h3 className="text-base font-bold text-white tracking-tight">
                    {selectedPlayer.name} {selectedPlayer.korean_name && <span className="text-sm font-normal text-gray-400">({selectedPlayer.korean_name})</span>}
                  </h3>
                  <span className="px-1.5 py-0.5 text-[10px] font-mono font-bold rounded bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/40">
                    {selectedPlayer.primary_pos}
                  </span>
                </div>
                <div className="text-xs text-gray-400 font-mono mt-0.5 flex items-center gap-2">
                  <span>{selectedPlayer.club}</span>
                  <span>•</span>
                  <span>{selectedPlayer.league}</span>
                  <span>•</span>
                  <span className="text-[#00ff88]">€{selectedPlayer.market_value_eur}M</span>
                  <span>•</span>
                  <span className="text-gray-300">종합 {selectedPlayer.overall_grade} ({selectedPlayer.overall_score}점)</span>
                </div>
              </div>
            ) : (
              <span className="text-sm text-gray-400">타깃 선수를 선택하세요</span>
            )}
          </div>

          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-[#1a1a38] hover:bg-[#222248] text-xs font-mono text-gray-200 border border-[#2a2e5c] transition-colors"
          >
            <Search className="w-3.5 h-3.5 text-[#00ff88]" />
            선수 변경 / 검색
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
          </button>
        </div>

        {/* Dropdown Modal / Popover */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 z-50 rounded-xl bg-[#121226] border border-[#2a2e5c] shadow-2xl p-4 max-h-96 flex flex-col">
            {/* Search Input */}
            <div className="relative mb-3">
              <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="선수명, 한글명, 구단명, 포지션 검색 (예: 손흥민, 이강인, Son, Haaland, London White)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-[#0a0a16] border border-[#1f2240] rounded-lg pl-9 pr-3 py-2 text-xs font-mono text-white placeholder-gray-500 focus:outline-none focus:border-[#00ff88]"
                autoFocus
              />
            </div>

            {/* Result count */}
            <div className="text-[10px] text-gray-400 font-mono mb-2 flex justify-between px-1">
              <span>검색 결과: <strong className="text-[#00ff88]">{filteredPlayers.length}명</strong></span>
              {filteredPlayers.length > 100 && <span className="text-gray-400">(상위 100명 표시 중)</span>}
            </div>

            {/* Players List */}
            <div className="overflow-y-auto space-y-1 pr-1 custom-scrollbar">
              {filteredPlayers.slice(0, 100).map((p) => {
                const isSelected = p.id === selectedTargetId;
                const flag = countryFlags[p.nationality] || "🌐";
                return (
                  <button
                    key={p.id}
                    onClick={() => {
                      onSelectTarget(p.id);
                      setIsOpen(false);
                      setSearchQuery("");
                    }}
                    className={`w-full text-left p-2.5 rounded-lg flex items-center justify-between text-xs font-mono transition-colors ${
                      isSelected
                        ? 'bg-[#00ff88]/15 border border-[#00ff88]/40 text-white'
                        : 'hover:bg-[#181832] text-gray-300 border border-transparent'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className="text-sm">{flag}</span>
                      <span className="font-bold text-white">{p.name}</span>
                      {p.korean_name && (
                        <span className="text-[#00ff88] font-sans text-[11px] font-medium">({p.korean_name})</span>
                      )}
                      <span className="text-gray-400 font-sans text-[11px] hidden sm:inline">{p.full_name}</span>
                      <span className="px-1.5 py-0.2 rounded bg-[#1f2240] text-gray-300 text-[10px]">
                        {p.primary_pos}
                      </span>
                    </div>

                    <div className="flex items-center gap-3 text-gray-400">
                      <span>{p.club}</span>
                      <span className="text-[#00ff88] font-bold">€{p.market_value_eur}M</span>
                      <span className="text-xs font-bold text-yellow-400">{p.overall_grade}</span>
                    </div>
                  </button>
                );
              })}
              {filteredPlayers.length === 0 && (
                <div className="p-4 text-center text-xs text-gray-500 font-mono">
                  일치하는 선수가 없습니다.
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Quick Tactical Preset Archetypes */}
      {archetypes.length > 0 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          <span className="text-[11px] font-mono text-gray-400 flex items-center gap-1 shrink-0">
            <Sparkles className="w-3 h-3 text-yellow-400" />
            전술 롤 프리셋:
          </span>
          {archetypes.map((arch) => (
            <button
              key={arch.id}
              onClick={() => onSelectTarget(arch.benchmark_player_id)}
              className={`shrink-0 px-2.5 py-1 rounded-md text-[11px] font-mono transition-all ${
                selectedTargetId === arch.benchmark_player_id
                  ? 'bg-[#00ff88]/20 border border-[#00ff88] text-[#00ff88] font-semibold shadow-glow-neon'
                  : 'bg-[#121226] border border-[#1f2240] text-gray-400 hover:text-gray-200 hover:border-[#2a2e5c]'
              }`}
            >
              {arch.title.split('/')[0].trim()} ({arch.benchmark_name.split(' ').pop()})
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
