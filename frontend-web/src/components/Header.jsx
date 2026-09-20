import React from 'react';
import { TRANSLATIONS, LANGUAGES } from '../translations';
<<<<<<< HEAD
import { Bot, Sun, Moon, HelpCircle, MapPin, Globe, Type, RotateCcw, User, UserCheck, PanelLeft, Plus } from 'lucide-react';

/**
 * Modern Header & Navigation Bar
 * Features app branding, sidebar toggle, personal account profile button,
 * dark mode toggle, text-size toggle, language badge, FAQ & Locator shortcuts.
=======
import { Bot, Sun, Moon, HelpCircle, MapPin, Globe, Type, RotateCcw } from 'lucide-react';

/**
 * Modern Header & Navigation Bar
 * Features app branding, dark mode toggle, text-size toggle, language badge, FAQ & Locator shortcuts.
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
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
<<<<<<< HEAD
  onOpenAccount,
  user,
  onResetChat,
  hasMessages,
  sidebarOpen,
  onToggleSidebar,
=======
  onResetChat,
  hasMessages,
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const currentLang = LANGUAGES.find((l) => l.code === langCode) || LANGUAGES[0];

  return (
    <header style={{
      position: 'sticky',
      top: 0,
<<<<<<< HEAD
      zIndex: 80,
=======
      zIndex: 100,
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
      background: 'var(--header-bg)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--bg-card-border)',
<<<<<<< HEAD
      padding: '0.75rem 1.25rem',
      boxShadow: 'var(--shadow-sm)',
    }}>
      <div style={{
        maxWidth: '1280px',
=======
      padding: '0.85rem 1.5rem',
      boxShadow: 'var(--shadow-sm)',
    }}>
      <div style={{
        maxWidth: '1200px',
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
<<<<<<< HEAD
        gap: '0.75rem',
      }}>
        {/* Left: Sidebar Toggle & Branding */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {/* Sidebar Toggle Button */}
          <button
            onClick={onToggleSidebar}
            title={sidebarOpen ? 'Collapse Recent Chats' : 'Open Recent Chats'}
            style={{
              background: sidebarOpen ? 'rgba(37, 99, 235, 0.12)' : 'var(--bg-card)',
              border: '1px solid var(--bg-card-border)',
              color: sidebarOpen ? '#2563eb' : 'var(--text-primary)',
              padding: '0.45rem',
              borderRadius: '0.6rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease',
            }}
          >
            <PanelLeft size={19} />
          </button>

          <div style={{
            width: '38px',
            height: '38px',
=======
        gap: '1rem',
      }}>
        {/* Left: Branding & Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{
            width: '42px',
            height: '42px',
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
            borderRadius: '0.75rem',
            background: 'var(--primary-gradient)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff',
            boxShadow: 'var(--shadow-glow)',
          }}>
<<<<<<< HEAD
            <Bot size={22} />
          </div>

          <div>
            <h1 style={{
              fontSize: '1.15rem',
=======
            <Bot size={24} />
          </div>
          <div>
            <h1 style={{
              fontSize: '1.25rem',
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
              fontWeight: '700',
              lineHeight: '1.2',
              color: 'var(--text-primary)',
              letterSpacing: '-0.01em',
<<<<<<< HEAD
              margin: 0,
=======
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
            }}>
              {t.appName}
            </h1>
            <span style={{
<<<<<<< HEAD
              fontSize: '0.72rem',
=======
              fontSize: '0.75rem',
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
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
<<<<<<< HEAD
          gap: '0.5rem',
          flexWrap: 'wrap',
        }}>
          {/* New Chat Reset Button */}
          <button
            onClick={onResetChat}
            className="btn-secondary"
            title={t.newChat}
            style={{ padding: '0.45rem 0.8rem', fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}
          >
            <Plus size={15} color="#2563eb" />
            <span className="hide-mobile">New Chat</span>
          </button>

          {/* User Account / Profile Button */}
          <button
            onClick={onOpenAccount}
            className="btn-secondary"
            title={user ? 'View Member Account Profile' : 'Create Member Account'}
            style={{
              padding: '0.45rem 0.8rem',
              fontSize: '0.82rem',
              borderColor: user ? 'rgba(16, 185, 129, 0.4)' : 'rgba(37, 99, 235, 0.4)',
              background: user ? 'rgba(16, 185, 129, 0.08)' : 'rgba(37, 99, 235, 0.08)',
              color: user ? '#059669' : '#2563eb',
              fontWeight: '600',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}
          >
            {user ? <UserCheck size={15} color="#10b981" /> : <User size={15} color="#2563eb" />}
            <span>{user ? `${user.name.split(' ')[0]} (${user.district || 'Member'})` : 'Account'}</span>
          </button>
=======
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
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5

          {/* FAQ Modal Trigger */}
          <button
            onClick={onOpenFaq}
            className="btn-secondary"
            title={t.faq}
<<<<<<< HEAD
            style={{ padding: '0.45rem 0.75rem', fontSize: '0.82rem' }}
          >
            <HelpCircle size={16} color="#3b82f6" />
            <span className="hide-mobile">{t.faq}</span>
=======
            style={{ padding: '0.5rem 0.85rem', fontSize: '0.85rem' }}
          >
            <HelpCircle size={17} color="#3b82f6" />
            <span>{t.faq}</span>
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
          </button>

          {/* Office Locator Trigger */}
          <button
            onClick={onOpenLocator}
            className="btn-secondary"
            title={t.locator}
<<<<<<< HEAD
            style={{ padding: '0.45rem 0.75rem', fontSize: '0.82rem' }}
          >
            <MapPin size={16} color="#10b981" />
            <span className="hide-mobile">{t.locator}</span>
          </button>

          {/* Language Selector Modal Button */}
=======
            style={{ padding: '0.5rem 0.85rem', fontSize: '0.85rem' }}
          >
            <MapPin size={17} color="#10b981" />
            <span>{t.locator}</span>
          </button>

          {/* Language Selector Button */}
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
          <button
            onClick={onOpenLangModal}
            className="btn-secondary"
            title={t.changeLang}
            style={{
<<<<<<< HEAD
              padding: '0.45rem 0.75rem',
              fontSize: '0.82rem',
=======
              padding: '0.5rem 0.85rem',
              fontSize: '0.85rem',
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
              borderColor: 'rgba(59, 130, 246, 0.4)',
              background: 'rgba(59, 130, 246, 0.08)',
            }}
          >
<<<<<<< HEAD
            <Globe size={15} color="#3b82f6" />
=======
            <Globe size={16} color="#3b82f6" />
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
            <span style={{ fontWeight: '600' }}>{currentLang.native}</span>
          </button>

          {/* Text-Size Toggle (Normal / Large) */}
          <button
            onClick={onToggleTextSize}
            className="btn-secondary"
            title={textSize === 'large' ? t.textSizeNormal : t.textSizeLarge}
<<<<<<< HEAD
            style={{ padding: '0.45rem 0.65rem' }}
          >
            <Type size={15} />
            <span style={{ fontSize: '0.72rem', fontWeight: '700' }}>
=======
            style={{ padding: '0.5rem 0.7rem' }}
          >
            <Type size={16} />
            <span style={{ fontSize: '0.75rem', fontWeight: '700' }}>
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
              {textSize === 'large' ? 'A+' : 'A'}
            </span>
          </button>

          {/* Dark / Light Theme Toggle */}
          <button
            onClick={onToggleTheme}
            className="btn-secondary"
            title={theme === 'dark' ? t.themeLight : t.themeDark}
<<<<<<< HEAD
            style={{ padding: '0.45rem 0.65rem' }}
          >
            {theme === 'dark' ? (
              <Sun size={16} color="#fbbf24" />
            ) : (
              <Moon size={16} color="#6366f1" />
=======
            style={{ padding: '0.5rem 0.7rem' }}
          >
            {theme === 'dark' ? (
              <Sun size={17} color="#fbbf24" />
            ) : (
              <Moon size={17} color="#6366f1" />
>>>>>>> 81da5195a93e95f1f781c66ff8e3f8902b68e3c5
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
