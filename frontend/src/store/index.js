import { createStore } from "vuex";
import { getCurrentLocation } from "../services/locationService";
import { fetchWeatherByCoordinates } from "../services/weatherService";

export default createStore({
  state: {
    weather: JSON.parse(localStorage.getItem("weather")) || null,
    loading: false,
    error: null,
  },
  mutations: {
    setWeather(state, weather) {
      state.weather = weather;
      localStorage.setItem("weather", JSON.stringify(weather));
    },
    setLoading(state, isLoading) {
      state.loading = isLoading;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    async fetchWeather({ commit, state }) {
      // 캐싱된 데이터가 있다면 바로 반환
      if (state.weather) return;

      commit("setLoading", true);
      commit("setError", null);

      try {
        const { latitude, longitude } = await getCurrentLocation();
        const weatherData = await fetchWeatherByCoordinates(latitude, longitude);
        commit("setWeather", weatherData);
      } catch (error) {
        // 기본 위치 (서울)로 대체
        const defaultLat = 37.5665;
        const defaultLon = 126.9780;
        try {
          const weatherData = await fetchWeatherByCoordinates(defaultLat, defaultLon);
          commit("setWeather", weatherData);
        } catch (fallbackError) {
          commit("setError", "Failed to fetch weather data.");
        }
      } finally {
        commit("setLoading", false);
      }
    },
  },
});
