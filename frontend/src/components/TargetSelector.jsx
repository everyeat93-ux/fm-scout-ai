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

  const activePlayer = targetPlayer || players.find(p => p.id === selectedTargetId) || players[0];
  const displayResults = searchQuery.trim() ? searchResults : players.slice(0, 50);

  const quickStars = [
    { id: "p_son", name: "손흥민", sub: "토트넘", icon: "👑" },
    { id: "p_lee_kangin", name: "이강인", sub: "PSG", icon: "⚡" },
    { id: "p_kim_minjae", name: "김민재", sub: "뮌헨", icon: "🛡️" },
    { id: "p_hwang_heechan", name: "황희찬", sub: "울버햄튼", icon: "🚀" },
    { id: "p_mbappe", name: "음바페", sub: "레알", icon: "🌟" },
    { id: "p_haaland", name: "홀란드", sub: "맨시티", icon: "⚽" },
    { id: "p_odegaard", name: "외데고르", sub: "아스널", icon: "🪄" },
    { id: "p_salah", name: "살라", sub: "리버풀", icon: "👑" },
    { id: "p_messi", name: "메시", sub: "마이애미", icon: "🐐" },
  ];

  return (
    <div className="flex flex-col gap-2.5 w-full select-none">
      {/* 1. Top Target Benchmark Display (Clean White Theme) */}
      <div className="relative">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 p-3 sm:p-4 rounded-2xl bg-white border-2 border-gray-900 shadow-sm transition-all">
          
          {/* Active Target Player Info Card */}
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-12 h-12 rounded-xl bg-gray-100 border border-gray-300 flex items-center justify-center relative shrink-0 shadow-inner">
              <User className="w-6 h-6 text-gray-500" />
              <span className="absolute -bottom-1 -right-1 text-sm drop-shadow">
                {activePlayer ? (countryFlags[activePlayer.nationality] || '🌐') : '🌐'}
              </span>
            </div>

            {activePlayer ? (
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className="text-[10px] sm:text-[11px] font-mono font-extrabold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300 shrink-0">
                    🎯 비교 기준 타깃
                  </span>
                  <h3 className="text-base sm:text-lg font-black text-gray-950 tracking-tight break-keep font-sans">
                    {activePlayer.korean_name || activePlayer.name}
                    {activePlayer.korean_name && (
                      <span className="text-xs font-mono font-bold text-gray-500 ml-1.5 hidden sm:inline">
                        ({activePlayer.name})
                      </span>
                    )}
                  </h3>
                  <span className="px-1.5 py-0.5 text-[10px] sm:text-xs font-mono font-bold rounded bg-purple-100 text-purple-800 border border-purple-200 shrink-0">
                    {activePlayer.primary_pos}
                  </span>
                  <span className="px-1.5 py-0.5 text-[10px] sm:text-xs font-mono font-bold rounded bg-amber-100 text-amber-800 border border-amber-300 shrink-0">
                    {activePlayer.overall_grade}급 ({activePlayer.overall_score}점)
                  </span>
                </div>

                <div className="text-xs text-gray-600 font-mono mt-1 flex items-center gap-1.5 flex-wrap break-keep">
                  <span className="font-bold text-gray-900">{activePlayer.club}</span>
                  <span className="text-gray-400">•</span>
                  <span>{activePlayer.league}</span>
                  <span className="text-gray-400">•</span>
                  <span>{activePlayer.age}세</span>
                  <span className="text-gray-400">•</span>
                  <span className="text-emerald-700 font-bold">시장가치 €{activePlayer.market_value_eur}M</span>
                </div>
              </div>
            ) : (
              <span className="text-sm text-gray-500">선수를 검색하여 기준 선수로 선택하세요</span>
            )}
          </div>

          {/* Search Trigger Button */}
          <div className="shrink-0">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="w-full md:w-auto flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gray-900 hover:bg-gray-800 text-xs font-mono text-white font-bold shadow-sm transition-all cursor-pointer"
            >
              <Search className="w-4 h-4 text-emerald-400" />
              <span>선수 검색 / 변경</span>
              <ChevronDown className={`w-3.5 h-3.5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>
          </div>
        </div>

        {/* Live Search Modal Popover (Clean White) */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 z-50 rounded-2xl bg-white border-2 border-gray-900 shadow-2xl p-3 sm:p-4 max-h-[440px] flex flex-col backdrop-blur-xl">
            {/* Search Input */}
            <div className="relative mb-2.5">
              <Search className="w-4 h-4 text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="선수명 또는 구단명 입력 (예: 손흥민, 이강인, Son, PSG, Tottenham)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-gray-50 border border-gray-300 rounded-xl pl-10 pr-4 py-2.5 sm:py-3 text-xs sm:text-sm font-sans text-gray-900 placeholder-gray-400 focus:outline-none focus:border-purple-600 focus:bg-white shadow-inner"
                autoFocus
              />
              {isSearching && (
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono text-purple-600 animate-pulse">
                  검색 중...
                </span>
              )}
            </div>

            {/* Result count */}
            <div className="text-[11px] text-gray-500 font-mono mb-2 flex justify-between px-1">
              <span>검색 결과: <strong className="text-gray-900 font-bold">{displayResults.length}명</strong></span>
              <span className="text-gray-400 hidden sm:inline">클릭 시 즉시 스카우팅 분석 시작</span>
            </div>

            {/* Players List */}
            <div className="overflow-y-auto space-y-1.5 pr-1 max-h-64 custom-scrollbar">
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
                    className={`w-full text-left p-2.5 sm:p-3 rounded-xl flex items-center justify-between text-xs font-mono transition-all cursor-pointer border ${
                      isSelected
                        ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-sm'
                        : 'bg-white hover:bg-gray-50 text-gray-800 border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <span className="text-base shrink-0">{flag}</span>
                      <div className="min-w-0">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <span className="font-bold text-gray-900 text-xs sm:text-sm break-keep">
                            {p.korean_name || p.name}
                          </span>
                          {p.korean_name && (
                            <span className="text-gray-500 text-[11px]">({p.name})</span>
                          )}
                          <span className="px-1.5 py-0.2 rounded bg-purple-100 text-purple-800 text-[10px] font-bold">
                            {p.primary_pos}
                          </span>
                        </div>
                        <div className="text-[10px] sm:text-[11px] text-gray-500 mt-0.5 truncate">
                          {p.club} • {p.league} • {p.age}세
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-right shrink-0">
                      <div>
                        <div className="text-emerald-700 font-black text-xs">€{p.market_value_eur}M</div>
                        <div className="text-[10px] text-amber-700 font-bold">{p.overall_grade}급</div>
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

      {/* 2. Quick Star Presets (Clean White Pills) */}
      <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1 -mx-1 px-1">
        <span className="text-[11px] font-mono text-gray-600 flex items-center gap-1 shrink-0 font-bold">
          <Sparkles className="w-3.5 h-3.5 text-amber-500 shrink-0" />
          <span className="hidden sm:inline">인기 스타 즉시 분석:</span>
          <span className="sm:hidden">인기 스타:</span>
        </span>
        {quickStars.map((star) => {
          const isSelected = (targetPlayer?.id || selectedTargetId) === star.id;
          return (
            <button
              key={star.id}
              onClick={() => onSelectTarget(star.id)}
              className={`shrink-0 px-3 py-1.5 rounded-full text-xs font-mono transition-all flex items-center gap-1.5 cursor-pointer whitespace-nowrap border ${
                isSelected
                  ? 'bg-gray-900 border-gray-900 text-white font-bold shadow-md scale-105'
                  : 'bg-white border-gray-300 text-gray-700 hover:text-black hover:border-gray-500 hover:bg-gray-50 shadow-xs'
              }`}
            >
              <span>{star.icon}</span>
              <span className="font-bold">{star.name}</span>
              <span className="text-[10px] text-gray-400 hidden sm:inline">({star.sub})</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
