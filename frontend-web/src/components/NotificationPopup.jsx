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

  const isUrgent = notification.priority === 'High' || notification.category === 'Emergency' || notification.title?.toLowerCase().includes('window') || notification.title?.toLowerCase().includes('urgent');
  const isUnlockedOrBenefit = notification.type === 'New Eligibility' || notification.badge === 'Personalized' || notification.type === 'Credit Opportunity' || notification.title?.toLowerCase().includes('unlocked') || notification.title?.toLowerCase().includes('subsidy');

  // Semantic card theme based on case:
  let cardBorder = '1.5px solid rgba(37, 99, 235, 0.45)';
  let cardBg = 'var(--header-bg)';
  let badgeBg = 'linear-gradient(135deg, #0284c7 0%, #2563eb 100%)';
  let badgeLabel = notification.badge || 'Scheme Update';
  let btnBg = 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)';

  if (isUrgent) {
    cardBorder = '1.5px solid rgba(245, 158, 11, 0.7)';
    badgeBg = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    badgeLabel = '🟡 Action Required';
    btnBg = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
  } else if (isUnlockedOrBenefit) {
    cardBorder = '1.5px solid rgba(16, 185, 129, 0.7)';
    badgeBg = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    badgeLabel = '🟢 Eligible For You';
    btnBg = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
  }

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 99999,
        maxWidth: '440px',
        width: 'calc(100vw - 48px)',
        background: cardBg,
        backdropFilter: 'blur(18px)',
        WebkitBackdropFilter: 'blur(18px)',
        borderRadius: '1.1rem',
        border: cardBorder,
        boxShadow: '0 16px 40px rgba(0, 0, 0, 0.35)',
        padding: '1.15rem 1.25rem',
        transition: 'all 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
        transform: visible ? 'translateY(0) scale(1)' : 'translateY(24px) scale(0.94)',
        opacity: visible ? 1 : 0,
        pointerEvents: visible ? 'all' : 'none'
      }}
    >
      {/* Header bar - RED NOTIFICATION NAME */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 2px 10px rgba(239, 68, 68, 0.45)'
          }}>
            <Bell size={15} />
          </div>
          <span style={{
            fontSize: '0.82rem',
            fontWeight: '800',
            color: '#ef4444'
          }}>
            Notification
          </span>

          <span style={{
            fontSize: '0.7rem',
            fontWeight: '700',
            padding: '0.15rem 0.5rem',
            borderRadius: '1rem',
            background: badgeBg,
            color: '#ffffff',
            marginLeft: '0.25rem'
          }}>
            {badgeLabel}
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
            background: btnBg,
            color: '#ffffff',
            border: 'none',
            cursor: 'pointer',
            boxShadow: '0 3px 12px rgba(0, 0, 0, 0.25)'
          }}
        >
          <span>View / Ask AI</span>
          <ArrowRight size={13} />
        </button>
      </div>
    </div>
  );
}
