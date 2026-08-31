import React from 'react';
import { Bot, Settings, History, Sparkles, Github, Globe } from 'lucide-react';

export default function Header({
  provider,
  model,
  onOpenSettings,
  onOpenHistory,
  historyCount = 0
}) {
  const getProviderBadge = () => {
    switch (provider) {
      case 'groq':
        return { label: 'Groq Cloud', color: 'bg-orange-500/10 text-orange-400 border-orange-500/30' };
      case 'openai':
        return { label: 'OpenAI', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' };
      case 'gemini':
        return { label: 'Google Gemini', color: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
      case 'anthropic':
        return { label: 'Claude', color: 'bg-purple-500/10 text-purple-400 border-purple-500/30' };
      default:
        return { label: 'Groq', color: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30' };
    }
  };

  const badge = getProviderBadge();

  return (
    <header className="sticky top-0 z-40 glass-panel border-b border-slate-800/80 px-4 lg:px-8 py-3.5 flex items-center justify-between">
      {/* Brand & Logo */}
      <div className="flex items-center gap-3">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 via-indigo-600 to-violet-600 shadow-lg shadow-cyan-500/20">
          <Bot className="w-5 h-5 text-white" />
          <span className="absolute -top-1 -right-1 flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
          </span>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold tracking-tight text-white">
              Multi-Agent <span className="gradient-text-cyan">Research Team</span>
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-semibold px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
              v1.0
            </span>
          </div>
          <p className="text-xs text-slate-400 hidden sm:block">
            Autonomous live-web pipeline powered by LangGraph
          </p>
        </div>
      </div>

      {/* Model Status & Actions */}
      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* Model Badge */}
        <button
          onClick={onOpenSettings}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-xs font-medium transition hover:brightness-125 ${badge.color}`}
          title="Click to change model or API keys"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>{badge.label}</span>
          <span className="text-slate-400 hidden md:inline">• {model}</span>
        </button>

        {/* History Button */}
        <button
          onClick={onOpenHistory}
          className="relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-white border border-slate-700/60 text-xs font-medium transition"
        >
          <History className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">History</span>
          {historyCount > 0 && (
            <span className="flex items-center justify-center w-4 h-4 rounded-full bg-cyan-500 text-[10px] font-bold text-slate-950">
              {historyCount}
            </span>
          )}
        </button>

        {/* Settings Button */}
        <button
          onClick={onOpenSettings}
          className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-white border border-slate-700/60 transition"
          title="Settings & API Keys"
        >
          <Settings className="w-4 h-4" />
        </button>

        {/* GitHub Link */}
        <a
          href="https://github.com/Ashik150/Multi-Agent-Web-Research-Team"
          target="_blank"
          rel="noreferrer"
          className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-white border border-slate-700/60 transition"
          title="View GitHub Repository"
        >
          <Github className="w-4 h-4" />
        </a>
      </div>
    </header>
  );
}
