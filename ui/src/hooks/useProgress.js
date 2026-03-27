import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';

export function useProgress() {
  return useQuery({
    queryKey: ['progress'],
    queryFn: api.getProgress,
    staleTime: 30_000,
  });
}

export function useSaveProgress() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: api.saveProgress,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['progress'] }),
  });
}

export function useGaps(level = 'sde2') {
  return useQuery({
    queryKey: ['gaps', level],
    queryFn: () => api.getGaps(level),
    staleTime: 60_000,
  });
}

export function useDailyPlan() {
  return useQuery({
    queryKey: ['dailyPlan'],
    queryFn: api.getDailyPlan,
    staleTime: 120_000,
  });
}

export function useWeeklyPlan() {
  return useQuery({
    queryKey: ['weeklyPlan'],
    queryFn: api.getWeeklyPlan,
    staleTime: 300_000,
  });
}

export function usePlanStats() {
  return useQuery({
    queryKey: ['planStats'],
    queryFn: api.getPlanStats,
    staleTime: 30_000,
  });
}

export function useTodayLog() {
  return useQuery({
    queryKey: ['todayLog'],
    queryFn: api.getTodayLog,
    staleTime: 15_000,
  });
}

export function useLogActivity() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: api.logActivity,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['todayLog'] });
      qc.invalidateQueries({ queryKey: ['planStats'] });
    },
  });
}

export function useDrillStats() {
  return useQuery({
    queryKey: ['drillStats'],
    queryFn: api.getDrillStats,
    staleTime: 60_000,
  });
}

export function useMockTrend() {
  return useQuery({
    queryKey: ['mockTrend'],
    queryFn: api.getMockTrend,
    staleTime: 60_000,
  });
}

export function useIntelStats() {
  return useQuery({
    queryKey: ['intelStats'],
    queryFn: api.getIntelStats,
    staleTime: 120_000,
  });
}

export function useCurriculum() {
  return useQuery({
    queryKey: ['curriculum'],
    queryFn: api.getCurriculum,
    staleTime: 300_000,
  });
}
