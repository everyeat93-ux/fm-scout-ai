import React, { useState } from 'react';
import { Star, Trash2, ArrowRight, X, Copy, Check, Target, Trophy, Sparkles, User, Layers } from 'lucide-react';

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
  "Colombia": "🇨🇴",
  "Poland": "🇵🇱",
  "Serbia": "🇷🇸",
  "Nigeria": "🇳🇬",
  "Guinea": "🇬🇳",
  "Ivory Coast": "🇨🇮",
  "Greece": "🇬🇷",
  "Saudi Arabia": "🇸🇦"
};

export default function ShortlistModal({
  isOpen,
  onClose,
  bookmarkedPlayerIds = [],
  allPlayers = [],
  onRemoveBookmark,
  onClearAllBookmarks,
  onSelectAsTarget,
  onOpen1v1Compare,
  targetPlayerId
}) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const bookmarkedPlayers = allPlayers.filter(p => bookmarkedPlayerIds.includes(p.id));

  const handleCopyShortlistText = () => {
    if (bookmarkedPlayers.length === 0) return;
    const text = bookmarkedPlayers.map((p, idx) => 
      `${idx + 1}. ${p.korean_name || p.name} (${p.name}) | ${p.club} | ${p.primary_pos} | ${p.age}세 | €${p.market_value_eur}M`
    ).join('\n');

    navigator.clipboard.writeText(`[FM Scout AI 관심 선수 쇼트리스트]\n` + text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="bg-[#121226] border border-amber-400/40 rounded-2xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b border-[#1f2240] flex items-center justify-between bg-[#0a0a16]">
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-amber-400/20 text-amber-400 border border-amber-400/30">
              <Star className="w-4 h-4 fill-amber-400" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white font-mono flex items-center gap-2">
                <span>관심 선수 쇼트리스트 (SHORTLIST)</span>
                <span className="px-2 py-0.2 rounded-full bg-amber-400/20 text-amber-300 text-xs font-mono">
                  {bookmarkedPlayers.length}명 보관 중
                </span>
              </h3>
              <p className="text-[11px] text-gray-400 font-mono">찜해둔 유망주 및 타겟 선수를 한눈에 비교하고 관리합니다.</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-[#181832] text-gray-400 hover:text-white transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content List */}
        <div className="p-4 overflow-y-auto max-h-[55vh] space-y-2.5 divide-y divide-[#1f2240]/40">
          {bookmarkedPlayers.length === 0 ? (
            <div className="py-12 text-center flex flex-col items-center justify-center gap-3 text-gray-400 font-mono text-xs">
              <Star className="w-8 h-8 text-gray-600 stroke-[1.5]" />
              <div className="text-gray-300 font-bold text-sm">아직 찜한 선수가 없습니다.</div>
              <div className="text-gray-500 text-[11px]">
                후보 카드나 리포트에서 ⭐ 버튼을 눌러 관심 선수를 쇼트리스트에 담아보세요!
              </div>
            </div>
          ) : (
            bookmarkedPlayers.map((player) => {
              const flag = countryFlags[player.nationality] || "🌐";

              return (
                <div
                  key={player.id}
                  className="pt-2.5 first:pt-0 p-3 rounded-xl bg-[#0a0a16] border border-[#1f2240] hover:border-amber-400/40 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                >
                  {/* Player Basic Info */}
                  <div className="flex items-start gap-2.5 min-w-0 flex-1">
                    <span className="text-lg shrink-0 mt-0.5">{flag}</span>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="font-bold text-white text-sm tracking-tight break-keep">
                          {player.korean_name || player.name}
                        </span>
                        {player.korean_name && (
                          <span className="text-gray-400 text-xs font-mono">
                            ({player.name})
                          </span>
                        )}
                        <span className="px-1.5 py-0.2 rounded bg-[#00e5ff]/20 text-[#00e5ff] text-[10px] font-mono font-bold">
                          {player.primary_pos}
                        </span>
                      </div>

                      <div className="text-xs text-gray-400 font-mono mt-0.5 flex items-center gap-1.5 flex-wrap break-keep">
                        <span className="text-gray-300">{player.club}</span>
                        <span className="text-gray-600">•</span>
                        <span>{player.league}</span>
                        <span className="text-gray-600">•</span>
                        <span>{player.age}세</span>
                        <span className="text-gray-600">•</span>
                        <span className="text-[#00ff88] font-bold">€{player.market_value_eur}M</span>
                      </div>

                      {/* 5 Pillars Badges */}
                      <div className="flex items-center gap-1 flex-wrap text-[10px] font-mono mt-1.5 text-gray-400">
                        <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">🪄 {player.vision_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">⚽ {player.striking_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">⚡ {player.dribble_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">🛡️ {player.defense_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-[#121226] border border-[#1f2240]">💪 {player.physical_grade}</span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                    <button
                      onClick={() => {
                        onSelectAsTarget(player.id);
                        onClose();
                      }}
                      className="px-2.5 py-1.5 rounded-lg bg-[#181832] hover:bg-[#202046] text-[#00ff88] text-xs font-mono border border-[#00ff88]/30 flex items-center gap-1 transition-colors cursor-pointer"
                      title="이 선수를 스카우트 기준으로 설정"
                    >
                      <Target className="w-3 h-3" />
                      <span>타겟 지정</span>
                    </button>

                    <button
                      onClick={() => {
                        onOpen1v1Compare(targetPlayerId, player.id);
                        onClose();
                      }}
                      className="px-2.5 py-1.5 rounded-lg bg-[#00e5ff]/15 hover:bg-[#00e5ff]/25 text-[#00e5ff] text-xs font-mono border border-[#00e5ff]/30 flex items-center gap-1 transition-colors cursor-pointer"
                      title="1v1 비교 아레나로 이동"
                    >
                      <Layers className="w-3 h-3" />
                      <span>1v1 비교</span>
                    </button>

                    <button
                      onClick={() => onRemoveBookmark(player.id)}
                      className="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 transition-colors cursor-pointer"
                      title="쇼트리스트에서 삭제"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer Actions */}
        {bookmarkedPlayers.length > 0 && (
          <div className="p-3.5 border-t border-[#1f2240] bg-[#0a0a16] flex items-center justify-between gap-2 flex-wrap">
            <button
              onClick={onClearAllBookmarks}
              className="px-3 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs font-mono border border-rose-500/30 transition-colors cursor-pointer"
            >
              전체 비우기
            </button>

            <button
              onClick={handleCopyShortlistText}
              className="px-4 py-1.5 rounded-lg bg-amber-400 hover:bg-amber-300 text-black font-bold text-xs font-mono flex items-center gap-1.5 shadow-glow-neon transition-all cursor-pointer ml-auto"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>복사 완료!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>쇼트리스트 클립보드 복사</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
