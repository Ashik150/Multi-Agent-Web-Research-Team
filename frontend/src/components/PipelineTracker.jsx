import React from 'react';
import { Check, Loader2, ArrowRight } from 'lucide-react';

export default function PipelineTracker({ currentStage, stagesCompleted = [] }) {
  const steps = [
    { id: 'planning', label: '1. Plan & Query' },
    { id: 'searching', label: '2. Live Web Search' },
    { id: 'scraping', label: '3. Deep Scraping' },
    { id: 'debate', label: '4. Persona Debate' },
    { id: 'drafting', label: '5. Draft Report' },
    { id: 'reviewing', label: '6. Editorial Review' },
    { id: 'complete', label: '7. Final Polish' },
  ];

  return (
    <div className="glass-panel rounded-2xl p-4 my-4 overflow-x-auto">
      <div className="flex items-center justify-between min-w-[680px] gap-2">
        {steps.map((step, index) => {
          const isDone = stagesCompleted.includes(step.id);
          const isCurrent = currentStage === step.id;

          let badgeClass = 'bg-slate-800/80 text-slate-500 border-slate-800';
          if (isDone) {
            badgeClass = 'bg-emerald-950/60 text-emerald-400 border-emerald-700/60';
          } else if (isCurrent) {
            badgeClass = 'bg-cyan-950 text-cyan-300 border-cyan-500 glow-cyan animate-pulse';
          }

          return (
            <React.Fragment key={step.id}>
              <div className="flex items-center gap-2">
                <div
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-all ${badgeClass}`}
                >
                  {isDone ? (
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                  ) : isCurrent ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-400" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-slate-700" />
                  )}
                  <span>{step.label}</span>
                </div>
              </div>
              {index < steps.length - 1 && (
                <ArrowRight className="w-3.5 h-3.5 text-slate-700 shrink-0" />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
