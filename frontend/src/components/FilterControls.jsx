import React, { useState } from 'react';
import { Sliders, Zap, Shield, Target, Compass, Award, DollarSign, Calendar, RefreshCw, Search } from 'lucide-react';

export default function FilterControls({
  algorithm,
  setAlgorithm,
  hybridBalance = 0.5,
  setHybridBalance,
  sequentialCutoff = 80.0,
  setSequentialCutoff,
  positionMatch,
  setPositionMatch,
  maxMarketValue,
  setMaxMarketValue,
  maxAge,
  setMaxAge,
  leagueTier,
  setLeagueTier,
  customWeights,
  setCustomWeights,
  onResetFilters,
  onRunScouting,
  loading = false
}) {
  const [showAdvancedWeights, setShowAdvancedWeights] = useState(false);

  const handleWeightChange = (key, value) => {
    setCustomWeights(prev => ({
      ...prev,
      [key]: parseFloat(value)
    }));
  };

  return (
    <div className="p-4 rounded-xl bg-[#121226] border border-[#1f2240] flex flex-col gap-4">
      {/* Top Bar: Algorithm Toggle & Position Grouping */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 1. Algorithm Switcher (4 Modes: Hybrid, Sequential, Cosine, Euclidean) */}
        <div>
          <label className="text-xs font-mono font-bold text-gray-300 mb-1.5 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Compass className="w-3.5 h-3.5 text-[#00ff88]" />
              AI 유사도 알고리즘 (Algorithm)
            </span>
            <span className="text-[10px] text-[#00ff88] font-mono">
              {algorithm === 'hybrid' ? '🎯 앙상블 결합' : algorithm === 'sequential' ? '🔄 2단계 순차' : algorithm === 'cosine' ? '스타일 비율' : '체급 볼륨'}
            </span>
          </label>

          <div className="grid grid-cols-2 gap-2 bg-[#0a0a16] p-1.5 rounded-lg border border-[#1f2240]">
            <button
              onClick={() => setAlgorithm('hybrid')}
              className={`py-2 px-2.5 rounded-md text-xs font-mono transition-all flex flex-col items-start ${
                algorithm === 'hybrid'
                  ? 'bg-[#00ff88]/20 border border-[#00ff88] text-[#00ff88] font-bold shadow-glow-neon'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              <span className="text-[11px] font-bold flex items-center gap-1">
                🎯 하이브리드 앙상블 <span className="text-[9px] px-1 py-0.2 bg-[#00ff88]/20 rounded text-[#00ff88]">추천</span>
              </span>
              <span className="text-[9px] text-gray-400">스타일(코사인) + 체급(유클리드) 결합</span>
            </button>

            <button
              onClick={() => setAlgorithm('sequential')}
              className={`py-2 px-2.5 rounded-md text-xs font-mono transition-all flex flex-col items-start ${
                algorithm === 'sequential'
                  ? 'bg-[#a855f7]/20 border border-[#a855f7] text-[#c084fc] font-bold'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              <span className="text-[11px] font-bold">🔄 2단계 순차 스카우팅</span>
              <span className="text-[9px] text-gray-400">1단계 스타일 선별 → 2단계 체급순 정렬</span>
            </button>

            <button
              onClick={() => setAlgorithm('cosine')}
              className={`py-2 px-2.5 rounded-md text-xs font-mono transition-all flex flex-col items-start ${
                algorithm === 'cosine'
                  ? 'bg-[#00ff88]/20 border border-[#00ff88] text-[#00ff88] font-bold'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              <span className="text-[11px] font-bold">① 코사인 유사도</span>
              <span className="text-[9px] text-gray-400">순수 플레이스타일 비율 (가성비 진주)</span>
            </button>

            <button
              onClick={() => setAlgorithm('euclidean')}
              className={`py-2 px-2.5 rounded-md text-xs font-mono transition-all flex flex-col items-start ${
                algorithm === 'euclidean'
                  ? 'bg-[#00e5ff]/20 border border-[#00e5ff] text-[#00e5ff] font-bold'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              <span className="text-[11px] font-bold">② 유클리드 거리</span>
              <span className="text-[9px] text-gray-400">순수 절대 퍼포먼스 볼륨 (완성형 주전)</span>
            </button>
          </div>

          {/* Sub-slider for Hybrid Ensemble Balance */}
          {algorithm === 'hybrid' && setHybridBalance && (
            <div className="mt-2 p-2.5 rounded-lg bg-[#0e0e22] border border-[#1f2240] flex flex-col gap-1.5 animate-fadeIn">
              <div className="flex items-center justify-between text-[10px] font-mono">
                <span className="text-gray-400">
                  체급 볼륨 <strong className="text-[#00e5ff]">{Math.round((1 - hybridBalance) * 100)}%</strong>
                </span>
                <span className="text-white font-bold">
                  [ 앙상블 가중치 밸런스: {Math.round(hybridBalance * 100)} : {Math.round((1 - hybridBalance) * 100)} ]
                </span>
                <span className="text-gray-400">
                  스타일 비율 <strong className="text-[#00ff88]">{Math.round(hybridBalance * 100)}%</strong>
                </span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={hybridBalance}
                onChange={(e) => setHybridBalance(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-[#1f2240] rounded-lg appearance-none cursor-pointer accent-[#00ff88]"
              />
            </div>
          )}

          {/* Sub-slider for Sequential Cutoff */}
          {algorithm === 'sequential' && setSequentialCutoff && (
            <div className="mt-2 p-2.5 rounded-lg bg-[#0e0e22] border border-[#1f2240] flex flex-col gap-1.5 animate-fadeIn">
              <div className="flex items-center justify-between text-[10px] font-mono">
                <span className="text-gray-400">1단계 플레이스타일 최소 일치율 커트라인:</span>
                <span className="text-[#c084fc] font-bold font-mono">{sequentialCutoff}% 이상</span>
              </div>
              <input
                type="range"
                min="70"
                max="95"
                step="1"
                value={sequentialCutoff}
                onChange={(e) => setSequentialCutoff(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-[#1f2240] rounded-lg appearance-none cursor-pointer accent-[#c084fc]"
              />
            </div>
          )}
        </div>

        {/* 2. Position Filter (Strict vs Group vs All) */}
        <div>
          <label className="text-xs font-mono font-bold text-gray-300 mb-1.5 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-[#00e5ff]" />
              포지션 전처리 필터링 (Position Scope)
            </span>
            <span className="text-[10px] text-gray-400 font-normal">축구 도메인 왜곡 방지</span>
          </label>

          <div className="grid grid-cols-3 gap-1.5 bg-[#0a0a16] p-1 rounded-lg border border-[#1f2240]">
            <button
              onClick={() => setPositionMatch('group')}
              className={`py-2 px-2 text-center rounded-md text-xs font-mono transition-all ${
                positionMatch === 'group'
                  ? 'bg-[#181832] border border-[#00e5ff] text-[#00e5ff] font-bold'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              군집 (MF/FW/DF)
            </button>

            <button
              onClick={() => setPositionMatch('strict')}
              className={`py-2 px-2 text-center rounded-md text-xs font-mono transition-all ${
                positionMatch === 'strict'
                  ? 'bg-[#181832] border border-[#00e5ff] text-[#00e5ff] font-bold'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              엄격 (동일 포지션)
            </button>

            <button
              onClick={() => setPositionMatch('all')}
              className={`py-2 px-2 text-center rounded-md text-xs font-mono transition-all ${
                positionMatch === 'all'
                  ? 'bg-[#181832] border border-[#00e5ff] text-[#00e5ff] font-bold'
                  : 'text-gray-400 hover:text-gray-200 border border-transparent'
              }`}
            >
              전체 포지션
            </button>
          </div>
        </div>
      </div>

      {/* Sliders: Budget, Age, League Tier */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 border-t border-[#1f2240]">
        {/* Budget Max Market Value Slider */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-gray-400 flex items-center gap-1">
              <DollarSign className="w-3.5 h-3.5 text-yellow-400" />
              최대 이적료 (Budget):
            </span>
            <span className="text-[#00ff88] font-bold">
              {maxMarketValue ? `€${maxMarketValue}M 이하` : '전체 (제한없음)'}
            </span>
          </div>
          <input
            type="range"
            min="5"
            max="150"
            step="5"
            value={maxMarketValue || 150}
            onChange={(e) => {
              const val = parseInt(e.target.value);
              setMaxMarketValue(val >= 150 ? null : val);
            }}
            className="w-full accent-[#00ff88] bg-[#0a0a16] h-1.5 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-gray-400">
            <button onClick={() => setMaxMarketValue(15)} className="hover:text-white">€15M 흙속의진주</button>
            <button onClick={() => setMaxMarketValue(35)} className="hover:text-white">€35M 가성비</button>
            <button onClick={() => setMaxMarketValue(null)} className="hover:text-white">전체</button>
          </div>
        </div>

        {/* Max Age Slider (Wonderkid filter) */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-gray-400 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-[#00e5ff]" />
              최대 나이 (Age):
            </span>
            <span className="text-[#00e5ff] font-bold">
              {maxAge ? `${maxAge}세 이하` : '전체 연령'}
            </span>
          </div>
          <input
            type="range"
            min="19"
            max="35"
            step="1"
            value={maxAge || 35}
            onChange={(e) => {
              const val = parseInt(e.target.value);
              setMaxAge(val >= 35 ? null : val);
            }}
            className="w-full accent-[#00e5ff] bg-[#0a0a16] h-1.5 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-gray-400">
            <button onClick={() => setMaxAge(21)} className="hover:text-white">U-21 원더키드</button>
            <button onClick={() => setMaxAge(23)} className="hover:text-white">U-23 유망주</button>
            <button onClick={() => setMaxAge(null)} className="hover:text-white">전체</button>
          </div>
        </div>

        {/* League Scope Filter */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-gray-400 flex items-center gap-1">
              <Award className="w-3.5 h-3.5 text-purple-400" />
              리그 범위 (Leagues):
            </span>
            <span className="text-purple-300 font-bold">
              {leagueTier === 1 ? '5대 빅리그' : leagueTier === 2 || leagueTier === 3 ? '하위/세컨더리 리그' : '모든 리그'}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-1 bg-[#0a0a16] p-0.5 rounded-lg border border-[#1f2240]">
            <button
              onClick={() => setLeagueTier(null)}
              className={`py-1 text-[10px] font-mono rounded ${leagueTier === null ? 'bg-[#2a2e5c] text-white font-bold' : 'text-gray-400'}`}
            >
              전체
            </button>
            <button
              onClick={() => setLeagueTier(2)}
              className={`py-1 text-[10px] font-mono rounded ${leagueTier === 2 ? 'bg-[#2a2e5c] text-purple-300 font-bold' : 'text-gray-400'}`}
            >
              하위 리그
            </button>
            <button
              onClick={() => setLeagueTier(1)}
              className={`py-1 text-[10px] font-mono rounded ${leagueTier === 1 ? 'bg-[#2a2e5c] text-white font-bold' : 'text-gray-400'}`}
            >
              5대 빅리그
            </button>
          </div>
        </div>
      </div>

      {/* Advanced Custom Pillar Weights Toggle */}
      <div className="flex items-center justify-between pt-2 border-t border-[#1f2240]">
        <button
          onClick={() => setShowAdvancedWeights(!showAdvancedWeights)}
          className="text-[11px] font-mono text-gray-400 hover:text-white flex items-center gap-1.5"
        >
          <Sliders className="w-3 h-3 text-[#00ff88]" />
          {showAdvancedWeights ? '▼ 5대 전술 능력 가중치 접기' : '▶ 5대 전술 능력 가중치 커스텀 조정'}
        </button>

        <button
          onClick={onResetFilters}
          className="text-[11px] font-mono text-gray-400 hover:text-red-400 flex items-center gap-1 transition-colors"
        >
          <RefreshCw className="w-3 h-3" />
          필터 초기화
        </button>
      </div>

      {/* Advanced Weights Sliders */}
      {showAdvancedWeights && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 p-3 rounded-lg bg-[#0a0a16] border border-[#1f2240] text-xs font-mono">
          <div>
            <div className="text-[10px] text-gray-400 flex justify-between">
              <span>창의성 (Vision)</span>
              <span className="text-[#00ff88]">{customWeights.vision}x</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="2.0"
              step="0.1"
              value={customWeights.vision}
              onChange={(e) => handleWeightChange('vision', e.target.value)}
              className="w-full accent-[#00ff88]"
            />
          </div>

          <div>
            <div className="text-[10px] text-gray-400 flex justify-between">
              <span>슈팅 (Striking)</span>
              <span className="text-[#00ff88]">{customWeights.striking}x</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="2.0"
              step="0.1"
              value={customWeights.striking}
              onChange={(e) => handleWeightChange('striking', e.target.value)}
              className="w-full accent-[#00ff88]"
            />
          </div>

          <div>
            <div className="text-[10px] text-gray-400 flex justify-between">
              <span>드리블 (Dribble)</span>
              <span className="text-[#00ff88]">{customWeights.dribble}x</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="2.0"
              step="0.1"
              value={customWeights.dribble}
              onChange={(e) => handleWeightChange('dribble', e.target.value)}
              className="w-full accent-[#00ff88]"
            />
          </div>

          <div>
            <div className="text-[10px] text-gray-400 flex justify-between">
              <span>수비력 (Defense)</span>
              <span className="text-[#00ff88]">{customWeights.defense}x</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="2.0"
              step="0.1"
              value={customWeights.defense}
              onChange={(e) => handleWeightChange('defense', e.target.value)}
              className="w-full accent-[#00ff88]"
            />
          </div>

          <div>
            <div className="text-[10px] text-gray-400 flex justify-between">
              <span>경합력 (Physical)</span>
              <span className="text-[#00ff88]">{customWeights.physical}x</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="2.0"
              step="0.1"
              value={customWeights.physical}
              onChange={(e) => handleWeightChange('physical', e.target.value)}
              className="w-full accent-[#00ff88]"
            />
          </div>
        </div>
      )}

      {/* Search & Apply Action CTA Bar */}
      <div className="pt-3 border-t border-[#1f2240] flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="text-xs font-mono text-gray-400 flex items-center gap-1.5">
          <Zap className="w-3.5 h-3.5 text-[#00ff88]" />
          <span>설정된 필터 조건으로 <strong className="text-white font-bold">11,685명</strong> 전 세계 선수 풀을 정밀 스카우팅합니다.</span>
        </div>

        <button
          onClick={onRunScouting}
          disabled={loading}
          className={`w-full sm:w-auto py-2.5 px-6 rounded-xl font-mono text-xs font-bold transition-all flex items-center justify-center gap-2 shadow-lg ${
            loading
              ? 'bg-gray-700 text-gray-300 cursor-not-allowed opacity-80'
              : 'bg-gradient-to-r from-[#00ff88] via-[#00e5ff] to-[#00ff88] bg-[length:200%_auto] hover:bg-right text-[#0a0a16] shadow-glow-neon active:scale-95 cursor-pointer font-extrabold'
          }`}
        >
          {loading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin text-gray-300" />
              <span>11,685명 정밀 분석 중...</span>
            </>
          ) : (
            <>
              <Search className="w-4 h-4 text-black stroke-[2.5]" />
              <span>🚀 스카우팅 리포트 생성 & 검색 실행</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
