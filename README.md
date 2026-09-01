# Multilingual Cooperative Governance & Legal Assistance Portal (SIH 2026)
### Team BRAVITS | Problem Statement ID: SIH26088
**Theme:** Multilingual Cooperative Governance & Legal Assistance Chatbot

---

## 🌟 Overview
An intelligent, multilingual, voice-enabled AI system designed for farmers, rural citizens, and cooperative managers. The system runs both as a modern web portal and an **offline-capable Smart Kiosk on Raspberry Pi / Mini PC**.

---

## 🚀 Key Features

1. **Multilingual Voice & Text Assistant (11 Indian Languages)**
   - Voice STT (Speech-to-Text) and TTS (Text-to-Speech)
   - English, Hindi (हिन्दी), Marathi (मराठी), Tamil (தமிழ்), Telugu (తెలుగు), Gujarati (ગુજરાતી), Bengali (বাংলা), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Punjabi (ਪੰਜਾਬੀ), Odia (ଓଡ଼ିଆ).

2. **Resolution Navigator for Citizen Grievances**
   - Step-by-step grievance routing with statutory timelines (SLAs).
   - Designated Primary Officers (PACS Secretary, DAO, ARCS, DCCB).
   - Multi-tier escalation pathways and document checklists.

3. **Multi-Domain Verified Knowledge Base**
   - **Cooperative Law:** MSCS Act 2002, 2023 Amendments, Model State Bylaws.
   - **PMFBY Crop Insurance:** 72-hour localized calamity deadlines, claim procedures.
   - **PACS Multi-Service Centers:** Computerization, ERP, CSC onboarding.
   - **Schemes & Financial Literacy:** PM-KISAN, AIF, KCC Scale of Finance (4% effective interest).

4. **Hallucination Prevention with Citation Box**
   - Every guidance references authentic Gazette notifications and circulars.

---

## 🏗️ Project Architecture

```
cooperative-ai-portal/
├── frontend/                     # React + Vite (Multilingual UI, Voice, Kiosk Mode)
│   ├── src/
│   │   ├── components/           # Navbar, LanguageSelector, ChatBox, VoiceInput, etc.
│   │   ├── pages/                # Dashboard, Chat, Law, Schemes, PMFBY, PACS, Grievance
│   │   └── services/api.js       # Unified client bridge
├── backend/                      # FastAPI Python Application
│   ├── app/                      # API routes, Services, Schemas, Main app
│   └── requirements.txt
├── ai_engine/                    # Multi-Domain RAG & Reasoning
│   ├── orchestration/            # Intent Classifier & Domain Router
│   ├── retrieval/                # Hybrid Retrieval (Vector + Metadata)
│   ├── rag/                      # RAG Pipeline & Prompt Builder
│   ├── llm/                      # Reasoner (Groq / Gemini / Local Edge)
│   ├── verification/             # Source Validator & Citation Generator
│   ├── resolution_navigator/     # Grievance Classifier & Officer Recommender
│   └── language/                 # Multilingual STT, TTS & Translation
├── database/                     # Verified Datasets & Authorities Directory
├── notifications/                # Smart Scheme Alerts & Monitor
├── scripts/                      # Data loaders & Index builders
└── docker-compose.yml
```

---

## ⚡ Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m backend.app.main
```
The backend will run on `http://localhost:8000` (Swagger docs at `/docs`).

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The portal will run on `http://localhost:5173`.

### 3. Docker Deployment
```bash
docker-compose up --build
```
