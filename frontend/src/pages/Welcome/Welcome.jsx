import React from 'react';
import { MessageCircle, ArrowRight } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function Welcome({ onStart }) {
  const { t } = useLanguage();

  return (
    <div className="screen-container">
      <div className="screen-card" style={{ maxWidth: '520px', width: '100%', textAlign: 'center' }}>
        <div style={{
          width: '64px',
          height: '64px',
          borderRadius: '18px',
          background: 'var(--primary-gradient)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 24px',
          color: '#fff',
        }}>
          <MessageCircle size={32} />
        </div>

        <h1 style={{ fontSize: '28px', fontWeight: '700', color: 'var(--primary-dark)', marginBottom: '12px' }}>
          {t('welcomeTitle')}
        </h1>

        <p style={{ fontSize: '16px', color: 'var(--text-muted)', lineHeight: 1.6, marginBottom: '32px' }}>
          {t('welcomeMessage')}
        </p>

        <button onClick={onStart} className="kiosk-btn kiosk-btn-primary" style={{ width: '100%', padding: '16px 24px', fontSize: '16px' }}>
          {t('startConversation')}
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  );
}
