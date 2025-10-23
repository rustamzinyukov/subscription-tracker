'use client';

import { Subscription } from '@/types';
import { formatCurrency, formatDate, getUpcomingBills, getOverdueBills } from '@/lib/utils';

interface UpcomingBillsProps {
  subscriptions: Subscription[];
}

export default function UpcomingBills({ subscriptions }: UpcomingBillsProps) {
  const upcomingBills = getUpcomingBills(subscriptions);
  const overdueBills = getOverdueBills(subscriptions);

  if (upcomingBills.length === 0 && overdueBills.length === 0) {
    return null;
  }

  return (
    <div className="mb-8">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Предстоящие платежи</h2>
      
      <div className="space-y-4">
        {/* Overdue Bills */}
        {overdueBills.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-red-600 mb-2">Просроченные платежи</h3>
            <div className="space-y-2">
              {overdueBills.map((subscription) => (
                <div key={subscription.id} className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <h4 className="font-medium text-red-900">{subscription.name}</h4>
                      <p className="text-sm text-red-600">
                        Просрочено с {formatDate(subscription.next_billing_date)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-red-900">
                        {formatCurrency(subscription.amount, subscription.currency)}
                      </p>
                      <p className="text-sm text-red-600">
                        {subscription.frequency === 'monthly' ? 'в месяц' : 'в год'}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Upcoming Bills */}
        {upcomingBills.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">
              Ближайшие 30 дней
            </h3>
            <div className="space-y-2">
              {upcomingBills.map((subscription) => (
                <div key={subscription.id} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                  <div className="flex justify-between items-center">
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
                            {subscription.name[0].toUpperCase()}
                          </span>
                        </div>
                      )}
                      <div>
                        <h4 className="font-medium text-gray-900">{subscription.name}</h4>
                        <p className="text-sm text-gray-500">
                          {formatDate(subscription.next_billing_date)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">
                        {formatCurrency(subscription.amount, subscription.currency)}
                      </p>
                      <p className="text-sm text-gray-500">
                        {subscription.frequency === 'monthly' ? 'в месяц' : 'в год'}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
