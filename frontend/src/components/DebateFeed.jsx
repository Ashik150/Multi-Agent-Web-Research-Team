import React, { useRef, useEffect } from 'react';
import { Terminal, Search, Scale, PenTool, CheckCircle, ExternalLink, Sparkles } from 'lucide-react';

export default function DebateFeed({ events = [], isStreaming = false }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  const getAgentTheme = (agent) => {
    switch (agent) {
      case 'Researcher':
        return {
          icon: Search,
          badge: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
          border: 'border-cyan-500/20',
          bg: 'bg-cyan-950/20',
        };
      case 'Debater':
        return {
          icon: Scale,
          badge: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
          border: 'border-amber-500/20',
          bg: 'bg-amber-950/20',
        };
      case 'Writer':
        return {
          icon: PenTool,
          badge: 'bg-violet-500/10 text-violet-400 border-violet-500/30',
          border: 'border-violet-500/20',
          bg: 'bg-violet-950/20',
        };
      case 'Reviewer':
        return {
          icon: CheckCircle,
          badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
          border: 'border-emerald-500/20',
          bg: 'bg-emerald-950/20',
        };
      default:
        return {
          icon: Terminal,
          badge: 'bg-slate-700 text-slate-300 border-slate-600',
          border: 'border-slate-800',
          bg: 'bg-slate-900/40',
        };
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 my-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Agent Collaboration & Debate Stream
          </h3>
        </div>
        {isStreaming && (
          <div className="flex items-center gap-2 text-xs text-cyan-400">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </span>
            <span className="font-mono text-[11px]">Streaming live agent thoughts...</span>
          </div>
        )}
      </div>

      <div
        ref={scrollRef}
        className="mt-4 max-h-[420px] overflow-y-auto space-y-3 pr-2 scroll-smooth"
      >
        {events.length === 0 ? (
          <div className="text-center py-12 text-slate-500 text-sm">
            <Sparkles className="w-8 h-8 mx-auto mb-2 opacity-30 text-cyan-400" />
            Enter a research query above to witness the agents collaborate and debate live.
          </div>
        ) : (
          events.map((ev, idx) => {
            const theme = getAgentTheme(ev.agent);
            const Icon = theme.icon;

            return (
              <div
                key={idx}
                className={`p-3.5 rounded-xl border ${theme.border} ${theme.bg} transition-all duration-200`}
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className={`flex items-center gap-1 px-2 py-0.5 rounded-md border text-[11px] font-bold ${theme.badge}`}>
                      <Icon className="w-3 h-3" />
                      {ev.agent}
                    </span>
                    {ev.stage && (
                      <span className="text-[10px] font-mono text-slate-400 uppercase">
                        [{ev.stage}]
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-slate-200 leading-relaxed font-sans whitespace-pre-wrap">
                  {ev.message}
                </p>

                {/* Sub-queries display */}
                {ev.queries && ev.queries.length > 0 && (
                  <div className="mt-2.5 pt-2 border-t border-slate-800/80 flex flex-wrap gap-1.5">
                    {ev.queries.map((q, qIdx) => (
                      <span
                        key={qIdx}
                        className="px-2 py-0.5 rounded-md bg-slate-900/90 text-cyan-300 border border-slate-700 text-[11px] font-mono"
                      >
                        🔍 {q}
                      </span>
                    ))}
                  </div>
                )}

                {/* Discovered Sources preview */}
                {ev.sources && ev.sources.length > 0 && (
                  <div className="mt-2.5 pt-2 border-t border-slate-800/80 space-y-1">
                    <span className="text-[10px] uppercase font-semibold text-slate-400">
                      Discovered Live Sources:
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                      {ev.sources.slice(0, 4).map((s, sIdx) => (
                        <a
                          key={sIdx}
                          href={s.url}
                          target="_blank"
                          rel="noreferrer"
                          className="flex items-center justify-between p-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 text-[11px] text-slate-300 hover:text-cyan-300 border border-slate-800 transition"
                        >
                          <span className="truncate pr-2">{s.title || s.url}</span>
                          <ExternalLink className="w-3 h-3 shrink-0 text-slate-500" />
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* Debate Snippet */}
                {ev.debate_preview && (
                  <div className="mt-2 p-2 rounded bg-slate-950/80 border border-amber-500/20 text-[11px] text-amber-200/90 font-serif italic">
                    "{ev.debate_preview}"
                  </div>
                )}

                {/* Review Data badge */}
                {ev.review_data && (
                  <div className="mt-2 flex items-center gap-3 text-xs">
                    <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-700 font-semibold">
                      Quality Score: {ev.review_data.quality_score}/100
                    </span>
                    <span className="text-slate-300">
                      Verdict: <strong className="text-emerald-400">{ev.review_data.verdict}</strong>
                    </span>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
