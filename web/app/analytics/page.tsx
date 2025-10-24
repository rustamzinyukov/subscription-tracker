'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { Analytics, Subscription } from '@/types';
import { formatCurrency, calculateTotalMonthlySpend, calculateTotalYearlySpend } from '@/lib/utils';
import Header from '@/components/Header';
import StatsCard from '@/components/StatsCard';

export default function AnalyticsPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [monthlyAnalytics, setMonthlyAnalytics] = useState<Analytics | null>(null);
  const [yearlyAnalytics, setYearlyAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }

    loadData();
  }, [router]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [userData, subscriptionsData, monthlyData, yearlyData] = await Promise.all([
        apiClient.getCurrentUser(),
        apiClient.getSubscriptions(),
        apiClient.getMonthlyAnalytics(),
        apiClient.getYearlyAnalytics(),
      ]);
      
      setUser(userData);
      setSubscriptions(subscriptionsData);
      setMonthlyAnalytics(monthlyData);
      setYearlyAnalytics(yearlyData);
    } catch (err: any) {
      console.error('Error loading analytics:', err);
      let errorMessage = 'Ошибка загрузки аналитики';
      
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
    } finally {
      setLoading(false);
    }
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
            onClick={() => router.push('/')}
            className="btn-primary"
          >
            На главную
          </button>
        </div>
      </div>
    );
  }

  const totalMonthlySpend = calculateTotalMonthlySpend(subscriptions);
  const totalYearlySpend = calculateTotalYearlySpend(subscriptions);
  const activeSubscriptions = subscriptions.filter(sub => sub.is_active).length;
  const cancelledSubscriptions = subscriptions.filter(sub => !sub.is_active).length;

  // Calculate spending by category (simplified)
  const spendingByFrequency = {
    monthly: subscriptions
      .filter(sub => sub.is_active && sub.frequency === 'monthly')
      .reduce((total, sub) => total + sub.amount, 0),
    yearly: subscriptions
      .filter(sub => sub.is_active && sub.frequency === 'yearly')
      .reduce((total, sub) => total + sub.amount, 0),
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Аналитика</h1>
          <p className="text-gray-600">
            Подробная статистика ваших подписок и расходов
          </p>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Активных подписок"
            value={activeSubscriptions.toString()}
            icon="📱"
            color="blue"
          />
          <StatsCard
            title="Отмененных подписок"
            value={cancelledSubscriptions.toString()}
            icon="❌"
            color="red"
          />
          <StatsCard
            title="Траты в месяц"
            value={formatCurrency(totalMonthlySpend, 'RUB')}
            icon="💰"
            color="green"
          />
          <StatsCard
            title="Траты в год"
            value={formatCurrency(totalYearlySpend, 'RUB')}
            icon="📊"
            color="purple"
          />
        </div>

        {/* Detailed Analytics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Monthly vs Yearly Spending */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Расходы по периодичности
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Ежемесячные подписки</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(spendingByFrequency.monthly, 'RUB')}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Ежегодные подписки</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(spendingByFrequency.yearly, 'RUB')}
                </span>
              </div>
              <div className="border-t pt-4">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-900">Итого в месяц</span>
                  <span className="font-bold text-lg text-primary-600">
                    {formatCurrency(totalMonthlySpend, 'RUB')}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Subscription Status */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Статус подписок
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-gray-600">Активные</span>
                </div>
                <span className="font-semibold text-gray-900">{activeSubscriptions}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span className="text-gray-600">Отмененные</span>
                </div>
                <span className="font-semibold text-gray-900">{cancelledSubscriptions}</span>
              </div>
              <div className="border-t pt-4">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-900">Всего подписок</span>
                  <span className="font-bold text-lg text-primary-600">
                    {subscriptions.length}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Top Subscriptions by Cost */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Самые дорогие подписки
          </h3>
          <div className="space-y-3">
            {subscriptions
              .filter(sub => sub.is_active)
              .sort((a, b) => {
                const aMonthly = a.frequency === 'monthly' ? a.amount : a.amount / 12;
                const bMonthly = b.frequency === 'monthly' ? b.amount : b.amount / 12;
                return bMonthly - aMonthly;
              })
              .slice(0, 5)
              .map((subscription) => {
                const monthlyAmount = subscription.frequency === 'monthly' 
                  ? subscription.amount 
                  : subscription.amount / 12;
                
                return (
                  <div key={subscription.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
                    <div className="flex items-center space-x-3">
                      {subscription.logo_url ? (
                        <img
                          src={subscription.logo_url}
                          alt={subscription.name}
                          className="w-8 h-8 rounded-lg object-cover"
                        />
                      ) : (
                        <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                          <span className="text-primary-600 font-bold text-sm">
                            {subscription.name?.[0]?.toUpperCase() || 'S'}
                          </span>
                        </div>
                      )}
                      <div>
                        <p className="font-medium text-gray-900">{subscription.name}</p>
                        <p className="text-sm text-gray-500">
                          {subscription.frequency === 'monthly' ? 'в месяц' : 'в год'}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">
                        {formatCurrency(monthlyAmount, subscription.currency)}
                      </p>
                      <p className="text-sm text-gray-500">в месяц</p>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>

        {/* Monthly vs Yearly Comparison */}
        {monthlyAnalytics && yearlyAnalytics && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Месячная аналитика
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Период:</span>
                  <span className="font-medium">
                    {new Date(monthlyAnalytics.period_start).toLocaleDateString('ru-RU')} - 
                    {new Date(monthlyAnalytics.period_end).toLocaleDateString('ru-RU')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Потрачено:</span>
                  <span className="font-semibold text-green-600">
                    {formatCurrency(monthlyAnalytics.total_monthly_spend, 'RUB')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Активных подписок:</span>
                  <span className="font-semibold">{monthlyAnalytics.active_subscriptions}</span>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Годовая аналитика
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Период:</span>
                  <span className="font-medium">
                    {new Date(yearlyAnalytics.period_start).toLocaleDateString('ru-RU')} - 
                    {new Date(yearlyAnalytics.period_end).toLocaleDateString('ru-RU')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Потрачено:</span>
                  <span className="font-semibold text-green-600">
                    {formatCurrency(yearlyAnalytics.total_yearly_spend, 'RUB')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Отмененных подписок:</span>
                  <span className="font-semibold">{yearlyAnalytics.cancelled_subscriptions}</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
