import React, { useState } from 'react';
import { X, Key, Cpu, Zap, Check, AlertCircle, RefreshCw } from 'lucide-react';

export default function SettingsModal({
  isOpen,
  onClose,
  config,
  onSaveConfig,
  modelsData
}) {
  if (!isOpen) return null;

  const [provider, setProvider] = useState(config.provider || 'groq');
  const [model, setModel] = useState(config.model || 'llama-3.3-70b-versatile');
  const [apiKey, setApiKey] = useState(config.apiKey || '');
  const [maxIterations, setMaxIterations] = useState(config.maxIterations || 2);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const currentProviderObj = modelsData?.providers?.find((p) => p.id === provider) || {
    models: [
      { id: 'llama-3.3-70b-versatile', name: 'LLaMA 3.3 70B Versatile' },
      { id: 'gpt-4o', name: 'GPT-4o' }
    ]
  };

  const handleProviderChange = (newProvider) => {
    setProvider(newProvider);
    const newProvObj = modelsData?.providers?.find((p) => p.id === newProvider);
    if (newProvObj && newProvObj.models && newProvObj.models.length > 0) {
      setModel(newProvObj.models[0].id);
    }
  };

  const handleSave = (e) => {
    e.preventDefault();
    onSaveConfig({
      provider,
      model,
      apiKey: apiKey.trim(),
      maxIterations: Number(maxIterations),
    });
    setSaveSuccess(true);
    setTimeout(() => {
      setSaveSuccess(false);
      onClose();
    }, 800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="relative w-full max-w-md rounded-2xl glass-panel p-6 border border-slate-700 shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-white">System & Model Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSave} className="space-y-4 mt-4 text-xs">
          {/* Provider Selection */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5">
              LLM Provider
            </label>
            <div className="grid grid-cols-2 gap-2">
              {[
                { id: 'groq', name: 'Groq Cloud (Fast)', badge: 'Recommended' },
                { id: 'openai', name: 'OpenAI GPT-4' },
                { id: 'gemini', name: 'Google Gemini' },
                { id: 'anthropic', name: 'Claude' },
              ].map((p) => (
                <button
                  type="button"
                  key={p.id}
                  onClick={() => handleProviderChange(p.id)}
                  className={`p-2.5 rounded-xl border text-left transition ${
                    provider === p.id
                      ? 'bg-cyan-950/60 border-cyan-500 text-cyan-300 glow-cyan'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <div className="font-semibold text-white">{p.name}</div>
                  {p.badge && (
                    <span className="text-[9px] uppercase tracking-wider text-cyan-400 font-mono">
                      {p.badge}
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Model Selection */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1">
              Selected Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-cyan-500 text-xs"
            >
              {currentProviderObj.models.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name || m.id}
                </option>
              ))}
            </select>
          </div>

          {/* Custom API Key Override */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="font-semibold text-slate-300 flex items-center gap-1.5">
                <Key className="w-3.5 h-3.5 text-cyan-400" />
                API Key Override (Optional)
              </label>
              <span className="text-[10px] text-slate-500">
                Leave empty to use server .env
              </span>
            </div>
            <input
              type="password"
              placeholder={provider === 'groq' ? 'gsk_...' : 'sk-...'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 font-mono text-xs"
            />
          </div>

          {/* Max Editorial Iterations */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1">
              Max Reviewer Feedback Cycles: <span className="text-cyan-400 font-bold">{maxIterations}</span>
            </label>
            <input
              type="range"
              min="1"
              max="3"
              value={maxIterations}
              onChange={(e) => setMaxIterations(e.target.value)}
              className="w-full accent-cyan-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 mt-0.5">
              <span>1 (Fastest)</span>
              <span>2 (Standard)</span>
              <span>3 (Deepest)</span>
            </div>
          </div>

          {/* Actions */}
          <div className="pt-3 border-t border-slate-800 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold transition shadow-lg shadow-cyan-500/20"
            >
              {saveSuccess ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  Saved!
                </>
              ) : (
                'Save Settings'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
