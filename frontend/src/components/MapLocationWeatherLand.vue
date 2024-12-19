<template>
  <div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else-if="weatherData" class="weather-info">
      <h3>현재 날씨 정보</h3>
      <div v-if="weatherData.weather">
        <div>기온: {{ weatherData.weather.temp }}°C</div>
        <div>습도: {{ weatherData.weather.humidity }}%</div>
        <div>풍속: {{ weatherData.weather.wind_speed }}m/s</div>
        <div>풍향: {{ weatherData.weather.wind_deg }}</div>
        <div>날씨: {{ weatherData.weather.weather }}</div>
        <div>일출: {{ weatherData.weather.sunrise }}</div>
        <div>일몰: {{ weatherData.weather.sunset }}</div>
      </div>
    </div>
    <div v-else class="loading">
      날씨 정보를 불러오는 중...
    </div>
  </div>
</template>

<script>
import { fetchWeatherByCoordinates } from '@/services/weatherService';

export default {
  props: {
    spotlocation: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      weatherData: null,
      error: null,
    };
  },
  watch: {
    spotlocation: {
      immediate: true,
      handler: 'fetchWeather',
    },
  },
  methods: {
    async fetchWeather() {
      if (this.spotlocation && this.spotlocation.length === 2) {
        try {
          this.error = null;
          this.weatherData = null;
          const [lat, lon] = this.spotlocation;
          this.weatherData = await fetchWeatherByCoordinates(lat, lon);
        } catch (error) {
          console.error('날씨 정보를 가져오는데 실패했습니다:', error);
          this.error = '날씨 정보를 가져오는데 실패했습니다.';
        }
      }
    },
  },
};
</script>

<style scoped>
.error-message {
  color: red;
  padding: 10px;
}

.loading {
  color: #666;
  padding: 10px;
}

.weather-info {
  padding: 10px;
}
</style>

  