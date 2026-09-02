import React from 'react';
import { ShieldCheck, FileText, Info, Award, ExternalLink, X } from 'lucide-react';

export default function LegalModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-[#121226] border border-[#2a2e5c] rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto font-sans">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg bg-[#181832] hover:bg-[#202046] text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5 border-b border-[#1f2240] pb-4">
          <div className="p-2.5 rounded-xl bg-[#00ff88]/15 text-[#00ff88] border border-[#00ff88]/30">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white font-mono">
              [ LEGAL COMPLIANCE & OPEN DATA ATTRIBUTION ]
            </h2>
            <p className="text-xs text-gray-400 font-mono">오픈 라이선스 출처 명시 및 저작권/초상권 준수 성명서</p>
          </div>
        </div>

        {/* Legal Sections */}
        <div className="space-y-4 text-xs leading-relaxed text-gray-300 font-mono">
          {/* Wyscout CC BY 4.0 */}
          <div className="p-3.5 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
            <div className="flex items-center justify-between text-[#00ff88] font-bold mb-1">
              <span className="flex items-center gap-1.5">
                <FileText className="w-4 h-4" />
                1. Wyscout Open Dataset (CC BY 4.0)
              </span>
              <span className="text-[10px] bg-[#00ff88]/15 px-2 py-0.5 rounded">CC BY 4.0</span>
            </div>
            <p className="text-gray-300 mt-1">
              "경기 전술 이벤트 통계는 Luca Pappalardo 등이 Nature Scientific Data(2019) 저널에 배포한 Wyscout Open Dataset(CC BY 4.0)을 기반으로 역산되었습니다."
            </p>
            <div className="text-[10px] text-gray-500 mt-1">
              DOI: 10.1038/s41597-019-0247-7 / Nature Scientific Data (2019)
            </div>
          </div>

          {/* StatsBomb Open Data */}
          <div className="p-3.5 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
            <div className="flex items-center justify-between text-[#00e5ff] font-bold mb-1">
              <span className="flex items-center gap-1.5">
                <FileText className="w-4 h-4" />
                2. StatsBomb Open Data Model Compliance
              </span>
              <span className="text-[10px] bg-[#00e5ff]/15 px-2 py-0.5 rounded">Open Data</span>
            </div>
            <p className="text-gray-300 mt-1">
              본 시뮬레이터에 적용된 경기당 전술 공간 행동 지표 및 기대 득점(xG) 산출 모델은 StatsBomb Open Data 가이드라인 및 공인 학술 연구 표준을 준수하여 가공되었습니다.
            </p>
          </div>

          {/* Kaggle Open Databases */}
          <div className="p-3.5 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
            <div className="flex items-center justify-between text-yellow-400 font-bold mb-1">
              <span className="flex items-center gap-1.5">
                <FileText className="w-4 h-4" />
                3. Kaggle Static Soccer Databases (ODbL & CDLA)
              </span>
              <span className="text-[10px] bg-yellow-400/15 px-2 py-0.5 rounded">ODbL / CDLA 1.0</span>
            </div>
            <ul className="list-disc list-inside space-y-1 text-gray-400 mt-1">
              <li>European Soccer Database (by Hugo Mathien) - Open Database License (ODbL)</li>
              <li>European Leagues Database (by Kamran Gayibov) - CDLA-Sharing Version 1.0</li>
            </ul>
          </div>

          {/* Portrait Rights & Trademark Protection */}
          <div className="p-3.5 rounded-xl bg-[#0a0a16] border border-[#1f2240]">
            <div className="text-purple-400 font-bold mb-1 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4" />
              4. 선수 초상권(Portrait Rights) 및 클럽 상표권 보호 조치
            </div>
            <p className="text-gray-400">
              FM Scout AI (FC Finder)는 비상업/학술 시뮬레이터 목적으로 구축되었습니다. FIFPRO 및 각 프로축구 협회의 초상권 제재 대상이 되는 실제 선수 경기 스냅샷 사진을 데이터베이스에 일체 적재하지 않으며, 국기(Flag) 아이콘 및 미니멀 남/여 실루엣 아바타를 사용합니다. 클럽 명칭 역시 라이선스 분쟁을 사전에 우회할 수 있도록 범용/약식 텍스트로 처리됩니다.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-5 pt-4 border-t border-[#1f2240] flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-[#00ff88] hover:bg-[#00e577] text-black font-mono font-bold text-xs shadow-glow-neon"
          >
            확인 및 닫기
          </button>
        </div>
      </div>
    </div>
  );
}
