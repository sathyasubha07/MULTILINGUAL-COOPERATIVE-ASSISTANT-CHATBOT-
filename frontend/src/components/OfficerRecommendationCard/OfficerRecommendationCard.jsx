import React from 'react';
import { UserCheck, Building, Phone, ArrowUpCircle } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function OfficerRecommendationCard({ officer }) {
  const { t } = useLanguage();

  if (!officer) return null;

  return (
    <div className="officer-card">
      <div className="officer-card-header">
        <UserCheck size={18} />
        <span>{t('officerRecommendation')}</span>
      </div>

      <div className="officer-card-body">
        {officer.name && (
          <h4 className="officer-name">{officer.name}</h4>
        )}
        <p className="officer-detail">
          <strong>{t('designation')}:</strong>{' '}
          {officer.designation}
        </p>
        {officer.office && (
          <p className="officer-detail">
            <Building size={14} />
            <strong>{t('office')}:</strong> {officer.office}
          </p>
        )}
        {officer.phone && (
          <p className="officer-detail">
            <Phone size={14} />
            <strong>{t('contact')}:</strong> {officer.phone}
          </p>
        )}
        {officer.escalationStep != null && (
          <p className="officer-escalation">
            <ArrowUpCircle size={14} />
            <strong>{t('escalationStep')}:</strong> {officer.escalationStep}
          </p>
        )}
      </div>
    </div>
  );
}
