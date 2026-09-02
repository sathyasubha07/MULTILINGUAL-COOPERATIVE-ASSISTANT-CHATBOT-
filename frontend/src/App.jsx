import React, { useState } from 'react';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import LanguageSelection from './pages/LanguageSelection/LanguageSelection';
import Welcome from './pages/Welcome/Welcome';
import Chat from './pages/Chat/Chat';

const SCREENS = {
  LANGUAGE: 'language',
  WELCOME: 'welcome',
  CHAT: 'chat',
};

function AppContent() {
  const { hasSelectedLanguage, clearLanguage } = useLanguage();
  const [screen, setScreen] = useState(() =>
    hasSelectedLanguage ? SCREENS.WELCOME : SCREENS.LANGUAGE
  );

  const handleLanguageComplete = () => setScreen(SCREENS.WELCOME);
  const handleStartChat = () => setScreen(SCREENS.CHAT);
  const handleChangeLanguage = () => {
    clearLanguage();
    setScreen(SCREENS.LANGUAGE);
  };

  return (
    <div className="app-root">
      {screen === SCREENS.LANGUAGE && (
        <LanguageSelection onComplete={handleLanguageComplete} />
      )}
      {screen === SCREENS.WELCOME && (
        <Welcome onStart={handleStartChat} />
      )}
      {screen === SCREENS.CHAT && (
        <Chat onChangeLanguage={handleChangeLanguage} />
      )}

      <footer className="app-footer">
        Smart India Hackathon 2026 • Team BRAVITS (PS ID: SIH26088)
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}
