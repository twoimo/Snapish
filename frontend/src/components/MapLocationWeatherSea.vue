

<template>
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <!-- Location Info -->
    <div v-if="seapostid_result">
      <p style="font-size: 0.7rem;">
        출처 : 바다누리 해양정보 서비스
      </p>
      <p style="font-size: 0.8rem;">
        기준 관측소 : <strong>{{ seapostid_result.obs_post_name }}</strong>
        와 <strong>{{ seapostid_result.distance.toFixed(3) }} km</strong> 차이
      </p>
    </div>
    <!-- Table Section -->
    <div v-if="seapostid_result" class="data-table">
      <div class="table-container" style="display: flex; gap: 2rem;">
        <!-- Left Space (Empty) -->

        <div style="flex: 1">
          <h3>조수간만</h3>
          <table class="tide-pre-tab">
            <thead>
              <tr>
                <th colspan="3">{{ getCurrentDate() }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in seapostid_result.api_response.tideObsPreTab" :key="index">
                <td>{{ item.tph_time.split(' ')[1].slice(0, 5) }}</td>
                <td :class="{ 'high-tide': item.hl_code === '고조', 'low-tide': item.hl_code === '저조' }">
                  {{ item.hl_code }}
                </td>
                <td>{{ item.tph_level }} cm</td>
              </tr>
            </tbody>
          </table>
        </div>


        <!-- Right Table -->
        <div style="flex: 1">
          <h3>현재 관측</h3>
          <table class="tide-pre-tab">
            <thead>
              <tr>
                <th colspan="2">{{ seapostid_result.api_response.tideObsRecent.record_time.split(' ')[1].slice(0, 5) }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>수온</td>
                <td>{{ seapostid_result.api_response.tideObsRecent.water_temp }}°C</td>
              </tr>
              <tr>
                <td>기온</td>
                <td>{{ seapostid_result.api_response.tideObsRecent.air_temp }}°C</td>
              </tr>
              <tr>
                <td>기압</td>
                <td>{{ seapostid_result.api_response.tideObsRecent.air_press }}hPa</td>
              </tr>
              <tr>
                <td>조위</td>
                <td>{{ seapostid_result.api_response.tideObsRecent.tide_level }}cm</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
// import axios from '@/axios';
import { fetchSeaPostidByCoordinates } from '../services/locationService';

export default {
  props: {
    spotlocation: {
      type: Array,
      required: true,
    },
    weatherData: Object
  },
  emits: ['update:weatherData'],
  data(){
    return {
      seapostid_result: null,
    }
  },
  mounted(){
    this.fetchWeatherData()
  },
  methods: {
    async fetchWeatherData() {
      if (this.weatherData) {
        // 이미 데이터가 있으면 API 호출하지 않음
        this.seapostid_result = this.weatherData;
        return;
      }

      console.log(`대상 낚시터 정보 (debug) : ${this.spotlocation}`);
      try {
        const [lat, lon] = this.spotlocation;
        // fetchSeaPostidByCoordinates를 호출하여 데이터를 가져옴
        const response = await fetchSeaPostidByCoordinates(lat, lon);
        this.seapostid_result = response;
        // 결과 데이터를 부모 컴포넌트에 전달
        this.$emit('update:weatherData', response);
      } catch (error) {
        console.error('Error fetching weather data:', error);
      }

      if (this.seapostid_result) {
        console.log(this.seapostid_result.api_response);
      }
    },

    getCurrentDate() {
      const now = new Date();
      return now.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
}
</script>


<style scoped>
.data-table {
  margin: 1rem 0;
}

.tide-pre-tab {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
}

.tide-pre-tab th, .tide-pre-tab td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.tide-pre-tab th {
  background-color: #f4f4f4;
  font-weight: bold;
  text-transform: uppercase;
}

.tide-pre-tab tr:nth-child(even) {
  background-color: #f9f9f9;
}

.tide-pre-tab tr:hover {
  background-color: #f1f1f1;
}

.table-container {
  max-width: 100%;
  overflow-x: auto;
}

h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

p {
  font-size: 1rem;
  color: #555;
}

.high-tide {
  background-color: #e6f3ff;  /* 파란 배경 */
}

.low-tide {
  background-color: #ffe6e6;  /* 붉은 배경 */
}

.tide-pre-tab th {
  background-color: #f4f4f4;
  font-weight: bold;
  text-align: center;
  padding: 10px;
}
</style>
