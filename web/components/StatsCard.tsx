'use client';

interface StatsCardProps {
  title: string;
  value: string;
  icon: string;
  color: 'blue' | 'green' | 'purple' | 'red' | 'yellow';
}

export default function StatsCard({ title, value, icon, color }: StatsCardProps) {
  const getColorClasses = () => {
    switch (color) {
      case 'blue':
        return 'bg-blue-50 border-blue-200 text-blue-600';
      case 'green':
        return 'bg-green-50 border-green-200 text-green-600';
      case 'purple':
        return 'bg-purple-50 border-purple-200 text-purple-600';
      case 'red':
        return 'bg-red-50 border-red-200 text-red-600';
      case 'yellow':
        return 'bg-yellow-50 border-yellow-200 text-yellow-600';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-600';
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`w-12 h-12 rounded-lg border-2 flex items-center justify-center text-2xl ${getColorClasses()}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
