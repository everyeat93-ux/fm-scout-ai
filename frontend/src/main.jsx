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
        <div className="min-h-screen bg-gray-50 text-gray-900 flex flex-col items-center justify-center p-6 font-mono">
          <div className="p-8 rounded-2xl bg-white border-2 border-gray-900 max-w-lg text-center shadow-2xl">
            <h2 className="text-lg font-black text-rose-600 mb-2">⚠️ 일시적 렌더링 오류 발생</h2>
            <p className="text-xs text-gray-600 mb-4">{this.state.error?.message || "UI 렌더링 중 오류가 발생했습니다."}</p>
            <button
              onClick={() => {
                this.setState({ hasError: false });
                window.location.reload();
              }}
              className="px-4 py-2 bg-gray-900 text-white font-bold rounded-xl text-xs hover:bg-gray-800 shadow-sm cursor-pointer"
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
