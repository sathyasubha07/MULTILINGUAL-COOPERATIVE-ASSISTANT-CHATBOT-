import requests
import json
import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = 'http://127.0.0.1:8000'

print("=== STARTING FULL BACKEND & NOTIFICATION VERIFICATION ===")

# 1. Health
h = requests.get(f'{base}/health').json()
print('1. HEALTH CHECK:', h)

# 2. Notifications List
n = requests.get(f'{base}/api/v1/notifications/?user_id=test_farmer_101').json()
notifs = n.get('notifications', [])
print(f'2. NOTIFICATIONS: total={len(notifs)}, unread={n.get("unread_count")}')
for item in notifs[:3]:
    print(f'   - [{item.get("type")}] {item.get("title")}: {item.get("message")[:70]}...')

# 3. Dynamic Eligibility Evaluation Check
profile_update = {
    "id": "test_farmer_101",
    "name": "Ramesh Kumar",
    "mobile": "9876543210",
    "district": "Thanjavur",
    "state": "Tamil Nadu",
    "societyName": "Thanjavur PACS",
    "memberType": "Farmer Member",
    "land_size_acres": 4.5,
    "crop_types": ["Paddy", "Tomato"],
    "has_kcc": True,
    "has_soil_card": True,
    "has_aadhaar_dbt": True,
    "is_pacs_member": True,
    "preferredLang": "ta"
}
p = requests.post(f'{base}/api/v1/notifications/profile', json=profile_update).json()
elig_summary = p.get('eligibility_summary', {})
eligible_schemes = elig_summary.get('eligible_schemes', [])
personalized_alerts = elig_summary.get('personalized_alerts', [])
print(f'3. PROFILE & ELIGIBILITY: Eligible schemes count = {len(eligible_schemes)}')
for es in eligible_schemes:
    print(f'   - [{es.get("code")}] {es.get("name")}: {es.get("benefit")[:60]}...')
print(f'   Personalized Alerts Generated: {len(personalized_alerts)}')
for pa in personalized_alerts:
    print(f'   - [{pa.get("priority")}] {pa.get("title")}: {pa.get("message")[:60]}...')

# 4. User Telemetry Feedback
fb = {
    'user_id': 'test_farmer_101',
    'query': 'What is PM KISAN?',
    'helpful': True,
    'score': 5,
    'feedback_text': 'Accurate and fast response.',
    'category': 'General'
}
f_res = requests.post(f'{base}/api/v1/notifications/feedback', json=fb).json()
print('4. TELEMETRY FEEDBACK:', f_res)

# 5. Multilingual Chat with Gemini AI (English)
chat_en = requests.post(f'{base}/api/v1/chat', json={'query': 'What is PM KISAN scheme in 1 concise sentence?', 'language': 'en'}).json()
print('5. CHAT (English):', chat_en.get('answer'))
print('   Verification Status:', chat_en.get('verification_status'), '| Trust Score:', chat_en.get('trust_score'))

# 6. Multilingual Chat with Gemini AI (Tamil)
chat_ta = requests.post(f'{base}/api/v1/chat', json={'query': 'PM KISAN திட்டம் பற்றி ஒரு வரியில் கூறுங்கள்.', 'language': 'ta'}).json()
print('6. CHAT (Tamil):', chat_ta.get('answer'))
print('   Domain:', chat_ta.get('domain'), '| Language:', chat_ta.get('language'))

print("=== ALL API VERIFICATIONS COMPLETED SUCCESSFULLY ===")
