'use client';

import { useState, useEffect } from 'react';
import { Subscription } from '@/types';
import { apiClient } from '@/lib/api';

interface AdvancedSubscriptionFormProps {
  isOpen: boolean;
  onClose: () => void;
  selectedDate?: Date;
  onSubscriptionAdd: (subscription: Subscription) => void;
}

type SubscriptionType = 'recurring' | 'one_time';
type IntervalUnit = 'day' | 'week' | 'month' | 'year';
type DurationType = 'days' | 'weeks' | 'months' | 'years' | 'indefinite';

export default function AdvancedSubscriptionForm({
  isOpen,
  onClose,
  selectedDate,
  onSubscriptionAdd
}: AdvancedSubscriptionFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [subscriptionType, setSubscriptionType] = useState<SubscriptionType>('recurring');
  const [hasTrial, setHasTrial] = useState(false);
  
  const [formData, setFormData] = useState({
    // Общие поля
    name: '',
    amount: '',
    currency: 'RUB',
    
    // Recurring поля
    next_billing_date: selectedDate ? selectedDate.toLocaleDateString('en-CA') : new Date().toLocaleDateString('en-CA'),
    interval_unit: 'month' as IntervalUnit,
    interval_count: 1,
    
    // Trial поля
    trial_start_date: new Date().toLocaleDateString('en-CA'),
    trial_end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
    
    // One-time поля
    start_date: selectedDate ? selectedDate.toLocaleDateString('en-CA') : new Date().toLocaleDateString('en-CA'),
    duration_type: 'months' as DurationType,
    duration_value: 3,
    
    // Дополнительные поля
    description: '',
    provider: '',
    logo_url: '',
    website_url: '',
  });

  // Обновляем даты при изменении selectedDate
  useEffect(() => {
    if (selectedDate) {
      const dateStr = selectedDate.toLocaleDateString('en-CA');
      setFormData(prev => ({
        ...prev,
        next_billing_date: dateStr,
        start_date: dateStr,
        trial_start_date: dateStr,
      }));
    }
  }, [selectedDate]);

  // Автоматический расчет trial_end_date при изменении trial_start_date
  useEffect(() => {
    if (hasTrial && formData.trial_start_date) {
      const startDate = new Date(formData.trial_start_date);
      const endDate = new Date(startDate.getTime() + 7 * 24 * 60 * 60 * 1000); // +7 дней
      setFormData(prev => ({
        ...prev,
        trial_end_date: endDate.toLocaleDateString('en-CA')
      }));
    }
  }, [hasTrial, formData.trial_start_date]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.amount) {
      alert('Пожалуйста, заполните обязательные поля');
      return;
    }

    try {
      setIsLoading(true);
      
      // Безопасная обработка дат
      const validateDate = (dateStr: string, fieldName: string) => {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) {
          throw new Error(`Неверный формат даты в поле "${fieldName}"`);
        }
        return date;
      };

      let subscriptionData: any = {
        name: formData.name,
        amount: parseFloat(formData.amount),
        currency: formData.currency,
        description: formData.description || undefined,
        provider: formData.provider || undefined,
        logo_url: formData.logo_url || undefined,
        website_url: formData.website_url || undefined,
        subscription_type: subscriptionType,
      };

      if (subscriptionType === 'recurring') {
        const nextPaymentDate = validateDate(formData.next_billing_date, 'Дата следующего платежа');
        subscriptionData = {
          ...subscriptionData,
          next_billing_date: nextPaymentDate.toISOString().split('T')[0],
          frequency: formData.interval_unit === 'day' ? 'daily' : 
                    formData.interval_unit === 'week' ? 'weekly' :
                    formData.interval_unit === 'month' ? 'monthly' : 'yearly',
          interval_unit: formData.interval_unit,
          interval_count: formData.interval_count,
          has_trial: hasTrial,
        };

        if (hasTrial) {
          const trialStartDate = validateDate(formData.trial_start_date, 'Дата начала пробного периода');
          const trialEndDate = validateDate(formData.trial_end_date, 'Дата окончания пробного периода');
          
          if (trialEndDate <= trialStartDate) {
            throw new Error('Дата окончания пробного периода должна быть позже даты начала');
          }
          
          if (trialEndDate >= nextPaymentDate) {
            throw new Error('Дата окончания пробного периода должна быть раньше даты первого платежа');
          }

          subscriptionData.trial_start_date = trialStartDate.toISOString().split('T')[0];
          subscriptionData.trial_end_date = trialEndDate.toISOString().split('T')[0];
        }
      } else {
        const startDate = validateDate(formData.start_date, 'Дата начала');
        subscriptionData = {
          ...subscriptionData,
          // next_billing_date не нужен для one_time подписок
          frequency: 'one_time', // Добавляем frequency для one_time подписок
          start_date: startDate.toISOString().split('T')[0],
          duration_type: formData.duration_type,
        };

        if (formData.duration_type !== 'indefinite') {
          if (!formData.duration_value || formData.duration_value < 1) {
            throw new Error('Укажите корректную продолжительность');
          }
          subscriptionData.duration_value = formData.duration_value;
        }
      }

      console.log('🔍 Advanced subscription data:', subscriptionData);
      
      const newSubscription = await apiClient.createSubscription(subscriptionData);
      onSubscriptionAdd(newSubscription);
      onClose();
      
      // Сброс формы
      setFormData({
        name: '',
        amount: '',
        currency: 'RUB',
        next_billing_date: new Date().toLocaleDateString('en-CA'),
        interval_unit: 'month',
        interval_count: 1,
        trial_start_date: new Date().toLocaleDateString('en-CA'),
        trial_end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
        start_date: new Date().toLocaleDateString('en-CA'),
        duration_type: 'months',
        duration_value: 3,
        description: '',
        provider: '',
        logo_url: '',
        website_url: '',
      });
      setSubscriptionType('recurring');
      setHasTrial(false);
      
    } catch (err: any) {
      console.error('Error creating subscription:', err);
      let errorMessage = 'Ошибка при создании подписки';
      
      if (err.message) {
        errorMessage = err.message;
      } else if (err.response?.data?.detail) {
        if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        } else if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map((item: any) => item.msg || item).join(', ');
        } else {
          errorMessage = JSON.stringify(err.response.data.detail);
        }
      }
      
      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Заголовок */}
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Добавить подписку</h2>
              {selectedDate && (
                <p className="text-sm text-gray-600">
                  Дата: {selectedDate.toLocaleDateString('ru-RU')}
                </p>
              )}
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

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Тип подписки */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Тип подписки *
              </label>
              <div className="grid grid-cols-2 gap-4">
                <label className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="radio"
                    name="subscription_type"
                    value="recurring"
                    checked={subscriptionType === 'recurring'}
                    onChange={(e) => setSubscriptionType(e.target.value as SubscriptionType)}
                    className="mr-3"
                  />
                  <div>
                    <div className="font-medium text-gray-900">С автопродлением</div>
                    <div className="text-sm text-gray-500">Регулярные платежи</div>
                  </div>
                </label>
                
                <label className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="radio"
                    name="subscription_type"
                    value="one_time"
                    checked={subscriptionType === 'one_time'}
                    onChange={(e) => setSubscriptionType(e.target.value as SubscriptionType)}
                    className="mr-3"
                  />
                  <div>
                    <div className="font-medium text-gray-900">Без автопродления</div>
                    <div className="text-sm text-gray-500">Фиксированный срок</div>
                  </div>
                </label>
              </div>
            </div>

            {/* Общие поля */}
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
                  placeholder="Spotify Premium"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Сумма *
                </label>
                <div className="flex">
                  <input
                    type="number"
                    step="0.01"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="199.00"
                    required
                  />
                  <select
                    value={formData.currency}
                    onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                    className="px-3 py-2 border border-l-0 border-gray-300 rounded-r-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="RUB">RUB</option>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Условные поля для recurring */}
            {subscriptionType === 'recurring' && (
              <>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Следующий платеж *
                    </label>
                    <input
                      type="date"
                      value={formData.next_billing_date}
                      onChange={(e) => setFormData({ ...formData, next_billing_date: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Период *
                    </label>
                    <select
                      value={formData.interval_unit}
                      onChange={(e) => setFormData({ ...formData, interval_unit: e.target.value as IntervalUnit })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="day">День(дней)</option>
                      <option value="week">Неделя(недель)</option>
                      <option value="month">Месяц(ев)</option>
                      <option value="year">Год(лет)</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Каждые *
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={formData.interval_count}
                      onChange={(e) => setFormData({ ...formData, interval_count: parseInt(e.target.value) || 1 })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      required
                    />
                  </div>
                </div>

                {/* Пробный период */}
                <div>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={hasTrial}
                      onChange={(e) => setHasTrial(e.target.checked)}
                      className="mr-2"
                    />
                    <span className="text-sm font-medium text-gray-700">
                      Есть пробный период
                    </span>
                  </label>
                </div>

                {hasTrial && (
                  <div className="grid grid-cols-2 gap-4 p-4 bg-blue-50 rounded-lg">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Начало пробного периода *
                      </label>
                      <input
                        type="date"
                        value={formData.trial_start_date}
                        onChange={(e) => setFormData({ ...formData, trial_start_date: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Окончание пробного периода *
                      </label>
                      <input
                        type="date"
                        value={formData.trial_end_date}
                        onChange={(e) => setFormData({ ...formData, trial_end_date: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Условные поля для one_time */}
            {subscriptionType === 'one_time' && (
              <>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Дата начала *
                    </label>
                    <input
                      type="date"
                      value={formData.start_date}
                      onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Тип срока *
                    </label>
                    <select
                      value={formData.duration_type}
                      onChange={(e) => setFormData({ ...formData, duration_type: e.target.value as DurationType })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="days">Дней</option>
                      <option value="weeks">Недель</option>
                      <option value="months">Месяцев</option>
                      <option value="years">Лет</option>
                      <option value="indefinite">Бессрочно</option>
                    </select>
                  </div>
                  
                  {formData.duration_type !== 'indefinite' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Продолжительность *
                      </label>
                      <input
                        type="number"
                        min="1"
                        value={formData.duration_value}
                        onChange={(e) => setFormData({ ...formData, duration_value: parseInt(e.target.value) || 1 })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>
                  )}
                </div>
              </>
            )}

            {/* Дополнительные поля */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Описание
                </label>
                <input
                  type="text"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Стриминг сервис"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Провайдер
                </label>
                <input
                  type="text"
                  value={formData.provider}
                  onChange={(e) => setFormData({ ...formData, provider: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Google, Apple, Yandex"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  URL логотипа
                </label>
                <input
                  type="url"
                  value={formData.logo_url}
                  onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="https://example.com/logo.png"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  URL сайта
                </label>
                <input
                  type="url"
                  value={formData.website_url}
                  onChange={(e) => setFormData({ ...formData, website_url: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="https://spotify.com"
                />
              </div>
            </div>

            {/* Кнопки */}
            <div className="flex space-x-3 pt-4">
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
              >
                {isLoading ? 'Создание...' : 'Создать подписку'}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="flex-1 py-2 px-4 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
              >
                Отмена
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
