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
    <div className="p-4 sm:p-5 rounded-2xl bg-white border-2 border-gray-900 shadow-sm flex flex-col gap-4 text-gray-900 select-none">
      {/* Top Bar: Algorithm Toggle & Position Grouping */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 1. Algorithm Switcher */}
        <div>
          <label className="text-xs font-mono font-bold text-gray-800 mb-1.5 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Compass className="w-3.5 h-3.5 text-purple-600" />
              AI 유사도 알고리즘 (Algorithm)
            </span>
            <span className="text-[10px] text-purple-700 font-mono font-bold">
              {algorithm === 'hybrid' ? '🎯 앙상블 결합' : algorithm === 'sequential' ? '🔄 2단계 순차' : algorithm === 'cosine' ? '스타일 비율' : '체급 볼륨'}
            </span>
          </label>

          <div className="grid grid-cols-2 gap-2 bg-gray-50 p-1.5 rounded-xl border border-gray-300">
            <button
              onClick={() => setAlgorithm('hybrid')}
              className={`py-2 px-2.5 rounded-lg text-xs font-mono transition-all flex flex-col items-start border cursor-pointer ${
                algorithm === 'hybrid'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              <span className="text-[11px] font-bold flex items-center gap-1">
                🎯 하이브리드 앙상블 <span className="text-[9px] px-1 py-0.2 bg-emerald-100 text-emerald-800 rounded font-bold">추천</span>
              </span>
              <span className="text-[9px] text-gray-500">스타일(코사인) + 체급(유클리드) 결합</span>
            </button>

            <button
              onClick={() => setAlgorithm('sequential')}
              className={`py-2 px-2.5 rounded-lg text-xs font-mono transition-all flex flex-col items-start border cursor-pointer ${
                algorithm === 'sequential'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              <span className="text-[11px] font-bold">🔄 2단계 순차 스카우팅</span>
              <span className="text-[9px] text-gray-500">1단계 스타일 선별 → 2단계 체급순</span>
            </button>

            <button
              onClick={() => setAlgorithm('cosine')}
              className={`py-2 px-2.5 rounded-lg text-xs font-mono transition-all flex flex-col items-start border cursor-pointer ${
                algorithm === 'cosine'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              <span className="text-[11px] font-bold">① 코사인 유사도</span>
              <span className="text-[9px] text-gray-500">순수 플레이스타일 비율 (가성비 진주)</span>
            </button>

            <button
              onClick={() => setAlgorithm('euclidean')}
              className={`py-2 px-2.5 rounded-lg text-xs font-mono transition-all flex flex-col items-start border cursor-pointer ${
                algorithm === 'euclidean'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              <span className="text-[11px] font-bold">② 유클리드 거리</span>
              <span className="text-[9px] text-gray-500">순수 절대 퍼포먼스 볼륨 (완성형 주전)</span>
            </button>
          </div>

          {/* Sub-slider for Hybrid Ensemble Balance */}
          {algorithm === 'hybrid' && setHybridBalance && (
            <div className="mt-2 p-2.5 rounded-lg bg-gray-50 border border-gray-300 flex flex-col gap-1.5">
              <div className="flex items-center justify-between text-[10px] font-mono">
                <span className="text-gray-600">
                  체급 볼륨 <strong className="text-blue-700">{Math.round((1 - hybridBalance) * 100)}%</strong>
                </span>
                <span className="text-gray-900 font-bold">
                  [ 앙상블 밸런스: {Math.round(hybridBalance * 100)} : {Math.round((1 - hybridBalance) * 100)} ]
                </span>
                <span className="text-gray-600">
                  스타일 비율 <strong className="text-purple-700">{Math.round(hybridBalance * 100)}%</strong>
                </span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={hybridBalance}
                onChange={(e) => setHybridBalance(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-purple-600"
              />
            </div>
          )}

          {/* Sub-slider for Sequential Cutoff */}
          {algorithm === 'sequential' && setSequentialCutoff && (
            <div className="mt-2 p-2.5 rounded-lg bg-gray-50 border border-gray-300 flex flex-col gap-1.5">
              <div className="flex items-center justify-between text-[10px] font-mono">
                <span className="text-gray-600">1단계 플레이스타일 최소 일치율 커트라인:</span>
                <span className="text-purple-700 font-bold font-mono">{sequentialCutoff}% 이상</span>
              </div>
              <input
                type="range"
                min="70"
                max="95"
                step="1"
                value={sequentialCutoff}
                onChange={(e) => setSequentialCutoff(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-purple-600"
              />
            </div>
          )}
        </div>

        {/* 2. Position Filter */}
        <div>
          <label className="text-xs font-mono font-bold text-gray-800 mb-1.5 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-purple-600" />
              포지션 전처리 필터링 (Position Scope)
            </span>
            <span className="text-[10px] text-gray-500 font-normal">축구 도메인 왜곡 방지</span>
          </label>

          <div className="grid grid-cols-3 gap-1.5 bg-gray-50 p-1 rounded-xl border border-gray-300">
            <button
              onClick={() => setPositionMatch('group')}
              className={`py-2 px-2 text-center rounded-lg text-xs font-mono transition-all border cursor-pointer ${
                positionMatch === 'group'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              군집 (MF/FW/DF)
            </button>

            <button
              onClick={() => setPositionMatch('strict')}
              className={`py-2 px-2 text-center rounded-lg text-xs font-mono transition-all border cursor-pointer ${
                positionMatch === 'strict'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              엄격 (동일 포지션)
            </button>

            <button
              onClick={() => setPositionMatch('all')}
              className={`py-2 px-2 text-center rounded-lg text-xs font-mono transition-all border cursor-pointer ${
                positionMatch === 'all'
                  ? 'bg-purple-100 border-purple-600 text-purple-950 font-bold shadow-xs'
                  : 'bg-white text-gray-600 hover:text-gray-900 border-gray-200'
              }`}
            >
              전체 (포지션 무관)
            </button>
          </div>

          {/* Quick Real-World Constraints (Age, Market Value, League Tier) */}
          <div className="grid grid-cols-3 gap-2 mt-3 text-xs font-mono">
            {/* Max Market Value */}
            <div>
              <span className="text-[10px] text-gray-600 flex items-center gap-1 mb-1 font-bold">
                <DollarSign className="w-3 h-3 text-emerald-600" /> 최대 이적료:
              </span>
              <select
                value={maxMarketValue || ""}
                onChange={(e) => setMaxMarketValue(e.target.value ? parseFloat(e.target.value) : null)}
                className="w-full bg-gray-50 border border-gray-300 rounded-lg p-1.5 text-xs text-gray-900 focus:outline-none focus:border-purple-600"
              >
                <option value="">제한 없음 (전체)</option>
                <option value="10">€10M 이하 (초가성비)</option>
                <option value="25">€25M 이하 (중저가 보석)</option>
                <option value="50">€50M 이하 (준척급 주전)</option>
                <option value="80">€80M 이하 (빅클럽 수준)</option>
              </select>
            </div>

            {/* Max Age */}
            <div>
              <span className="text-[10px] text-gray-600 flex items-center gap-1 mb-1 font-bold">
                <Calendar className="w-3 h-3 text-blue-600" /> 최대 나이:
              </span>
              <select
                value={maxAge || ""}
                onChange={(e) => setMaxAge(e.target.value ? parseInt(e.target.value) : null)}
                className="w-full bg-gray-50 border border-gray-300 rounded-lg p-1.5 text-xs text-gray-900 focus:outline-none focus:border-purple-600"
              >
                <option value="">제한 없음 (전체)</option>
                <option value="21">21세 이하 (원더키드)</option>
                <option value="23">23세 이하 (올림픽/유망주)</option>
                <option value="26">26세 이하 (전성기 초입)</option>
                <option value="30">30세 이하 (완성형 주전)</option>
              </select>
            </div>

            {/* League Tier */}
            <div>
              <span className="text-[10px] text-gray-600 flex items-center gap-1 mb-1 font-bold">
                <Award className="w-3 h-3 text-amber-600" /> 리그 체급:
              </span>
              <select
                value={leagueTier || ""}
                onChange={(e) => setLeagueTier(e.target.value ? parseInt(e.target.value) : null)}
                className="w-full bg-gray-50 border border-gray-300 rounded-lg p-1.5 text-xs text-gray-900 focus:outline-none focus:border-purple-600"
              >
                <option value="">전체 리그</option>
                <option value="1">유럽 5대 리그만 (Tier 1)</option>
                <option value="2">5대 리그 + 포르투갈/네덜란드</option>
                <option value="3">글로벌 하위/중소 리그 포함</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Advanced Custom Pillar Weights (Collapsible) */}
      <div className="border-t border-gray-200 pt-2.5">
        <button
          onClick={() => setShowAdvancedWeights(!showAdvancedWeights)}
          className="text-xs font-mono font-bold text-gray-700 hover:text-black flex items-center gap-1.5 cursor-pointer"
        >
          <Sliders className="w-3.5 h-3.5 text-purple-600" />
          <span>전술 5대 영역 가중치 미세 조정 (Custom Pillar Weights) {showAdvancedWeights ? '접기 ▲' : '열기 ▼'}</span>
        </button>

        {showAdvancedWeights && (
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 mt-3 p-3 rounded-xl bg-gray-50 border border-gray-300 font-mono text-xs">
            {/* Vision */}
            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-gray-700">창의성 (Vision)</span>
                <span className="text-purple-700 font-bold">{customWeights.vision.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="2.5"
                step="0.1"
                value={customWeights.vision}
                onChange={(e) => handleWeightChange('vision', e.target.value)}
                className="w-full h-1 bg-gray-300 rounded appearance-none cursor-pointer accent-purple-600"
              />
            </div>

            {/* Striking */}
            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-gray-700">슈팅 (Striking)</span>
                <span className="text-rose-700 font-bold">{customWeights.striking.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="2.5"
                step="0.1"
                value={customWeights.striking}
                onChange={(e) => handleWeightChange('striking', e.target.value)}
                className="w-full h-1 bg-gray-300 rounded appearance-none cursor-pointer accent-rose-600"
              />
            </div>

            {/* Dribble */}
            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-gray-700">드리블 (Dribble)</span>
                <span className="text-amber-700 font-bold">{customWeights.dribble.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="2.5"
                step="0.1"
                value={customWeights.dribble}
                onChange={(e) => handleWeightChange('dribble', e.target.value)}
                className="w-full h-1 bg-gray-300 rounded appearance-none cursor-pointer accent-amber-600"
              />
            </div>

            {/* Defense */}
            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-gray-700">수비 (Defense)</span>
                <span className="text-blue-700 font-bold">{customWeights.defense.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="2.5"
                step="0.1"
                value={customWeights.defense}
                onChange={(e) => handleWeightChange('defense', e.target.value)}
                className="w-full h-1 bg-gray-300 rounded appearance-none cursor-pointer accent-blue-600"
              />
            </div>

            {/* Physical */}
            <div>
              <div className="flex justify-between text-[11px] mb-1">
                <span className="text-gray-700">피지컬 (Physical)</span>
                <span className="text-emerald-700 font-bold">{customWeights.physical.toFixed(1)}x</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="2.5"
                step="0.1"
                value={customWeights.physical}
                onChange={(e) => handleWeightChange('physical', e.target.value)}
                className="w-full h-1 bg-gray-300 rounded appearance-none cursor-pointer accent-emerald-600"
              />
            </div>
          </div>
        )}
      </div>

      {/* Action Footer: Reset & Re-run Scouting Button */}
      <div className="flex items-center justify-between pt-2 border-t border-gray-200">
        <button
          onClick={onResetFilters}
          className="text-xs font-mono text-gray-500 hover:text-gray-800 flex items-center gap-1 cursor-pointer transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>필터 초기화</span>
        </button>

        <button
          onClick={onRunScouting}
          disabled={loading}
          className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gray-900 hover:bg-gray-800 text-white font-bold text-xs font-mono shadow-sm transition-all cursor-pointer disabled:opacity-50"
        >
          {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Search className="w-3.5 h-3.5 text-emerald-400" />}
          <span>🚀 스카우팅 리포트 생성 & 검색 실행</span>
        </button>
      </div>
    </div>
  );
}
