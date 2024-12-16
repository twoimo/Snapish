<template>
  <div id="container">
    <MapComponent v-if="locations.length > 0" :locations="locations"></MapComponent>
  </div>
</template>

<script>
import axios from "@/axios";
import MapComponent from '@/components/MapComponent.vue'

export default {
  components: {
    // MapComponent 등록
    MapComponent,
  },
  data() {
    return {
      locations: [] // 위치 데이터를 저장할 배열
    };
  },
  mounted() {
    // 컴포넌트가 마운트된 후에 DB에서 위치 정보 가져오기
    this.fetchLocations();
  },
  methods: {
    // DB에서 위치 정보 가져오기, 주소 고정값 추후 해결
    async fetchLocations() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/map_fishing_spot');
        if (response.data.location) {
          this.locations = response.data.location;
          console.log(this.locations)
        }
      } catch (error) {
        console.error('Error fetching locations:', error);
      }
    },
  }
};
</script>

<style scoped>
#container {
    width: 100%;
    height: 100%;
    max-width: 1500px; /* 전체 컨테이너의 최대 너비 제한 */
    margin: 0 auto; /* 가운데 정렬 */
}
</style>