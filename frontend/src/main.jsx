import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("React ErrorBoundary caught error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#0a0a16] text-white flex flex-col items-center justify-center p-6 font-mono">
          <div className="p-8 rounded-xl bg-[#121226] border border-red-500/40 max-w-lg text-center shadow-2xl">
            <h2 className="text-lg font-bold text-red-400 mb-2">⚠️ 일시적 렌더링 오류 발생</h2>
            <p className="text-xs text-gray-400 mb-4">{this.state.error?.message || "UI 렌더링 중 오류가 발생했습니다."}</p>
            <button
              onClick={() => {
                this.setState({ hasError: false });
                window.location.reload();
              }}
              className="px-4 py-2 bg-[#00ff88] text-black font-bold rounded-lg text-xs hover:brightness-110"
            >
              🔄 페이지 새로고침
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
