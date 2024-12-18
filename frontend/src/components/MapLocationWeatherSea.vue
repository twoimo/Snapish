<template>
  <div>
    <div>

      {{ spotlocation }}

      {{  seapostid }}

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
      seapostid: null,
    }
  },
  mounted(){
    this.getWeatherData()
  },
  methods : {
    async getWeatherData() {
      try {
        const [lat, lon] = this.spotlocation
        // fetchSeaPostidByCoordinates를 호출하여 데이터를 가져옴
        const response = await fetchSeaPostidByCoordinates(lat, lon);
        this.seapostid = response; // 결과 데이터를 weatherData에 저장
      } catch (error) {
        console.error('Error fetching weather data:', error);
      }
    },
  },
};
</script>