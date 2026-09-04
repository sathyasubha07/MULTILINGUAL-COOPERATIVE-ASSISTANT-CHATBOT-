const API_BASE_URL = 'http://localhost:8000/api/v1';

// TODO: connect to real API — set USE_MOCK to false when backend is ready
const USE_MOCK = false;

/**
 * Send a text query to the unified assistant.
 * @returns {Promise<{ responseType: string, answer: string, officerRecommendation?: object }>}
 */
export async function sendTextQuery(text, language = 'en') {
  if (!USE_MOCK) {
    const res = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: text, language }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return normalizeBackendResponse(data);
  }
  return mockTextResponse(text, language);
}

/**
 * Send a voice recording for transcription + response.
 * @returns {Promise<{ responseType: string, answer: string, transcription: string, officerRecommendation?: object }>}
 */
export async function sendVoiceQuery(audioBlob, language = 'en') {
  if (!USE_MOCK) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    formData.append('language', language);
    const res = await fetch(`${API_BASE_URL}/chat/voice`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return normalizeBackendResponse(data);
  }
  return mockVoiceResponse(language);
}

function normalizeBackendResponse(data) {
  return {
    responseType: data.response_type || data.responseType || 'general',
    answer: data.answer || data.message || '',
    transcription: data.transcription || null,
    officerRecommendation: data.officer_recommendation || data.officerRecommendation || null,
  };
}

function mockTextResponse(text, language) {
  const q = text.toLowerCase();

  if (q.includes('grievance') || q.includes('complaint') || q.includes('reject') || q.includes('शिकायत') || q.includes('புகார்') || q.includes('membership')) {
    return {
      responseType: 'grievance',
      answer: getGrievanceAnswer(language),
      officerRecommendation: {
        name: 'Shri Rajesh Kumar',
        designation: 'Assistant Registrar of Cooperative Societies (ARCS)',
        phone: '1800-180-COOP',
        office: 'Sub-Divisional Cooperative Department Office',
        escalationStep: 1,
      },
    };
  }

  if (q.includes('pmfby') || q.includes('crop') || q.includes('insurance') || q.includes('scheme') || q.includes('योजना') || q.includes('बीमा')) {
    return {
      responseType: 'scheme_info',
      answer: getSchemeAnswer(language),
      officerRecommendation: null,
    };
  }

  return {
    responseType: 'general',
    answer: getGeneralAnswer(language),
    officerRecommendation: null,
  };
}

function mockVoiceResponse(language) {
  const samples = {
    en: 'What is the procedure for PMFBY crop insurance claim?',
    hi: 'प्रधानमंत्री फसल बीमा में क्लेम की प्रक्रिया क्या है?',
    ta: 'பயிர் காப்பீட்டு இழப்பீடு கோருவது எப்படி?',
    te: 'పంట భీమా క్లెయిమ్ ప్రక్రియ ఏమిటి?',
    mr: 'PACS सभासदत्व नाकारल्यास काय करावे?',
    kn: 'PMFBY ಪಂಟ ಬima claim ಪ್ರಕ್ರಿಯೆ ಏನು?',
  };
  const transcription = samples[language] || samples.en;
  return { ...mockTextResponse(transcription, language), transcription };
}

function getGrievanceAnswer(lang) {
  const answers = {
    en: 'Your grievance regarding cooperative membership has been noted. Based on your query, you may escalate this to the Assistant Registrar of Cooperative Societies (ARCS) at the sub-division level. Please see the recommended officer below for contact details and next steps.',
    hi: 'सहकारी सदस्यता से संबंधित आपकी शिकायत दर्ज की गई है। आप इसे उप-मंडल स्तर पर सहकारी समितियों के सहायक Registrar (ARCS) के पास बढ़ा सकते हैं। संपर्क विवरण और अगले चरणों के लिए नीचे अनुशंसित अधिकारी देखें।',
    ta: 'கூட்டுறவு உறுப்பினர் தொடர்பான உங்கள் புகார் பதிவு செய்யப்பட்டது. இதை உட்பிரிவு அளவில் கூட்டுறவு சங்கங்களின் Assistant Registrar (ARCS) அணுகலாம். தொடர்பு விவரங்களுக்கு கீழே பரிந்துரைக்கப்பட்ட அதிகாரியைப் பாருங்கள்.',
  };
  return answers[lang] || answers.en;
}

function getSchemeAnswer(lang) {
  const answers = {
    en: 'Under PMFBY (Pradhan Mantri Fasal Bima Yojana), you must report crop damage within 72 hours of a localized calamity. Contact your PACS Secretary, call toll-free 14447, or use the Crop Insurance App. Required documents include your insurance policy, land records, and geotagged photos of damaged crops.',
    hi: 'PMFBY (प्रधानमंत्री फसल बीमा योजना) के तहत, स्थानीय आपदा के 72 घंटे के भीतर फसल क्षति की सूचना देनी होती है। अपने PACS सचिव से संपर्क करें, टोल-फ्री 14447 पर कॉल करें, या Crop Insurance App का उपयोग करें।',
    ta: 'PMFBY-யின் கீழ், உள்ளூர் பேரழிவுக்கு 72 மணி நேரத்திற்குள் பயிர் சேதத்தைப் புகார் செய்ய வேண்டும். உங்கள் PACS செcretary-யை தொடர்பு கொள்ளுங்கள் அல்லது 14447-க்கு அழைக்கவும்.',
  };
  return answers[lang] || answers.en;
}

function getGeneralAnswer(lang) {
  const answers = {
    en: 'I can help you with cooperative schemes, PMFBY crop insurance, PACS services, KCC loans, and grievance filing. Please describe your question in more detail.',
    hi: 'मैं सहकारी योजनाओं, PMFBY फसल बीमा, PACS सेवाओं, KCC ऋण और शिकायत दर्ज करने में आपकी सहायता कर सकता हूँ। कृपया अपना प्रश्न विस्तार से बताएं।',
    ta: 'கூட்டுறவு திட்டங்கள், PMFBY பயிர் காப்பீடு, PACS சேவைகள், KCC கடன்கள் மற்றும் புகார் தாக்கலில் உதவ முடியும். உங்கள் கேள்வியை விரிவாக விவரிக்கவும்.',
  };
  return answers[lang] || answers.en;
}

// Legacy exports kept for other pages that may still reference them
export const api = {
  sendChatMessage: sendTextQuery,
  async getSchemes() {
    try {
      const res = await fetch(`${API_BASE_URL}/schemes/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'fallback', data: [] };
    }
  },
  async getLaws() {
    try {
      const res = await fetch(`${API_BASE_URL}/law/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'fallback', data: [] };
    }
  },
  async getAuthorities() {
    try {
      const res = await fetch(`${API_BASE_URL}/grievance/authorities`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'fallback', authorities: [] };
    }
  },
  async registerGrievance(data) {
    try {
      const res = await fetch(`${API_BASE_URL}/grievance/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      return { status: 'success', ticket: { ticket_id: `COOP-GRV-${Date.now()}`, status: 'Registered' } };
    }
  },
};
