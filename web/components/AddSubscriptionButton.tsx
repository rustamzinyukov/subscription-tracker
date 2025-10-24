'use client';

import { useState } from 'react';
import { Subscription } from '@/types';
import { apiClient } from '@/lib/api';

interface AddSubscriptionButtonProps {
  onSubscriptionAdd: (subscription: Subscription) => void;
}

export default function AddSubscriptionButton({ onSubscriptionAdd }: AddSubscriptionButtonProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    amount: '',
    currency: 'RUB',
    frequency: 'monthly' as 'monthly' | 'yearly',
    next_billing_date: new Date().toLocaleDateString('en-CA'),
    provider: '',
    logo_url: '',
    website_url: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.amount) {
      alert('Пожалуйста, заполните обязательные поля');
      return;
    }

    try {
      setIsLoading(true);
      
      // Debug logging
      console.log('🔍 Form data being sent:', {
        name: formData.name,
        amount: formData.amount,
        next_billing_date: formData.next_billing_date,
        frequency: formData.frequency
      });
      
          // Безопасная обработка даты
          let billingDate;
          try {
            billingDate = new Date(formData.next_billing_date);
            if (isNaN(billingDate.getTime())) {
              throw new Error('Invalid date');
            }
          } catch (error) {
            console.error('Invalid date format:', formData.next_billing_date);
            alert('Неверный формат даты. Пожалуйста, выберите корректную дату.');
            return;
          }

          const subscriptionData = {
            name: formData.name,
            description: formData.description || undefined,
            amount: parseFloat(formData.amount),
            currency: formData.currency,
            frequency: formData.frequency,
            next_billing_date: billingDate.toISOString(),
            provider: formData.provider || undefined,
            logo_url: formData.logo_url || undefined,
            website_url: formData.website_url || undefined,
          };
      
      console.log('🔍 Subscription data:', subscriptionData);
      
      const newSubscription = await apiClient.createSubscription(subscriptionData);
      
      onSubscriptionAdd(newSubscription);
      setIsModalOpen(false);
      setFormData({
        name: '',
        description: '',
        amount: '',
        currency: 'RUB',
        frequency: 'monthly',
        next_billing_date: new Date().toLocaleDateString('en-CA'),
        provider: '',
        logo_url: '',
        website_url: '',
      });
    } catch (error: any) {
      console.error('Error creating subscription:', error);
      let errorMessage = 'Ошибка при создании подписки';
      
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
      setIsLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setIsModalOpen(true)}
        className="btn-primary flex items-center space-x-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        <span>Добавить подписку</span>
      </button>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900">Добавить подписку</h2>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Название * <span className="text-red-500">(обязательно)</span>
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="input-field"
                    placeholder="Netflix, Spotify, YouTube Premium..."
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Описание
                  </label>
                  <input
                    type="text"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="input-field"
                    placeholder="Стриминг сервис"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Сумма * <span className="text-red-500">(обязательно)</span>
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.amount}
                      onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                      className="input-field"
                      placeholder="599"
                      required
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

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Провайдер
                  </label>
                  <input
                    type="text"
                    value={formData.provider}
                    onChange={(e) => setFormData({ ...formData, provider: e.target.value })}
                    className="input-field"
                    placeholder="Netflix, Inc."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    URL логотипа
                  </label>
                  <input
                    type="url"
                    value={formData.logo_url}
                    onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
                    className="input-field"
                    placeholder="https://example.com/logo.png"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Веб-сайт
                  </label>
                  <input
                    type="url"
                    value={formData.website_url}
                    onChange={(e) => setFormData({ ...formData, website_url: e.target.value })}
                    className="input-field"
                    placeholder="https://netflix.com"
                  />
                </div>

                <div className="text-sm text-gray-500 mb-4">
                  <p><span className="text-red-500">*</span> - обязательные поля</p>
                  <p>Остальные поля можно оставить пустыми</p>
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="btn-primary flex-1"
                  >
                    {isLoading ? 'Создание...' : 'Создать подписку'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="btn-secondary flex-1"
                  >
                    Отмена
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
