'use client';

import { useState } from 'react';
import { Subscription } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';
import { apiClient } from '@/lib/api';

interface DateModalProps {
  isOpen: boolean;
  onClose: () => void;
  date: Date | null;
  subscriptions: Subscription[];
  onSubscriptionAdd: (subscription: Subscription) => void;
  onSubscriptionUpdate: (subscription: Subscription) => void;
  onSubscriptionDelete: (id: number) => void;
}

export default function DateModal({
  isOpen,
  onClose,
  date,
  subscriptions,
  onSubscriptionAdd,
  onSubscriptionUpdate,
  onSubscriptionDelete
}: DateModalProps) {
  const [isAddingSubscription, setIsAddingSubscription] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    amount: '',
    currency: 'RUB',
    frequency: 'monthly' as 'monthly' | 'yearly',
    next_billing_date: date ? date.toLocaleDateString('en-CA') : new Date().toLocaleDateString('en-CA'),
    provider: '',
    logo_url: '',
    website_url: '',
  });

  if (!isOpen || !date) return null;

  const subscriptionsOnDate = subscriptions.filter(sub => {
    if (!sub.next_billing_date) return false;
    const billingDate = new Date(sub.next_billing_date);
    return billingDate.toDateString() === date.toDateString();
  });

  const totalAmount = subscriptionsOnDate.reduce((sum, sub) => sum + sub.amount, 0);

  const handleAddSubscription = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.amount) {
      alert('Пожалуйста, заполните обязательные поля');
      return;
    }

    try {
      setIsLoading(true);
      
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
      
      const newSubscription = await apiClient.createSubscription(subscriptionData);
      onSubscriptionAdd(newSubscription);
      
      // Сброс формы
      setFormData({
        name: '',
        description: '',
        amount: '',
        currency: 'RUB',
        frequency: 'monthly',
        next_billing_date: date.toLocaleDateString('en-CA'),
        provider: '',
        logo_url: '',
        website_url: '',
      });
      
      setIsAddingSubscription(false);
    } catch (err: any) {
      console.error('Error creating subscription:', err);
      let errorMessage = 'Ошибка при создании подписки';
      
      if (err.response?.data?.detail) {
        if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        } else if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map((item: any) => item.msg || item).join(', ');
        } else {
          errorMessage = JSON.stringify(err.response.data.detail);
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteSubscription = async (subscriptionId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту подписку?')) return;
    
    try {
      console.log('🗑️ Удаляем подписку с ID:', subscriptionId);
      await apiClient.deleteSubscription(subscriptionId);
      console.log('✅ Подписка успешно удалена с сервера');
      onSubscriptionDelete(subscriptionId);
      console.log('✅ Подписка удалена из локального состояния');
    } catch (err: any) {
      console.error('❌ Ошибка при удалении подписки:', err);
      let errorMessage = 'Ошибка при удалении подписки';
      
      if (err.response?.data?.detail) {
        if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        } else if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map((item: any) => item.msg || item).join(', ');
        } else {
          errorMessage = JSON.stringify(err.response.data.detail);
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      alert(errorMessage);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Заголовок */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                {formatDate(date.toISOString())}
              </h2>
              <p className="text-gray-600">
                {subscriptionsOnDate.length} подписок • {formatCurrency(totalAmount)}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Кнопка добавления подписки */}
          {!isAddingSubscription && (
            <div className="mb-6">
              <button
                onClick={() => setIsAddingSubscription(true)}
                className="w-full py-3 px-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Добавить подписку на эту дату
              </button>
            </div>
          )}

          {/* Форма добавления подписки */}
          {isAddingSubscription && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Новая подписка</h3>
              <form onSubmit={handleAddSubscription} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Название *
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      placeholder="Netflix, Spotify..."
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Сумма *
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.amount}
                      onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      placeholder="599"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Валюта
                    </label>
                    <select
                      value={formData.currency}
                      onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="RUB">RUB</option>
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Период
                    </label>
                    <select
                      value={formData.frequency}
                      onChange={(e) => setFormData({ ...formData, frequency: e.target.value as 'monthly' | 'yearly' })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="monthly">Ежемесячно</option>
                      <option value="yearly">Ежегодно</option>
                    </select>
                  </div>
                </div>

                <div className="flex space-x-3">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {isLoading ? 'Создание...' : 'Создать'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsAddingSubscription(false)}
                    className="flex-1 py-2 px-4 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Отмена
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Список подписок на дату */}
          <div className="space-y-3">
            {subscriptionsOnDate.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <p>На эту дату нет подписок</p>
              </div>
            ) : (
              subscriptionsOnDate.map((subscription) => (
                <div key={subscription.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {subscription.logo_url ? (
                      <img
                        src={subscription.logo_url}
                        alt={subscription.name}
                        className="w-10 h-10 rounded-lg object-cover"
                      />
                    ) : (
                      <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                        <span className="text-indigo-600 font-bold text-lg">
                          {subscription.name?.[0]?.toUpperCase() || 'S'}
                        </span>
                      </div>
                    )}
                    <div>
                      <h3 className="font-semibold text-gray-900">{subscription.name}</h3>
                      <p className="text-sm text-gray-600">
                        {formatCurrency(subscription.amount)} {subscription.frequency === 'monthly' ? 'в месяц' : 'в год'}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteSubscription(subscription.id)}
                    className="text-red-500 hover:text-red-700 p-2"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
