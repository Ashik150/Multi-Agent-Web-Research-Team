import React, { useState, useEffect } from 'react';
import {
  Search,
  Sparkles,
  Zap,
  ArrowRight,
  Loader2,
  Cpu,
  Globe,
  CheckCircle2,
  RefreshCw,
  Scale,
  FileText
} from 'lucide-react';

import Header from './components/Header';
import AgentStatusCards from './components/AgentStatusCards';
import PipelineTracker from './components/PipelineTracker';
import DebateFeed from './components/DebateFeed';
import ReportViewer from './components/ReportViewer';
import SettingsModal from './components/SettingsModal';
import HistoryDrawer from './components/HistoryDrawer';

const SUGGESTED_TOPICS = [
  "Quantum Computing breakthroughs in 2025/2026",
  "AI Agents vs Traditional Robotic Process Automation (RPA)",
  "Next-Gen Solid State Battery commercialization timeline",
  "Nuclear Fusion energy progress & private sector race",
  "Open Source LLMs vs Proprietary Frontier Models in 2026"
];

export default function App() {
  const [query, setQuery] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [events, setEvents] = useState([]);
  const [activeAgent, setActiveAgent] = useState(null);
  const [activeStage, setActiveStage] = useState(null);
  const [currentActivity, setCurrentActivity] = useState('');
  const [stagesCompleted, setStagesCompleted] = useState([]);

  // Final Results
  const [report, setReport] = useState('');
  const [debate, setDebate] = useState('');
  const [sources, setSources] = useState([]);

  // Settings & Models
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [modelsData, setModelsData] = useState(null);
  const [config, setConfig] = useState(() => {
    const saved = localStorage.getItem('agent_research_config');
    return saved
      ? JSON.parse(saved)
      : {
          provider: 'groq',
          model: 'llama-3.3-70b-versatile',
          apiKey: '',
          maxIterations: 2,
        };
  });

  // History
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('agent_research_history');
    return saved ? JSON.parse(saved) : [];
  });

  // Fetch available models on load
  useEffect(() => {
    fetch('/api/models')
      .then((r) => r.json())
      .then((d) => setModelsData(d))
      .catch((e) => console.warn('Could not fetch models config:', e));
  }, []);

  const handleSaveConfig = (newConfig) => {
    setConfig(newConfig);
    localStorage.setItem('agent_research_config', JSON.stringify(newConfig));
  };

  const handleClearHistory = () => {
    setHistory([]);
    localStorage.removeItem('agent_research_history');
  };

  const handleSelectHistorySession = (session) => {
    setQuery(session.query);
    setReport(session.report);
    setDebate(session.debate || '');
    setSources(session.sources || []);
    setEvents(session.events || []);
    setStagesCompleted(['planning', 'searching', 'scraping', 'debate', 'drafting', 'reviewing', 'complete']);
    setActiveAgent(null);
    setActiveStage(null);
  };

  const startResearch = async (searchTopic) => {
    const topicToSearch = (searchTopic || query).trim();
    if (!topicToSearch || isStreaming) return;

    // Reset state
    setQuery(topicToSearch);
    setIsStreaming(true);
    setEvents([]);
    setReport('');
    setDebate('');
    setSources([]);
    setStagesCompleted([]);
    setActiveAgent('Researcher');
    setActiveStage('planning');
    setCurrentActivity('Analyzing research angles...');

    const accumulatedEvents = [];
    let finalReportText = '';
    let finalDebateText = '';
    let finalSourcesList = [];

    try {
      const response = await fetch('/api/research/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: topicToSearch,
          provider: config.provider,
          model: config.model,
          apiKey: config.apiKey,
          maxIterations: config.maxIterations,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.replace('data: ', '').trim());
              accumulatedEvents.push(event);
              setEvents([...accumulatedEvents]);

              // Update Agent & Stage states
              if (event.agent) setActiveAgent(event.agent);
              if (event.stage) {
                setActiveStage(event.stage);
                setStagesCompleted((prev) =>
                  prev.includes(event.stage) ? prev : [...prev, event.stage]
                );
              }
              if (event.message) setCurrentActivity(event.message);

              if (event.sources) {
                finalSourcesList = event.sources;
                setSources(event.sources);
              }
              if (event.debate || event.debate_transcript) {
                finalDebateText = event.debate || event.debate_transcript;
                setDebate(finalDebateText);
              }
              if (event.final_report) {
                finalReportText = event.final_report;
                setReport(event.final_report);
              }
            } catch (err) {
              console.error('Error parsing SSE event payload:', err);
            }
          }
        }
      }

      // Finalize and save to history
      if (finalReportText) {
        const newSession = {
          id: Date.now().toString(),
          query: topicToSearch,
          timestamp: new Date().toISOString(),
          provider: config.provider,
          model: config.model,
          report: finalReportText,
          debate: finalDebateText,
          sources: finalSourcesList,
          sourcesCount: finalSourcesList.length,
          events: accumulatedEvents,
        };
        const updatedHistory = [newSession, ...history.slice(0, 19)];
        setHistory(updatedHistory);
        localStorage.setItem('agent_research_history', JSON.stringify(updatedHistory));
      }
    } catch (err) {
      console.error('Research stream error:', err);
      setEvents((prev) => [
        ...prev,
        {
          agent: 'System',
          stage: 'error',
          message: `Network/API Error: ${err.message}. Please check server and API keys.`,
        },
      ]);
    } finally {
      setIsStreaming(false);
      setActiveAgent(null);
      setCurrentActivity('');
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex flex-col">
      {/* Top Navbar */}
      <Header
        provider={config.provider}
        model={config.model}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onOpenHistory={() => setIsHistoryOpen(true)}
        historyCount={history.length}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5 animate-pulse" />
            <span>Autonomous Multi-Agent Intelligence</span>
          </div>

          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white mb-3">
            Autonomous <span className="gradient-text-cyan">Web Research</span> Pipeline
          </h2>

          <p className="text-sm sm:text-base text-slate-400 leading-relaxed max-w-2xl mx-auto">
            Three AI agents (<strong className="text-cyan-300">Researcher</strong>,{' '}
            <strong className="text-amber-300">Debater</strong>, and{' '}
            <strong className="text-emerald-300">Reviewer</strong>) collaborate to browse the live web,
            debate trade-offs, and draft publication-grade research reports.
          </p>

          {/* Search Input Box */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              startResearch();
            }}
            className="mt-8 relative max-w-2xl mx-auto"
          >
            <div className="relative flex items-center">
              <Search className="absolute left-4 w-5 h-5 text-slate-400 pointer-events-none" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter any topic or question to investigate..."
                disabled={isStreaming}
                className="w-full pl-12 pr-36 py-4 rounded-2xl bg-slate-900/90 border border-slate-700/80 hover:border-slate-600 focus:border-cyan-500 text-white placeholder-slate-500 text-sm shadow-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/20 transition"
              />
              <button
                type="submit"
                disabled={!query.trim() || isStreaming}
                className="absolute right-2 flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs sm:text-sm shadow-lg shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {isStreaming ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Researching...</span>
                  </>
                ) : (
                  <>
                    <span>Launch</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>

            {/* Suggested Prompts */}
            <div className="flex flex-wrap items-center justify-center gap-1.5 mt-3.5">
              <span className="text-[11px] text-slate-500 mr-1">Suggestions:</span>
              {SUGGESTED_TOPICS.map((topic, i) => (
                <button
                  type="button"
                  key={i}
                  disabled={isStreaming}
                  onClick={() => {
                    setQuery(topic);
                    startResearch(topic);
                  }}
                  className="px-2.5 py-1 rounded-lg bg-slate-900/60 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-cyan-300 text-[11px] transition"
                >
                  {topic}
                </button>
              ))}
            </div>
          </form>
        </div>

        {/* Dynamic Agent Cards */}
        <AgentStatusCards
          activeAgent={activeAgent}
          activeStage={activeStage}
          currentActivity={currentActivity}
        />

        {/* Step-by-Step Pipeline Tracker */}
        <PipelineTracker
          currentStage={activeStage}
          stagesCompleted={stagesCompleted}
        />

        {/* Live Collaboration & Debate Feed */}
        <DebateFeed events={events} isStreaming={isStreaming} />

        {/* Final Report Viewer */}
        <ReportViewer
          report={report}
          debate={debate}
          sources={sources}
          query={query}
        />
      </main>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        config={config}
        onSaveConfig={handleSaveConfig}
        modelsData={modelsData}
      />

      {/* History Drawer */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectSession={handleSelectHistorySession}
        onClearHistory={handleClearHistory}
      />

      {/* Footer */}
      <footer className="glass-panel border-t border-slate-800/80 py-4 px-6 text-center text-xs text-slate-500">
        <p>
          Multi-Agent Web Research Team • Built with{' '}
          <span className="text-cyan-400 font-semibold">LangGraph</span>,{' '}
          <span className="text-orange-400 font-semibold">Groq</span> &{' '}
          <span className="text-emerald-400 font-semibold">DuckDuckGo</span>
        </p>
      </footer>
    </div>
  );
}
