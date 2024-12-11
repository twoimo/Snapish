<template>
    <div>
      <div v-if="loading">정보를 가져오는 중...</div>
      <div v-if="weather">
        <h2>{{ weather.location.name }}</h2>
        <p>Temperature: {{ weather.current.temp_c }}°C</p>
        <p>Condition: {{ weather.current.condition.text }}</p>
      </div>
      <div v-if="error">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import { mapState } from "vuex";
  import { getCurrentLocation } from "../services/locationService";
  import { fetchWeatherByCoordinates } from "../services/weatherService";
  
  export default {
    computed: {
    ...mapState(["weather", "loading", "error"]),
    },
    mounted() {
    if (!this.weather) {
      this.$store.dispatch("fetchWeather");
      }
    },

    methods: {
      async loadWeatherData() {
        this.loading = true;
        this.error = null;
  
        try {
          const { latitude, longitude } = await getCurrentLocation();
          const weatherData = await fetchWeatherByCoordinates(latitude, longitude);
          if (weatherData.error) {
            this.error = weatherData.error;
          } else {
            this.weather = weatherData;
          }
        } catch (error) {
          this.error = error;
          // 기본 위치 사용 (서울)
          await this.loadFallbackWeather();
        } finally {
          this.loading = false;
        }
      },
      async loadFallbackWeather() {
        const defaultLat = 37.5665; // 서울 위도
        const defaultLon = 126.9780; // 서울 경도
        try {
          const weatherData = await fetchWeatherByCoordinates(defaultLat, defaultLon);
          if (weatherData.error) {
            this.error = weatherData.error;
          } else {
            this.weather = weatherData;
          }
        } catch (error) {
          this.error = "Failed to fetch fallback weather data.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 스타일은 선택 사항 */
  </style>
  