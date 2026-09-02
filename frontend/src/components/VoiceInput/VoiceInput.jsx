import React, { useState } from 'react';
import { Mic, Square } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function VoiceInput({ onVoiceResult, disabled }) {
  const { t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);

  const handleMicClick = () => {
    if (isRecording) {
      setIsRecording(false);
      if (onVoiceResult) {
        onVoiceResult();
      }
    } else {
      setIsRecording(true);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
      <button
        type="button"
        onClick={handleMicClick}
        disabled={disabled}
        className={`voice-btn ${isRecording ? 'voice-btn-recording' : ''}`}
        aria-label={isRecording ? t('listening') : t('voiceSearch')}
      >
        {isRecording ? <Square size={22} fill="currentColor" /> : <Mic size={22} />}
      </button>
      {isRecording && (
        <div className="recording-indicator">
          <span className="recording-dot" />
          <span className="recording-dot" />
          <span className="recording-dot" />
          <span style={{ fontSize: '11px', color: '#ef4444', fontWeight: '600', marginLeft: '4px' }}>
            {t('listening')}
          </span>
        </div>
      )}
    </div>
  );
}

