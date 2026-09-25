import React, { useState, useRef } from 'react';
import { Mic, Square } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function VoiceInput({ onVoiceResult, disabled }) {
  const { language, t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const recognitionRef = useRef(null);
  const transcriptRef = useRef('');

  const startRecording = async () => {
    setIsRecording(true);
    audioChunksRef.current = [];
    transcriptRef.current = '';

    // Map language code to speech recognition locale
    const langLocales = {
      en: 'en-IN',
      hi: 'hi-IN',
      ta: 'ta-IN',
      te: 'te-IN',
      mr: 'mr-IN',
      kn: 'kn-IN',
      bn: 'bn-IN',
      gu: 'gu-IN',
      ml: 'ml-IN',
      pa: 'pa-IN',
      or: 'or-IN',
    };

    // 1. Initialize Web Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = langLocales[language] || 'en-IN';
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;

        recognition.onresult = (event) => {
          let fullTranscript = '';
          for (let i = 0; i < event.results.length; i++) {
            if (event.results[i][0]) {
              fullTranscript += event.results[i][0].transcript;
            }
          }
          if (fullTranscript.trim()) {
            transcriptRef.current = fullTranscript.trim();
          }
        };

        recognition.onerror = (err) => {
          console.warn('SpeechRecognition error:', err);
        };

        recognition.onend = () => {
          if (isRecording && transcriptRef.current) {
            stopRecording();
          }
        };

        recognition.start();
        recognitionRef.current = recognition;
      } catch (err) {
        console.warn('SpeechRecognition init error:', err);
      }
    }

    // 2. Initialize MediaStream recording for audio fallback
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = () => {
          const audioBlob = audioChunksRef.current.length > 0 ? new Blob(audioChunksRef.current, { type: 'audio/wav' }) : null;
          stream.getTracks().forEach((track) => track.stop());
          const finalTranscript = transcriptRef.current.trim();
          if (onVoiceResult) {
            onVoiceResult(audioBlob, finalTranscript);
          }
        };

        mediaRecorder.start();
      } else {
        mediaRecorderRef.current = null;
      }
    } catch (err) {
      console.warn('Microphone stream access not available or denied:', err);
      mediaRecorderRef.current = null;
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {}
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      try {
        mediaRecorderRef.current.stop();
      } catch {}
    } else {
      const finalTranscript = transcriptRef.current.trim();
      if (onVoiceResult) {
        onVoiceResult(null, finalTranscript);
      }
    }
  };

  const handleMicClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
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


