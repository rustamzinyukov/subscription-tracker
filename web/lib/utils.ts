import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: number, currency: string = 'RUB'): string {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: currency,
  }).format(amount);
}

export function formatDate(date: string | Date): string {
  const dateObj = new Date(date);
  
  // Check if the date is valid
  if (isNaN(dateObj.getTime())) {
    console.warn('Invalid date:', date);
    return 'Неверная дата';
  }
  
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(dateObj);
}

export function formatDateTime(date: string | Date): string {
  const dateObj = new Date(date);
  
  // Check if the date is valid
  if (isNaN(dateObj.getTime())) {
    console.warn('Invalid date:', date);
    return 'Неверная дата';
  }
  
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(dateObj);
}

export function getDaysUntilBilling(nextBillingDate: string): number {
  const today = new Date();
  const billingDate = new Date(nextBillingDate);
  
  // Check if the date is valid
  if (isNaN(billingDate.getTime())) {
    console.warn('Invalid date:', nextBillingDate);
    return 0; // Return 0 if date is invalid
  }
  
  const diffTime = billingDate.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

export function getBillingStatus(daysUntilBilling: number): 'upcoming' | 'due' | 'overdue' {
  if (daysUntilBilling < 0) return 'overdue';
  if (daysUntilBilling <= 3) return 'due';
  return 'upcoming';
}

export function calculateTotalMonthlySpend(subscriptions: any[]): number {
  return subscriptions.reduce((total, sub) => {
    if (sub.frequency === 'monthly') {
      return total + sub.amount;
    } else if (sub.frequency === 'yearly') {
      return total + (sub.amount / 12);
    }
    return total;
  }, 0);
}

export function calculateTotalYearlySpend(subscriptions: any[]): number {
  return subscriptions.reduce((total, sub) => {
    if (sub.frequency === 'yearly') {
      return total + sub.amount;
    } else if (sub.frequency === 'monthly') {
      return total + (sub.amount * 12);
    }
    return total;
  }, 0);
}

export function getUpcomingBills(subscriptions: any[]): any[] {
  const today = new Date();
  const nextWeek = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
  
  return subscriptions.filter(sub => {
    if (!sub.is_active) return false;
    const billingDate = new Date(sub.next_billing_date);
    return billingDate >= today && billingDate <= nextWeek;
  });
}

export function getOverdueBills(subscriptions: any[]): any[] {
  const today = new Date();
  
  return subscriptions.filter(sub => {
    if (!sub.is_active) return false;
    const billingDate = new Date(sub.next_billing_date);
    return billingDate < today;
  });
}