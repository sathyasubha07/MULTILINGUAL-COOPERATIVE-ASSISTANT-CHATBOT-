import React, { useState } from 'react';
import { TRANSLATIONS } from '../translations';
import { 
  X, Bell, AlertTriangle, CheckCircle2, Sparkles, ExternalLink, 
  MessageSquare, ArrowRight, ShieldAlert, Zap, Clock, Filter 
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

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="modal-content" 
        onClick={(e) => e.stopPropagation()} 
        style={{ maxWidth: '640px', maxHeight: '88vh', display: 'flex', flexDirection: 'column' }}
      >
        {/* Modal Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'var(--header-bg)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '0.75rem',
              background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              boxShadow: '0 4px 12px rgba(37, 99, 235, 0.25)'
            }}>
              <Bell size={22} />
            </div>
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                Scheme Alerts & Live Notifications
              </h2>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Real-time updates on subsidies, eligibility unlocks & deadlines
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '0.4rem',
              borderRadius: '0.5rem',
              display: 'flex',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Filter Pills */}
        <div style={{
          padding: '0.75rem 1.5rem',
          display: 'flex',
          gap: '0.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          background: 'var(--bg-main)',
          overflowX: 'auto'
        }}>
          {[
            { id: 'all', label: 'All Alerts' },
            { id: 'urgent', label: '🚨 Urgent / Deadlines' },
            { id: 'eligibility', label: '✨ Personalized Eligibility' },
            { id: 'updates', label: '📢 Major Scheme Updates' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilter(tab.id)}
              style={{
                padding: '0.4rem 0.85rem',
                borderRadius: '2rem',
                border: filter === tab.id ? '1px solid #2563eb' : '1px solid var(--bg-card-border)',
                background: filter === tab.id ? 'rgba(37, 99, 235, 0.12)' : 'var(--bg-card)',
                color: filter === tab.id ? '#2563eb' : 'var(--text-primary)',
                fontSize: '0.8rem',
                fontWeight: filter === tab.id ? '600' : '500',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                transition: 'all 0.2s ease'
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Notification List Container */}
        <div style={{
          padding: '1.25rem 1.5rem',
          overflowY: 'auto',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {filteredNotifs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2.5rem 1rem', color: 'var(--text-muted)' }}>
              <CheckCircle2 size={42} color="#10b981" style={{ margin: '0 auto 0.75rem' }} />
              <p style={{ margin: 0, fontWeight: '600', fontSize: '1rem', color: 'var(--text-primary)' }}>
                You are all caught up!
              </p>
              <p style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>
                No active notifications in this category right now.
              </p>
            </div>
          ) : (
            filteredNotifs.map((item) => {
              const isUrgent = item.priority === 'High';
              const isPersonal = item.badge === 'Personalized' || item.type === 'New Eligibility';
              return (
                <div
                  key={item.id}
                  style={{
                    padding: '1rem 1.15rem',
                    borderRadius: '0.85rem',
                    background: isPersonal 
                      ? 'rgba(16, 185, 129, 0.05)' 
                      : isUrgent 
                        ? 'rgba(239, 68, 68, 0.04)' 
                        : 'var(--bg-card)',
                    border: isPersonal 
                      ? '1px solid rgba(16, 185, 129, 0.3)' 
                      : isUrgent 
                        ? '1px solid rgba(239, 68, 68, 0.3)' 
                        : '1px solid var(--bg-card-border)',
                    boxShadow: 'var(--shadow-sm)',
                    transition: 'all 0.2s ease',
                    position: 'relative'
                  }}
                >
                  {/* Top Badges */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.45rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                      <span style={{
                        fontSize: '0.72rem',
                        fontWeight: '700',
                        padding: '0.2rem 0.55rem',
                        borderRadius: '1rem',
                        background: isUrgent ? '#ef4444' : isPersonal ? '#10b981' : '#2563eb',
                        color: '#ffffff'
                      }}>
                        {item.badge || (isUrgent ? 'Urgent' : 'Update')}
                      </span>
                      {item.category && (
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '600' }}>
                          • {item.category}
                        </span>
                      )}
                    </div>
                    {item.date && (
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        {item.date}
                      </span>
                    )}
                  </div>

                  {/* Title & Message */}
                  <h4 style={{
                    fontSize: '0.98rem',
                    fontWeight: '700',
                    color: 'var(--text-primary)',
                    margin: '0 0 0.35rem 0',
                    lineHeight: '1.35'
                  }}>
                    {item.title}
                  </h4>
                  <p style={{
                    fontSize: '0.86rem',
                    color: 'var(--text-secondary)',
                    lineHeight: '1.45',
                    margin: '0 0 0.75rem 0'
                  }}>
                    {item.message}
                  </p>

                  {/* Impact Highlight */}
                  {item.impact && (
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.4rem',
                      padding: '0.45rem 0.75rem',
                      borderRadius: '0.5rem',
                      background: 'rgba(37, 99, 235, 0.08)',
                      color: '#2563eb',
                      fontSize: '0.78rem',
                      fontWeight: '600',
                      marginBottom: '0.75rem'
                    }}>
                      <Zap size={14} />
                      <span>Benefit Impact: {item.impact}</span>
                    </div>
                  )}

                  {/* Actions */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
                    <button
                      onClick={() => {
                        onSelectQuery(item.action_query || `Tell me full details about ${item.title}`);
                        onMarkRead(item.id);
                        onClose();
                      }}
                      className="btn-primary"
                      style={{
                        padding: '0.45rem 0.85rem',
                        fontSize: '0.8rem',
                        fontWeight: '600',
                        borderRadius: '0.6rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.35rem'
                      }}
                    >
                      <MessageSquare size={14} />
                      <span>Ask AI Assistant</span>
                    </button>

                    {item.scheme_code && (
                      <button
                        onClick={() => {
                          onSelectQuery(`What are the documents and eligibility criteria for ${item.scheme_code}?`);
                          onMarkRead(item.id);
                          onClose();
                        }}
                        className="btn-secondary"
                        style={{
                          padding: '0.45rem 0.85rem',
                          fontSize: '0.8rem',
                          fontWeight: '600',
                          borderRadius: '0.6rem',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.35rem'
                        }}
                      >
                        <ExternalLink size={14} />
                        <span>Check Requirements</span>
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
          padding: '1rem 1.5rem',
          borderTop: '1px solid var(--bg-card-border)',
          background: 'var(--bg-main)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '0.6rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <Sparkles size={16} color="#10b981" />
            <span>Update your profile anytime to automatically check newly unlocked schemes.</span>
          </div>

          <button
            onClick={() => {
              onClose();
              if (onOpenAccount) onOpenAccount();
            }}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#2563eb',
              fontWeight: '700',
              fontSize: '0.82rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem'
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
