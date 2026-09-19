import React, { useState } from 'react';
import { TRANSLATIONS } from '../translations';
import { X, MapPin, Search, Phone, Clock, ExternalLink, Building, ShieldCheck } from 'lucide-react';

/**
 * Nearby Office Locator Modal
 * Allows users to find nearby Assistant Registrar & PACS Cooperative Offices.
 * NOTE: Mock office directory dataset below is structured to be replaced with real backend API responses.
 */

// Mock Cooperative Office Directory Dataset
const MOCK_OFFICES = [
  {
    id: 1,
    name: 'Sub-Divisional Cooperative Department Office',
    officer: 'Shri Rajesh Kumar (ARCS)',
    district: 'Chennai North',
    address: '14, Cooperative Bhavan Road, Egmore, Chennai - 600008',
    phone: '1800-180-COOP / 044-28551234',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Membership appeals, audit complaints & PACS registration',
  },
  {
    id: 2,
    name: 'District Cooperative Central Bank (DCCB) Head Office',
    officer: 'Smt. Lakshmi Sundaram (Branch Manager)',
    district: 'Coimbatore',
    address: '88, DB Road, RS Puram, Coimbatore - 641002',
    phone: '0422-2479001',
    hours: 'Mon - Sat: 10:00 AM - 4:00 PM',
    jurisdiction: 'KCC Loans, interest subvention & crop insurance claims',
  },
  {
    id: 3,
    name: 'Primary Agricultural Credit Society (PACS) Outlet #12',
    officer: 'Thiru M. Arumugam (PACS Secretary)',
    district: 'Madurai',
    address: 'Main Bazaar Road, Vadipatti, Madurai - 625218',
    phone: '0452-2882104',
    hours: 'Mon - Sat: 9:00 AM - 6:00 PM',
    jurisdiction: 'Direct seed/fertilizer distribution & member loan sanctioning',
  },
  {
    id: 4,
    name: 'Regional Registrar of Cooperative Societies',
    officer: 'Shri V. K. Sharma (Joint Registrar)',
    district: 'Salem',
    address: 'Collectorate Complex, Hasthampatti, Salem - 636007',
    phone: '0427-2415520',
    hours: 'Mon - Fri: 9:30 AM - 5:30 PM',
    jurisdiction: 'Second-level grievance escalation & society disputes',
  },
  {
    id: 5,
    name: 'Tiruchirappalli District PACS Extension Center',
    officer: 'K. R. Vengat (Field Officer)',
    district: 'Tiruchirappalli',
    address: 'Cantonment Area, Trichy - 620001',
    phone: '0431-2418900',
    hours: 'Mon - Sat: 9:30 AM - 5:00 PM',
    jurisdiction: 'PMFBY loss verification & computerization support',
  },
];

export default function OfficeLocatorModal({ langCode, onClose }) {
  const t = TRANSLATIONS[langCode] || TRANSLATIONS.en;
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('all');

  const districts = ['all', 'Chennai North', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli'];

  const filteredOffices = MOCK_OFFICES.filter((office) => {
    const matchesDistrict = selectedDistrict === 'all' || office.district === selectedDistrict;
    const matchesQuery =
      office.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      office.officer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      office.address.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDistrict && matchesQuery;
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--bg-card-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <MapPin size={22} color="#10b981" />
            <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--text-primary)' }}>
              {t.locator}
            </h2>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              color: 'var(--text-muted)',
              padding: '0.4rem',
              borderRadius: '0.5rem',
              display: 'flex',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Filter Controls Bar */}
        <div style={{
          padding: '1.25rem 1.5rem 0.5rem 1.5rem',
          display: 'flex',
          gap: '0.75rem',
          flexWrap: 'wrap',
        }}>
          {/* Search Input */}
          <div style={{
            flex: 1,
            minWidth: '220px',
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            background: 'var(--bg-main)',
            border: '1px solid var(--bg-card-border)',
            borderRadius: '0.75rem',
            padding: '0.6rem 1rem',
          }}>
            <Search size={17} color="var(--text-muted)" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={t.locatorSearchPlaceholder}
              style={{
                border: 'none',
                outline: 'none',
                background: 'transparent',
                width: '100%',
                color: 'var(--text-primary)',
                fontFamily: 'inherit',
                fontSize: '0.9rem',
              }}
            />
          </div>

          {/* District Select Dropdown */}
          <select
            value={selectedDistrict}
            onChange={(e) => setSelectedDistrict(e.target.value)}
            style={{
              background: 'var(--bg-main)',
              color: 'var(--text-primary)',
              border: '1px solid var(--bg-card-border)',
              borderRadius: '0.75rem',
              padding: '0.6rem 1rem',
              fontFamily: 'inherit',
              fontSize: '0.9rem',
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            <option value="all">{t.allDistricts}</option>
            {districts.filter(d => d !== 'all').map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        {/* Office Cards List */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '1rem 1.5rem 1.5rem 1.5rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
        }}>
          {filteredOffices.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
              No cooperative offices found for the selected criteria.
            </div>
          ) : (
            filteredOffices.map((office) => (
              <div
                key={office.id}
                style={{
                  border: '1px solid var(--bg-card-border)',
                  borderRadius: '1rem',
                  padding: '1.25rem',
                  background: 'var(--bg-main)',
                  boxShadow: 'var(--shadow-sm)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                    {office.name}
                  </h3>
                  <span style={{
                    fontSize: '0.75rem',
                    background: 'rgba(16, 185, 129, 0.12)',
                    color: '#10b981',
                    padding: '0.2rem 0.6rem',
                    borderRadius: '1rem',
                    fontWeight: '600',
                  }}>
                    {office.district}
                  </span>
                </div>

                <div style={{ fontSize: '0.88rem', color: '#3b82f6', fontWeight: '600', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <ShieldCheck size={16} />
                  <span>{office.officer}</span>
                </div>

                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.4rem' }}>
                    <MapPin size={15} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <span>{office.address}</span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <Phone size={15} color="#10b981" style={{ flexShrink: 0 }} />
                    <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{office.phone}</span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <Clock size={15} color="var(--text-muted)" style={{ flexShrink: 0 }} />
                    <span>{office.hours}</span>
                  </div>
                </div>

                <div style={{ marginTop: '0.85rem', paddingTop: '0.75rem', borderTop: '1px dashed var(--bg-card-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    Jurisdiction: {office.jurisdiction}
                  </span>
                  <a
                    href={`https://maps.google.com/?q=${encodeURIComponent(office.name + ' ' + office.address)}`}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                      fontSize: '0.82rem',
                      color: '#3b82f6',
                      textDecoration: 'none',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.3rem',
                      fontWeight: '600',
                    }}
                  >
                    <span>Directions</span>
                    <ExternalLink size={14} />
                  </a>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
