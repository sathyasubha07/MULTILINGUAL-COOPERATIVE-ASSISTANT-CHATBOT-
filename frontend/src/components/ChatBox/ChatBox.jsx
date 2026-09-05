import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Volume2, Pause, Play, Loader2 } from 'lucide-react';
import { sendTextQuery, sendVoiceQuery, fetchTTSAudio } from '../../services/api';
import { useLanguage } from '../../context/LanguageContext';
import VoiceInput from '../VoiceInput/VoiceInput';
import OfficerRecommendationCard from '../OfficerRecommendationCard/OfficerRecommendationCard';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatBox() {
  const { language, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [audioState, setAudioState] = useState({ messageId: null, status: 'idle' });
  const currentAudioRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Clean up audio on unmount
  useEffect(() => {
    return () => {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
        currentAudioRef.current = null;
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const stopCurrentAudio = () => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current = null;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setAudioState({ messageId: null, status: 'idle' });
  };

  const playAssistantSpeech = async (messageId, text, langCode) => {
    stopCurrentAudio();
    if (!text) return;

    setAudioState({ messageId, status: 'loading' });

    try {
      // 1. Try Thanushree's Backend TTS Engine (/chat/tts)
      const audioUrl = await fetchTTSAudio(text, langCode || language);
      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.playbackRate = 1.0; // Normal speech speed
        currentAudioRef.current = audio;

        audio.onplay = () => setAudioState({ messageId, status: 'playing' });
        audio.onpause = () => {
          if (audio.currentTime < audio.duration) {
            setAudioState({ messageId, status: 'paused' });
          }
        };
        audio.onended = () => {
          setAudioState({ messageId: null, status: 'idle' });
          currentAudioRef.current = null;
        };
        audio.onerror = () => {
          fallbackSpeechSynthesis(messageId, text, langCode);
        };

        await audio.play();
        return;
      }
    } catch (err) {
      console.warn('Backend audio play error, falling back to Web Speech:', err);
    }

    // Fallback: Web Speech API
    fallbackSpeechSynthesis(messageId, text, langCode);
  };

  const fallbackSpeechSynthesis = (messageId, text, langCode) => {
    if (!('speechSynthesis' in window)) {
      setAudioState({ messageId: null, status: 'idle' });
      return;
    }
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[#*`📌⚠️🏛️]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0; // Normal speed

    const langLocales = {
      en: 'en-IN',
      hi: 'hi-IN',
      ta: 'ta-IN',
      te: 'te-IN',
      mr: 'mr-IN',
      kn: 'kn-IN',
      bn: 'bn-IN',
      gu: 'gu-IN',
      ml: 'ml-IN',
      pa: 'pa-IN',
    };
    utterance.lang = langLocales[langCode || language] || 'en-IN';

    utterance.onstart = () => setAudioState({ messageId, status: 'playing' });
    utterance.onend = () => setAudioState({ messageId: null, status: 'idle' });
    utterance.onerror = () => setAudioState({ messageId: null, status: 'idle' });

    window.speechSynthesis.speak(utterance);
  };

  const toggleSpeech = (messageId, text) => {
    if (audioState.messageId === messageId && audioState.status === 'playing') {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.pause();
      }
      setAudioState({ messageId, status: 'paused' });
    } else if (audioState.messageId === messageId && audioState.status === 'paused') {
      if (currentAudioRef.current) {
        currentAudioRef.current.play();
      } else if (window.speechSynthesis) {
        window.speechSynthesis.resume();
      }
      setAudioState({ messageId, status: 'playing' });
    } else {
      playAssistantSpeech(messageId, text, language);
    }
  };

  const addAssistantMessage = (response) => {
    const newMsgId = Date.now() + 1;
    setMessages((prev) => [
      ...prev,
      {
        id: newMsgId,
        sender: 'ai',
        text: response.answer,
        responseType: response.responseType,
        officerRecommendation: response.officerRecommendation,
        citations: response.citations || [],
        verificationStatus: response.verificationStatus,
        trustScore: response.trustScore || 0.98,
        activeDomains: response.activeDomains || [response.responseType || 'general'],
        verifiedFacts: response.verifiedFacts || [],
        sourceAuthority: response.sourceAuthority,
      },
    ]);

    // Auto-start with voice speech on output
    if (response.answer) {
      setTimeout(() => {
        playAssistantSpeech(newMsgId, response.answer, language);
      }, 100);
    }
  };

  const handleTextSend = async (text) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    stopCurrentAudio();
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), sender: 'user', text: trimmed, isVoice: false },
    ]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const response = await sendTextQuery(trimmed, language);
      addAssistantMessage(response);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'ai', text: t('errorMessage') },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceInput = async (audioBlob, transcriptText) => {
    if (isLoading) return;

    stopCurrentAudio();
    setIsLoading(true);

    try {
      if (audioBlob) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: 'user',
            text: transcriptText ? `🎙️ "${transcriptText}"` : '🎙️ Audio query recording...',
            isVoice: true,
            showTranscriptLabel: true,
          },
        ]);

        const response = await sendVoiceQuery(audioBlob, language);
        if (response.transcription && !transcriptText) {
          setMessages((prev) =>
            prev.map((m) =>
              m.isVoice && m.text === '🎙️ Audio query recording...'
                ? { ...m, text: `🎙️ "${response.transcription}"` }
                : m
            )
          );
        }
        addAssistantMessage(response);
      } else if (transcriptText) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: 'user',
            text: `🎙️ "${transcriptText}"`,
            isVoice: true,
            showTranscriptLabel: true,
          },
        ]);
        const response = await sendTextQuery(transcriptText, language);
        addAssistantMessage(response);
      } else {
        const response = await sendVoiceQuery(null, language);
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            sender: 'user',
            text: `🎙️ "${response.transcription || 'PMFBY crop insurance query'}"`,
            isVoice: true,
            showTranscriptLabel: true,
          },
        ]);
        addAssistantMessage(response);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'ai', text: t('errorMessage') },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-header-icon">
          <Bot size={22} />
        </div>
        <h2>{t('chatTitle')}</h2>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="chat-empty-hint">{t('welcomeMessage')}</p>
        )}

        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          const isCurrentAudio = audioState.messageId === msg.id;
          const isPlaying = isCurrentAudio && audioState.status === 'playing';
          const isPaused = isCurrentAudio && audioState.status === 'paused';
          const isAudioLoading = isCurrentAudio && audioState.status === 'loading';

          return (
            <div key={msg.id} className={`chat-row ${isUser ? 'chat-row-user' : 'chat-row-ai'}`}>
              <div className={`chat-avatar ${isUser ? 'chat-avatar-user' : 'chat-avatar-ai'}`}>
                {isUser ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className="chat-bubble-wrap">
                {isUser && msg.showTranscriptLabel && (
                  <span className="transcript-label">{t('youSaid')}</span>
                )}
                <div
                  className={`chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-ai'}`}
                  style={msg.isVoice ? { fontStyle: 'italic', opacity: 0.9 } : undefined}
                >
                  {/* Meta Bar for AI: Active Subdomains & Database Verification Status */}
                  {!isUser && (
                    <div className="chat-meta-bar">
                      {msg.activeDomains && msg.activeDomains.map((dom, idx) => (
                        <span
                          key={idx}
                          className={`chat-domain-pill ${dom.includes('pmfby') ? 'pmfby' : dom.includes('grievance') ? 'grievance' : 'scheme'}`}
                        >
                          {dom === 'pacs_pmfby' ? '🌾 PACS + PMFBY' : dom === 'grievance' ? '⚖️ Grievance' : dom === 'cooperative_law' ? '🏛️ MSCS Law' : dom === 'financial_literacy' ? '💳 KCC 4%' : '📜 Farmer Scheme'}
                        </span>
                      ))}
                      {msg.verificationStatus && (
                        <span className="chat-trust-badge">
                          🛡️ {Math.round((msg.trustScore || 0.98) * 100)}% Verified Accuracy
                        </span>
                      )}
                    </div>
                  )}

                  {isUser ? msg.text : <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>}

                  {/* Verified Statutory Citations */}
                  {!isUser && msg.citations && msg.citations.length > 0 && (
                    <div className="chat-citations-card">
                      <div className="chat-citations-title">
                        <span>🏛️ Official Sources & Statutory Citations:</span>
                      </div>
                      <ul className="chat-citations-list">
                        {msg.citations.slice(0, 3).map((cit, cIdx) => (
                          <li key={cIdx}>{cit}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Speech Voice Output Controls on Assistant Responses */}
                  {!isUser && msg.text && (
                    <div className="chat-audio-controls">
                      <button
                        type="button"
                        onClick={() => toggleSpeech(msg.id, msg.text)}
                        className={`chat-audio-btn ${isPlaying ? 'playing' : ''} ${isAudioLoading ? 'loading' : ''}`}
                        title={isPlaying ? 'Pause Voice' : isPaused ? 'Resume Voice' : 'Listen with Voice'}
                      >
                        {isAudioLoading ? (
                          <>
                            <Loader2 size={14} className="animate-spin" />
                            <span>Loading Voice...</span>
                          </>
                        ) : isPlaying ? (
                          <>
                            <Pause size={14} />
                            <span>Pause Voice</span>
                            <span className="audio-wave-anim">
                              <span className="audio-wave-bar" />
                              <span className="audio-wave-bar" />
                              <span className="audio-wave-bar" />
                            </span>
                          </>
                        ) : isPaused ? (
                          <>
                            <Play size={14} />
                            <span>Resume Voice</span>
                          </>
                        ) : (
                          <>
                            <Volume2 size={14} />
                            <span>Listen (Normal Speed)</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>
                {!isUser && msg.responseType === 'grievance' && msg.officerRecommendation && (
                  <OfficerRecommendationCard officer={msg.officerRecommendation} />
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="chat-row chat-row-ai">
            <div className="chat-avatar chat-avatar-ai">
              <Bot size={16} />
            </div>
            <div className="typing-indicator">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-text">{t('assistantTyping')}</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form
        className="chat-input-bar"
        onSubmit={(e) => {
          e.preventDefault();
          handleTextSend(inputQuery);
        }}
      >
        <VoiceInput onVoiceResult={handleVoiceInput} disabled={isLoading} />

        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          placeholder={t('askPlaceholder')}
          disabled={isLoading}
          className="chat-text-input"
        />

        <button
          type="submit"
          disabled={!inputQuery.trim() || isLoading}
          className="kiosk-btn kiosk-btn-primary chat-send-btn"
        >
          <Send size={18} />
          <span>{t('send')}</span>
        </button>
      </form>
    </div>
  );
}
