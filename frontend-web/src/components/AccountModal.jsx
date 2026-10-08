import React, { useState } from 'react';
import { TRANSLATIONS } from '../translations';
import { 
  X, User, Phone, MapPin, Building, ShieldCheck, CheckCircle2, 
  LogOut, Sparkles, Sprout, CreditCard, FileCheck, Layers 
} from 'lucide-react';

const TN_DISTRICTS = [
  'Theni', 'Madurai', 'Pudukkottai', 'Coimbatore', 'Thanjavur', 'Dindigul',
  'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Erode', 'Vellore', 'Kanchipuram',
  'Cuddalore', 'Villupuram', 'Tiruppur', 'Ramanathapuram', 'Sivaganga',
  'Virudhunagar', 'Karur', 'Nagapattinam', 'Tiruvarur', 'Krishnagiri',
  'Dharmapuri', 'Namakkal', 'Nilgiris', 'Thoothukudi', 'Kanyakumari',
  'Tiruvallur', 'Tiruvannamalai', 'Ranipet', 'Tenkasi', 'Chengalpattu',
  'Kallakurichi', 'Mayiladuthurai', 'Ariyalur', 'Perambalur', 'Tirupathur', 'Chennai'
];

const CROP_OPTIONS = [
  'Paddy (நெல்)', 'Tomato / Vegetables (தக்காளி / காய்கறிகள்)', 'Cotton (பருத்தி)',
  'Sugarcane (கரும்பு)', 'Banana / Fruits (வாழை / பழங்கள்)', 'Spices / Cardamom (மசாலா / ஏலக்காய்)',
  'Pulses / Millets (பயறு / சிறுதானியங்கள்)', 'Dairy / Cattle (கால்நடை / பால் பண்ணை)', 'Fisheries (மீன்வளம்)'
];

export default function AccountModal({ langCode, user, onSaveUser, onLogout, onClose, onShowEligibilityAlert }) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;

  const [formData, setFormData] = useState({
    name: user?.name || '',
    mobile: user?.mobile || '',
    district: user?.district || 'Theni',
    societyName: user?.societyName || '',
    memberType: user?.memberType || 'Farmer Member',
    land_size_acres: user?.land_size_acres !== undefined ? user.land_size_acres : 2.5,
    crop_types: user?.crop_types || ['Paddy (நெல்)', 'Tomato / Vegetables (தக்காளி / காய்கறிகள்)'],
    has_kcc: user?.has_kcc || false,
    has_soil_card: user?.has_soil_card || false,
    has_aadhaar_dbt: user?.has_aadhaar_dbt !== undefined ? user.has_aadhaar_dbt : true,
    preferredLang: user?.preferredLang || langCode || 'en',
  });

  const [isSubmitted, setIsSubmitted] = useState(false);
  const [eligibilityResult, setEligibilityResult] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({ 
      ...prev, 
      [name]: type === 'checkbox' ? checked : value 
    }));
  };

  const handleCropToggle = (crop) => {
    setFormData((prev) => {
      const exists = prev.crop_types.includes(crop);
      const updated = exists 
        ? prev.crop_types.filter((c) => c !== crop)
        : [...prev.crop_types, crop];
      return { ...prev, crop_types: updated };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) return;

    const updatedUser = {
      ...formData,
      id: user?.id || `MEMBER-${Date.now().toString().slice(-6)}`,
      createdAt: user?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    localStorage.setItem('coop_portal_user', JSON.stringify(updatedUser));
    onSaveUser(updatedUser);

    // Call backend profile and dynamic eligibility evaluation
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/v1/notifications/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedUser)
      });
      if (resp.ok) {
        const data = await resp.json();
        setEligibilityResult(data.eligibility_summary);
        if (data.eligibility_summary?.personalized_alerts?.length > 0 && onShowEligibilityAlert) {
          onShowEligibilityAlert(data.eligibility_summary.personalized_alerts[0]);
        }
      }
    } catch (err) {
      console.log('Profile sync background notice:', err);
    }

    setIsSubmitted(true);
    setTimeout(() => {
      setIsSubmitted(false);
      onClose();
    }, 1200);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="modal-content" 
        onClick={(e) => e.stopPropagation()} 
        style={{ maxWidth: '580px', maxHeight: '90vh', overflowY: 'auto' }}
      >
        {/* Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'var(--header-bg)',
          position: 'sticky',
          top: 0,
          zIndex: 10
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #2563eb 0%, #10b981 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
            }}>
              <User size={20} />
            </div>
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                {user ? 'Farmer Profile & Scheme Preferences' : 'Create Cooperative Member Account'}
              </h2>
              <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                Enables automatic eligibility tracking & tailored AI statutory advice
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '0.4rem',
              borderRadius: '0.5rem',
              display: 'flex',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
          {isSubmitted && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              padding: '0.85rem 1rem',
              background: 'rgba(16, 185, 129, 0.12)',
              border: '1px solid #10b981',
              borderRadius: '0.75rem',
              color: '#059669',
              fontWeight: '600',
              fontSize: '0.9rem',
            }}>
              <CheckCircle2 size={18} />
              <span>
                {eligibilityResult 
                  ? `Profile updated! ${eligibilityResult.total_eligible_schemes} schemes currently eligible.` 
                  : 'Profile saved successfully!'}
              </span>
            </div>
          )}

          {/* Full Name */}
          <div>
            <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
              Farmer / Member Name *
            </label>
            <input
              type="text"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. M. Ramasamy / எஸ். முருகன்"
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '0.75rem',
                border: '1px solid var(--bg-card-border)',
                background: 'var(--bg-main)',
                color: 'var(--text-primary)',
                fontSize: '0.92rem',
                outline: 'none',
              }}
            />
          </div>

          {/* Mobile & Category */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
                Mobile Number
              </label>
              <input
                type="tel"
                name="mobile"
                value={formData.mobile}
                onChange={handleChange}
                placeholder="e.g. 9876543210"
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.92rem',
                  outline: 'none',
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
                Member Category
              </label>
              <select
                name="memberType"
                value={formData.memberType}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.92rem',
                  outline: 'none',
                }}
              >
                <option value="Farmer Member">🌾 Farmer Member</option>
                <option value="PACS Secretary / Officer">🏛️ PACS Secretary / Staff</option>
                <option value="Cooperative Society Member">🤝 Society Member</option>
                <option value="General Citizen">👤 General Citizen</option>
              </select>
            </div>
          </div>

          {/* Landholding Size & District */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
                Landholding (in Acres) 🌾
              </label>
              <input
                type="number"
                step="0.1"
                min="0"
                name="land_size_acres"
                value={formData.land_size_acres}
                onChange={handleChange}
                placeholder="e.g. 2.5"
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.92rem',
                  outline: 'none',
                  fontWeight: '600'
                }}
              />
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                {formData.land_size_acres <= 2.5 ? '🌱 Marginal (<2.5 Acres)' : formData.land_size_acres <= 5.0 ? '🌿 Small (2.5-5.0 Acres)' : '🌳 Large (>5 Acres)'}
              </span>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
                Jurisdictional District 📍
              </label>
              <select
                name="district"
                value={formData.district}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '0.75rem',
                  border: '1px solid var(--bg-card-border)',
                  background: 'var(--bg-main)',
                  color: 'var(--text-primary)',
                  fontSize: '0.92rem',
                  outline: 'none',
                  fontWeight: '600',
                }}
              >
                <optgroup label="🌟 Priority Core Districts">
                  <option value="Theni">📍 Theni (தேனி)</option>
                  <option value="Madurai">📍 Madurai (மதுரை)</option>
                  <option value="Pudukkottai">📍 Pudukkottai (புதுக்கோட்டை)</option>
                </optgroup>
                <optgroup label="All Tamil Nadu Districts">
                  {TN_DISTRICTS.filter((d) => !['Theni', 'Madurai', 'Pudukkottai'].includes(d)).map((dist) => (
                    <option key={dist} value={dist}>
                      {dist}
                    </option>
                  ))}
                </optgroup>
              </select>
            </div>
          </div>

          {/* Primary Crops Selection */}
          <div>
            <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
              Cultivated Crops / Enterprises (Unlocks Specific Subsidies) 🌱
            </label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.45rem' }}>
              {CROP_OPTIONS.map((crop) => {
                const isSelected = formData.crop_types.includes(crop);
                return (
                  <button
                    type="button"
                    key={crop}
                    onClick={() => handleCropToggle(crop)}
                    style={{
                      padding: '0.35rem 0.65rem',
                      borderRadius: '1rem',
                      border: isSelected ? '1px solid #10b981' : '1px solid var(--bg-card-border)',
                      background: isSelected ? 'rgba(16, 185, 129, 0.12)' : 'var(--bg-main)',
                      color: isSelected ? '#059669' : 'var(--text-primary)',
                      fontSize: '0.78rem',
                      fontWeight: isSelected ? '600' : '500',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    {crop}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Scheme Checkboxes */}
          <div style={{
            padding: '0.85rem 1rem',
            borderRadius: '0.75rem',
            background: 'var(--bg-main)',
            border: '1px solid var(--bg-card-border)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.65rem'
          }}>
            <span style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-primary)' }}>
              📋 Documentation & Existing Scheme Status
            </span>

            <label style={{ display: 'flex', alignItems: 'center', gap: '0.55rem', fontSize: '0.84rem', cursor: 'pointer', color: 'var(--text-secondary)' }}>
              <input
                type="checkbox"
                name="has_aadhaar_dbt"
                checked={formData.has_aadhaar_dbt}
                onChange={handleChange}
                style={{ width: '16px', height: '16px', accentColor: '#10b981' }}
              />
              <span>Aadhaar Seeding with Bank Account on NPCI Mapper (For DBT Subsidies)</span>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '0.55rem', fontSize: '0.84rem', cursor: 'pointer', color: 'var(--text-secondary)' }}>
              <input
                type="checkbox"
                name="has_kcc"
                checked={formData.has_kcc}
                onChange={handleChange}
                style={{ width: '16px', height: '16px', accentColor: '#2563eb' }}
              />
              <span>Currently holds a Kisan Credit Card (KCC) Crop Loan Account</span>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '0.55rem', fontSize: '0.84rem', cursor: 'pointer', color: 'var(--text-secondary)' }}>
              <input
                type="checkbox"
                name="has_soil_card"
                checked={formData.has_soil_card}
                onChange={handleChange}
                style={{ width: '16px', height: '16px', accentColor: '#7c3aed' }}
              />
              <span>Has Soil Health Card / Free Soil Nutrient Test Completed</span>
            </label>
          </div>

          {/* Local PACS Society Name */}
          <div>
            <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
              Local PACS Society / Village
            </label>
            <input
              type="text"
              name="societyName"
              value={formData.societyName}
              onChange={handleChange}
              placeholder="e.g. Vadipatti Primary Agricultural Credit Society"
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '0.75rem',
                border: '1px solid var(--bg-card-border)',
                background: 'var(--bg-main)',
                color: 'var(--text-primary)',
                fontSize: '0.92rem',
                outline: 'none',
              }}
            />
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
            <button
              type="submit"
              className="btn-primary"
              style={{
                flex: 1,
                padding: '0.75rem',
                borderRadius: '0.75rem',
                fontWeight: '700',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
              }}
            >
              <Sparkles size={16} />
              <span>{user ? 'Update Profile & Check Subsidies' : 'Save & Check Eligible Schemes'}</span>
            </button>

            {user && (
              <button
                type="button"
                onClick={() => {
                  localStorage.removeItem('coop_portal_user');
                  onLogout();
                  onClose();
                }}
                className="btn-secondary"
                style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '0.75rem',
                  borderColor: '#ef4444',
                  color: '#ef4444',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                }}
              >
                <LogOut size={16} />
                <span>Sign Out</span>
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
