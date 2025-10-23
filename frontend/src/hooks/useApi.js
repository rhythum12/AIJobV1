/**
 * Custom React hook for API calls with loading states and error handling
 */

import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (apiCall, ...args) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiCall(...args);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { execute, loading, error };
};

export const useApiData = (apiCall, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiCall();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, dependencies);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
};

// Specific hooks for common API calls
export const useJobs = (params = {}) => {
  return useApiData(() => apiService.getJobs(params), [JSON.stringify(params)]);
};

export const useJobDetail = (jobId) => {
  return useApiData(() => apiService.getJobDetail(jobId), [jobId]);
};

export const useJobRecommendations = () => {
  return useApiData(() => apiService.getJobRecommendations());
};

export const useAppliedJobs = () => {
  return useApiData(() => apiService.getAppliedJobs());
};

export const useSavedJobs = () => {
  return useApiData(() => apiService.getSavedJobs());
};

export const useUserPreferences = () => {
  return useApiData(() => apiService.getUserPreferences());
};

export const useUserSettings = () => {
  return useApiData(() => apiService.getUserSettings());
};

export const useDashboardAnalytics = () => {
  return useApiData(() => apiService.getDashboardAnalytics());
};

export const useJobTrends = () => {
  return useApiData(() => apiService.getJobTrends());
};

export const useUserProfile = () => {
  return useApiData(() => apiService.getUserProfile());
};

