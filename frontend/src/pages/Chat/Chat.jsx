import React from 'react';
import { Globe } from 'lucide-react';
import ChatBox from '../../components/ChatBox/ChatBox';
import { useLanguage } from '../../context/LanguageContext';

export default function Chat({ onChangeLanguage }) {
  const { t } = useLanguage();

  return (
    <div className="chat-page">
      <div className="chat-page-header">
        <span className="chat-page-title">{t('appName')}</span>
        <button onClick={onChangeLanguage} className="change-lang-btn">
          <Globe size={16} />
          {t('changeLanguage')}
        </button>
      </div>
      <ChatBox />
    </div>
  );
}
