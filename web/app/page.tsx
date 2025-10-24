'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { User, Subscription } from '@/types';
import { formatCurrency, getDaysUntilBilling, getBillingStatus, calculateTotalMonthlySpend } from '@/lib/utils';
import Header from '@/components/Header';
import SubscriptionCard from '@/components/SubscriptionCard';
import AddSubscriptionButton from '@/components/AddSubscriptionButton';
import StatsCard from '@/components/StatsCard';
import UpcomingBills from '@/components/UpcomingBills';
import Calendar from '@/components/Calendar';
import DateModal from '@/components/DateModal';

export default function HomePage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [isDateModalOpen, setIsDateModalOpen] = useState(false);

  // Функция для логирования
  const addLog = (message: string) => {
    console.log(message);
    const existingLogs = JSON.parse(localStorage.getItem('debug_logs') || '[]');
    existingLogs.push(message);
    localStorage.setItem('debug_logs', JSON.stringify(existingLogs));
    setLogs(prev => [...prev, message]);
  };

  useEffect(() => {
    addLog('🏠 Главная страница загружена');
    addLog(`📍 Текущий URL: ${window.location.href}`);
    
    const token = localStorage.getItem('access_token');
    addLog(`🔑 Токен в localStorage: ${token ? 'найден' : 'не найден'}`);
    addLog(`🔑 Тип токена: ${typeof token}`);
    addLog(`🔑 Значение токена: ${token}`);
    if (token) {
      addLog(`🔑 Токен (первые 20 символов): ${token.substring(0, 20)}...`);
    }
    
    if (!token) {
      addLog('❌ Токен не найден, перенаправляем на логин');
      router.push('/login');
      return;
    }

    addLog('✅ Токен найден, загружаем данные');
    loadData();
    
    // Загружаем существующие логи
    const existingLogs = JSON.parse(localStorage.getItem('debug_logs') || '[]');
    setLogs(existingLogs);
  }, [router]);

  const loadData = async () => {
    try {
      addLog('📤 Загружаем данные пользователя...');
      addLog(`🔑 Токен перед запросом: ${localStorage.getItem('access_token')?.substring(0, 20)}...`);
      setLoading(true);
      
      addLog('🚀 Вызываем apiClient.getCurrentUser()...');
      const userData = await apiClient.getCurrentUser();
      addLog('✅ getCurrentUser() успешен');
      
      addLog('🚀 Вызываем apiClient.getSubscriptions()...');
      const subscriptionsData = await apiClient.getSubscriptions();
      addLog('✅ getSubscriptions() успешен');
      
      addLog('✅ Данные пользователя загружены успешно');
      
          // Debug logging for subscriptions
          console.log('🔍 Raw subscriptions data from API:', subscriptionsData);
          console.log('🔍 Subscriptions data type:', typeof subscriptionsData);
          console.log('🔍 Subscriptions data keys:', Object.keys(subscriptionsData));
          console.log('🔍 Subscriptions items:', subscriptionsData.items);
          console.log('🔍 Subscriptions total:', subscriptionsData.total);
          console.log('🔍 Subscriptions page:', subscriptionsData.page);
          console.log('🔍 Full subscriptions data structure:', JSON.stringify(subscriptionsData, null, 2));
          
          // Проверяем, что именно приходит от API
          if (Array.isArray(subscriptionsData)) {
            console.log('🔍 API вернул массив напрямую:', subscriptionsData);
            setSubscriptions(subscriptionsData);
          } else if (subscriptionsData.items) {
            console.log('🔍 API вернул объект с items:', subscriptionsData.items);
            setSubscriptions(subscriptionsData.items);
          } else {
            console.log('🔍 Неизвестная структура данных:', subscriptionsData);
            setSubscriptions([]);
          }
          
          if (subscriptionsData.items && subscriptionsData.items.length > 0) {
            console.log('🔍 First subscription:', subscriptionsData.items[0]);
          }
      
      setUser(userData);
    } catch (err: any) {
      const errorLog = `❌ Ошибка загрузки данных: ${JSON.stringify({
        status: err.response?.status,
        data: err.response?.data,
        message: err.message
      })}`;
      addLog(errorLog);
      console.error('Error loading data:', err);
      let errorMessage = 'Ошибка загрузки данных';
      
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
      
      setError(errorMessage);
      localStorage.removeItem('access_token');
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  const handleSubscriptionUpdate = (updatedSubscription: Subscription) => {
    setSubscriptions(prev => 
      prev.map(sub => sub.id === updatedSubscription.id ? updatedSubscription : sub)
    );
  };

  const handleSubscriptionDelete = (subscriptionId: number) => {
    console.log('🗑️ Удаляем подписку из главного компонента, ID:', subscriptionId);
    setSubscriptions(prev => {
      const filtered = prev.filter(sub => sub.id !== subscriptionId);
      console.log('📊 Подписок до удаления:', prev.length);
      console.log('📊 Подписок после удаления:', filtered.length);
      return filtered;
    });
  };

  const handleSubscriptionAdd = (newSubscription: Subscription) => {
    setSubscriptions(prev => [...prev, newSubscription]);
  };

  const handleDateClick = (date: Date) => {
    setSelectedDate(date);
    // Не открываем модальное окно, просто выбираем дату для панели
  };

  const handleCloseDateModal = () => {
    setIsDateModalOpen(false);
    setSelectedDate(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Ошибка</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => router.push('/login')}
            className="btn-primary"
          >
            Войти в систему
          </button>
        </div>
      </div>
    );
  }

  const totalMonthlySpend = calculateTotalMonthlySpend(subscriptions);
  const activeSubscriptions = subscriptions.filter(sub => sub.is_active).length;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Добро пожаловать, {user?.first_name || user?.username || 'Пользователь'}!
          </h1>
          <p className="text-gray-600">
            Управляйте своими подписками и отслеживайте расходы
          </p>
        </div>

        {/* Только основная статистика */}
        <div className="mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Общие расходы в месяц</h3>
                <p className="text-2xl font-bold text-indigo-600">{formatCurrency(totalMonthlySpend, 'RUB')}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-500">Активных подписок</p>
                <p className="text-xl font-semibold text-gray-900">{activeSubscriptions}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Основной контент: Календарь + Панель */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Календарь (2/3 ширины) */}
          <div className="lg:col-span-2">
            <Calendar
              subscriptions={subscriptions}
              onDateClick={handleDateClick}
              onSubscriptionAdd={handleSubscriptionAdd}
            />
          </div>
          
          {/* Панель подписок (1/3 ширины) */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 h-fit">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                {selectedDate ? `Подписки на ${selectedDate.toLocaleDateString('ru-RU')}` : 'Выберите дату'}
              </h3>
              
              {selectedDate ? (
                <div className="space-y-3">
                  {subscriptions.filter(sub => {
                    if (!sub.next_billing_date) return false;
                    const billingDate = new Date(sub.next_billing_date);
                    return billingDate.toDateString() === selectedDate.toDateString();
                  }).length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <div className="text-4xl mb-2">📅</div>
                      <p className="text-sm">На эту дату нет подписок</p>
                      <button
                        onClick={() => setIsDateModalOpen(true)}
                        className="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm"
                      >
                        Добавить подписку
                      </button>
                    </div>
                  ) : (
                    <>
                      {subscriptions.filter(sub => {
                        if (!sub.next_billing_date) return false;
                        const billingDate = new Date(sub.next_billing_date);
                        return billingDate.toDateString() === selectedDate.toDateString();
                      }).map((subscription) => (
                        <div key={subscription.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-3">
                            {subscription.logo_url ? (
                              <img
                                src={subscription.logo_url}
                                alt={subscription.name}
                                className="w-8 h-8 rounded-lg object-cover"
                              />
                            ) : (
                              <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                                <span className="text-indigo-600 font-bold text-sm">
                                  {subscription.name?.[0]?.toUpperCase() || 'S'}
                                </span>
                              </div>
                            )}
                            <div>
                              <h4 className="font-medium text-gray-900 text-sm">{subscription.name}</h4>
                              <p className="text-xs text-gray-600">
                                {formatCurrency(subscription.amount)} {subscription.frequency === 'monthly' ? 'в месяц' : 'в год'}
                              </p>
                            </div>
                          </div>
                          <button
                            onClick={() => handleSubscriptionDelete(subscription.id)}
                            className="text-red-500 hover:text-red-700 p-1"
                            title="Удалить подписку"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      ))}
                      
                      <button
                        onClick={() => setIsDateModalOpen(true)}
                        className="w-full mt-4 py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm flex items-center justify-center gap-2"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        Добавить подписку
                      </button>
                    </>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <div className="text-4xl mb-2">📅</div>
                  <p className="text-sm">Кликните на дату в календаре, чтобы увидеть подписки</p>
                </div>
              )}
            </div>
          </div>
        </div>

      </main>
      
      {/* Отображение логов */}
      {logs.length > 0 && (
        <div className="mt-8 max-w-6xl mx-auto px-4">
          <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-white font-bold">📋 Логи отладки ({logs.length})</h3>
              <button
                onClick={() => {
                  localStorage.removeItem('debug_logs');
                  setLogs([]);
                }}
                className="text-red-400 hover:text-red-300 text-xs"
              >
                Очистить логи
              </button>
            </div>
            <div className="max-h-60 overflow-y-auto">
              {logs.map((log, index) => (
                <div key={index} className="mb-1 text-xs">
                  {log}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно для просмотра подписок на дату */}
      <DateModal
        isOpen={isDateModalOpen}
        onClose={handleCloseDateModal}
        date={selectedDate}
        subscriptions={subscriptions}
        onSubscriptionAdd={handleSubscriptionAdd}
        onSubscriptionUpdate={handleSubscriptionUpdate}
        onSubscriptionDelete={handleSubscriptionDelete}
      />
    </div>
  );
}
