import { useState, useEffect } from 'react';

export function createMockStream<T>(
  initialData: T[],
  updateFn: (data: T[]) => T[],
  intervalMs: number = 1000,
  callback: (data: T[]) => void
) {
  let currentData = [...initialData];
  
  const intervalId = setInterval(() => {
    currentData = updateFn(currentData);
    callback([...currentData]);
  }, intervalMs);

  return () => clearInterval(intervalId);
}

// Helper to fluctuate a number by a percentage
export function fluctuate(value: number, maxPercentChange: number = 0.05): number {
  const change = value * maxPercentChange * (Math.random() * 2 - 1);
  return Math.max(0, value + change);
}

// Helper to fluctuate an integer
export function fluctuateInt(value: number, maxPercentChange: number = 0.05): number {
  return Math.round(fluctuate(value, maxPercentChange));
}

// React Hook for easy integration
export function useMockStream<T>(
  initialData: T[],
  updateFn: (data: T[]) => T[],
  intervalMs: number = 2000
): T[] {
  const [data, setData] = useState<T[]>(initialData);

  useEffect(() => {
    const cleanup = createMockStream(initialData, updateFn, intervalMs, setData);
    return cleanup;
  }, [initialData, updateFn, intervalMs]);

  return data;
}

