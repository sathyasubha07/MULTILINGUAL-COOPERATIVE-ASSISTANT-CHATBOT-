import React from 'react';
import ChatBox from '../../components/ChatBox/ChatBox';

export default function Chat({ currentLang, initialQuery }) {
  return (
    <div style={{ maxWidth: '1080px', margin: '0 auto' }}>
      <div style={{ marginBottom: '16px' }}>
        <h2 style={{ fontSize: '22px', fontWeight: '800', color: '#064e3b' }}>
          Multilingual Cooperative Legal & Advisory Chatbot
        </h2>
        <p style={{ fontSize: '14px', color: '#64748b' }}>
          Ask queries in 11 Indian languages via Voice or Text. Grounded in official Gazette notifications and acts.
        </p>
      </div>

      <ChatBox currentLang={currentLang} initialQuery={initialQuery} />
    </div>
  );
}
