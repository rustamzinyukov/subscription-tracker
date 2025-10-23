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

export default function HomePage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

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
      setUser(userData);
      setSubscriptions(subscriptionsData);
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
    setSubscriptions(prev => prev.filter(sub => sub.id !== subscriptionId));
  };

  const handleSubscriptionAdd = (newSubscription: Subscription) => {
    setSubscriptions(prev => [...prev, newSubscription]);
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

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatsCard
            title="Активных подписок"
            value={activeSubscriptions.toString()}
            icon="📱"
            color="blue"
          />
          <StatsCard
            title="Траты в месяц"
            value={formatCurrency(totalMonthlySpend, 'RUB')}
            icon="💰"
            color="green"
          />
          <StatsCard
            title="Средняя подписка"
            value={activeSubscriptions > 0 ? formatCurrency(totalMonthlySpend / activeSubscriptions, 'RUB') : '0 ₽'}
            icon="📊"
            color="purple"
          />
        </div>

        {/* Upcoming Bills */}
        <UpcomingBills subscriptions={subscriptions} />

        {/* Subscriptions Section */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Ваши подписки</h2>
            <AddSubscriptionButton onSubscriptionAdd={handleSubscriptionAdd} />
          </div>

          {subscriptions.length === 0 ? (
            <div className="card text-center py-12">
              <div className="text-6xl mb-4">📱</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                У вас пока нет подписок
              </h3>
              <p className="text-gray-600 mb-6">
                Добавьте свою первую подписку, чтобы начать отслеживать расходы
              </p>
              <AddSubscriptionButton onSubscriptionAdd={handleSubscriptionAdd} />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {subscriptions.map((subscription) => (
                <SubscriptionCard
                  key={subscription.id}
                  subscription={subscription}
                  onUpdate={handleSubscriptionUpdate}
                  onDelete={handleSubscriptionDelete}
                />
              ))}
            </div>
          )}
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
    </div>
  );
}
