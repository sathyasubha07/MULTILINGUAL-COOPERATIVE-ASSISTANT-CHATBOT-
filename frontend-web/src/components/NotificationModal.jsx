import React, { useState } from 'react';
import { TRANSLATIONS } from '../translations';
import { 
  X, Bell, AlertTriangle, CheckCircle2, Sparkles, ExternalLink, 
  MessageSquare, ArrowRight, Zap, Clock, Info, ShieldCheck, Flame
} from 'lucide-react';

export default function NotificationModal({ 
  langCode, 
  notifications = [], 
  onSelectQuery, 
  onMarkRead, 
  onClose,
  onOpenAccount,
  user
}) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [filter, setFilter] = useState('all'); // all, urgent, eligibility, updates

  const filteredNotifs = notifications.filter((n) => {
    if (filter === 'urgent') return n.priority === 'High' || n.category === 'Emergency';
    if (filter === 'eligibility') return n.type === 'New Eligibility' || n.badge === 'Personalized' || n.type === 'Credit Opportunity';
    if (filter === 'updates') return n.badge !== 'Personalized' && n.type !== 'New Eligibility';
    return true;
  });

  // Determines card presentation based on emergency / opportunity type:
  // - Emergency / Urgent Deadlines -> Warm Golden Yellow / Amber
  // - Newly Unlocked / Subsidy Match -> Fresh Emerald Green
  // - Major Policy Updates -> Professional Royal Blue
  const getNotificationTheme = (item) => {
    const isUrgent = item.priority === 'High' || item.category === 'Emergency' || item.title?.toLowerCase().includes('window') || item.title?.toLowerCase().includes('urgent');
    const isUnlockedOrBenefit = item.type === 'New Eligibility' || item.badge === 'Personalized' || item.type === 'Credit Opportunity' || item.title?.toLowerCase().includes('unlocked') || item.title?.toLowerCase().includes('subsidy');

    if (isUrgent) {
      return {
        type: 'urgent',
        badgeBg: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
        badgeBorder: '1px solid #d97706',
        badgeText: '#ffffff',
        badgeLabel: '⏳ ACTION REQUIRED / DEADLINE',
        cardBg: 'linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.02) 100%)',
        cardBorder: '1px solid rgba(245, 158, 11, 0.45)',
        hoverBorder: 'rgba(245, 158, 11, 0.8)',
        btnBg: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
        btnShadow: '0 3px 12px rgba(245, 158, 11, 0.35)',
        impactBg: 'rgba(245, 158, 11, 0.1)',
        impactBorder: '1px solid rgba(245, 158, 11, 0.35)',
        impactText: '#d97706',
        impactIconColor: '#f59e0b',
        codeBg: 'rgba(245, 158, 11, 0.15)',
        codeText: '#d97706',
        codeBorder: '1px solid rgba(245, 158, 11, 0.3)'
      };
    }

    if (isUnlockedOrBenefit) {
      return {
        type: 'unlocked',
        badgeBg: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        badgeBorder: '1px solid #059669',
        badgeText: '#ffffff',
        badgeLabel: '✨ NEWLY UNLOCKED SCHEME',
        cardBg: 'linear-gradient(180deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.02) 100%)',
        cardBorder: '1px solid rgba(16, 185, 129, 0.45)',
        hoverBorder: 'rgba(16, 185, 129, 0.8)',
        btnBg: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        btnShadow: '0 3px 12px rgba(16, 185, 129, 0.35)',
        impactBg: 'rgba(16, 185, 129, 0.1)',
        impactBorder: '1px solid rgba(16, 185, 129, 0.35)',
        impactText: '#10b981',
        impactIconColor: '#10b981',
        codeBg: 'rgba(16, 185, 129, 0.15)',
        codeText: '#10b981',
        codeBorder: '1px solid rgba(16, 185, 129, 0.3)'
      };
    }

    // Standard Scheme Update
    return {
      type: 'update',
      badgeBg: 'linear-gradient(135deg, #0284c7 0%, #2563eb 100%)',
      badgeBorder: '1px solid #2563eb',
      badgeText: '#ffffff',
      badgeLabel: '📢 SCHEME UPDATE',
      cardBg: 'linear-gradient(180deg, rgba(37, 99, 235, 0.06) 0%, rgba(37, 99, 235, 0.01) 100%)',
      cardBorder: '1px solid rgba(37, 99, 235, 0.35)',
      hoverBorder: 'rgba(37, 99, 235, 0.75)',
      btnBg: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
      btnShadow: '0 3px 12px rgba(37, 99, 235, 0.35)',
      impactBg: 'rgba(37, 99, 235, 0.08)',
      impactBorder: '1px solid rgba(37, 99, 235, 0.25)',
      impactText: '#2563eb',
      impactIconColor: '#2563eb',
      codeBg: 'rgba(37, 99, 235, 0.12)',
      codeText: '#2563eb',
      codeBorder: '1px solid rgba(37, 99, 235, 0.25)'
    };
  };

  return (
    <div className="modal-overlay" onClick={onClose} style={{ zIndex: 99999 }}>
      <div 
        className="modal-content notification-modal-box" 
        onClick={(e) => e.stopPropagation()} 
        style={{ 
          maxWidth: '680px', 
          width: '94vw',
          maxHeight: '88vh', 
          display: 'flex', 
          flexDirection: 'column',
          borderRadius: '1.25rem',
          border: '1px solid var(--bg-card-border)',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.45)',
          background: 'var(--bg-card)',
          overflow: 'hidden',
          animation: 'slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
        }}
      >
        {/* Sticky Modal Header - ONLY Name & Bell in Red */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'var(--header-bg)',
          flexShrink: 0
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.9rem' }}>
            {/* Red Glowing Notification Icon */}
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: '0.85rem',
              background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              boxShadow: '0 4px 18px rgba(239, 68, 68, 0.45)',
              position: 'relative',
              flexShrink: 0
            }}>
              <Bell size={22} />
              <span style={{
                position: 'absolute',
                top: '-3px',
                right: '-3px',
                width: '11px',
                height: '11px',
                borderRadius: '50%',
                background: '#ffedd5',
                border: '2px solid #ef4444'
              }} />
            </div>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
                <h2 style={{ fontSize: '1.22rem', fontWeight: '800', color: '#ef4444', margin: 0, letterSpacing: '-0.01em' }}>
                  Notifications & Scheme Updates
                </h2>
                <span style={{
                  fontSize: '0.68rem',
                  fontWeight: '800',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  padding: '0.18rem 0.5rem',
                  borderRadius: '1rem',
                  background: 'rgba(239, 68, 68, 0.12)',
                  color: '#ef4444',
                  border: '1px solid rgba(239, 68, 68, 0.3)'
                }}>
                  {filteredNotifs.length} Active
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.2rem 0 0 0' }}>
                Official announcements, yellow action deadlines & green eligible subsidies
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            aria-label="Close Notifications"
            style={{
              background: 'rgba(255, 255, 255, 0.06)',
              border: '1px solid var(--bg-card-border)',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '0.45rem',
              borderRadius: '0.6rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(239, 68, 68, 0.12)';
              e.currentTarget.style.color = '#ef4444';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.06)';
              e.currentTarget.style.color = 'var(--text-muted)';
            }}
          >
            <X size={19} />
          </button>
        </div>

        {/* Sticky Professional Filter Bar */}
        <div style={{
          padding: '0.75rem 1.5rem',
          display: 'flex',
          gap: '0.55rem',
          borderBottom: '1px solid var(--bg-card-border)',
          background: 'var(--bg-main)',
          flexShrink: 0,
          overflowX: 'auto',
          scrollbarWidth: 'none'
        }}>
          {[
            { id: 'all', label: 'All Notifications' },
            { id: 'urgent', label: '🟡 Urgent & Deadlines' },
            { id: 'eligibility', label: '🟢 Eligible For You' },
            { id: 'updates', label: '🔵 Scheme Updates' }
          ].map((tab) => {
            const isActive = filter === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setFilter(tab.id)}
                style={{
                  padding: '0.42rem 0.95rem',
                  borderRadius: '2rem',
                  border: isActive ? '1px solid var(--primary-color, #2563eb)' : '1px solid var(--bg-card-border)',
                  background: isActive ? 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)' : 'var(--bg-card)',
                  color: isActive ? '#ffffff' : 'var(--text-primary)',
                  fontSize: '0.8rem',
                  fontWeight: isActive ? '700' : '500',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  boxShadow: isActive ? '0 3px 10px rgba(37, 99, 235, 0.35)' : 'none',
                  transition: 'all 0.2s ease',
                  flexShrink: 0
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Scrollable Notification List with Green / Yellow Semantic Cards */}
        <div 
          className="notification-scroll-container"
          style={{
            padding: '1.25rem 1.5rem',
            overflowY: 'auto',
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            overscrollBehavior: 'contain',
            scrollBehavior: 'smooth'
          }}
        >
          {filteredNotifs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3.5rem 1rem', color: 'var(--text-muted)' }}>
              <div style={{
                width: '60px',
                height: '60px',
                borderRadius: '50%',
                background: 'rgba(16, 185, 129, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
                color: '#10b981'
              }}>
                <CheckCircle2 size={32} />
              </div>
              <p style={{ margin: 0, fontWeight: '700', fontSize: '1.05rem', color: 'var(--text-primary)' }}>
                You are all caught up!
              </p>
              <p style={{ fontSize: '0.84rem', marginTop: '0.35rem', color: 'var(--text-muted)' }}>
                No active notifications found in this category right now.
              </p>
            </div>
          ) : (
            filteredNotifs.map((item) => {
              const theme = getNotificationTheme(item);

              return (
                <div
                  key={item.id}
                  className="notification-card-item"
                  style={{
                    padding: '1.15rem 1.25rem',
                    borderRadius: '1rem',
                    background: theme.cardBg,
                    border: theme.cardBorder,
                    boxShadow: '0 4px 14px rgba(0, 0, 0, 0.08)',
                    transition: 'transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease',
                    position: 'relative'
                  }}
                >
                  {/* Top Bar with Badges */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                      <span style={{
                        fontSize: '0.72rem',
                        fontWeight: '800',
                        letterSpacing: '0.04em',
                        padding: '0.22rem 0.65rem',
                        borderRadius: '2rem',
                        background: theme.badgeBg,
                        color: theme.badgeText,
                        border: theme.badgeBorder,
                        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.3rem'
                      }}>
                        {theme.badgeLabel}
                      </span>

                      {item.scheme_code && (
                        <span style={{
                          fontSize: '0.72rem',
                          fontWeight: '700',
                          padding: '0.2rem 0.55rem',
                          borderRadius: '0.4rem',
                          background: theme.codeBg,
                          color: theme.codeText,
                          border: theme.codeBorder
                        }}>
                          {item.scheme_code}
                        </span>
                      )}

                      {item.category && (
                        <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)', fontWeight: '600' }}>
                          • {item.category}
                        </span>
                      )}
                    </div>

                    {item.date && (
                      <span style={{ 
                        fontSize: '0.74rem', 
                        color: 'var(--text-muted)', 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: '0.25rem',
                        fontWeight: '500'
                      }}>
                        <Clock size={12} />
                        {item.date}
                      </span>
                    )}
                  </div>

                  {/* Title */}
                  <h3 style={{
                    fontSize: '1.02rem',
                    fontWeight: '800',
                    color: 'var(--text-primary)',
                    margin: '0 0 0.45rem 0',
                    lineHeight: '1.35'
                  }}>
                    {item.title}
                  </h3>

                  {/* Message */}
                  <p style={{
                    fontSize: '0.86rem',
                    color: 'var(--text-secondary)',
                    lineHeight: '1.5',
                    margin: '0 0 0.85rem 0'
                  }}>
                    {item.message}
                  </p>

                  {/* Highlight Benefit Box */}
                  {item.impact && (
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.45rem',
                      padding: '0.55rem 0.85rem',
                      borderRadius: '0.6rem',
                      background: theme.impactBg,
                      border: theme.impactBorder,
                      color: theme.impactText,
                      fontSize: '0.8rem',
                      fontWeight: '700',
                      marginBottom: '0.9rem'
                    }}>
                      <Zap size={15} color={theme.impactIconColor} style={{ flexShrink: 0 }} />
                      <span>Benefit Impact: {item.impact}</span>
                    </div>
                  )}

                  {/* Action Shortcuts */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
                    <button
                      onClick={() => {
                        onSelectQuery(item.action_query || `Tell me full details about ${item.title}`);
                        onMarkRead(item.id);
                        onClose();
                      }}
                      style={{
                        padding: '0.48rem 0.95rem',
                        fontSize: '0.82rem',
                        fontWeight: '700',
                        borderRadius: '0.65rem',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.4rem',
                        background: theme.btnBg,
                        color: '#ffffff',
                        border: 'none',
                        cursor: 'pointer',
                        boxShadow: theme.btnShadow,
                        transition: 'transform 0.15s ease, box-shadow 0.15s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-1px)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                      }}
                    >
                      <MessageSquare size={14} />
                      <span>Ask AI Assistant</span>
                    </button>

                    {item.scheme_code && (
                      <button
                        onClick={() => {
                          onSelectQuery(`What are the documents, guidelines and eligibility criteria for ${item.scheme_code}?`);
                          onMarkRead(item.id);
                          onClose();
                        }}
                        style={{
                          padding: '0.48rem 0.95rem',
                          fontSize: '0.82rem',
                          fontWeight: '600',
                          borderRadius: '0.65rem',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.4rem',
                          background: 'rgba(255, 255, 255, 0.05)',
                          color: 'var(--text-primary)',
                          border: '1px solid var(--bg-card-border)',
                          cursor: 'pointer',
                          transition: 'all 0.15s ease'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
                        }}
                      >
                        <ExternalLink size={14} />
                        <span>Check Criteria</span>
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer info box */}
        <div style={{
          padding: '0.9rem 1.5rem',
          borderTop: '1px solid var(--bg-card-border)',
          background: 'var(--bg-main)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '0.6rem',
          flexShrink: 0
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            <Sparkles size={16} color="#10b981" />
            <span>Update your farm details anytime to trigger new scheme matches.</span>
          </div>

          <button
            onClick={() => {
              onClose();
              if (onOpenAccount) onOpenAccount();
            }}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#10b981',
              fontWeight: '700',
              fontSize: '0.84rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem',
              padding: '0.2rem 0'
            }}
          >
            <span>Edit Profile</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}
