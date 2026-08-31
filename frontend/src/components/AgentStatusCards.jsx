import React from 'react';
import { Search, PenTool, CheckCircle, Scale, Loader2, Sparkles } from 'lucide-react';

export default function AgentStatusCards({ activeAgent, activeStage, currentActivity }) {
  const agents = [
    {
      id: 'Researcher',
      name: 'Researcher Agent',
      role: 'Web Search & Evidence Mining',
      icon: Search,
      color: 'cyan',
      borderActive: 'border-cyan-500 shadow-lg shadow-cyan-500/20',
      badgeBg: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
      iconBg: 'bg-cyan-500/20 text-cyan-400',
      description: 'Browses live web via DuckDuckGo, extracts quotes, facts, and sources.',
    },
    {
      id: 'Debater',
      name: 'Debate Engine',
      role: 'Multi-Perspective Synthesis',
      icon: Scale,
      color: 'amber',
      borderActive: 'border-amber-500 shadow-lg shadow-amber-500/20',
      badgeBg: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
      iconBg: 'bg-amber-500/20 text-amber-400',
      description: 'Simulates Advocate vs Skeptic round-table debate to analyze trade-offs.',
    },
    {
      id: 'Writer',
      name: 'Writer Agent',
      role: 'Comprehensive Report Drafter',
      icon: PenTool,
      color: 'violet',
      borderActive: 'border-violet-500 shadow-lg shadow-violet-500/20',
      badgeBg: 'bg-violet-500/10 text-violet-400 border-violet-500/30',
      iconBg: 'bg-violet-500/20 text-violet-400',
      description: 'Synthesizes findings into deep Markdown analysis with tables & citations.',
    },
    {
      id: 'Reviewer',
      name: 'Reviewer Agent',
      role: 'Editor & Fact-Checker',
      icon: CheckCircle,
      color: 'emerald',
      borderActive: 'border-emerald-500 shadow-lg shadow-emerald-500/20',
      badgeBg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
      iconBg: 'bg-emerald-500/20 text-emerald-400',
      description: 'Verifies factual rigor, scores depth, and applies publication polish.',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 my-6">
      {agents.map((agent) => {
        const isActive = activeAgent === agent.id;
        const Icon = agent.icon;

        return (
          <div
            key={agent.id}
            className={`relative rounded-2xl p-4 transition-all duration-300 glass-card ${
              isActive
                ? `${agent.borderActive} bg-slate-800/90 scale-[1.02]`
                : 'border-slate-800/80 hover:border-slate-700/80'
            }`}
          >
            {/* Active Glow Pill */}
            {isActive && (
              <div className="absolute -top-2.5 right-3 flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-slate-900 border border-slate-700 text-[10px] font-semibold text-white shadow-md">
                <span className="flex h-2 w-2 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
                </span>
                <span>Active Now</span>
              </div>
            )}

            <div className="flex items-start gap-3">
              <div className={`p-2.5 rounded-xl ${agent.iconBg} shrink-0`}>
                {isActive ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Icon className="w-5 h-5" />
                )}
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5">
                  <h3 className="text-sm font-bold text-white truncate">{agent.name}</h3>
                </div>
                <p className="text-xs text-slate-400 truncate">{agent.role}</p>
              </div>
            </div>

            <p className="text-[11px] text-slate-400 mt-3 leading-relaxed line-clamp-2">
              {agent.description}
            </p>

            {/* Current Realtime Status */}
            {isActive && currentActivity && (
              <div className="mt-3 pt-2.5 border-t border-slate-700/60">
                <div className="flex items-center gap-1.5 text-[11px] text-cyan-300 font-medium">
                  <Sparkles className="w-3 h-3 shrink-0 animate-pulse text-cyan-400" />
                  <span className="truncate">{currentActivity}</span>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
