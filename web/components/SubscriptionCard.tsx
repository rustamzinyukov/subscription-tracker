'use client';

import { useState } from 'react';
import { Subscription } from '@/types';
import { formatCurrency, formatDate, getDaysUntilBilling, getBillingStatus } from '@/lib/utils';
import { apiClient } from '@/lib/api';

interface SubscriptionCardProps {
  subscription: Subscription;
  onUpdate: (subscription: Subscription) => void;
  onDelete: (id: number) => void;
}

export default function SubscriptionCard({ subscription, onUpdate, onDelete }: SubscriptionCardProps) {
  // Debug logging
  console.log('🔍 SubscriptionCard received subscription:', {
    id: subscription.id,
    name: subscription.name,
    amount: subscription.amount,
    currency: subscription.currency,
    frequency: subscription.frequency,
    next_billing_date: subscription.next_billing_date,
    is_active: subscription.is_active
  });
  
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [formData, setFormData] = useState({
    name: subscription.name,
    amount: subscription.amount,
    currency: subscription.currency,
    frequency: subscription.frequency,
    next_billing_date: subscription.next_billing_date?.split('T')[0] || subscription.next_billing_date, // Format for date input
  });

  const daysUntilBilling = getDaysUntilBilling(subscription.next_billing_date);
  const billingStatus = getBillingStatus(daysUntilBilling);

  const getStatusColor = () => {
    if (!subscription.is_active) return 'bg-gray-100 text-gray-600';
    switch (billingStatus) {
      case 'overdue': return 'bg-red-100 text-red-600';
      case 'due': return 'bg-yellow-100 text-yellow-600';
      case 'upcoming': return 'bg-green-100 text-green-600';
      default: return 'bg-green-100 text-green-600';
    }
  };

  const getStatusText = () => {
    if (!subscription.is_active) return 'Неактивна';
    switch (billingStatus) {
      case 'overdue': return 'Просрочена';
      case 'due': return 'Скоро';
      case 'upcoming': return `${daysUntilBilling} дн.`;
      default: return `${daysUntilBilling} дн.`;
    }
  };

  const handleSave = async () => {
    try {
      const updatedSubscription = await apiClient.updateSubscription(subscription.id, {
        ...formData,
        next_billing_date: new Date(formData.next_billing_date).toISOString(),
      });
      onUpdate(updatedSubscription);
      setIsEditing(false);
    } catch (error: any) {
      console.error('Error updating subscription:', error);
      let errorMessage = 'Ошибка при обновлении подписки';
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map((item: any) => item.msg || item).join(', ');
        } else {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      alert(errorMessage);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Вы уверены, что хотите удалить эту подписку?')) return;
    
    try {
      setIsDeleting(true);
      await apiClient.deleteSubscription(subscription.id);
      onDelete(subscription.id);
    } catch (error: any) {
      console.error('Error deleting subscription:', error);
      let errorMessage = 'Ошибка при удалении подписки';
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map((item: any) => item.msg || item).join(', ');
        } else {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      alert(errorMessage);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleToggleActive = async () => {
    try {
      const updatedSubscription = await apiClient.updateSubscription(subscription.id, {
        is_active: !subscription.is_active,
      });
      onUpdate(updatedSubscription);
    } catch (error: any) {
      console.error('Error toggling subscription:', error);
      let errorMessage = 'Ошибка при изменении статуса подписки';
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map((item: any) => item.msg || item).join(', ');
        } else {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      alert(errorMessage);
    }
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {subscription.logo_url ? (
            <img
              src={subscription.logo_url}
              alt={subscription.name}
              className="w-10 h-10 rounded-lg object-cover"
            />
          ) : (
            <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <span className="text-primary-600 font-bold text-lg">
                {subscription.name?.[0]?.toUpperCase() || 'S'}
              </span>
            </div>
          )}
          <div>
            <h3 className="font-semibold text-gray-900">{subscription.name}</h3>
            {subscription.provider && (
              <p className="text-sm text-gray-500">{subscription.provider}</p>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor()}`}>
            {getStatusText()}
          </span>
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="p-1 text-gray-400 hover:text-gray-600"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Content */}
      {isEditing ? (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Название
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="input-field"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Сумма
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Валюта
              </label>
              <select
                value={formData.currency}
                onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                className="input-field"
              >
                <option value="RUB">RUB</option>
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
              </select>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Период
              </label>
              <select
                value={formData.frequency}
                onChange={(e) => setFormData({ ...formData, frequency: e.target.value as 'monthly' | 'yearly' })}
                className="input-field"
              >
                <option value="monthly">Ежемесячно</option>
                <option value="yearly">Ежегодно</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Следующий платеж
              </label>
              <input
                type="date"
                value={formData.next_billing_date}
                onChange={(e) => setFormData({ ...formData, next_billing_date: e.target.value })}
                className="input-field"
              />
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button onClick={handleSave} className="btn-primary flex-1">
              Сохранить
            </button>
            <button 
              onClick={() => setIsEditing(false)} 
              className="btn-secondary flex-1"
            >
              Отмена
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-2xl font-bold text-gray-900">
              {formatCurrency(subscription.amount, subscription.currency)}
            </span>
            <span className="text-sm text-gray-500">
              {subscription.frequency === 'monthly' ? 'в месяц' : 'в год'}
            </span>
          </div>
          
          <div className="text-sm text-gray-600">
            <p>Следующий платеж: {formatDate(subscription.next_billing_date)}</p>
            {subscription.description && (
              <p className="mt-1">{subscription.description}</p>
            )}
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={handleToggleActive}
              className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                subscription.is_active
                  ? 'bg-red-100 text-red-700 hover:bg-red-200'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              }`}
            >
              {subscription.is_active ? 'Деактивировать' : 'Активировать'}
            </button>
            
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="px-3 py-2 bg-red-100 text-red-700 hover:bg-red-200 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
              {isDeleting ? '...' : 'Удалить'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
