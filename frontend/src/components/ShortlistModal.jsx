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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/50 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white border-2 border-gray-900 rounded-2xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden text-gray-900">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between bg-amber-50/50">
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-amber-100 text-amber-900 border border-amber-300">
              <Star className="w-4 h-4 fill-amber-500 text-amber-500" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-gray-950 font-mono flex items-center gap-2">
                <span>관심 선수 쇼트리스트 (SHORTLIST)</span>
                <span className="px-2 py-0.2 rounded-full bg-amber-100 text-amber-900 font-bold text-xs font-mono border border-amber-300">
                  {bookmarkedPlayers.length}명 보관 중
                </span>
              </h3>
              <p className="text-[11px] text-gray-500 font-mono">찜해둔 유망주 및 타겟 선수를 한눈에 비교하고 관리합니다.</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-gray-200 text-gray-500 hover:text-gray-900 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content List */}
        <div className="p-4 overflow-y-auto max-h-[55vh] space-y-2.5 divide-y divide-gray-100">
          {bookmarkedPlayers.length === 0 ? (
            <div className="py-12 text-center flex flex-col items-center justify-center gap-3 text-gray-500 font-mono text-xs">
              <Star className="w-8 h-8 text-gray-400 stroke-[1.5]" />
              <div className="text-gray-900 font-bold text-sm">아직 찜한 선수가 없습니다.</div>
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
                  className="pt-2.5 first:pt-0 p-3 rounded-xl bg-gray-50 border border-gray-200 hover:border-amber-400 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs"
                >
                  {/* Player Basic Info */}
                  <div className="flex items-start gap-2.5 min-w-0 flex-1">
                    <span className="text-lg shrink-0 mt-0.5">{flag}</span>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="font-black text-gray-950 text-sm tracking-tight break-keep">
                          {player.korean_name || player.name}
                        </span>
                        {player.korean_name && (
                          <span className="text-gray-500 text-xs font-mono">
                            ({player.name})
                          </span>
                        )}
                        <span className="px-1.5 py-0.2 rounded bg-purple-100 text-purple-900 text-[10px] font-mono font-bold border border-purple-200">
                          {player.primary_pos}
                        </span>
                      </div>

                      <div className="text-xs text-gray-600 font-mono mt-0.5 flex items-center gap-1.5 flex-wrap break-keep">
                        <span className="text-gray-900 font-medium">{player.club}</span>
                        <span className="text-gray-400">•</span>
                        <span>{player.league}</span>
                        <span className="text-gray-400">•</span>
                        <span>{player.age}세</span>
                        <span className="text-gray-400">•</span>
                        <span className="text-emerald-700 font-bold">€{player.market_value_eur}M</span>
                      </div>

                      {/* 5 Pillars Badges */}
                      <div className="flex items-center gap-1 flex-wrap text-[10px] font-mono mt-1.5 text-gray-600">
                        <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">🪄 {player.vision_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">⚽ {player.striking_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">⚡ {player.dribble_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">🛡️ {player.defense_grade}</span>
                        <span className="px-1.5 py-0.2 rounded bg-white border border-gray-200">💪 {player.physical_grade}</span>
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
                      className="px-2.5 py-1.5 rounded-lg bg-white hover:bg-purple-50 text-purple-700 text-xs font-mono font-bold border border-purple-300 flex items-center gap-1 transition-colors cursor-pointer shadow-xs"
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
                      className="px-2.5 py-1.5 rounded-lg bg-white hover:bg-amber-50 text-amber-900 text-xs font-mono font-bold border border-amber-300 flex items-center gap-1 transition-colors cursor-pointer shadow-xs"
                      title="1v1 비교 아레나로 이동"
                    >
                      <Layers className="w-3 h-3" />
                      <span>1v1 비교</span>
                    </button>

                    <button
                      onClick={() => onRemoveBookmark(player.id)}
                      className="p-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-300 transition-colors cursor-pointer shadow-xs"
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
          <div className="p-3.5 border-t border-gray-200 bg-gray-50 flex items-center justify-between gap-2 flex-wrap">
            <button
              onClick={onClearAllBookmarks}
              className="px-3 py-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-mono font-bold border border-rose-300 transition-colors cursor-pointer"
            >
              전체 비우기
            </button>

            <button
              onClick={handleCopyShortlistText}
              className="px-4 py-1.5 rounded-lg bg-gray-900 hover:bg-gray-800 text-white font-bold text-xs font-mono flex items-center gap-1.5 shadow-sm transition-all cursor-pointer ml-auto"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span>복사 완료!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-amber-400" />
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
