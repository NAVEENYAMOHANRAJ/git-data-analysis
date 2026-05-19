import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const analyzeRepository = async (url: string) => {
  const response = await api.post('/api/analyze', {
    url,
  })
  return response.data
}

export const getKPI = async (repoId: number) => {
  const response = await api.get(`/api/kpi/${repoId}`)
  return response.data
}

export const getOldestPRs = async (repoId: number, limit: number = 10) => {
  const response = await api.get(`/api/oldest-prs/${repoId}`, {
    params: { limit },
  })
  return response.data
}

export const getSlowestPRs = async (repoId: number, limit: number = 10) => {
  const response = await api.get(`/api/slowest-prs/${repoId}`, {
    params: { limit },
  })
  return response.data
}

export const getContributorActivity = async (repoId: number) => {
  const response = await api.get(`/api/contributor-activity/${repoId}`)
  return response.data
}

export const getMonthlyFlow = async (repoId: number, months: number = 3) => {
  const response = await api.get(`/api/monthly-flow/${repoId}`, {
    params: { months },
  })
  return response.data
}

export const getThroughput = async (repoId: number, weeks: number = 4) => {
  const response = await api.get(`/api/throughput/${repoId}`, {
    params: { weeks },
  })
  return response.data
}
