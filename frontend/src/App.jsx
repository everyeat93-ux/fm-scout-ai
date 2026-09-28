import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { 
  Activity, Search, Compass, Shield, Sparkles, Layers, Sliders, 
  Download, HelpCircle, ArrowRight, CheckCircle2, User, Trophy, Eye, BookOpen, RefreshCw, Target, Star, Lock, Unlock, Key,
  Menu, X, ChevronLeft, ChevronRight
} from 'lucide-react';
import TargetSelector from './components/TargetSelector';
import FilterControls from './components/FilterControls';
import ScoutReportCard from './components/ScoutReportCard';
import ComparisonArena from './components/ComparisonArena';
import LegalModal from './components/LegalModal';
import MetricGuideModal from './components/MetricGuideModal';
import ShortlistModal from './components/ShortlistModal';
import { API_BASE } from './apiConfig';

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
  "Hungary": "🇭🇺",
  "Ghana": "🇬🇭",
  "Ecuador": "🇪🇨",
  "Senegal": "🇸🇳",
  "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
  "Mali": "🇲🇱",
  "Cameroon": "🇨🇲",
  "Turkey": "🇹🇷",
  "Switzerland": "🇨🇭",
  "Poland": "🇵🇱",
  "Serbia": "🇷🇸",
  "Nigeria": "🇳🇬",
  "Guinea": "🇬🇳",
  "Ivory Coast": "🇨🇮",
  "Greece": "🇬🇷",
  "Saudi Arabia": "🇸🇦"
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

export default function App() {
  const [players, setPlayers] = useState([]);
  const [archetypes, setArchetypes] = useState([]);
  const [targetPlayerId, setTargetPlayerId] = useState("p_son");
  const [targetPlayer, setTargetPlayer] = useState(null);
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  
  // Similarity Engine Settings
  const [algorithm, setAlgorithm] = useState("hybrid");
  const [hybridBalance, setHybridBalance] = useState(0.5);
  const [sequentialCutoff, setSequentialCutoff] = useState(80.0);
  const [positionMatch, setPositionMatch] = useState("group");
  const [maxMarketValue, setMaxMarketValue] = useState(null);
  const [maxAge, setMaxAge] = useState(null);
  const [leagueTier, setLeagueTier] = useState(null);
  const [customWeights, setCustomWeights] = useState({
    vision: 1.0,
    striking: 1.0,
    dribble: 1.0,
    defense: 1.0,
    physical: 1.0
  });

  // Results State
  const [scoutResults, setScoutResults] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [quickFilter, setQuickFilter] = useState("all"); // 'all', 'gems', 'u23', 'top5', 'kleague'
  const [mobileTab, setMobileTab] = useState("candidates"); // 'target', 'candidates', 'report', 'arena'

  // Shortlist Bookmarks State (with LocalStorage persistence)
  const [bookmarkedPlayerIds, setBookmarkedPlayerIds] = useState(() => {
    try {
      const saved = localStorage.getItem('fm_scout_bookmarks');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });
  const [isShortlistOpen, setIsShortlistOpen] = useState(false);

  const toggleBookmark = useCallback((playerId) => {
    setBookmarkedPlayerIds((prev) => {
      const next = prev.includes(playerId)
        ? prev.filter((id) => id !== playerId)
        : [...prev, playerId];
      try {
        localStorage.setItem('fm_scout_bookmarks', JSON.stringify(next));
      } catch (e) {}
      return next;
    });
  }, []);

  const clearAllBookmarks = useCallback(() => {
    setBookmarkedPlayerIds([]);
    try {
      localStorage.removeItem('fm_scout_bookmarks');
    } catch (e) {}
  }, []);

  // UI Modes
  const [isCompareArenaOpen, setIsCompareArenaOpen] = useState(false);
  const [comparePlayerAId, setComparePlayerAId] = useState("p_son");
  const [comparePlayerBId, setComparePlayerBId] = useState("p_stengs");
  const [isLegalModalOpen, setIsLegalModalOpen] = useState(false);
  const [isMetricGuideOpen, setIsMetricGuideOpen] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncNotification, setSyncNotification] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Quick Filter Slider Ref & Drag Handlers
  const quickFiltersRef = useRef(null);
  const [isFilterDragging, setIsFilterDragging] = useState(false);
  const [filterStartX, setFilterStartX] = useState(0);
  const [filterScrollLeft, setFilterScrollLeft] = useState(0);

  const handleScrollFilters = (direction) => {
    if (quickFiltersRef.current) {
      const scrollAmount = direction === 'left' ? -180 : 180;
      quickFiltersRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  const handleFilterMouseDown = (e) => {
    if (!quickFiltersRef.current) return;
    setIsFilterDragging(true);
    setFilterStartX(e.pageX - quickFiltersRef.current.offsetLeft);
    setFilterScrollLeft(quickFiltersRef.current.scrollLeft);
  };

  const handleFilterMouseMove = (e) => {
    if (!isFilterDragging || !quickFiltersRef.current) return;
    e.preventDefault();
    const x = e.pageX - quickFiltersRef.current.offsetLeft;
    const walk = (x - filterStartX) * 1.5;
    quickFiltersRef.current.scrollLeft = filterScrollLeft - walk;
  };

  const handleFilterMouseUpOrLeave = () => {
    setIsFilterDragging(false);
  };

  // Admin Access Control
  const [adminKey, setAdminKey] = useState(() => localStorage.getItem('fm_admin_key') || '');
  const [isAdmin, setIsAdmin] = useState(() => !!localStorage.getItem('fm_admin_key'));
  const [isAdminModalOpen, setIsAdminModalOpen] = useState(false);
  const [adminPasswordInput, setAdminPasswordInput] = useState('');

  // Check URL query parameters on mount (?admin=KEY or ?key=KEY)
  useEffect(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const keyFromUrl = params.get('admin') || params.get('key');
      if (keyFromUrl) {
        setAdminKey(keyFromUrl);
        setIsAdmin(true);
        localStorage.setItem('fm_admin_key', keyFromUrl);
      }
    } catch (e) {}
  }, []);

  const handleAdminLogin = (e) => {
    e?.preventDefault();
    const cleanKey = adminPasswordInput.trim();
    if (cleanKey) {
      setAdminKey(cleanKey);
      setIsAdmin(true);
      localStorage.setItem('fm_admin_key', cleanKey);
      setIsAdminModalOpen(false);
      setSyncNotification({
        type: 'success',
        message: '🔒 관리자 권한이 활성화되었습니다. 실시간 동기화 버튼이 잠금 해제되었습니다.'
      });
    }
  };

  const handleAdminLogout = () => {
    setAdminKey('');
    setIsAdmin(false);
    localStorage.removeItem('fm_admin_key');
    setSyncNotification({
      type: 'info',
      message: '🔒 관리자 권한이 비활성화되었습니다.'
    });
  };

  // Initial Fetch: Players & Archetypes
  const fetchInitialData = useCallback(async () => {
    try {
      const [playersRes, archRes] = await Promise.all([
        fetch(`${API_BASE}/api/players?limit=1000`),
        fetch(`${API_BASE}/api/archetypes`)
      ]);
      const pData = await playersRes.json();
      const aData = await archRes.json();
      setPlayers(pData.players || []);
      setArchetypes(aData.archetypes || []);
    } catch (err) {
      console.error("Initial load error:", err);
    }
  }, []);

  useEffect(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  // Handle Live Data Sync (Admin Only)
  const handleLiveSync = async () => {
    if (isSyncing) return;
    setIsSyncing(true);
    setSyncNotification({ type: 'info', message: '⚽ 실시간 경기 스탯 및 Wyscout 레이더 지표 동기화 중...' });
    try {
      const res = await fetch(`${API_BASE}/api/admin/sync-live-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Key': adminKey || 'scout2026'
        }
      });
      const data = await res.json();
      if (res.ok && data.status === 'success') {
        setSyncNotification({
          type: 'success',
          message: `✅ 실시간 데이터 동기화 완료! ${data.live_stats_fetched}명 선수의 최신 경기 스탯이 갱신되었습니다.`
        });
        await fetchInitialData();
        runScouting();
      } else {
        setSyncNotification({ type: 'error', message: `❌ 동기화 실패: ${data.detail || '관리자 권한 오류'}` });
      }
    } catch (err) {
      setSyncNotification({ type: 'error', message: `❌ 동기화 요청 실패: ${err.message}` });
    } finally {
      setIsSyncing(false);
      setTimeout(() => setSyncNotification(null), 6000);
    }
  };

  // Fetch Target Player and Run Similarity Search
  const runScouting = useCallback(async () => {
    if (!targetPlayerId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/scout/similar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_player_id: targetPlayerId,
          algorithm,
          hybrid_balance: hybridBalance,
          sequential_cutoff: sequentialCutoff,
          position_match: positionMatch,
          max_age: maxAge,
          max_market_value: maxMarketValue,
          league_tier: leagueTier,
          limit: 20,
          custom_weights: customWeights
        })
      });

      const data = await res.json();
      if (data.target_player) {
        setTargetPlayer(data.target_player);
        const results = data.results || [];
        setScoutResults(results);
        if (results && results.length > 0) {
          setSelectedCandidate(results[0]);
        } else {
          setSelectedCandidate(null);
        }
      }
    } catch (err) {
      console.error("Scouting search error:", err);
    } finally {
      setLoading(false);
    }
  }, [targetPlayerId, algorithm, hybridBalance, sequentialCutoff, positionMatch, maxMarketValue, maxAge, leagueTier, customWeights]);

  useEffect(() => {
    runScouting();
  }, [runScouting]);

  // Dynamic 1-Click Quick Filtering
  const filteredScoutResults = useMemo(() => {
    if (quickFilter === 'gems') {
      return scoutResults.filter(r => (r.player.market_value_eur <= 25) || (r.gem_score && r.gem_score >= 80));
    }
    if (quickFilter === 'u23') {
      return scoutResults.filter(r => r.player.age <= 23);
    }
    if (quickFilter === 'top5') {
      return scoutResults.filter(r => ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1'].includes(r.player.league));
    }
    if (quickFilter === 'kleague') {
      return scoutResults.filter(r => (r.player.league && r.player.league.includes('K-League')) || r.player.nationality === 'South Korea');
    }
    return scoutResults;
  }, [scoutResults, quickFilter]);

  const handleResetFilters = () => {
    setAlgorithm("hybrid");
    setHybridBalance(0.5);
    setSequentialCutoff(80.0);
    setPositionMatch("group");
    setMaxMarketValue(null);
    setMaxAge(null);
    setLeagueTier(null);
    setQuickFilter("all");
    setCustomWeights({ vision: 1.0, striking: 1.0, dribble: 1.0, defense: 1.0, physical: 1.0 });
  };

  const handleSelectCandidate = (item) => {
    setSelectedCandidate(item);
    setMobileTab('report'); // Seamlessly switches view to report on mobile
  };

  const handleOpen1v1Compare = (pA, pB) => {
    setComparePlayerAId(pA || targetPlayerId);
    setComparePlayerBId(pB || (selectedCandidate?.player?.id || "p_stengs"));
    setIsCompareArenaOpen(true);
    setMobileTab('arena');
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] text-gray-900 flex flex-col font-sans">
      {/* Top Tactical Navigation Bar (Clean Light Theme) */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200 px-3 sm:px-6 lg:px-8 py-2.5 sm:py-3.5 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-2">
          {/* Logo & Subtitle */}
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-gray-900 p-0.5 shadow-sm shrink-0">
              <div className="w-full h-full bg-gray-900 rounded-[6px] sm:rounded-[7px] flex items-center justify-center">
                <Activity className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400" />
              </div>
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="font-mono font-extrabold text-sm sm:text-base tracking-tight text-gray-950 whitespace-nowrap">
                  FM SCOUT <span className="text-emerald-600">AI</span>
                </span>
                <button
                  onClick={() => setIsAdminModalOpen(true)}
                  title={isAdmin ? "관리자 모드 활성화됨 (클릭하여 설정)" : "관리자 인증 (클릭)"}
                  className={`px-1.5 py-0.5 rounded text-[9px] sm:text-[10px] font-mono font-bold border shrink-0 transition-all cursor-pointer flex items-center gap-1 ${
                    isAdmin 
                      ? 'bg-purple-100 text-purple-900 border-purple-300 shadow-sm' 
                      : 'bg-gray-100 text-gray-700 border-gray-300 hover:border-gray-400'
                  }`}
                >
                  {isAdmin && <Lock className="w-2.5 h-2.5 text-purple-600" />}
                  <span>v2.4 {isAdmin ? '(ADMIN)' : ''}</span>
                </button>
              </div>
              <p className="text-[10px] font-mono text-gray-500 hidden sm:block truncate">
                Wyscout / Metrica Nexus Tactical Engine • 100% Real Football Database
              </p>
            </div>
          </div>

          {/* Desktop Action Toolbar (hidden on mobile) */}
          <div className="hidden sm:flex items-center gap-2.5 shrink-0">
            {/* Live Sync button ONLY rendered when isAdmin is true */}
            {isAdmin && (
              <div className="flex items-center gap-1 bg-purple-50 p-0.5 rounded-lg border border-purple-200">
                <button
                  onClick={handleLiveSync}
                  disabled={isSyncing}
                  className={`flex items-center gap-1 px-2.5 py-1.5 rounded-md text-[11px] sm:text-xs font-mono font-bold transition-all shadow-sm whitespace-nowrap cursor-pointer ${
                    isSyncing
                      ? 'bg-purple-200 text-purple-800 animate-pulse'
                      : 'bg-purple-600 hover:bg-purple-700 text-white'
                  }`}
                  title="FotMob / Wyscout 실시간 경기 스탯 & 5각 레이더 지표 자동 갱신 (관리자 전용)"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin text-white' : 'text-white'}`} />
                  <span>{isSyncing ? '동기화 중...' : '⚡ 실시간 동기화'}</span>
                </button>
                <button
                  onClick={handleAdminLogout}
                  title="관리자 모드 잠금 (로그아웃)"
                  className="p-1 hover:bg-purple-100 rounded text-purple-700 transition-colors cursor-pointer"
                >
                  <Unlock className="w-3.5 h-3.5" />
                </button>
              </div>
            )}

            <button
              onClick={() => setIsShortlistOpen(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 text-xs font-mono font-bold border border-amber-300 transition-all shadow-xs whitespace-nowrap cursor-pointer"
            >
              <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
              <span>쇼트리스트 ({bookmarkedPlayerIds.length})</span>
            </button>

            <button
              onClick={() => setIsMetricGuideOpen(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-900 text-xs font-mono font-bold border border-emerald-300 transition-all shadow-xs whitespace-nowrap cursor-pointer"
            >
              <BookOpen className="w-3.5 h-3.5 text-emerald-700" />
              <span>전술 가이드</span>
            </button>

            <button
              onClick={() => setIsCompareArenaOpen(!isCompareArenaOpen)}
              className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono transition-all whitespace-nowrap cursor-pointer border ${
                isCompareArenaOpen
                  ? 'bg-purple-600 text-white font-bold shadow-sm border-purple-600'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 shadow-xs'
              }`}
            >
              <Layers className="w-3.5 h-3.5 text-purple-600" />
              <span>1v1 비교 아레나</span>
            </button>

            <button
              onClick={() => setIsLegalModalOpen(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-white hover:bg-gray-100 text-gray-600 hover:text-gray-900 text-xs font-mono border border-gray-300 transition-colors whitespace-nowrap cursor-pointer shadow-xs"
            >
              <Shield className="w-3.5 h-3.5 text-gray-500" />
              <span>라이선스</span>
            </button>
          </div>

          {/* Mobile Right: Bookmark Count & Hamburger Menu Button (Clean & Zero-Clipping) */}
          <div className="flex sm:hidden items-center gap-1.5 shrink-0">
            <button
              onClick={() => setIsShortlistOpen(true)}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 text-xs font-mono font-bold border border-amber-300 shadow-xs cursor-pointer"
              title="관심 선수 쇼트리스트"
            >
              <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
              <span>{bookmarkedPlayerIds.length}</span>
            </button>

            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className={`p-2 rounded-xl border-2 transition-all cursor-pointer shadow-xs ${
                isMobileMenuOpen 
                  ? 'bg-gray-900 border-gray-900 text-white' 
                  : 'bg-white border-gray-900 text-gray-950 hover:bg-gray-100'
              }`}
              aria-label="전체 메뉴 열기"
            >
              {isMobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu Drawer */}
        {isMobileMenuOpen && (
          <div className="sm:hidden border-t border-gray-200 bg-white p-3.5 shadow-xl animate-fadeIn flex flex-col gap-2 z-40">
            <div className="text-[10px] font-mono font-bold text-gray-400 px-1 tracking-wider uppercase">
              전체 메뉴 & 기능 바로가기
            </div>

            <button
              onClick={() => {
                setIsCompareArenaOpen(true);
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center justify-between p-2.5 rounded-xl bg-purple-50 hover:bg-purple-100 text-purple-900 border border-purple-200 font-mono font-bold text-xs transition-colors cursor-pointer text-left"
            >
              <span className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-purple-700" />
                <span>1v1 정밀 비교 아레나</span>
              </span>
              <ChevronRight className="w-4 h-4 text-purple-500" />
            </button>

            <button
              onClick={() => {
                setIsShortlistOpen(true);
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center justify-between p-2.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 font-mono font-bold text-xs transition-colors cursor-pointer text-left"
            >
              <span className="flex items-center gap-2">
                <Star className="w-4 h-4 fill-amber-500 text-amber-500" />
                <span>관심 선수 쇼트리스트</span>
              </span>
              <span className="px-2 py-0.5 rounded-full bg-amber-200 text-amber-950 text-[10px] font-bold">
                {bookmarkedPlayerIds.length}명
              </span>
            </button>

            <button
              onClick={() => {
                setIsMetricGuideOpen(true);
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center justify-between p-2.5 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-200 font-mono font-bold text-xs transition-colors cursor-pointer text-left"
            >
              <span className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-emerald-700" />
                <span>5대 전술 축 & 지표 가이드</span>
              </span>
              <ChevronRight className="w-4 h-4 text-emerald-500" />
            </button>

            <button
              onClick={() => {
                setIsLegalModalOpen(true);
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center justify-between p-2.5 rounded-xl bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 font-mono font-bold text-xs transition-colors cursor-pointer text-left"
            >
              <span className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-gray-500" />
                <span>오픈 데이터 & 라이선스 고지</span>
              </span>
              <ChevronRight className="w-4 h-4 text-gray-400" />
            </button>

            {isAdmin && (
              <button
                onClick={() => {
                  handleLiveSync();
                  setIsMobileMenuOpen(false);
                }}
                disabled={isSyncing}
                className="flex items-center justify-between p-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-mono font-bold text-xs mt-1 shadow-sm cursor-pointer text-left"
              >
                <span className="flex items-center gap-2">
                  <RefreshCw className={`w-4 h-4 ${isSyncing ? 'animate-spin' : ''}`} />
                  <span>실시간 데이터 동기화 (관리자)</span>
                </span>
                <span className="text-[9px] bg-purple-800 px-2 py-0.5 rounded font-bold">ADMIN</span>
              </button>
            )}
          </div>
        )}

        {/* Live Sync Notification Toast */}
        {syncNotification && (
          <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 mt-2">
            <div className={`px-4 py-2.5 rounded-xl text-xs font-mono flex items-center justify-between border-2 shadow-sm ${
              syncNotification.type === 'success'
                ? 'bg-emerald-50 border-emerald-400 text-emerald-950 font-bold'
                : syncNotification.type === 'error'
                ? 'bg-rose-50 border-rose-400 text-rose-950 font-bold'
                : 'bg-purple-50 border-purple-400 text-purple-950 font-bold'
            }`}>
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>{syncNotification.message}</span>
              </div>
              <button 
                onClick={() => setSyncNotification(null)}
                className="text-gray-500 hover:text-gray-900 ml-3 text-xs cursor-pointer font-bold"
              >
                ✕
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 flex-1 flex flex-col gap-4 sm:gap-6 pb-20 sm:pb-6">
        {/* 1v1 Compare Arena View (if opened) */}
        {isCompareArenaOpen ? (
          <ComparisonArena
            players={players}
            initialPlayerAId={comparePlayerAId}
            initialPlayerBId={comparePlayerBId}
            onClose={() => {
              setIsCompareArenaOpen(false);
              setMobileTab('candidates');
            }}
          />
        ) : (
          <>
            {/* Intuitive 3-Step Scouting Workflow Guide Bar */}
            <div className="bg-white border-2 border-gray-900 rounded-2xl p-2.5 sm:p-3.5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-2.5 text-xs font-mono">
              <div className="flex items-center justify-between gap-2 shrink-0">
                <div className="flex items-center gap-2">
                  <span className="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-purple-600 text-white font-bold flex items-center justify-center text-[10px] sm:text-xs shadow-xs">💡</span>
                  <span className="font-black text-gray-950 text-xs sm:text-sm">스카우팅 3단계 진행:</span>
                </div>
                <span className="sm:hidden text-[10px] text-purple-700 font-bold bg-purple-50 px-2 py-0.5 rounded-full border border-purple-200">
                  {mobileTab === 'target' ? 'Step 1' : mobileTab === 'candidates' ? 'Step 2' : 'Step 3'}
                </span>
              </div>

              {/* Mobile 3-Column Equal Grid: ZERO Clipping, 100% fits on any phone! */}
              <div className="grid grid-cols-3 gap-1.5 sm:hidden w-full">
                {/* Step 1 */}
                <button
                  onClick={() => {
                    setIsCompareArenaOpen(false);
                    setMobileTab('target');
                  }}
                  className={`flex flex-col items-center justify-center py-2 px-1 rounded-xl border text-[11px] font-mono transition-all cursor-pointer ${
                    !isCompareArenaOpen && mobileTab === 'target'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-xs'
                      : 'bg-purple-50/60 border-purple-200 text-purple-900 font-medium'
                  }`}
                >
                  <span className="font-bold">① 타깃</span>
                  <span className="text-[9px] truncate max-w-[85px]">{targetPlayer?.korean_name || targetPlayer?.name}</span>
                </button>

                {/* Step 2 */}
                <button
                  onClick={() => {
                    setIsCompareArenaOpen(false);
                    setMobileTab('candidates');
                  }}
                  className={`flex flex-col items-center justify-center py-2 px-1 rounded-xl border text-[11px] font-mono transition-all cursor-pointer ${
                    !isCompareArenaOpen && mobileTab === 'candidates'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-xs'
                      : 'bg-gray-50 border-gray-200 text-gray-700 font-medium'
                  }`}
                >
                  <span className="font-bold">② AI 추천</span>
                  <span className="text-[9px]">{filteredScoutResults.length}명 발견</span>
                </button>

                {/* Step 3 */}
                <button
                  onClick={() => {
                    setIsCompareArenaOpen(false);
                    setMobileTab('report');
                  }}
                  className={`flex flex-col items-center justify-center py-2 px-1 rounded-xl border text-[11px] font-mono transition-all cursor-pointer ${
                    !isCompareArenaOpen && mobileTab === 'report'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-xs'
                      : 'bg-gray-50 border-gray-200 text-gray-700 font-medium'
                  }`}
                >
                  <span className="font-bold">③ 1v1 카드</span>
                  <span className="text-[9px]">인포그래픽</span>
                </button>
              </div>

              {/* Desktop / Tablet Horizontal Workflow Bar */}
              <div className="hidden sm:flex items-center gap-1 sm:gap-2 overflow-x-auto no-scrollbar py-0.5 w-full md:w-auto">
                {/* Step 1 */}
                <button
                  onClick={() => {
                    setIsCompareArenaOpen(false);
                    setMobileTab('target');
                  }}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border transition-all cursor-pointer whitespace-nowrap text-xs ${
                    !isCompareArenaOpen && mobileTab === 'target'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-xs'
                      : 'bg-purple-50/70 border-purple-200 text-purple-900 hover:bg-purple-100 font-medium'
                  }`}
                >
                  <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    !isCompareArenaOpen && mobileTab === 'target' ? 'bg-white/20 text-white' : 'bg-purple-200 text-purple-900'
                  }`}>1</span>
                  <span>타깃: <strong>{targetPlayer?.korean_name || targetPlayer?.name}</strong></span>
                </button>

                <span className="text-gray-400 text-xs shrink-0">➔</span>

                {/* Step 2 */}
                <button
                  onClick={() => {
                    setIsCompareArenaOpen(false);
                    setMobileTab('candidates');
                  }}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border transition-all cursor-pointer whitespace-nowrap text-xs ${
                    !isCompareArenaOpen && mobileTab === 'candidates'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-xs'
                      : 'bg-gray-100 border-gray-200 text-gray-700 hover:bg-gray-200 font-medium'
                  }`}
                >
                  <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    !isCompareArenaOpen && mobileTab === 'candidates' ? 'bg-white/20 text-white' : 'bg-gray-300 text-gray-800'
                  }`}>2</span>
                  <span>AI 추천 ({filteredScoutResults.length}명)</span>
                </button>

                <span className="text-gray-400 text-xs shrink-0">➔</span>

                {/* Step 3 */}
                <button
                  onClick={() => {
                    setIsCompareArenaOpen(false);
                    setMobileTab('report');
                  }}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border transition-all cursor-pointer whitespace-nowrap text-xs ${
                    !isCompareArenaOpen && mobileTab === 'report'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-xs'
                      : 'bg-gray-100 border-gray-200 text-gray-700 hover:bg-gray-200 font-medium'
                  }`}
                >
                  <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    !isCompareArenaOpen && mobileTab === 'report' ? 'bg-white/20 text-white' : 'bg-gray-300 text-gray-800'
                  }`}>3</span>
                  <span>카드 & 1v1</span>
                </button>
              </div>
            </div>

            {/* Target Player Selector & Presets (Always on Desktop, shown on Mobile if tab is 'target' or default) */}
            <div className={`flex flex-col gap-4 ${mobileTab === 'target' ? 'block' : 'hidden sm:block'}`}>
              <TargetSelector
                players={players}
                selectedTargetId={targetPlayerId}
                targetPlayer={targetPlayer}
                onSelectTarget={(id) => {
                  setTargetPlayerId(id);
                  setMobileTab('candidates');
                }}
                archetypes={archetypes}
              />

              {/* Mobile Target Summary & Next Step Call to Action (Prevents empty void on mobile) */}
              <div className="sm:hidden flex flex-col gap-3 p-4 rounded-2xl bg-gradient-to-br from-purple-50 via-white to-amber-50 border-2 border-gray-900 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-gray-700">현재 스카우팅 기준 선수</span>
                  <span className="px-2 py-0.5 rounded bg-purple-100 text-purple-900 font-bold text-[10px] font-mono border border-purple-200">
                    {targetPlayer?.primary_pos}
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-white border-2 border-purple-300 flex items-center justify-center text-xl shadow-xs shrink-0">
                    {countryFlags[targetPlayer?.nationality] || "🌐"}
                  </div>
                  <div className="min-w-0 flex-1">
                    <h3 className="text-base font-black text-gray-950 truncate">
                      {targetPlayer?.korean_name || targetPlayer?.name}
                    </h3>
                    <p className="text-xs text-gray-600 font-mono mt-0.5 truncate">
                      {targetPlayer?.club} • {targetPlayer?.league} • €{targetPlayer?.market_value_eur}M
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => setMobileTab('candidates')}
                  className="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs font-mono shadow-md flex items-center justify-center gap-2 cursor-pointer active:scale-95 transition-all"
                >
                  <Sparkles className="w-4 h-4 text-amber-300" />
                  <span>이 선수와 닮은 추천 선수 ({filteredScoutResults.length}명) 보기 ➔</span>
                </button>

                <p className="text-[11px] text-gray-500 font-mono text-center">
                  💡 다른 선수를 찾으시려면 위 빠른 프리셋 버튼이나 검색창을 이용하세요!
                </p>
              </div>

              {/* Collapsible Filter Toggle Bar (Clean White Theme) */}
              <div className="flex items-center justify-between">
                <button
                  onClick={() => setShowFilterPanel(!showFilterPanel)}
                  className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white hover:bg-gray-100 border-2 border-gray-900 text-xs font-mono font-bold text-gray-900 transition-all cursor-pointer shadow-xs"
                >
                  <Sliders className="w-3.5 h-3.5 text-purple-700" />
                  <span>
                    {showFilterPanel ? '▲ 세부 검색 필터 닫기' : '▼ 세부 필터 & AI 가중치 설정'}
                  </span>
                </button>

                <div className="text-[11px] font-mono text-gray-500 hidden sm:block">
                  ⚡ 100% 현역 실데이터 AI 전술 스카우팅 엔진
                </div>
              </div>

              {/* Tactical Filter Controls Panel */}
              {showFilterPanel && (
                <FilterControls
                  algorithm={algorithm}
                  setAlgorithm={setAlgorithm}
                  hybridBalance={hybridBalance}
                  setHybridBalance={setHybridBalance}
                  sequentialCutoff={sequentialCutoff}
                  setSequentialCutoff={setSequentialCutoff}
                  positionMatch={positionMatch}
                  setPositionMatch={setPositionMatch}
                  maxMarketValue={maxMarketValue}
                  setMaxMarketValue={setMaxMarketValue}
                  maxAge={maxAge}
                  setMaxAge={setMaxAge}
                  leagueTier={leagueTier}
                  setLeagueTier={setLeagueTier}
                  customWeights={customWeights}
                  setCustomWeights={setCustomWeights}
                  onResetFilters={handleResetFilters}
                  onRunScouting={runScouting}
                  loading={loading}
                />
              )}
            </div>

            {/* 1-Second One-Click Quick Filter Chips Bar with Smooth Slide & Drag Support */}
            <div className="relative flex items-center w-full py-1">
              {/* Left Slide Arrow */}
              <button
                onClick={() => handleScrollFilters('left')}
                className="flex items-center justify-center w-7 h-7 rounded-full bg-white hover:bg-gray-100 border-2 border-gray-900 shadow-xs text-gray-900 shrink-0 mr-1.5 cursor-pointer transition-all active:scale-90 z-10"
                title="이전 필터 보기"
                aria-label="이전 필터"
              >
                <ChevronLeft className="w-3.5 h-3.5 stroke-[2.5]" />
              </button>

              {/* Horizontal Scrollable Track */}
              <div
                ref={quickFiltersRef}
                onMouseDown={handleFilterMouseDown}
                onMouseMove={handleFilterMouseMove}
                onMouseUp={handleFilterMouseUpOrLeave}
                onMouseLeave={handleFilterMouseUpOrLeave}
                className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1 w-full scroll-smooth select-none cursor-grab active:cursor-grabbing"
              >
                <span className="text-[11px] font-mono text-gray-500 shrink-0 mr-1 hidden sm:inline font-bold">⚡ 퀵 필터:</span>
                
                <button
                  onClick={() => setQuickFilter('all')}
                  className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 cursor-pointer border ${
                    quickFilter === 'all'
                      ? 'bg-gray-900 border-gray-900 text-white font-bold shadow-sm'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100 shadow-xs'
                  }`}
                >
                  ✨ 전체 ({scoutResults.length})
                </button>

                <button
                  onClick={() => setQuickFilter('gems')}
                  className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 flex items-center gap-1 cursor-pointer border ${
                    quickFilter === 'gems'
                      ? 'bg-amber-500 border-amber-500 text-white font-bold shadow-sm'
                      : 'bg-white text-amber-900 border-amber-300 hover:bg-amber-50 shadow-xs'
                  }`}
                >
                  <Sparkles className="w-3 h-3 text-amber-500" />
                  <span>💎 가성비 진주 (≤€25M)</span>
                </button>

                <button
                  onClick={() => setQuickFilter('u23')}
                  className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 flex items-center gap-1 cursor-pointer border ${
                    quickFilter === 'u23'
                      ? 'bg-blue-600 border-blue-600 text-white font-bold shadow-sm'
                      : 'bg-white text-blue-900 border-blue-300 hover:bg-blue-50 shadow-xs'
                  }`}
                >
                  <span>🌟 U-23 특급 유망주</span>
                </button>

                <button
                  onClick={() => setQuickFilter('top5')}
                  className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 cursor-pointer border ${
                    quickFilter === 'top5'
                      ? 'bg-purple-600 border-purple-600 text-white font-bold shadow-sm'
                      : 'bg-white text-purple-900 border-purple-300 hover:bg-purple-50 shadow-xs'
                  }`}
                >
                  <span>🇪🇺 유럽 5대 리그</span>
                </button>

                <button
                  onClick={() => setQuickFilter('kleague')}
                  className={`px-3 py-1.5 rounded-full text-xs font-mono transition-all shrink-0 cursor-pointer border ${
                    quickFilter === 'kleague'
                      ? 'bg-rose-600 border-rose-600 text-white font-bold shadow-sm'
                      : 'bg-white text-rose-900 border-rose-300 hover:bg-rose-50 shadow-xs'
                  }`}
                >
                  <span>🇰🇷 K리그 보석</span>
                </button>
              </div>

              {/* Right Slide Arrow */}
              <button
                onClick={() => handleScrollFilters('right')}
                className="flex items-center justify-center w-7 h-7 rounded-full bg-white hover:bg-gray-100 border-2 border-gray-900 shadow-xs text-gray-900 shrink-0 ml-1.5 cursor-pointer transition-all active:scale-90 z-10"
                title="다음 필터 더보기"
                aria-label="다음 필터"
              >
                <ChevronRight className="w-3.5 h-3.5 stroke-[2.5]" />
              </button>
            </div>

            {/* Dashboard Workspace */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* Left Column (7 cols): Hero Scout Report Card */}
              <div className={`lg:col-span-7 flex flex-col gap-4 ${mobileTab === 'report' ? 'block' : 'hidden sm:block'}`}>
                {selectedCandidate && targetPlayer ? (
                  <ScoutReportCard
                    candidate={selectedCandidate}
                    targetPlayer={targetPlayer}
                    similarityPct={selectedCandidate.similarity_pct}
                    algorithm={algorithm}
                    onCompareDirectly={handleOpen1v1Compare}
                    isBookmarked={bookmarkedPlayerIds.includes(selectedCandidate?.player?.id)}
                    onToggleBookmark={toggleBookmark}
                  />
                ) : (
                  <div className="p-12 text-center rounded-xl bg-white border border-gray-300 text-gray-500 font-mono text-xs shadow-sm">
                    {loading ? '전술 유사도 계산 중...' : '조건에 맞는 선수가 없습니다. 필터 조건을 완화해보세요.'}
                  </div>
                )}
              </div>

              {/* Right Column (5 cols): Candidates Scouting Board (Clean White Cards) */}
              <div className={`lg:col-span-5 flex flex-col gap-3 ${mobileTab === 'candidates' ? 'block' : 'hidden sm:block'}`}>
                <div className="flex items-center justify-between px-1">
                  <div className="text-xs font-mono font-bold text-gray-900 flex items-center gap-2">
                    <Trophy className="w-3.5 h-3.5 text-amber-500" />
                    유사 선수 랭킹 ({filteredScoutResults.length}명)
                  </div>
                  <span className="text-[11px] font-mono text-gray-500">
                    정렬: 유사도 높은 순
                  </span>
                </div>

                <div className="space-y-2.5 max-h-[750px] overflow-y-auto pr-1 custom-scrollbar">
                  {loading ? (
                    <div className="p-10 text-center rounded-xl bg-white border border-purple-300 text-gray-700 font-mono text-xs flex flex-col items-center justify-center gap-3 shadow-md animate-pulse">
                      <RefreshCw className="w-7 h-7 text-purple-600 animate-spin" />
                      <div className="text-gray-900 font-bold text-sm">실시간 AI 전술 스카우팅 연산 중...</div>
                      <div className="text-[11px] text-gray-500">코사인 전술 스타일 + 유클리드 퍼포먼스 체급 종합 계산 중</div>
                    </div>
                  ) : filteredScoutResults.length === 0 ? (
                    <div className="p-8 text-center rounded-xl bg-white border border-gray-300 text-gray-500 font-mono text-xs shadow-sm">
                      조건에 일치하는 선수가 없습니다. 퀵 필터를 '전체'로 변경해보세요.
                    </div>
                  ) : (
                    filteredScoutResults.map((item) => {
                      const p = item.player;
                      const isSelected = selectedCandidate?.player?.id === p.id;
                      const isBookmarked = bookmarkedPlayerIds.includes(p.id);
                      const flag = countryFlags[p.nationality] || "🌐";
                      const isTopGem = item.gem_score && item.gem_score > 90;

                      return (
                        <div
                          key={p.id}
                          onClick={() => handleSelectCandidate(item)}
                          className={`p-3 sm:p-3.5 rounded-xl transition-all cursor-pointer border ${
                            isSelected
                              ? 'bg-purple-50/60 border-2 border-purple-600 shadow-md ring-2 ring-purple-100'
                              : 'bg-white border-gray-200 hover:border-gray-400 hover:shadow-md shadow-xs'
                          }`}
                        >
                          {/* Card Top: Identity & Match Score */}
                          <div className="flex items-start justify-between gap-2.5">
                            {/* Player Basic Info */}
                            <div className="flex items-start gap-2.5 min-w-0 flex-1">
                              <span className="text-base sm:text-lg shrink-0 mt-0.5">{flag}</span>
                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="font-bold text-gray-950 text-xs sm:text-sm tracking-tight break-keep">
                                    {p.korean_name || p.name}
                                  </span>
                                  {p.korean_name && (
                                    <span className="text-gray-500 text-[11px] font-mono shrink-0">
                                      ({p.name})
                                    </span>
                                  )}
                                  <span className="px-1.5 py-0.2 rounded bg-purple-100 text-purple-800 text-[10px] font-mono font-bold shrink-0">
                                    {p.primary_pos}
                                  </span>
                                  {isTopGem && (
                                    <span className="px-1.5 py-0.2 rounded bg-amber-100 text-amber-800 text-[10px] font-mono flex items-center gap-0.5 shrink-0 whitespace-nowrap border border-amber-200">
                                      <Sparkles className="w-2.5 h-2.5 text-amber-600" /> 진주
                                    </span>
                                  )}
                                  {item.manager_fit?.best_fit && (
                                    <span className="px-1.5 py-0.2 rounded bg-amber-50 text-amber-900 text-[10px] font-mono border border-amber-300 flex items-center gap-0.5 shrink-0 whitespace-nowrap">
                                      👑 {item.manager_fit.best_fit.name.split(' ')[0]} {item.manager_fit.best_fit.score}점
                                    </span>
                                  )}
                                </div>
                                <div className="text-[11px] text-gray-600 font-mono mt-0.5 flex items-center gap-1.5 flex-wrap break-keep">
                                  <span className="text-gray-900 font-medium">{p.club}</span>
                                  <span className="text-gray-400">•</span>
                                  <span>{p.league}</span>
                                  <span className="text-gray-400">•</span>
                                  <span>{p.age}세</span>
                                  <span className="text-gray-400">•</span>
                                  <span className="text-emerald-700 font-bold">€{p.market_value_eur}M</span>
                                </div>
                              </div>
                            </div>

                            {/* Match % & Sub-Metrics */}
                            <div className="text-right shrink-0">
                              <div className="text-base sm:text-lg font-black font-mono text-purple-700 tracking-tight">
                                {(Number(item.similarity_pct) || 0).toFixed(1)}%
                              </div>
                              <div className="text-[10px] font-mono text-gray-500 whitespace-nowrap">
                                스타일 <span className="text-purple-700 font-bold">{(Number(item.cosine_pct) || 0).toFixed(0)}%</span> • 체급 <span className="text-blue-600 font-bold">{(Number(item.euclidean_pct) || 0).toFixed(0)}%</span>
                              </div>
                            </div>
                          </div>

                          {/* AI Scout Narrative Briefing Pill */}
                          {item.ai_briefing && (
                            <div className="mt-2 text-[11px] text-gray-700 bg-gray-50 px-2.5 py-1.5 rounded-lg border border-gray-200 flex items-start gap-1.5 break-keep">
                              <span className="text-purple-700 font-mono font-bold text-[10px] shrink-0 mt-0.5">🤖 AI 코멘트</span>
                              <span className="leading-snug text-gray-700 line-clamp-2">{item.ai_briefing}</span>
                            </div>
                          )}

                          {/* Tactical 5-Pillar Clean Badges Bar */}
                          <div className="mt-2.5 pt-2 border-t border-gray-200 flex items-center justify-between gap-2 flex-wrap text-[10px] font-mono">
                            <div className="flex items-center gap-1 flex-wrap text-gray-600">
                              <span className="px-1.5 py-0.5 rounded bg-gray-100 border border-gray-200">🪄 패스 {p.vision_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-gray-100 border border-gray-200">⚽ 슈팅 {p.striking_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-gray-100 border border-gray-200">⚡ 드리블 {p.dribble_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-gray-100 border border-gray-200">🛡️ 수비 {p.defense_grade}</span>
                              <span className="px-1.5 py-0.5 rounded bg-gray-100 border border-gray-200">💪 경합 {p.physical_grade}</span>
                            </div>

                            <div className="flex items-center gap-1.5 ml-auto">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  toggleBookmark(p.id);
                                }}
                                className={`px-2 py-0.5 rounded text-[10px] font-mono border flex items-center gap-1 shrink-0 transition-colors cursor-pointer ${
                                  isBookmarked
                                    ? 'bg-amber-100 text-amber-800 border-amber-400 font-bold'
                                    : 'bg-white hover:bg-gray-100 text-gray-600 border-gray-300'
                                }`}
                                title="관심 선수 쇼트리스트에 담기"
                              >
                                <Star className={`w-2.5 h-2.5 ${isBookmarked ? 'fill-amber-500 text-amber-500' : ''}`} />
                                <span>{isBookmarked ? '찜함' : '찜'}</span>
                              </button>

                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleOpen1v1Compare(targetPlayerId, p.id);
                                }}
                                className="px-2 py-0.5 rounded bg-purple-50 hover:bg-purple-100 text-purple-700 text-[10px] font-mono font-bold border border-purple-200 flex items-center gap-1 shrink-0 transition-colors cursor-pointer"
                              >
                                <span>1v1 비교</span>
                                <ArrowRight className="w-2.5 h-2.5" />
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Floating Mobile Bottom Navigation Bar (Clean White Theme) */}
      <nav className="sm:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-xl border-t border-gray-200 px-3 py-2 flex items-center justify-around shadow-xl">
        <button
          onClick={() => {
            setIsCompareArenaOpen(false);
            setMobileTab('target');
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            mobileTab === 'target' && !isCompareArenaOpen ? 'text-purple-700 font-bold' : 'text-gray-400'
          }`}
        >
          <Target className="w-4 h-4" />
          <span>타겟</span>
        </button>

        <button
          onClick={() => {
            setIsCompareArenaOpen(false);
            setMobileTab('candidates');
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            mobileTab === 'candidates' && !isCompareArenaOpen ? 'text-purple-700 font-bold' : 'text-gray-400'
          }`}
        >
          <Trophy className="w-4 h-4" />
          <span>랭킹</span>
        </button>

        <button
          onClick={() => {
            setIsCompareArenaOpen(false);
            setMobileTab('report');
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            mobileTab === 'report' && !isCompareArenaOpen ? 'text-purple-700 font-bold' : 'text-gray-400'
          }`}
        >
          <Activity className="w-4 h-4" />
          <span>리포트</span>
        </button>

        <button
          onClick={() => setIsShortlistOpen(true)}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            bookmarkedPlayerIds.length > 0 ? 'text-amber-600 font-bold' : 'text-gray-400'
          }`}
        >
          <Star className={`w-4 h-4 ${bookmarkedPlayerIds.length > 0 ? 'fill-amber-500 text-amber-500' : ''}`} />
          <span>찜 ({bookmarkedPlayerIds.length})</span>
        </button>

        <button
          onClick={() => {
            handleOpen1v1Compare(targetPlayerId, selectedCandidate?.player?.id);
          }}
          className={`flex flex-col items-center gap-0.5 text-[10px] font-mono transition-colors cursor-pointer ${
            isCompareArenaOpen ? 'text-purple-700 font-bold' : 'text-gray-400'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>1v1</span>
        </button>
      </nav>

      {/* Footer & License Attribution Bar (Clean White) */}
      <footer className="border-t border-gray-200 bg-white py-4 px-4 lg:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-xs font-mono text-gray-500">
          <div>
            경기 전술 이벤트 통계: Wyscout Open Dataset(CC BY 4.0) 및 StatsBomb Open Data 기반 역산.
          </div>
          <div className="flex items-center gap-4 shrink-0">
            <button onClick={() => setIsLegalModalOpen(true)} className="hover:text-gray-900 underline">
              법적 고지 & 라이선스
            </button>
            <span className="text-purple-700 font-bold">FM Scout AI © 2026</span>
          </div>
        </div>
      </footer>

      {/* Shortlist Modal */}
      <ShortlistModal
        isOpen={isShortlistOpen}
        onClose={() => setIsShortlistOpen(false)}
        bookmarkedPlayerIds={bookmarkedPlayerIds}
        allPlayers={players}
        onRemoveBookmark={toggleBookmark}
        onClearAllBookmarks={clearAllBookmarks}
        onSelectAsTarget={(id) => {
          setTargetPlayerId(id);
          setMobileTab('candidates');
        }}
        onOpen1v1Compare={handleOpen1v1Compare}
        targetPlayerId={targetPlayerId}
      />

      {/* Legal & Compliance Modal */}
      <LegalModal
        isOpen={isLegalModalOpen}
        onClose={() => setIsLegalModalOpen(false)}
      />

      {/* Metric Guide & Tactical Glossary Modal */}
      <MetricGuideModal
        isOpen={isMetricGuideOpen}
        onClose={() => setIsMetricGuideOpen(false)}
      />

      {/* Admin Passcode Modal */}
      {isAdminModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white border-2 border-gray-900 rounded-2xl max-w-sm w-full p-6 shadow-2xl relative text-gray-900">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-purple-100 border border-purple-200 flex items-center justify-center text-purple-700">
                <Key className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-gray-950 font-mono font-bold text-sm">관리자 보안 인증 (Admin)</h3>
                <p className="text-[11px] text-gray-500 font-mono">실시간 데이터 동기화 관리 권한</p>
              </div>
            </div>

            <form onSubmit={handleAdminLogin} className="flex flex-col gap-4">
              <div>
                <label className="text-xs font-mono text-gray-700 font-bold block mb-1.5">
                  관리자 보안 키 (Admin Key)
                </label>
                <input
                  type="password"
                  value={adminPasswordInput}
                  onChange={(e) => setAdminPasswordInput(e.target.value)}
                  placeholder="관리자 키 입력 (기본: scout2026)"
                  className="w-full bg-gray-50 border border-gray-300 focus:border-purple-600 rounded-xl px-3 py-2 text-sm text-gray-900 font-mono outline-none"
                  autoFocus
                />
              </div>

              <div className="flex items-center justify-between gap-2 pt-2">
                {isAdmin ? (
                  <button
                    type="button"
                    onClick={handleAdminLogout}
                    className="px-3 py-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-mono font-bold border border-rose-300 cursor-pointer"
                  >
                    모드 해제
                  </button>
                ) : (
                  <div></div>
                )}
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setIsAdminModalOpen(false)}
                    className="px-3 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 hover:text-gray-900 text-xs font-mono border border-gray-300 cursor-pointer"
                  >
                    닫기
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white text-xs font-mono font-bold shadow-sm cursor-pointer"
                  >
                    인증하기
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
