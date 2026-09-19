import React, { useState, useRef, useEffect } from 'react';
import { TRANSLATIONS } from '../translations';
import { Send, Mic, MicOff, Download, User, Bot, PhoneCall, Building, AlertCircle } from 'lucide-react';

/**
 * Unified Chat Interface (Center of Page)
 * Features text input, mock voice recording input, chat bubble history, typing indicators,
 * officer escalation recommendation cards, and PDF transcript download.
 */
export default function ChatInterface({
  messages,
  langCode,
  onSendMessage,
  onSendVoice,
  isLoading,
  onDownloadPdf,
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const messagesEndRef = useRef(null);
  const timerRef = useRef(null);

  // Auto-scroll to bottom of chat history on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Voice recording simulation timer
  useEffect(() => {
    if (isRecording) {
      setRecordingSeconds(0);
      timerRef.current = setInterval(() => {
        setRecordingSeconds((prev) => {
          if (prev >= 4) {
            // Auto stop after 5 seconds
            handleStopRecording();
            return 0;
          }
          return prev + 1;
        });
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isRecording]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  const handleToggleRecording = () => {
    if (isRecording) {
      handleStopRecording();
    } else {
      setIsRecording(true);
    }
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    if (timerRef.current) clearInterval(timerRef.current);
    // Submit mock audio blob
    onSendVoice(new Blob(['mock-audio'], { type: 'audio/webm' }));
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      minHeight: '520px',
      position: 'relative',
    }}>
      {/* Top Action Bar (Download Conversation Button when exchanges exist) */}
      {messages.length > 0 && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          paddingBottom: '0.85rem',
          borderBottom: '1px solid var(--bg-card-border)',
          marginBottom: '1rem',
        }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            {messages.length} {messages.length === 1 ? 'message' : 'messages'}
          </span>
          <button
            onClick={onDownloadPdf}
            className="btn-secondary"
            style={{
              padding: '0.45rem 0.85rem',
              fontSize: '0.82rem',
              borderColor: 'rgba(16, 185, 129, 0.4)',
              color: '#10b981',
              background: 'rgba(16, 185, 129, 0.08)',
            }}
          >
            <Download size={15} color="#10b981" />
            <span>{t.downloadPdf}</span>
          </button>
        </div>
      )}

      {/* Messages Scroll Area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        paddingRight: '0.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.25rem',
        marginBottom: '1.25rem',
      }}>
        {messages.map((msg, idx) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
                gap: '0.75rem',
                alignItems: 'flex-start',
              }}
            >
              {/* Avatar for Assistant */}
              {!isUser && (
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: 'var(--primary-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#fff',
                  flexShrink: 0,
                  boxShadow: 'var(--shadow-sm)',
                }}>
                  <Bot size={20} />
                </div>
              )}

              {/* Chat Bubble Container */}
              <div style={{ maxWidth: '80%' }}>
                {/* Voice transcription badge if present */}
                {msg.transcription && (
                  <div style={{
                    fontSize: '0.78rem',
                    color: 'var(--text-muted)',
                    marginBottom: '0.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.3rem',
                  }}>
                    <Mic size={12} color="#3b82f6" />
                    <span>Transcribed: "{msg.transcription}"</span>
                  </div>
                )}

                {/* Main Bubble Content */}
                <div style={{
                  background: isUser ? 'var(--chat-user-bg)' : 'var(--chat-assistant-bg)',
                  color: isUser ? 'var(--chat-user-text)' : 'var(--chat-assistant-text)',
                  border: isUser ? 'none' : '1px solid var(--chat-assistant-border)',
                  padding: '0.9rem 1.2rem',
                  borderRadius: isUser ? '1.25rem 1.25rem 0.25rem 1.25rem' : '1.25rem 1.25rem 1.25rem 0.25rem',
                  boxShadow: 'var(--shadow-sm)',
                  fontSize: '0.98rem',
                  lineHeight: '1.55',
                  wordBreak: 'break-word',
                }}>
                  {msg.text}
                </div>

                {/* Officer Escalation Card if attached */}
                {msg.officerRecommendation && (
                  <div style={{
                    marginTop: '0.85rem',
                    background: 'rgba(239, 68, 68, 0.06)',
                    border: '1px solid rgba(239, 68, 68, 0.25)',
                    borderRadius: '1rem',
                    padding: '1rem',
                    boxShadow: 'var(--shadow-sm)',
                  }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      color: '#ef4444',
                      fontWeight: '600',
                      fontSize: '0.88rem',
                      marginBottom: '0.65rem',
                    }}>
                      <AlertCircle size={17} />
                      <span>{t.recommendedOfficer}</span>
                    </div>

                    <div style={{ fontSize: '0.88rem', color: 'var(--text-primary)', spaceY: '0.3rem' }}>
                      <div style={{ fontWeight: '700', fontSize: '0.98rem', color: 'var(--text-primary)', marginBottom: '0.2rem' }}>
                        {msg.officerRecommendation.name}
                      </div>
                      <div style={{ color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
                        {msg.officerRecommendation.designation}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '0.25rem' }}>
                        <Building size={14} />
                        <span>{msg.officerRecommendation.office}</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#10b981', fontWeight: '600', fontSize: '0.88rem' }}>
                        <PhoneCall size={14} />
                        <span>{msg.officerRecommendation.phone}</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Timestamp */}
                <div style={{
                  fontSize: '0.72rem',
                  color: 'var(--text-muted)',
                  marginTop: '0.35rem',
                  textAlign: isUser ? 'right' : 'left',
                }}>
                  {msg.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>

              {/* Avatar for User */}
              {isUser && (
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: 'var(--accent-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#fff',
                  flexShrink: 0,
                  boxShadow: 'var(--shadow-sm)',
                }}>
                  <User size={20} />
                </div>
              )}
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'var(--primary-gradient)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
            }}>
              <Bot size={20} />
            </div>
            <div style={{
              background: 'var(--chat-assistant-bg)',
              border: '1px solid var(--chat-assistant-border)',
              padding: '0.85rem 1.25rem',
              borderRadius: '1.25rem 1.25rem 1.25rem 0.25rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Voice Recording Overlay Banner */}
      {isRecording && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: '0.85rem',
          padding: '0.75rem 1.25rem',
          marginBottom: '0.75rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          animation: 'fadeIn 0.2s ease',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#ef4444', fontWeight: '600' }}>
            <div style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              background: '#ef4444',
              animation: 'pulseGlow 1s infinite',
            }} />
            <span>{t.recording} ({5 - recordingSeconds}s)</span>
          </div>
          <button
            onClick={handleStopRecording}
            style={{
              background: '#ef4444',
              color: '#fff',
              padding: '0.4rem 0.85rem',
              borderRadius: '0.5rem',
              fontSize: '0.82rem',
              fontWeight: '600',
            }}
          >
            {t.stopRecording}
          </button>
        </div>
      )}

      {/* Chat Input Bar */}
      <form onSubmit={handleSubmit} style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.6rem',
        background: 'var(--bg-card)',
        border: '1px solid var(--bg-card-border)',
        borderRadius: '1rem',
        padding: '0.5rem 0.6rem 0.5rem 1rem',
        boxShadow: 'var(--shadow-md)',
      }}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={t.chatPlaceholder}
          disabled={isLoading || isRecording}
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            outline: 'none',
            color: 'var(--text-primary)',
            fontSize: '0.98rem',
            fontFamily: 'inherit',
          }}
        />

        {/* Voice Input Button */}
        <button
          type="button"
          onClick={handleToggleRecording}
          disabled={isLoading}
          style={{
            background: isRecording ? '#ef4444' : 'rgba(148, 163, 184, 0.15)',
            color: isRecording ? '#ffffff' : 'var(--text-primary)',
            width: '42px',
            height: '42px',
            borderRadius: '0.75rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.2s ease',
          }}
          title={t.recordVoice}
        >
          {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
        </button>

        {/* Send Button */}
        <button
          type="submit"
          disabled={!inputText.trim() || isLoading || isRecording}
          className="btn-primary"
          style={{
            padding: '0.65rem 1.1rem',
            borderRadius: '0.75rem',
            opacity: (!inputText.trim() || isLoading || isRecording) ? 0.5 : 1,
            cursor: (!inputText.trim() || isLoading || isRecording) ? 'not-allowed' : 'pointer',
          }}
        >
          <Send size={18} />
          <span className="hide-mobile">{t.send}</span>
        </button>
      </form>
    </div>
  );
}
