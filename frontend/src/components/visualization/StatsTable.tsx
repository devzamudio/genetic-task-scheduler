import type { StatisticalReport } from '../../types';

interface StatsTableProps {
  stats: StatisticalReport;
}

export function StatsTable({ stats }: StatsTableProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Estadísticas Descriptivas (20 Ejecuciones)
      </h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Métrica
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Valor
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Mejor Makespan
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {stats.best_makespan.toFixed(2)}
              </td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Peor Makespan
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {stats.worst_makespan.toFixed(2)}
              </td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Promedio
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {stats.average_makespan.toFixed(2)}
              </td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Desviación Estándar
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {stats.std_dev.toFixed(2)}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}