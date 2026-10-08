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
  const [filter, setFilter] = useState('all'); // all, updates, eligibility, urgent

  const filteredNotifs = notifications.filter((n) => {
    if (filter === 'urgent') return n.priority === 'High';
    if (filter === 'eligibility') return n.type === 'New Eligibility' || n.badge === 'Personalized';
    if (filter === 'updates') return n.badge !== 'Personalized';
    return true;
  });

  const getBadgeStyle = (item) => {
    const isUrgent = item.priority === 'High';
    const isPersonal = item.badge === 'Personalized' || item.type === 'New Eligibility';
    
    if (isUrgent) {
      return {
        bg: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)',
        text: '#ffffff',
        border: '1px solid #dc2626',
        label: '🚨 URGENT NOTICE'
      };
    }
    if (isPersonal) {
      return {
        bg: 'linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)',
        text: '#ffffff',
        border: '1px solid #e11d48',
        label: '✨ NEWLY UNLOCKED'
      };
    }
    return {
      bg: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
      text: '#ffffff',
      border: '1px solid #ef4444',
      label: item.badge || '📢 SCHEME UPDATE'
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
          border: '1px solid rgba(239, 68, 68, 0.35)',
          boxShadow: '0 20px 60px rgba(239, 68, 68, 0.12), 0 10px 30px rgba(0, 0, 0, 0.35)',
          background: 'var(--bg-card)',
          overflow: 'hidden',
          animation: 'slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
        }}
      >
        {/* Sticky Modal Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid rgba(239, 68, 68, 0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'linear-gradient(180deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.02) 100%)',
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
              <Bell size={22} className="animate-pulse" />
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
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h2 style={{ fontSize: '1.22rem', fontWeight: '800', color: 'var(--text-primary)', margin: 0, letterSpacing: '-0.01em' }}>
                  Scheme Notifications & Updates
                </h2>
                <span style={{
                  fontSize: '0.68rem',
                  fontWeight: '800',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  padding: '0.18rem 0.5rem',
                  borderRadius: '1rem',
                  background: 'rgba(239, 68, 68, 0.15)',
                  color: '#ef4444',
                  border: '1px solid rgba(239, 68, 68, 0.3)'
                }}>
                  {filteredNotifs.length} Active
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.2rem 0 0 0' }}>
                Official government notices, subsidy revisions & dynamic eligibility unlocks
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

        {/* Sticky Filter Bar */}
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
            { id: 'urgent', label: '🚨 Action & Deadlines' },
            { id: 'eligibility', label: '✨ Eligible For You' },
            { id: 'updates', label: '📢 Scheme Updates' }
          ].map((tab) => {
            const isActive = filter === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setFilter(tab.id)}
                style={{
                  padding: '0.42rem 0.95rem',
                  borderRadius: '2rem',
                  border: isActive ? '1px solid #ef4444' : '1px solid var(--bg-card-border)',
                  background: isActive ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' : 'var(--bg-card)',
                  color: isActive ? '#ffffff' : 'var(--text-primary)',
                  fontSize: '0.8rem',
                  fontWeight: isActive ? '700' : '500',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  boxShadow: isActive ? '0 3px 10px rgba(239, 68, 68, 0.35)' : 'none',
                  transition: 'all 0.2s ease',
                  flexShrink: 0
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Scrollable Notification List */}
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
                background: 'rgba(239, 68, 68, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
                color: '#ef4444'
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
              const isUrgent = item.priority === 'High';
              const isPersonal = item.badge === 'Personalized' || item.type === 'New Eligibility';
              const badgeStyle = getBadgeStyle(item);

              return (
                <div
                  key={item.id}
                  className="notification-card-item"
                  style={{
                    padding: '1.15rem 1.25rem',
                    borderRadius: '1rem',
                    background: isUrgent 
                      ? 'linear-gradient(180deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.02) 100%)'
                      : isPersonal
                        ? 'linear-gradient(180deg, rgba(244, 63, 94, 0.06) 0%, rgba(244, 63, 94, 0.02) 100%)'
                        : 'var(--bg-card)',
                    border: isUrgent 
                      ? '1px solid rgba(239, 68, 68, 0.45)' 
                      : isPersonal
                        ? '1px solid rgba(244, 63, 94, 0.4)'
                        : '1px solid rgba(239, 68, 68, 0.25)',
                    boxShadow: isUrgent 
                      ? '0 6px 20px rgba(239, 68, 68, 0.12)' 
                      : '0 4px 14px rgba(0, 0, 0, 0.06)',
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
                        background: badgeStyle.bg,
                        color: badgeStyle.text,
                        border: badgeStyle.border,
                        boxShadow: '0 2px 8px rgba(239, 68, 68, 0.25)',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.3rem'
                      }}>
                        {badgeStyle.label}
                      </span>

                      {item.scheme_code && (
                        <span style={{
                          fontSize: '0.72rem',
                          fontWeight: '700',
                          padding: '0.2rem 0.55rem',
                          borderRadius: '0.4rem',
                          background: 'rgba(239, 68, 68, 0.1)',
                          color: '#ef4444',
                          border: '1px solid rgba(239, 68, 68, 0.2)'
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
                      background: 'rgba(239, 68, 68, 0.08)',
                      border: '1px solid rgba(239, 68, 68, 0.25)',
                      color: '#ef4444',
                      fontSize: '0.8rem',
                      fontWeight: '700',
                      marginBottom: '0.9rem'
                    }}>
                      <Flame size={15} color="#ef4444" style={{ flexShrink: 0 }} />
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
                        background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                        color: '#ffffff',
                        border: 'none',
                        cursor: 'pointer',
                        boxShadow: '0 3px 12px rgba(239, 68, 68, 0.35)',
                        transition: 'transform 0.15s ease, box-shadow 0.15s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-1px)';
                        e.currentTarget.style.boxShadow = '0 5px 16px rgba(239, 68, 68, 0.45)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = '0 3px 12px rgba(239, 68, 68, 0.35)';
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
                          background: 'rgba(239, 68, 68, 0.08)',
                          color: '#ef4444',
                          border: '1px solid rgba(239, 68, 68, 0.3)',
                          cursor: 'pointer',
                          transition: 'all 0.15s ease'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.background = 'rgba(239, 68, 68, 0.16)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.background = 'rgba(239, 68, 68, 0.08)';
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
            <Sparkles size={16} color="#ef4444" />
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
              color: '#ef4444',
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
