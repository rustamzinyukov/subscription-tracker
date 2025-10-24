'use client';

import { useState, useEffect } from 'react';
import { Subscription } from '@/types';
import { formatCurrency } from '@/lib/utils';

interface CalendarProps {
  subscriptions: Subscription[];
  onDateClick: (date: Date) => void;
  onSubscriptionAdd: (subscription: Subscription) => void;
}

export default function Calendar({ subscriptions, onDateClick, onSubscriptionAdd }: CalendarProps) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  // Получаем первый день месяца и количество дней
  const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
  const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
  const daysInMonth = lastDayOfMonth.getDate();
  const startingDayOfWeek = firstDayOfMonth.getDay();

  // Создаем массив дней месяца
  const days = [];
  
  // Добавляем пустые ячейки для начала месяца
  for (let i = 0; i < startingDayOfWeek; i++) {
    days.push(null);
  }
  
  // Добавляем дни месяца
  for (let day = 1; day <= daysInMonth; day++) {
    days.push(new Date(currentDate.getFullYear(), currentDate.getMonth(), day));
  }

  // Функция для получения цвета даты на основе подписок
  const getDateColor = (date: Date) => {
    if (!date) return '';
    
    const today = new Date();
    const timeDiff = date.getTime() - today.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    
    // Находим подписки на эту дату
    const subscriptionsOnDate = subscriptions.filter(sub => {
      if (!sub.next_billing_date) return false;
      const billingDate = new Date(sub.next_billing_date);
      return billingDate.toDateString() === date.toDateString();
    });

    if (subscriptionsOnDate.length === 0) return '';

    // Определяем цвет на основе количества дней до платежа
    if (daysDiff < 0) return 'bg-gray-200 text-gray-600'; // Просрочено
    if (daysDiff <= 3) return 'bg-red-100 text-red-700 border-red-300'; // Срочно (1-3 дня)
    if (daysDiff <= 7) return 'bg-yellow-100 text-yellow-700 border-yellow-300'; // Скоро (4-7 дней)
    return 'bg-green-100 text-green-700 border-green-300'; // Далеко (8+ дней)
  };

  // Функция для получения подписок на дату
  const getSubscriptionsOnDate = (date: Date) => {
    return subscriptions.filter(sub => {
      if (!sub.next_billing_date) return false;
      const billingDate = new Date(sub.next_billing_date);
      return billingDate.toDateString() === date.toDateString();
    });
  };

  // Навигация по месяцам
  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  // Обработка клика на дату
  const handleDateClick = (date: Date) => {
    setSelectedDate(date);
    onDateClick(date);
  };

  const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Заголовок календаря */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={goToPreviousMonth}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">
            {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
          </h2>
          <button
            onClick={goToToday}
            className="text-sm text-indigo-600 hover:text-indigo-800 mt-1"
          >
            Сегодня
          </button>
        </div>
        
        <button
          onClick={goToNextMonth}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Сетка календаря */}
      <div className="grid grid-cols-7 gap-1">
        {/* Заголовки дней недели */}
        {dayNames.map(day => (
          <div key={day} className="p-2 text-center text-sm font-medium text-gray-500">
            {day}
          </div>
        ))}
        
        {/* Дни месяца */}
        {days.map((date, index) => {
          if (!date) {
            return <div key={index} className="h-12"></div>;
          }
          
          const subscriptionsOnDate = getSubscriptionsOnDate(date);
          const isToday = date.toDateString() === new Date().toDateString();
          const isSelected = selectedDate && date.toDateString() === selectedDate.toDateString();
          
          return (
            <div
              key={index}
              onClick={() => handleDateClick(date)}
              className={`
                h-12 p-1 cursor-pointer rounded-lg border-2 transition-all hover:shadow-md
                ${getDateColor(date)}
                ${isToday ? 'ring-2 ring-indigo-500' : ''}
                ${isSelected ? 'ring-2 ring-blue-500' : ''}
                ${subscriptionsOnDate.length > 0 ? 'font-semibold' : ''}
              `}
            >
              <div className="text-sm">
                {date.getDate()}
              </div>
              {subscriptionsOnDate.length > 0 && (
                <div className="text-xs mt-1">
                  {subscriptionsOnDate.length} платеж{subscriptionsOnDate.length > 1 ? 'ей' : ''}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Легенда цветов */}
      <div className="mt-6 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-100 border border-red-300 rounded"></div>
          <span>Срочно (1-3 дня)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-yellow-100 border border-yellow-300 rounded"></div>
          <span>Скоро (4-7 дней)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-100 border border-green-300 rounded"></div>
          <span>Далеко (8+ дней)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-gray-200 rounded"></div>
          <span>Просрочено</span>
        </div>
      </div>
    </div>
  );
}
