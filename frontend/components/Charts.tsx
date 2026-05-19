'use client'

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import { motion } from 'framer-motion'

interface ChartProps {
  title: string
  data: any[]
  type: 'line' | 'bar' | 'pie'
}

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']

export function MonthlyFlowChart({ data }: { data: any[] }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="card card-hover"
    >
      <h3 className="text-lg font-bold mb-4">Monthly PR Flow</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Bar dataKey="created" fill="#667eea" />
          <Bar dataKey="merged" fill="#10b981" />
          <Bar dataKey="closed" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  )
}

export function ThroughputChart({ data }: { data: any[] }) {
  const chartData = Object.entries(data).map(([week, count]) => ({
    week,
    prs: count,
  }))

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="card card-hover"
    >
      <h3 className="text-lg font-bold mb-4">PR Throughput (Weekly)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '8px',
            }}
          />
          <Line
            type="monotone"
            dataKey="prs"
            stroke="#667eea"
            strokeWidth={2}
            dot={{ fill: '#667eea' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  )
}

export function ContributorChart({ data }: { data: any[] }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="card card-hover"
    >
      <h3 className="text-lg font-bold mb-4">Contributor Activity - PRs Opened/Merged</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="username" stroke="#9ca3af" angle={-45} textAnchor="end" height={80} />
          <YAxis stroke="#9ca3af" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '8px',
            }}
            formatter={(value) => `${value} PRs`}
          />
          <Legend />
          <Bar dataKey="total_prs" fill="#667eea" name="Opened" />
          <Bar dataKey="merged_prs" fill="#10b981" name="Merged" />
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  )
}

export function ReviewTurnaroundChart({ data }: { data: any[] }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="card card-hover"
    >
      <h3 className="text-lg font-bold mb-4">Review Turnaround - Avg Wait for First Review</h3>
      <div className="space-y-3">
        {data.map((item, idx) => (
          <div key={idx} className="flex items-center gap-3">
            <div className="w-32 text-sm font-medium text-gray-300">{item.username}</div>
            <div className="flex-1 bg-dark-700 rounded h-6 relative overflow-hidden">
              <div
                className={`h-full rounded flex items-center justify-end pr-2 text-xs font-bold text-white ${
                  item.avg_wait_hours < 24
                    ? 'bg-green-600'
                    : item.avg_wait_hours < 48
                    ? 'bg-yellow-600'
                    : 'bg-red-600'
                }`}
                style={{ width: `${Math.min((item.avg_wait_hours / 100) * 100, 100)}%` }}
              >
                {item.avg_wait_hours > 10 && `${item.avg_wait_hours.toFixed(1)}h`}
              </div>
            </div>
            <div className="w-16 text-right text-sm font-semibold text-gray-300">
              {item.avg_wait_hours < 24
                ? `${item.avg_wait_hours.toFixed(1)}h`
                : `${(item.avg_wait_hours / 24).toFixed(1)}d`}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 text-xs text-gray-400 flex gap-4">
        <span>🟢 &lt;24h</span>
        <span>🟡 24-48h</span>
        <span>🔴 &gt;48h</span>
      </div>
    </motion.div>
  )
}
