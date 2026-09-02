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
  targetPlayer = null,
  onSelectTarget,
  archetypes = []
}) {
  const [searchQuery, setSearchQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsSearching(true);
      try {
        const res = await fetch(`/api/players?q=${encodeURIComponent(searchQuery)}&limit=50`);
        const data = await res.json();
        setSearchResults(data.players || []);
      } catch (err) {
        console.error("Search error:", err);
      } finally {
        setIsSearching(false);
      }
    }, 120);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // The active display player is ALWAYS targetPlayer from backend if available
  const activePlayer = targetPlayer || players.find(p => p.id === selectedTargetId) || players[0];
  const displayResults = searchQuery.trim() ? searchResults : players.slice(0, 50);

  // Quick Star Presets for 1-Click Fast Scouting
  const quickStars = [
    { id: "p_son", name: "손흥민", sub: "Tottenham/LAFC", icon: "👑" },
    { id: "p_lee_kangin", name: "이강인", sub: "Atlético/PSG", icon: "⚡" },
    { id: "p_kim_minjae", name: "김민재", sub: "Bayern Munich", icon: "🛡️" },
    { id: "p_mbappe", name: "음바페", sub: "Real Madrid", icon: "🌟" },
    { id: "p_haaland", name: "홀란드", sub: "Man City", icon: "⚽" },
    { id: "p_odegaard", name: "외데고르", sub: "Arsenal", icon: "🪄" },
    { id: "p_messi", name: "메시", sub: "Inter Miami", icon: "🐐" },
  ];

  return (
    <div className="flex flex-col gap-3.5">
      {/* 1. Top Prominent Search Bar & Target Benchmark Display */}
      <div className="relative">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 p-4 rounded-2xl bg-[#121226] border-2 border-[#1f2240] hover:border-[#00ff88]/50 shadow-xl transition-all">
          
          {/* Active Target Player Info Card */}
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-xl bg-[#181832] border border-[#2a2e5c] flex items-center justify-center relative shrink-0 shadow-inner">
              <User className="w-6 h-6 text-gray-400" />
              <span className="absolute -bottom-1 -right-1 text-sm drop-shadow">
                {activePlayer ? (countryFlags[activePlayer.nationality] || '🌐') : '🌐'}
              </span>
            </div>

            {activePlayer ? (
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-[11px] font-mono font-extrabold text-[#00ff88] bg-[#00ff88]/10 px-2 py-0.5 rounded border border-[#00ff88]/30">
                    🎯 현재 비교 기준 선수
                  </span>
                  <h3 className="text-lg font-extrabold text-white tracking-tight">
                    {activePlayer.korean_name || activePlayer.name} 
                    {activePlayer.korean_name && <span className="text-xs font-mono font-normal text-gray-400 ml-1.5">({activePlayer.name})</span>}
                  </h3>
                  <span className="px-2 py-0.5 text-xs font-mono font-bold rounded-md bg-[#00e5ff]/20 text-[#00e5ff] border border-[#00e5ff]/40">
                    {activePlayer.primary_pos}
                  </span>
                  <span className="px-2 py-0.5 text-xs font-mono font-bold rounded-md bg-yellow-400/20 text-yellow-300 border border-yellow-400/30">
                    {activePlayer.overall_grade}급 ({activePlayer.overall_score}점)
                  </span>
                </div>
                <div className="text-xs text-gray-300 font-mono mt-1 flex items-center gap-2 flex-wrap">
                  <span className="font-bold text-white">{activePlayer.club}</span>
                  <span>•</span>
                  <span>{activePlayer.league}</span>
                  <span>•</span>
                  <span>{activePlayer.age}세</span>
                  <span>•</span>
                  <span className="text-[#00ff88] font-bold">몸값 €{activePlayer.market_value_eur}M</span>
                </div>
              </div>
            ) : (
              <span className="text-sm text-gray-400">선수를 검색하여 기준 선수로 선택하세요</span>
            )}
          </div>

          {/* Search Trigger Button */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="w-full md:w-auto flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#1a1a38] to-[#222248] hover:from-[#222248] hover:to-[#2a2a58] text-xs font-mono text-white font-bold border border-[#00ff88]/40 shadow-glow-neon transition-all cursor-pointer"
            >
              <Search className="w-4 h-4 text-[#00ff88]" />
              <span>🔍 선수 검색 / 변경</span>
              <ChevronDown className={`w-3.5 h-3.5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>
          </div>
        </div>

        {/* Live Search Modal Popover */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 z-50 rounded-2xl bg-[#121226] border-2 border-[#00ff88]/40 shadow-2xl p-4 max-h-[420px] flex flex-col backdrop-blur-lg">
            {/* Search Input */}
            <div className="relative mb-3">
              <Search className="w-4 h-4 text-[#00ff88] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="선수 이름 또는 구단명을 입력하세요 (예: 손흥민, 이강인, Son, Haaland, Real Madrid, Tottenham)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-[#0a0a16] border border-[#2a2e5c] rounded-xl pl-10 pr-4 py-3 text-sm font-mono text-white placeholder-gray-500 focus:outline-none focus:border-[#00ff88] shadow-inner"
                autoFocus
              />
              {isSearching && (
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono text-[#00ff88] animate-pulse">
                  검색 중...
                </span>
              )}
            </div>

            {/* Result count */}
            <div className="text-[11px] text-gray-400 font-mono mb-2 flex justify-between px-1">
              <span>검색 결과: <strong className="text-[#00ff88]">{displayResults.length}명</strong></span>
              <span className="text-gray-500">클릭 시 즉시 해당 선수로 스카우팅 분석 시작</span>
            </div>

            {/* Players List */}
            <div className="overflow-y-auto space-y-1.5 pr-1 custom-scrollbar max-h-72">
              {displayResults.map((p) => {
                const isSelected = p.id === (targetPlayer?.id || selectedTargetId);
                const flag = countryFlags[p.nationality] || "🌐";
                return (
                  <button
                    key={p.id}
                    onClick={() => {
                      onSelectTarget(p.id);
                      setIsOpen(false);
                      setSearchQuery("");
                    }}
                    className={`w-full text-left p-3 rounded-xl flex items-center justify-between text-xs font-mono transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-[#00ff88]/20 border border-[#00ff88] text-white shadow-glow-neon'
                        : 'hover:bg-[#1a1a38] text-gray-300 border border-transparent hover:border-[#2a2e5c]'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-base">{flag}</span>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-white text-sm">
                            {p.korean_name || p.name}
                          </span>
                          {p.korean_name && (
                            <span className="text-gray-400 text-xs">({p.name})</span>
                          )}
                          <span className="px-1.5 py-0.2 rounded bg-[#00e5ff]/20 text-[#00e5ff] text-[10px] font-bold">
                            {p.primary_pos}
                          </span>
                        </div>
                        <div className="text-[11px] text-gray-400 mt-0.5">
                          {p.club} • {p.league} • {p.age}세
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 text-right">
                      <div>
                        <div className="text-[#00ff88] font-extrabold text-xs">€{p.market_value_eur}M</div>
                        <div className="text-[10px] text-yellow-400 font-bold">{p.overall_grade}급 ({p.overall_score}점)</div>
                      </div>
                    </div>
                  </button>
                );
              })}
              {displayResults.length === 0 && !isSearching && (
                <div className="p-6 text-center text-xs text-gray-500 font-mono">
                  검색어와 일치하는 선수가 없습니다. 다른 이름이나 구단명을 입력해보세요.
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 2. Quick Star Presets (1-Click Fast Selection) */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 custom-scrollbar">
        <span className="text-[11px] font-mono text-gray-400 flex items-center gap-1 shrink-0 font-bold">
          <Sparkles className="w-3.5 h-3.5 text-yellow-400" />
          인기 스타 즉시 분석:
        </span>
        {quickStars.map((star) => (
          <button
            key={star.id}
            onClick={() => onSelectTarget(star.id)}
            className={`shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono transition-all flex items-center gap-1.5 cursor-pointer ${
              (targetPlayer?.id || selectedTargetId) === star.id
                ? 'bg-[#00ff88]/20 border-2 border-[#00ff88] text-[#00ff88] font-bold shadow-glow-neon'
                : 'bg-[#121226] border border-[#1f2240] text-gray-300 hover:text-white hover:border-[#00ff88]/50 hover:bg-[#161633]'
            }`}
          >
            <span>{star.icon}</span>
            <span className="font-bold">{star.name}</span>
            <span className="text-[10px] text-gray-400">({star.sub})</span>
          </button>
        ))}
      </div>
    </div>
  );
}
