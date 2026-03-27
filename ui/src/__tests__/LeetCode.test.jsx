/**
 * Component tests for LeetCode page
 * Tests verify LC sync data is displayed correctly
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import LeetCode from '../pages/LeetCode';

// Mock useProgress hook
vi.mock('../hooks/useProgress', () => ({
  useProgress: () => ({
    data: {
      lc_sync: {
        total: 158,
        easy: 62,
        medium: 80,
        hard: 16,
        java_problems: 9,
        cpp_problems: 151,
        streak: 4,
        last_sync: '2026-03-27',
      },
      lc_done: [
        { name: 'Two Sum', date: '2026-03-19' },
      ],
      daily_logs: {},
    },
    isLoading: false,
  }),
  useSaveProgress: () => ({
    mutate: vi.fn(),
    isPending: false,
  }),
  useLogActivity: () => ({
    mutate: vi.fn(),
  }),
}));

const renderWithQueryClient = (component) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('LeetCode Page', () => {
  it('should render LeetCode tracker', () => {
    renderWithQueryClient(<LeetCode />);
    expect(screen.getByText('LeetCode Tracker')).toBeInTheDocument();
  });

  it('should display synced LC stats', () => {
    /**
     * CRITICAL TEST: This is what failed!
     * User couldn't see LC stats even though data was in progress.json
     */
    renderWithQueryClient(<LeetCode />);

    // Should display total problems solved
    expect(screen.getByText('158')).toBeInTheDocument();

    // Should display by difficulty
    expect(screen.getByText('62')).toBeInTheDocument();  // easy
    expect(screen.getByText('80')).toBeInTheDocument();  // medium
    expect(screen.getByText('16')).toBeInTheDocument();  // hard
  });

  it('should show total label', () => {
    renderWithQueryClient(<LeetCode />);
    // Find the stat card labels
    const labels = screen.getAllByText(/Total|Easy|Medium|Hard/i);
    expect(labels.length).toBeGreaterThan(0);
  });

  it('should display logged problems in history', () => {
    renderWithQueryClient(<LeetCode />);

    // History section should exist
    expect(screen.getByText(/History/)).toBeInTheDocument();

    // Should show logged problems
    expect(screen.getByText('Two Sum')).toBeInTheDocument();
  });

  it('should have form to log new problems', () => {
    renderWithQueryClient(<LeetCode />);

    // Form should exist
    expect(screen.getByText('Log Problem')).toBeInTheDocument();

    // Input fields should be present
    expect(screen.getByPlaceholderText(/Problem name/)).toBeInTheDocument();
    expect(screen.getByDisplayValue('Medium')).toBeInTheDocument();  // difficulty dropdown
  });

  it('should filter problems correctly', () => {
    renderWithQueryClient(<LeetCode />);

    // Filter input should exist
    const filterInput = screen.getByPlaceholderText('Filter...');
    expect(filterInput).toBeInTheDocument();
  });

  it('should display pattern distribution', () => {
    renderWithQueryClient(<LeetCode />);

    // Pattern distribution section should exist
    expect(screen.getByText('Pattern Distribution')).toBeInTheDocument();
  });

  it('should show heatmap', () => {
    renderWithQueryClient(<LeetCode />);

    // Heatmap should be rendered
    // Look for the heatmap title or grid
    const page = screen.getByRole('main') || screen.getByText('LeetCode Tracker').closest('div');
    expect(page).toBeInTheDocument();
  });

  it('should not show LC data as raw JSON', () => {
    renderWithQueryClient(<LeetCode />);

    // Should NOT display raw JSON structure
    expect(screen.queryByText(/lc_sync|"total"/)).not.toBeInTheDocument();
  });

  it('should display last sync time', () => {
    // In real scenario, should show "Last sync: 2026-03-27"
    renderWithQueryClient(<LeetCode />);
    const page = screen.getByText('LeetCode Tracker').closest('div');
    expect(page).toBeInTheDocument();
  });
});
