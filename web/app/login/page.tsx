'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { LoginRequest } from '@/types';

export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: '',
    first_name: '',
    last_name: '',
  });

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      router.push('/');
    }
    
    // Загружаем существующие логи
    const existingLogs = JSON.parse(localStorage.getItem('debug_logs') || '[]');
    setLogs(existingLogs);
  }, [router]);

  // Функция для логирования
  const addLog = (message: string) => {
    console.log(message);
    const existingLogs = JSON.parse(localStorage.getItem('debug_logs') || '[]');
    existingLogs.push(message);
    localStorage.setItem('debug_logs', JSON.stringify(existingLogs));
    localStorage.setItem('debug_log', message);
    
    // Обновляем состояние для отображения на странице
    setLogs(prev => [...prev, message]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    const logMessage = `🚀 handleSubmit вызван! ${new Date().toISOString()} - isLogin: ${isLogin}, formData: ${JSON.stringify(formData)}`;
    addLog(logMessage);
    
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (isLogin) {
        const loginLog = `🔐 Начинаем логин с данными: ${new Date().toISOString()} - email: ${formData.email}`;
        addLog(loginLog);
        
        const loginData: LoginRequest = {
          email: formData.email,
          password: formData.password,
        };
        
        const requestLog = `📤 Отправляем запрос на логин: ${new Date().toISOString()}`;
        addLog(requestLog);
        
        const response = await apiClient.login(loginData);
        
        const successLog = `✅ Логин успешен! ${new Date().toISOString()} - response: ${JSON.stringify(response)}`;
        addLog(successLog);
        
        // Проверяем структуру ответа
        addLog(`🔍 Структура ответа: data=${JSON.stringify(response.data)}`);
        addLog(`🔍 access_token в response: ${response.data?.access_token ? 'найден' : 'не найден'}`);
        addLog(`🔍 access_token значение: ${response.data?.access_token || 'undefined'}`);
        
        localStorage.setItem('access_token', response.access_token);
        
        const tokenLog = `💾 Токен сохранен в localStorage: ${new Date().toISOString()}`;
        addLog(tokenLog);
        
        const redirectLog = `🔄 Перенаправляем на главную страницу: ${new Date().toISOString()}`;
        addLog(redirectLog);
        
        addLog('🚀 Вызываем router.push("/")...');
        router.push('/');
        addLog('✅ router.push("/") вызван');
      } else {
        const registerData = {
          email: formData.email,
          password: formData.password,
          username: formData.username || undefined,
          first_name: formData.first_name || undefined,
          last_name: formData.last_name || undefined,
        };
        const response = await apiClient.register(registerData);
        localStorage.setItem('access_token', response.access_token);
        router.push('/');
      }
    } catch (err: any) {
      const errorLog = `❌ Ошибка при авторизации: ${new Date().toISOString()} - ${JSON.stringify({
        status: err.response?.status,
        data: err.response?.data,
        message: err.message
      })}`;
      addLog(errorLog);
      
      let errorMessage = 'Произошла ошибка при авторизации';
      
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
      const finalLog = `🏁 handleSubmit завершен: ${new Date().toISOString()} - isLoading = false`;
      addLog(finalLog);
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-xl">S</span>
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
          {isLogin ? 'Вход в аккаунт' : 'Создать аккаунт'}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          {isLogin ? (
            <>
              Нет аккаунта?{' '}
              <button
                onClick={() => setIsLogin(false)}
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Зарегистрироваться
              </button>
            </>
          ) : (
            <>
              Уже есть аккаунт?{' '}
              <button
                onClick={() => setIsLogin(true)}
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Войти
              </button>
            </>
          )}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email адрес
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="your@email.com"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Пароль
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete={isLogin ? 'current-password' : 'new-password'}
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="••••••••"
                />
              </div>
            </div>

            {!isLogin && (
              <>
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                    Имя пользователя (необязательно)
                  </label>
                  <div className="mt-1">
                    <input
                      id="username"
                      name="username"
                      type="text"
                      value={formData.username}
                      onChange={handleInputChange}
                      className="input-field"
                      placeholder="username"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                      Имя
                    </label>
                    <div className="mt-1">
                      <input
                        id="first_name"
                        name="first_name"
                        type="text"
                        value={formData.first_name}
                        onChange={handleInputChange}
                        className="input-field"
                        placeholder="Иван"
                      />
                    </div>
                  </div>

                  <div>
                    <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                      Фамилия
                    </label>
                    <div className="mt-1">
                      <input
                        id="last_name"
                        name="last_name"
                        type="text"
                        value={formData.last_name}
                        onChange={handleInputChange}
                        className="input-field"
                        placeholder="Иванов"
                      />
                    </div>
                  </div>
                </div>
              </>
            )}

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Загрузка...' : (isLogin ? 'Войти' : 'Создать аккаунт')}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Или</span>
              </div>
            </div>

            <div className="mt-6 space-y-3">
              <button
                onClick={() => {
                  const logs = JSON.parse(localStorage.getItem('debug_logs') || '[]');
                  if (logs.length > 0) {
                    const allLogs = logs.join('\n\n');
                    alert(`Все логи (${logs.length}):\n\n${allLogs}`);
                  } else {
                    alert('Логов пока нет');
                  }
                }}
                className="w-full flex justify-center items-center px-4 py-2 border border-blue-300 rounded-lg shadow-sm bg-blue-50 text-sm font-medium text-blue-600 hover:bg-blue-100"
              >
                📋 Показать все логи
              </button>
              
              <button
                onClick={() => {
                  // Telegram Mini App integration
                  if (window.Telegram?.WebApp) {
                    const tg = window.Telegram.WebApp;
                    tg.ready();
                    tg.expand();
                    // Handle Telegram auth
                    console.log('Telegram Mini App detected');
                  } else {
                    alert('Telegram Mini App не обнаружен');
                  }
                }}
                className="w-full flex justify-center items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.568 8.16l-1.61 7.59c-.12.54-.44.67-.9.42l-2.49-1.84-1.2 1.16c-.13.13-.24.24-.49.24l.18-2.56 4.64-4.19c.2-.18-.04-.28-.31-.1l-5.74 3.61-2.47-.77c-.54-.17-.55-.54.11-.8l9.66-3.72c.45-.17.84.1.7.8z"/>
                </svg>
                Войти через Telegram
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Отображение логов */}
      {logs.length > 0 && (
        <div className="mt-8 max-w-4xl mx-auto">
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
