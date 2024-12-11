import { createStore } from "vuex";
import { getCurrentLocation } from "../services/locationService";
import { fetchWeatherByCoordinates } from "../services/weatherService";

export default createStore({
  state: {
    weather: JSON.parse(localStorage.getItem("weather")) || null, // 캐시된 정보가 있으면 불러오기
    loading: false,
    error: null,
  },
  mutations: {
    setWeather(state, weather) {
      state.weather = weather;
      localStorage.setItem("weather", JSON.stringify(weather)); // 캐시 저장
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
      // weather가 null인 경우에만 API 요청
      if (state.weather === null) {
        commit("setLoading", true);
        commit("setError", null);

        try {
          const { latitude, longitude } = await getCurrentLocation();
          const weatherData = await fetchWeatherByCoordinates(latitude, longitude);
          
          if (weatherData) {
            commit("setWeather", weatherData); // 데이터를 상태에 저장
          } else {
            commit("setError", "No weather data found.");
          }
        } catch (error) {
          const defaultLat = 37.5665; // 서울
          const defaultLon = 126.9780;
          try {
            const weatherData = await fetchWeatherByCoordinates(defaultLat, defaultLon);
            if (weatherData) {
              commit("setWeather", weatherData); // 서울 데이터 저장
            } else {
              commit("setError", "No fallback weather data found.");
            }
          } catch (fallbackError) {
            commit("setError", "Failed to fetch weather data.");
          }
        } finally {
          commit("setLoading", false);
        }
      }
    },
  },
});