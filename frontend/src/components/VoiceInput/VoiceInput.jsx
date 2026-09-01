import React, { useState } from 'react';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import { TRANSLATIONS } from '../../utils/translations';

export default function VoiceInput({ onTranscript, currentLang }) {
  const [isRecording, setIsRecording] = useState(false);
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const handleToggleRecord = () => {
    if (isRecording) {
      setIsRecording(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech Recognition is not supported by this browser. Using simulation.');
      const sampleQueries = {
        hi: "प्रधानमंत्री फसल बीमा में क्लेम की प्रक्रिया क्या है?",
        mr: "PACS सभासदत्व नाकारल्यास काय करावे?",
        ta: "பயிர் காப்பீட்டு இழப்பீடு கோருவது எப்படி?",
        te: "పంట నష్టపరిహారం ఎలా పొందాలి?",
        en: "What is the procedure for PMFBY crop insurance claim?"
      };
      onTranscript(sampleQueries[currentLang] || sampleQueries.en);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = currentLang === 'hi' ? 'hi-IN' : currentLang === 'ta' ? 'ta-IN' : currentLang === 'te' ? 'te-IN' : 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => setIsRecording(true);
    recognition.onend = () => setIsRecording(false);
    recognition.onerror = (e) => {
      console.error(e);
      setIsRecording(false);
    };
    recognition.onresult = (e) => {
      const text = e.results[0][0].transcript;
      onTranscript(text);
      setIsRecording(false);
    };

    try {
      recognition.start();
    } catch (err) {
      console.error(err);
      setIsRecording(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleToggleRecord}
      className={`kiosk-btn ${isRecording ? 'mic-recording' : 'kiosk-btn-primary'}`}
      title={isRecording ? t.listening : t.voiceSearch}
      style={{
        padding: '12px 18px',
        borderRadius: '12px',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}
    >
      {isRecording ? <Loader2 size={20} className="animate-spin" /> : <Mic size={20} />}
      <span style={{ fontSize: '13px' }}>
        {isRecording ? t.listening : t.voiceSearch}
      </span>
    </button>
  );
}
