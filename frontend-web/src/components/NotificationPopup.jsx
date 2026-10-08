import React, { useEffect, useState } from 'react';
import { Bell, X, Sparkles, ArrowRight, Zap, AlertTriangle, Flame } from 'lucide-react';

export default function NotificationPopup({ 
  notification, 
  onClose, 
  onAction,
  autoCloseMs = 8000 
}) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (notification) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
        setTimeout(onClose, 300);
      }, autoCloseMs);
      return () => clearTimeout(timer);
    }
  }, [notification, autoCloseMs, onClose]);

  if (!notification) return null;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 99999,
        maxWidth: '440px',
        width: 'calc(100vw - 48px)',
        background: 'var(--header-bg)',
        backdropFilter: 'blur(18px)',
        WebkitBackdropFilter: 'blur(18px)',
        borderRadius: '1.1rem',
        border: '1.5px solid rgba(239, 68, 68, 0.65)',
        boxShadow: '0 16px 40px rgba(239, 68, 68, 0.22), 0 8px 24px rgba(0, 0, 0, 0.35)',
        padding: '1.15rem 1.25rem',
        transition: 'all 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
        transform: visible ? 'translateY(0) scale(1)' : 'translateY(24px) scale(0.94)',
        opacity: visible ? 1 : 0,
        pointerEvents: visible ? 'all' : 'none'
      }}
    >
      {/* Header bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
          <div style={{
            width: '30px',
            height: '30px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 2px 10px rgba(239, 68, 68, 0.45)'
          }}>
            <Bell size={16} />
          </div>
          <span style={{
            fontSize: '0.78rem',
            fontWeight: '800',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: '#ef4444'
          }}>
            🔴 {notification.badge || 'Scheme Notification'}
          </span>
        </div>

        <button
          onClick={() => {
            setVisible(false);
            setTimeout(onClose, 300);
          }}
          aria-label="Dismiss notification"
          style={{
            background: 'rgba(255, 255, 255, 0.06)',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '0.3rem',
            borderRadius: '0.4rem',
            display: 'flex'
          }}
        >
          <X size={16} />
        </button>
      </div>

      {/* Title & snippet */}
      <h4 style={{
        fontSize: '0.96rem',
        fontWeight: '800',
        color: 'var(--text-primary)',
        margin: '0 0 0.35rem 0',
        lineHeight: '1.35'
      }}>
        {notification.title}
      </h4>
      <p style={{
        fontSize: '0.84rem',
        color: 'var(--text-secondary)',
        lineHeight: '1.45',
        margin: '0 0 0.85rem 0'
      }}>
        {notification.message}
      </p>

      {/* Action Button */}
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
        <button
          onClick={() => {
            setVisible(false);
            onAction(notification.action_query || `Tell me more about ${notification.title}`);
            setTimeout(onClose, 300);
          }}
          style={{
            padding: '0.45rem 0.95rem',
            fontSize: '0.82rem',
            fontWeight: '700',
            borderRadius: '0.6rem',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
            background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
            color: '#ffffff',
            border: 'none',
            cursor: 'pointer',
            boxShadow: '0 3px 12px rgba(239, 68, 68, 0.4)'
          }}
        >
          <span>View / Ask AI</span>
          <ArrowRight size={13} />
        </button>
      </div>
    </div>
  );
}
