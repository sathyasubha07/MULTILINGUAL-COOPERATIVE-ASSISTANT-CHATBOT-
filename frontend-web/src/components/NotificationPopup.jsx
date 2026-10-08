import React, { useEffect, useState } from 'react';
import { Bell, X, Sparkles, ArrowRight, Zap, AlertTriangle } from 'lucide-react';

export default function NotificationPopup({ 
  notification, 
  onClose, 
  onAction,
  autoCloseMs = 7000 
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

  const isUrgent = notification.priority === 'High';
  const isPersonal = notification.badge === 'Personalized' || notification.type === 'New Eligibility';

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 9999,
        maxWidth: '420px',
        width: 'calc(100vw - 48px)',
        background: 'var(--header-bg)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        borderRadius: '1rem',
        border: isPersonal 
          ? '1.5px solid #10b981' 
          : isUrgent 
            ? '1.5px solid #ef4444' 
            : '1.5px solid #2563eb',
        boxShadow: '0 12px 36px rgba(0, 0, 0, 0.25)',
        padding: '1.15rem',
        transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        transform: visible ? 'translateY(0) scale(1)' : 'translateY(20px) scale(0.95)',
        opacity: visible ? 1 : 0,
        pointerEvents: visible ? 'all' : 'none'
      }}
    >
      {/* Header bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            background: isUrgent ? '#ef4444' : isPersonal ? '#10b981' : '#2563eb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff'
          }}>
            {isPersonal ? <Sparkles size={15} /> : isUrgent ? <AlertTriangle size={15} /> : <Bell size={15} />}
          </div>
          <span style={{
            fontSize: '0.78rem',
            fontWeight: '700',
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            color: isUrgent ? '#ef4444' : isPersonal ? '#10b981' : '#2563eb'
          }}>
            {notification.badge || 'Scheme Alert'}
          </span>
        </div>

        <button
          onClick={() => {
            setVisible(false);
            setTimeout(onClose, 300);
          }}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '0.2rem',
            borderRadius: '0.3rem',
            display: 'flex'
          }}
        >
          <X size={16} />
        </button>
      </div>

      {/* Title & snippet */}
      <h4 style={{
        fontSize: '0.92rem',
        fontWeight: '700',
        color: 'var(--text-primary)',
        margin: '0 0 0.3rem 0',
        lineHeight: '1.3'
      }}>
        {notification.title}
      </h4>
      <p style={{
        fontSize: '0.82rem',
        color: 'var(--text-secondary)',
        lineHeight: '1.4',
        margin: '0 0 0.75rem 0'
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
          className="btn-primary"
          style={{
            padding: '0.4rem 0.85rem',
            fontSize: '0.8rem',
            fontWeight: '600',
            borderRadius: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.35rem'
          }}
        >
          <span>View / Ask AI</span>
          <ArrowRight size={13} />
        </button>
      </div>
    </div>
  );
}
