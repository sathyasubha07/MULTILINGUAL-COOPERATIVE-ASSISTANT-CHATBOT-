import React from 'react';
import { TRANSLATIONS, LANGUAGES } from '../translations';
import { Bot, Sun, Moon, HelpCircle, MapPin, Globe, Type, RotateCcw } from 'lucide-react';

/**
 * Modern Header & Navigation Bar
 * Features app branding, dark mode toggle, text-size toggle, language badge, FAQ & Locator shortcuts.
 */
export default function Header({
  langCode,
  theme,
  onToggleTheme,
  textSize,
  onToggleTextSize,
  onOpenLangModal,
  onOpenFaq,
  onOpenLocator,
  onResetChat,
  hasMessages,
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const currentLang = LANGUAGES.find((l) => l.code === langCode) || LANGUAGES[0];

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 100,
      background: 'var(--header-bg)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--bg-card-border)',
      padding: '0.85rem 1.5rem',
      boxShadow: 'var(--shadow-sm)',
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
      }}>
        {/* Left: Branding & Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '0.75rem',
            background: 'var(--primary-gradient)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff',
            boxShadow: 'var(--shadow-glow)',
          }}>
            <Bot size={24} />
          </div>
          <div>
            <h1 style={{
              fontSize: '1.25rem',
              fontWeight: '700',
              lineHeight: '1.2',
              color: 'var(--text-primary)',
              letterSpacing: '-0.01em',
            }}>
              {t.appName}
            </h1>
            <span style={{
              fontSize: '0.75rem',
              color: 'var(--text-muted)',
              fontWeight: '500',
              display: 'block',
            }}>
              {t.tagline}
            </span>
          </div>
        </div>

        {/* Right Controls Area */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          flexWrap: 'wrap',
        }}>
          {/* New Chat Reset Button if messages exist */}
          {hasMessages && (
            <button
              onClick={onResetChat}
              className="btn-secondary"
              title={t.newChat}
              style={{ padding: '0.5rem 0.85rem', fontSize: '0.85rem' }}
            >
              <RotateCcw size={16} />
              <span className="hide-mobile">{t.newChat}</span>
            </button>
          )}

          {/* FAQ Modal Trigger */}
          <button
            onClick={onOpenFaq}
            className="btn-secondary"
            title={t.faq}
            style={{ padding: '0.5rem 0.85rem', fontSize: '0.85rem' }}
          >
            <HelpCircle size={17} color="#3b82f6" />
            <span>{t.faq}</span>
          </button>

          {/* Office Locator Trigger */}
          <button
            onClick={onOpenLocator}
            className="btn-secondary"
            title={t.locator}
            style={{ padding: '0.5rem 0.85rem', fontSize: '0.85rem' }}
          >
            <MapPin size={17} color="#10b981" />
            <span>{t.locator}</span>
          </button>

          {/* Language Selector Button */}
          <button
            onClick={onOpenLangModal}
            className="btn-secondary"
            title={t.changeLang}
            style={{
              padding: '0.5rem 0.85rem',
              fontSize: '0.85rem',
              borderColor: 'rgba(59, 130, 246, 0.4)',
              background: 'rgba(59, 130, 246, 0.08)',
            }}
          >
            <Globe size={16} color="#3b82f6" />
            <span style={{ fontWeight: '600' }}>{currentLang.native}</span>
          </button>

          {/* Text-Size Toggle (Normal / Large) */}
          <button
            onClick={onToggleTextSize}
            className="btn-secondary"
            title={textSize === 'large' ? t.textSizeNormal : t.textSizeLarge}
            style={{ padding: '0.5rem 0.7rem' }}
          >
            <Type size={16} />
            <span style={{ fontSize: '0.75rem', fontWeight: '700' }}>
              {textSize === 'large' ? 'A+' : 'A'}
            </span>
          </button>

          {/* Dark / Light Theme Toggle */}
          <button
            onClick={onToggleTheme}
            className="btn-secondary"
            title={theme === 'dark' ? t.themeLight : t.themeDark}
            style={{ padding: '0.5rem 0.7rem' }}
          >
            {theme === 'dark' ? (
              <Sun size={17} color="#fbbf24" />
            ) : (
              <Moon size={17} color="#6366f1" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
