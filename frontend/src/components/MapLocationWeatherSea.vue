

<template>
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <!-- Location Info -->
    <div v-if="seapostid_result">
      <p>
        기준 관측소 : <strong>{{ seapostid_result.obs_post_name }}</strong>
        와 <strong>{{ seapostid_result.distance.toFixed(3) }} km</strong> 차이
      </p>
    </div>

    <!-- Table Section -->
    <div v-if="seapostid_result" class="data-table">
      <h3>조수간만</h3>
      <div class="table-container" style="overflow-x: auto;">
        <table class="tide-pre-tab">
          <thead>
            <tr>
              <th><i class="fas fa-tag"></i> Name</th>
              <th><i class="fas fa-clock"></i> Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in seapostid_result.api_response.tideObsPreTab" :key="index">
              <td>{{ item.hl_code }}</td>
              <td>{{ item.tph_level }} / {{ item.tph_time }}</td>
            </tr>
          </tbody>
        </table>
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
  },
  data(){
    return {
      seapostid_result: null,
    }
  },
  mounted(){
    this.getWeatherData()
  },
  methods : {
    async getWeatherData() {
      console.log(`대상 낚시터 정보 (debug) :  ${ this.spotlocation }`)
      try {
        const [lat, lon] = this.spotlocation
        // fetchSeaPostidByCoordinates를 호출하여 데이터를 가져옴
        const response = await fetchSeaPostidByCoordinates(lat, lon);
        this.seapostid_result = response; // 결과 데이터를 weatherData에 저장
      } catch (error) {
        console.error('Error fetching weather data:', error);
      }

      console.log(this.seapostid_result.api_response)
    },
  },
};
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
</style>
