import { useState, useRef, useEffect } from 'react';
import { api } from '../api';
import { Send, Sparkles, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const QUICK_PROMPTS = [
  'Review my DSA preparation gaps and suggest next steps',
  'Help me prepare a STAR story for a leadership situation at GSTN',
  'Explain the trade-offs between Redis and Memcached for caching',
  'Give me a system design interview question and walk me through it',
  'What Java concurrency concepts should I review for SDE-2?',
  'Analyze my mock interview scores and suggest improvements',
];

export default function Coach() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    if (!text.trim() || streaming) return;
    const userMsg = { role: 'user', content: text.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput('');
    setStreaming(true);

    const assistantMsg = { role: 'assistant', content: '' };
    setMessages([...newMessages, assistantMsg]);

    try {
      await api.streamCoach(
        { messages: newMessages },
        (chunk) => {
          assistantMsg.content += chunk;
          setMessages([...newMessages, { ...assistantMsg }]);
        }
      );
    } catch (err) {
      try {
        const res = await api.coach({ messages: newMessages });
        assistantMsg.content = res?.text || 'No response received.';
        setMessages([...newMessages, { ...assistantMsg }]);
      } catch (fallbackErr) {
        // Provide specific error messages
        let errorMsg = 'Error: Could not reach the AI coach. Is the server running?';

        // Check for specific API errors
        if (fallbackErr?.status === 400) {
          errorMsg = '❌ ANTHROPIC_API_KEY not configured. Please set it in Railway environment variables.';
        } else if (fallbackErr?.status === 401) {
          errorMsg = '❌ Invalid ANTHROPIC_API_KEY. Please check your API key is correct.';
        } else if (fallbackErr?.status === 429) {
          errorMsg = '⏱️ Rate limited. Please wait a moment and try again.';
        } else if (fallbackErr?.status === 500) {
          errorMsg = `❌ Server error: ${fallbackErr?.detail || 'Internal server error'}`;
        } else if (!navigator.onLine) {
          errorMsg = '⚠️ No internet connection.';
        }

        assistantMsg.content = errorMsg;
        setMessages([...newMessages, { ...assistantMsg }]);
      }
    }
    setStreaming(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  return (
    <div className="page" style={{ height: 'calc(100vh - 48px)', display: 'flex', flexDirection: 'column' }}>
      <div className="page-header" style={{ marginBottom: 12 }}>
        <div className="flex-between">
          <div>
            <h2>AI Coach</h2>
            <div className="sub">Powered by Claude with your prep context and knowledge base</div>
          </div>
          {messages.length > 0 && (
            <button className="btn btn-red btn-sm" onClick={() => setMessages([])}>
              <Trash2 size={12} /> Clear
            </button>
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div style={{
        flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 12,
        padding: '8px 0', marginBottom: 12,
      }}>
        {messages.length === 0 && (
          <div style={{ padding: 20 }}>
            <div style={{ fontSize: 12, color: 'var(--text3)', marginBottom: 16 }}>
              Ask anything about your prep. The coach has access to your progress, gaps, knowledge base, and interview intel.
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {QUICK_PROMPTS.map((prompt) => (
                <button key={prompt} onClick={() => sendMessage(prompt)} style={{
                  padding: '10px 14px', textAlign: 'left', background: 'var(--bg3)',
                  border: '1px solid var(--bg4)', borderRadius: 8, fontSize: 12,
                  color: 'var(--text)', transition: 'all 0.15s',
                }}
                onMouseOver={e => e.currentTarget.style.borderColor = 'var(--gold-border)'}
                onMouseOut={e => e.currentTarget.style.borderColor = 'var(--bg4)'}>
                  <Sparkles size={12} style={{ color: 'var(--gold)', marginRight: 8, verticalAlign: -2 }} />
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} style={{
            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '85%', padding: '10px 14px', borderRadius: 8,
            background: msg.role === 'user' ? 'var(--bg4)' : 'var(--bg3)',
            border: msg.role === 'user' ? '1px solid #2a2a32' : '1px solid rgba(232,200,122,0.08)',
            fontSize: 12, lineHeight: 1.7,
          }}>
            <div style={{ fontSize: 9, letterSpacing: 1, textTransform: 'uppercase', marginBottom: 4,
                          color: msg.role === 'user' ? 'var(--text3)' : 'var(--gold)' }}>
              {msg.role}
            </div>
            {msg.content
              ? msg.role === 'assistant'
                ? <div className="markdown-content"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
                : <span style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</span>
              : (streaming && i === messages.length - 1 ? <span className="loading">Thinking...</span> : '')}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: 8, padding: '12px 0 4px', borderTop: '1px solid var(--bg4)' }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask your coach anything..."
          disabled={streaming}
          style={{ flex: 1 }}
        />
        <button className="btn btn-solid" onClick={() => sendMessage(input)} disabled={streaming || !input.trim()}>
          <Send size={14} />
        </button>
      </div>
    </div>
  );
}
