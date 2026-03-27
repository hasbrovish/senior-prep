/**
 * Component tests for TodayPlan
 * Tests verify markdown is rendered correctly, not shown as raw text
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import TodayPlan from '../components/TodayPlan';

// Mock api calls
vi.mock('../api', () => ({
  api: {
    refreshDailyPlan: vi.fn(() => Promise.resolve({ plan: '# Refreshed' })),
  },
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

describe('TodayPlan Component', () => {
  it('should render without crashing', () => {
    renderWithQueryClient(<TodayPlan dailyPlan={{}} />);
    expect(screen.getByText('AI Daily Plan')).toBeInTheDocument();
  });

  it('should display markdown headings as actual headings, not raw text', () => {
    /**
     * CRITICAL TEST: This is what failed!
     * Daily plan was showing:
     *   "# Morning Session"
     * Instead of rendering as:
     *   [HEADING] Morning Session
     */
    const plan = `# Morning Session\n## DSA Practice\nStart with Two Pointers patterns`;

    renderWithQueryClient(<TodayPlan dailyPlan={{ plan }} />);

    // Should render as heading elements
    const h1 = screen.getByRole('heading', { level: 1 });
    expect(h1).toHaveTextContent('Morning Session');

    const h2 = screen.getByRole('heading', { level: 2 });
    expect(h2).toHaveTextContent('DSA Practice');

    // Should NOT show raw markdown syntax
    expect(screen.queryByText(/^# Morning Session/)).not.toBeInTheDocument();
    expect(screen.queryByText(/^## DSA Practice/)).not.toBeInTheDocument();
  });

  it('should render markdown bullets as list items', () => {
    const plan = `# Tasks\n- Two Pointers practice\n- Review sliding window`;

    renderWithQueryClient(<TodayPlan dailyPlan={{ plan }} />);

    // Should render as list
    const listItems = screen.getAllByRole('listitem');
    expect(listItems).toHaveLength(2);
    expect(listItems[0]).toHaveTextContent('Two Pointers practice');
    expect(listItems[1]).toHaveTextContent('Review sliding window');

    // Should NOT show raw markdown dashes
    expect(screen.queryByText('- Two Pointers practice')).not.toBeInTheDocument();
  });

  it('should render bold text with emphasis', () => {
    const plan = `# Plan\n**Important:** Start with DSA`;

    renderWithQueryClient(<TodayPlan dailyPlan={{ plan }} />);

    // Bold text should be rendered
    const strong = screen.getByText('Important:');
    expect(strong.tagName.toLowerCase()).toBe('strong');
  });

  it('should render inline code with styling', () => {
    const plan = `# Learning\nStudy \`HashMap\` implementation in Java`;

    renderWithQueryClient(<TodayPlan dailyPlan={{ plan }} />);

    // Code should be rendered
    expect(screen.getByText('HashMap')).toBeInTheDocument();
    // Code should have styling class
    const codeElement = screen.getByText('HashMap').closest('code');
    expect(codeElement).toBeInTheDocument();
  });

  it('should handle empty plan gracefully', () => {
    renderWithQueryClient(<TodayPlan dailyPlan={{}} />);

    expect(screen.getByText(/No plan generated yet/)).toBeInTheDocument();
  });

  it('should show expanded/collapsed view', () => {
    const longPlan = `# Section 1\nContent 1\n# Section 2\nContent 2\n# Section 3\nContent 3\n# Section 4\nContent 4\n# Section 5\nContent 5\n# Section 6\nContent 6\n# Section 7\nContent 7`;

    const { rerender } = renderWithQueryClient(
      <TodayPlan dailyPlan={{ plan: longPlan }} />
    );

    // Initially should show preview
    expect(screen.getByText('Show more')).toBeInTheDocument();
  });

  it('should display "cached" label when plan is cached', () => {
    const plan = `# Plan`;

    renderWithQueryClient(<TodayPlan dailyPlan={{ plan, cached: true }} />);

    expect(screen.getByText('cached')).toBeInTheDocument();
  });
});
