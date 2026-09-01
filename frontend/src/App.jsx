import React, { useState } from 'react';
import Navbar from './components/Navbar/Navbar';
import Dashboard from './pages/Dashboard/Dashboard';
import Chat from './pages/Chat/Chat';
import Law from './pages/Law/Law';
import Schemes from './pages/Schemes/Schemes';
import PMFBY from './pages/PMFBY/PMFBY';
import PACS from './pages/PACS/PACS';
import FinancialLiteracy from './pages/FinancialLiteracy/FinancialLiteracy';
import Grievance from './pages/Grievance/Grievance';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentLang, setCurrentLang] = useState('en');
  const [chatInitialQuery, setChatInitialQuery] = useState(null);

  const handleAskQuery = (query) => {
    setChatInitialQuery(query);
    setActiveTab('chat');
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <Dashboard 
            currentLang={currentLang} 
            setActiveTab={setActiveTab} 
            setChatQuery={handleAskQuery} 
          />
        );
      case 'chat':
        return (
          <Chat 
            currentLang={currentLang} 
            initialQuery={chatInitialQuery} 
          />
        );
      case 'law':
        return <Law onAskQuery={handleAskQuery} />;
      case 'schemes':
        return <Schemes onAskQuery={handleAskQuery} />;
      case 'pmfby':
        return <PMFBY onAskQuery={handleAskQuery} />;
      case 'pacs':
        return <PACS onAskQuery={handleAskQuery} />;
      case 'financial':
        return <FinancialLiteracy onAskQuery={handleAskQuery} />;
      case 'grievance':
        return <Grievance currentLang={currentLang} />;
      default:
        return (
          <Dashboard 
            currentLang={currentLang} 
            setActiveTab={setActiveTab} 
            setChatQuery={handleAskQuery} 
          />
        );
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#f8fafc' }}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentLang={currentLang}
        setCurrentLang={setCurrentLang}
      />

      <main style={{ flex: 1, maxWidth: '1440px', margin: '0 auto', width: '100%', padding: '24px' }}>
        {renderContent()}
      </main>

      {/* Footer */}
      <footer style={{
        background: '#ffffff',
        borderTop: '1px solid #e2e8f0',
        padding: '24px',
        textAlign: 'center',
        fontSize: '13px',
        color: '#64748b'
      }}>
        <div style={{ maxWidth: '1440px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <strong>Smart India Hackathon 2026</strong> • Team BRAVITS (PS ID: SIH26088)
          </div>
          <div>
            Multilingual Cooperative Governance & Legal Assistance System • Open Source Prototype
          </div>
        </div>
      </footer>
    </div>
  );
}
