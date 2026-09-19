import React from 'react';
import { LANGUAGES, TRANSLATIONS } from '../translations';
import { Globe, Check, ArrowRight, Bot } from 'lucide-react';

/**
 * Native Script Language Selection Screen
 * Shown on initial load to establish session language before entering main chat portal.
 */
export default function LanguageSelectionScreen({ selectedLang, onSelectLanguage, onConfirm }) {
  const t = TRANSLATIONS[selectedLang] || TRANSLATIONS.en;

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(circle at 50% 20%, rgba(59, 130, 246, 0.15), transparent 70%), var(--bg-main)',
      padding: '2rem 1rem',
    }}>
      <div className="glass-panel" style={{
        maxWidth: '840px',
        width: '100%',
        padding: '2.5rem',
        borderRadius: '1.5rem',
        boxShadow: 'var(--shadow-lg)',
      }}>
        {/* Header / Logo */}
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '1rem',
            background: 'var(--primary-gradient)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            marginBottom: '1.25rem',
            boxShadow: 'var(--shadow-glow)',
          }}>
            <Bot size={36} />
          </div>
          <h1 style={{
            fontSize: '2.2rem',
            fontWeight: '700',
            background: 'var(--primary-gradient)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '0.5rem',
          }}>
            {t.appName}
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', maxWidth: '560px', margin: '0 auto' }}>
            {t.selectLanguageSubtitle}
          </p>
        </div>

        {/* Language Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
          gap: '1.25rem',
          marginBottom: '2.5rem',
        }}>
          {LANGUAGES.map((lang) => {
            const isSelected = selectedLang === lang.code;
            return (
              <button
                key={lang.code}
                onClick={() => onSelectLanguage(lang.code)}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: '1.25rem 1rem',
                  borderRadius: '1rem',
                  background: isSelected ? 'var(--primary-gradient)' : 'var(--bg-card)',
                  border: isSelected ? '2px solid transparent' : '1px solid var(--bg-card-border)',
                  color: isSelected ? '#ffffff' : 'var(--text-primary)',
                  boxShadow: isSelected ? 'var(--shadow-glow)' : 'var(--shadow-sm)',
                  cursor: 'pointer',
                  transform: isSelected ? 'scale(1.03)' : 'scale(1)',
                  transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                  position: 'relative',
                }}
              >
                {isSelected && (
                  <div style={{
                    position: 'absolute',
                    top: '8px',
                    right: '8px',
                    background: 'rgba(255, 255, 255, 0.25)',
                    borderRadius: '50%',
                    padding: '2px',
                    display: 'flex',
                  }}>
                    <Check size={14} color="#fff" />
                  </div>
                )}
                <span style={{ fontSize: '1.8rem', marginBottom: '0.4rem' }}>{lang.native}</span>
                <span style={{
                  fontSize: '0.88rem',
                  opacity: isSelected ? 0.9 : 0.7,
                  fontWeight: '500',
                }}>
                  {lang.name}
                </span>
              </button>
            );
          })}
        </div>

        {/* Action Button */}
        <div style={{ textAlign: 'center' }}>
          <button
            onClick={onConfirm}
            className="btn-primary"
            style={{
              padding: '0.9rem 2.5rem',
              fontSize: '1.1rem',
              borderRadius: '0.85rem',
              width: '100%',
              maxWidth: '320px',
              justifyContent: 'center',
            }}
          >
            <span>{t.continueBtn}</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
