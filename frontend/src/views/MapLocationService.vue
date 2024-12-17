<template>
  <div id="container">

    <!-- 버튼 추가 -->
    <button @click="toggleMapComponent" class="show-map-btn">
      지도 보기
    </button>
    <div v-if="isMapVisible" class="map-container">
      <MapComponent v-if="locations.length > 0" :locations="locations"></MapComponent>
    </div>
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
      locations: [], // DB에서 위치 데이터를 저장할 배열
      isMapVisible: false, // 지도 표시 여부
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
    // MapComponent 표시/숨김을 토글하는 메서드
    toggleMapComponent() {
      this.isMapVisible = !this.isMapVisible;
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

/* 버튼 스타일 */
.show-map-btn {
  margin: 10px 0;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
}

.show-map-btn:hover {
  background-color: #45a049;
}

/* MapComponent를 화면 위쪽에 위치시키기 */
.map-container {
  position: absolute;
  top: 0; /* 화면 위쪽에 고정 */
  left: 0;
  width: 100%;
  height: 400px; /* 원하는 높이 설정 */
  background-color: white; /* 배경색 설정 */
  z-index: 10; /* 다른 요소 위에 표시되도록 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid #ddd;
}

</style>