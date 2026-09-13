import React from 'react';
import { ShieldCheck, FileText, Info, Award, ExternalLink, X } from 'lucide-react';

export default function LegalModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white border-2 border-gray-900 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto font-sans text-gray-900">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-500 hover:text-gray-900 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5 border-b border-gray-200 pb-4">
          <div className="p-2.5 rounded-xl bg-purple-100 text-purple-700 border border-purple-200">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-black text-gray-950 font-mono">
              [ LEGAL COMPLIANCE & OPEN DATA ATTRIBUTION ]
            </h2>
            <p className="text-xs text-gray-500 font-mono">오픈 라이선스 출처 명시 및 저작권/초상권 준수 성명서</p>
          </div>
        </div>

        {/* Legal Sections */}
        <div className="space-y-4 text-xs leading-relaxed text-gray-700 font-mono">
          {/* Wyscout CC BY 4.0 */}
          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-200">
            <div className="flex items-center justify-between text-purple-900 font-bold mb-1">
              <span className="flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-purple-700" />
                1. Wyscout Open Dataset (CC BY 4.0)
              </span>
              <span className="text-[10px] bg-purple-100 text-purple-800 px-2 py-0.5 rounded font-bold border border-purple-200">CC BY 4.0</span>
            </div>
            <p className="text-gray-700 mt-1">
              "경기 전술 이벤트 통계는 Luca Pappalardo 등이 Nature Scientific Data(2019) 저널에 배포한 Wyscout Open Dataset(CC BY 4.0)을 기반으로 역산되었습니다."
            </p>
            <div className="text-[10px] text-gray-400 mt-1">
              DOI: 10.1038/s41597-019-0247-7 / Nature Scientific Data (2019)
            </div>
          </div>

          {/* StatsBomb Open Data */}
          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-200">
            <div className="flex items-center justify-between text-blue-900 font-bold mb-1">
              <span className="flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-blue-700" />
                2. StatsBomb Open Data Model Compliance
              </span>
              <span className="text-[10px] bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-bold border border-blue-200">Open Data</span>
            </div>
            <p className="text-gray-700 mt-1">
              본 시뮬레이터에 적용된 경기당 전술 공간 행동 지표 및 기대 득점(xG) 산출 모델은 StatsBomb Open Data 가이드라인 및 공인 학술 연구 표준을 준수하여 가공되었습니다.
            </p>
          </div>

          {/* Kaggle Open Databases */}
          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-200">
            <div className="flex items-center justify-between text-amber-900 font-bold mb-1">
              <span className="flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-amber-700" />
                3. Kaggle Static Soccer Databases (ODbL & CDLA)
              </span>
              <span className="text-[10px] bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-bold border border-amber-200">ODbL / CDLA 1.0</span>
            </div>
            <ul className="list-disc list-inside space-y-1 text-gray-600 mt-1">
              <li>European Soccer Database (by Hugo Mathien) - Open Database License (ODbL)</li>
              <li>European Leagues Database (by Kamran Gayibov) - CDLA-Sharing Version 1.0</li>
            </ul>
          </div>

          {/* Portrait Rights & Trademark Protection */}
          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-200">
            <div className="text-gray-900 font-bold mb-1 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-gray-700" />
              4. 선수 초상권(Portrait Rights) 및 클럽 상표권 보호 조치
            </div>
            <p className="text-gray-600">
              FM Scout AI (FC Finder)는 비상업/학술 시뮬레이터 목적으로 구축되었습니다. FIFPRO 및 각 프로축구 협회의 초상권 제재 대상이 되는 실제 선수 경기 스냅샷 사진을 데이터베이스에 일체 적재하지 않으며, 국기(Flag) 아이콘 및 미니멀 남/여 실루엣 아바타를 사용합니다. 클럽 명칭 역시 라이선스 분쟁을 사전에 우회할 수 있도록 범용/약식 텍스트로 처리됩니다.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-5 pt-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-gray-900 hover:bg-gray-800 text-white font-mono font-bold text-xs shadow-sm cursor-pointer"
          >
            확인 및 닫기
          </button>
        </div>
      </div>
    </div>
  );
}
