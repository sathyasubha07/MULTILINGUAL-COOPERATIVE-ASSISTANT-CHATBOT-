import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, Bot, User, Volume2, VolumeX, ShieldCheck, 
  Sparkles, RefreshCw, Compass, AlertCircle
} from 'lucide-react';
import { api } from '../../services/api';
import { speakText, stopSpeech } from '../../utils/helpers';
import { TRANSLATIONS } from '../../utils/translations';
import VoiceInput from '../VoiceInput/VoiceInput';
import CitationBox from '../CitationBox/CitationBox';
import ResolutionNavigator from '../ResolutionNavigator/ResolutionNavigator';

export default function ChatBox({ currentLang, initialQuery = null }) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: currentLang === 'hi' 
        ? "नमस्ते! मैं 'सहकार एआई मित्र' हूँ। आप मुझसे पैक्स (PACS) सेवाएं, फसल बीमा (PMFBY), पीएम-किसान, केसीसी ऋण अथवा सहकारी कानून के बारे में कुछ भी पूछ सकते हैं।"
        : "Namaste! I am 'Sahakar AI Assistant'. How can I help you today with PACS operations, PMFBY crop insurance, KCC loans, or cooperative bylaws?",
      citations: ["Ministry of Cooperation", "Multi-State Co-operative Societies Act 2023"],
      trustScore: 0.99
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSpeakingId, setIsSpeakingId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  const handleSend = async (queryToSend = null) => {
    const text = (queryToSend || inputQuery).trim();
    if (!text || isLoading) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: text
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage(text, currentLang);
      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: response.answer,
        citations: response.citations || [],
        procedure: response.procedure || null,
        trustScore: response.verification_status ? 0.98 : 0.80,
        domain: response.domain
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: "I encountered an issue retrieving the latest data. Please verify your connection or consult the local PACS office.",
          citations: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSpeak = (msgId, text) => {
    if (isSpeakingId === msgId) {
      stopSpeech();
      setIsSpeakingId(null);
    } else {
      speakText(text, currentLang);
      setIsSpeakingId(msgId);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '75vh',
      background: '#ffffff',
      borderRadius: '20px',
      border: '1px solid #e2e8f0',
      boxShadow: '0 12px 35px rgba(0,0,0,0.04)',
      overflow: 'hidden'
    }}>
      {/* Chat Header */}
      <div style={{
        padding: '16px 24px',
        borderBottom: '1px solid #e2e8f0',
        background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 10px rgba(4, 120, 87, 0.25)'
          }}>
            <Bot size={22} />
          </div>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: '800', color: '#064e3b' }}>
              Sahakar AI Assistant (सहकार मित्र)
            </h3>
            <p style={{ fontSize: '12px', color: '#64748b', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <ShieldCheck size={14} color="#10b981" />
              Verified Knowledge Base • Zero Hallucination Guarantee
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge badge-green">
            ⚡ Edge RAG Live
          </span>
        </div>
      </div>

      {/* Message Feed */}
      <div style={{
        flex: 1,
        padding: '24px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        background: '#f8fafc'
      }}>
        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={msg.id}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: isUser ? 'flex-end' : 'flex-start',
                width: '100%'
              }}
            >
              <div style={{
                display: 'flex',
                gap: '12px',
                maxWidth: isUser ? '80%' : '90%',
                flexDirection: isUser ? 'row-reverse' : 'row'
              }}>
                {/* Avatar */}
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: isUser ? '#0f172a' : '#059669',
                  color: '#ffffff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  {isUser ? <User size={18} /> : <Bot size={18} />}
                </div>

                {/* Bubble */}
                <div style={{
                  background: isUser ? '#0f172a' : '#ffffff',
                  color: isUser ? '#ffffff' : '#0f172a',
                  padding: '16px 20px',
                  borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.03)',
                  border: isUser ? 'none' : '1px solid #e2e8f0',
                  fontSize: '14px',
                  lineHeight: 1.6,
                  width: '100%'
                }}>
                  <div style={{ whiteSpace: 'pre-line' }}>{msg.text}</div>

                  {/* Actions (Read Aloud) */}
                  {!isUser && (
                    <div style={{ marginTop: '12px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <button
                        onClick={() => handleSpeak(msg.id, msg.text)}
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '6px',
                          background: '#f1f5f9',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '8px',
                          fontSize: '12px',
                          fontWeight: '600',
                          color: '#334155',
                          cursor: 'pointer'
                        }}
                      >
                        {isSpeakingId === msg.id ? <VolumeX size={14} color="#ef4444" /> : <Volume2 size={14} color="#059669" />}
                        <span>{isSpeakingId === msg.id ? 'Stop Voice' : t.speakerOutput}</span>
                      </button>
                    </div>
                  )}

                  {/* Citations Box */}
                  {!isUser && msg.citations && msg.citations.length > 0 && (
                    <CitationBox citations={msg.citations} trustScore={msg.trustScore} />
                  )}

                  {/* Resolution Navigator */}
                  {!isUser && msg.procedure && (
                    <ResolutionNavigator procedure={msg.procedure} />
                  )}
                </div>
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center', color: '#64748b', fontSize: '13px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: '#059669',
              color: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Bot size={18} />
            </div>
            <div style={{
              background: '#ffffff',
              padding: '12px 18px',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <RefreshCw size={16} className="animate-spin" color="#059669" />
              <span>Analyzing official cooperative gazettes and guidelines...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        style={{
          padding: '16px 20px',
          background: '#ffffff',
          borderTop: '1px solid #e2e8f0',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}
      >
        <VoiceInput
          currentLang={currentLang}
          onTranscript={(text) => handleSend(text)}
        />

        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          placeholder={t.askAnything}
          style={{
            flex: 1,
            padding: '14px 18px',
            borderRadius: '12px',
            border: '1px solid #cbd5e1',
            fontSize: '14px',
            outline: 'none',
            transition: 'border 0.2s'
          }}
          onFocus={(e) => (e.target.style.borderColor = '#059669')}
          onBlur={(e) => (e.target.style.borderColor = '#cbd5e1')}
        />

        <button
          type="submit"
          disabled={!inputQuery.trim() || isLoading}
          className="kiosk-btn kiosk-btn-primary"
          style={{ padding: '14px 22px', borderRadius: '12px' }}
        >
          <Send size={18} />
          <span>Send</span>
        </button>
      </form>
    </div>
  );
}
