import React from 'react';
import { Globe } from 'lucide-react';
import { LANGUAGES } from '../../utils/languages';
import { useLanguage } from '../../context/LanguageContext';

export default function LanguageSelection({ onComplete }) {
  const { setLanguage, t } = useLanguage();

  const handleSelect = (code) => {
    setLanguage(code);
    onComplete();
  };

  return (
    <div className="screen-container">
      <div className="screen-card" style={{ maxWidth: '480px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: '16px',
            background: 'var(--primary-gradient)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px',
            color: '#fff',
          }}>
            <Globe size={28} />
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: '700', color: 'var(--primary-dark)', marginBottom: '8px' }}>
            {t('selectLanguageTitle')}
          </h1>
          <p style={{ fontSize: '14px', color: 'var(--text-muted)' }}>
            {t('selectLanguageHint')}
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => handleSelect(lang.code)}
              className="language-option-btn"
            >
              {lang.native}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
