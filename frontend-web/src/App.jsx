import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import LanguageSelectionScreen from './components/LanguageSelectionScreen';
import ChatInterface from './components/ChatInterface';
import TopicShortcuts from './components/TopicShortcuts';
import FaqModal from './components/FaqModal';
import OfficeLocatorModal from './components/OfficeLocatorModal';
import { sendTextQuery, sendVoiceQuery } from './services/api';
import { downloadConversationPDF } from './utils/pdfExport';
import { TRANSLATIONS } from './translations';

/**
 * Multilingual Cooperative Assistant — Web Frontend Root App
 * 
 * ARCHITECTURE NOTICE:
 * This web-facing frontend is built inside /frontend-web and runs on Port 5174.
 * It is completely separate from the kiosk frontend in /frontend (Port 5173).
 * Both frontends communicate with the shared backend API (http://localhost:8000/api/v1).
 */
export default function App() {
  // Session & Preferences State
  const [langCode, setLangCode] = useState('en');
  const [showLangScreen, setShowLangScreen] = useState(true);
  const [theme, setTheme] = useState('light');
  const [textSize, setTextSize] = useState('normal');

  // Modal Visibility State
  const [activeModal, setActiveModal] = useState(null); // 'lang', 'faq', 'locator' or null

  // Chat State
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Sync theme & text-size attributes to document root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute('data-text-size', textSize);
  }, [textSize]);

  // Handlers
  const handleSelectLanguage = (code) => {
    setLangCode(code);
  };

  const handleConfirmLanguage = () => {
    setShowLangScreen(false);
  };

  const handleToggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const handleToggleTextSize = () => {
    setTextSize((prev) => (prev === 'normal' ? 'large' : 'normal'));
  };

  const handleSendMessage = async (text) => {
    const userMsg = {
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await sendTextQuery(text, langCode);
      const assistantMsg = {
        sender: 'assistant',
        text: res.answer,
        responseType: res.responseType,
        officerRecommendation: res.officerRecommendation,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: 'An error occurred while connecting to the assistant. Please try again.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendVoice = async (audioBlob) => {
    setIsLoading(true);

    try {
      const res = await sendVoiceQuery(audioBlob, langCode);
      
      if (res.transcription) {
        setMessages((prev) => [
          ...prev,
          {
            sender: 'user',
            text: res.transcription,
            transcription: res.transcription,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          },
        ]);
      }

      const assistantMsg = {
        sender: 'assistant',
        text: res.answer,
        responseType: res.responseType,
        officerRecommendation: res.officerRecommendation,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error('Voice chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetChat = () => {
    setMessages([]);
  };

  const handleDownloadPdf = () => {
    const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
    downloadConversationPDF(messages, langCode, t.appName);
  };

  // If first visit, present native language selection screen
  if (showLangScreen) {
    return (
      <LanguageSelectionScreen
        selectedLang={langCode}
        onSelectLanguage={handleSelectLanguage}
        onConfirm={handleConfirmLanguage}
      />
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header Bar */}
      <Header
        langCode={langCode}
        theme={theme}
        onToggleTheme={handleToggleTheme}
        textSize={textSize}
        onToggleTextSize={handleToggleTextSize}
        onOpenLangModal={() => setActiveModal('lang')}
        onOpenFaq={() => setActiveModal('faq')}
        onOpenLocator={() => setActiveModal('locator')}
        onResetChat={handleResetChat}
        hasMessages={messages.length > 0}
      />

      {/* Main Container */}
      <main style={{
        flex: 1,
        maxWidth: '1000px',
        width: '100%',
        margin: '0 auto',
        padding: '1.5rem 1rem',
        display: 'flex',
        flexDirection: 'column',
      }}>
        {/* Empty state: Show Topic Shortcuts */}
        {messages.length === 0 ? (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1.5rem',
            margin: 'auto 0',
          }}>
            <TopicShortcuts
              langCode={langCode}
              onSelectTopic={handleSendMessage}
            />

            {/* Embedded Initial Chat Input Box */}
            <div className="glass-panel" style={{ padding: '1.5rem' }}>
              <ChatInterface
                messages={messages}
                langCode={langCode}
                onSendMessage={handleSendMessage}
                onSendVoice={handleSendVoice}
                isLoading={isLoading}
                onDownloadPdf={handleDownloadPdf}
              />
            </div>
          </div>
        ) : (
          /* Active Chat Conversation view */
          <div className="glass-panel" style={{
            flex: 1,
            padding: '1.5rem',
            display: 'flex',
            flexDirection: 'column',
            minHeight: '650px',
          }}>
            <ChatInterface
              messages={messages}
              langCode={langCode}
              onSendMessage={handleSendMessage}
              onSendVoice={handleSendVoice}
              isLoading={isLoading}
              onDownloadPdf={handleDownloadPdf}
            />
          </div>
        )}
      </main>

      {/* Modals */}
      {activeModal === 'lang' && (
        <div className="modal-overlay" onClick={() => setActiveModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '750px' }}>
            <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--bg-card-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h2 style={{ fontSize: '1.15rem', fontWeight: '700' }}>Select Session Language</h2>
              <button onClick={() => setActiveModal(null)} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)' }}>✕</button>
            </div>
            <div style={{ padding: '1.5rem' }}>
              <LanguageSelectionScreen
                selectedLang={langCode}
                onSelectLanguage={(code) => {
                  handleSelectLanguage(code);
                  setActiveModal(null);
                }}
                onConfirm={() => setActiveModal(null)}
              />
            </div>
          </div>
        </div>
      )}

      {activeModal === 'faq' && (
        <FaqModal
          langCode={langCode}
          onClose={() => setActiveModal(null)}
        />
      )}

      {activeModal === 'locator' && (
        <OfficeLocatorModal
          langCode={langCode}
          onClose={() => setActiveModal(null)}
        />
      )}
    </div>
  );
}
