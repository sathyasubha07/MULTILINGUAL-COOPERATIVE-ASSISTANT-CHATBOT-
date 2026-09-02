import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { sendTextQuery } from '../../services/api';
import { useLanguage } from '../../context/LanguageContext';
import VoiceInput from '../VoiceInput/VoiceInput';
import OfficerRecommendationCard from '../OfficerRecommendationCard/OfficerRecommendationCard';

export default function ChatBox() {
  const { language, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const addAssistantMessage = (response) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now() + 1,
        sender: 'ai',
        text: response.answer,
        responseType: response.responseType,
        officerRecommendation: response.officerRecommendation,
      },
    ]);
  };

  const handleTextSend = async (text) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

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

  const VOICE_PLACEHOLDER = "🎙️ Voice input captured — live transcription will be available once Bhashini backend integration is complete.";

  const handleVoiceInput = () => {
    if (isLoading) return;

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        sender: 'user',
        text: VOICE_PLACEHOLDER,
        isVoice: true,
      },
    ]);
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
                  {msg.text}
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
