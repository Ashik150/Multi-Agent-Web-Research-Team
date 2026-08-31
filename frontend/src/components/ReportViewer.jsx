import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Download, FileText, Scale, Globe, Share2, ExternalLink, Printer } from 'lucide-react';

export default function ReportViewer({ report, debate, sources = [], query = '' }) {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState('report'); // 'report' | 'debate' | 'sources'

  if (!report) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([report], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    const cleanName = (query || 'research_report')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .slice(0, 40);
    link.download = `${cleanName}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="glass-panel rounded-2xl p-6 my-6 border border-cyan-500/30 glow-cyan">
      {/* Header & Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        {/* Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-900/80 border border-slate-800">
          <button
            onClick={() => setActiveTab('report')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'report'
                ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            Final Report
          </button>

          {debate && (
            <button
              onClick={() => setActiveTab('debate')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === 'debate'
                  ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Scale className="w-3.5 h-3.5" />
              Agent Debate
            </button>
          )}

          {sources && sources.length > 0 && (
            <button
              onClick={() => setActiveTab('sources')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === 'sources'
                  ? 'bg-violet-500 text-slate-950 shadow-md shadow-violet-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Globe className="w-3.5 h-3.5" />
              Sources ({sources.length})
            </button>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 text-xs font-medium transition"
            title="Copy Raw Markdown"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </button>

          <button
            onClick={handleDownload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-semibold text-xs transition shadow-md shadow-cyan-600/20"
            title="Download .md file"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download .MD</span>
          </button>

          <button
            onClick={handlePrint}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
            title="Print or Save PDF"
          >
            <Printer className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="mt-6">
        {activeTab === 'report' && (
          <article className="prose prose-invert prose-cyan max-w-none prose-headings:font-bold prose-h1:text-2xl sm:prose-h1:text-3xl prose-h2:text-xl prose-h2:border-b prose-h2:border-slate-800 prose-h2:pb-2 prose-h3:text-lg prose-p:leading-relaxed prose-table:border prose-table:border-slate-800 prose-th:bg-slate-900 prose-th:p-3 prose-td:p-3 prose-td:border-t prose-td:border-slate-800 prose-a:text-cyan-400 prose-a:underline hover:prose-a:text-cyan-300">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {report}
            </ReactMarkdown>
          </article>
        )}

        {activeTab === 'debate' && debate && (
          <div className="p-4 rounded-xl bg-slate-900/70 border border-amber-500/20 font-serif leading-relaxed text-slate-200">
            <div className="flex items-center gap-2 mb-4 pb-2 border-b border-slate-800">
              <Scale className="w-5 h-5 text-amber-400" />
              <h3 className="text-base font-bold text-amber-300 font-sans">
                Full Multi-Agent Round-Table Debate Transcript
              </h3>
            </div>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {debate}
            </ReactMarkdown>
          </div>
        )}

        {activeTab === 'sources' && (
          <div className="space-y-2.5">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3">
              Verified Web Sources & Citations
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {sources.map((s, idx) => (
                <a
                  key={idx}
                  href={s.url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex flex-col justify-between p-3.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/40 transition group"
                >
                  <div>
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300 transition line-clamp-1">
                        {s.title || s.url}
                      </h4>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyan-400 shrink-0" />
                    </div>
                    {s.snippet && (
                      <p className="text-[11px] text-slate-400 mt-1.5 line-clamp-2">
                        {s.snippet}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2 mt-3 pt-2 border-t border-slate-800/80 text-[10px] text-slate-500 font-mono">
                    <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                      {s.source || 'Web'}
                    </span>
                    <span className="truncate">{s.url}</span>
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
