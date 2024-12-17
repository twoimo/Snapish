<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-4xl bg-white shadow-lg overflow-hidden parent-container">
      <main class="pb-20 px-4">
        <section class="mb-3 pt-6">
          <div id="top-map">
            <!-- 버튼 추가 -->
            <button @click="toggleMapComponent" class="show-map-btn">
              전체 위치
            </button>
            <div v-if="isMapVisible && locations.length > 0" class="map-container">
              <MapComponent :locations="locations"></MapComponent>
            </div>
          </div>

          <div id="searchbar">
            <input
              type="text"
              placeholder="원하는 낚시터 이름을 넣어주세요"
              key="search-input"
              class="form-control search-input"
            />
            <button @click="filteredList" class="search-btn">검색</button>
          </div>
        </section>
        
        <br>
        <section class="mb-3">
          <div id="middle-list"
              :style="{ 
                maxHeight: `${dynamicMaxHeight}px`, 
                overflowY: 'scroll', 
                paddingRight: '10px' 
              }"
            >
              <div>
                <ul class="location-list">
                  <li
                    v-for="(location, index) in locations"
                    :key="index"
                    class="location-item"
                    @click="showDetails(location)"
                  >
                    <h3><strong>낚시터 이름 {{ location.location_id }}</strong></h3>
                    <p>{{ location.address_ko }}</p>
                    <p><strong>설명:</strong> {{ location.details }}</p>
                  </li>
                </ul>
              </div>
          </div>

          <div
            class="slide-up-panel"
            :class="{ visible: isDetailsVisible }"
            @click.self="hideDetails"
          >
            <div v-if="selectedLocation" class="details-content">
              <h2>낚시터 상세 정보</h2>
              <p><strong>이름:</strong> {{ selectedLocation.location_id }}</p>
              <p><strong>주소:</strong> {{ selectedLocation.address_ko }}</p>
              <p><strong>설명:</strong> {{ selectedLocation.details }}</p>
              <button class="close-btn" @click="hideDetails">닫기</button>
            </div>
          </div>
        </section>
      </main>
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
      locations: [
          {
            address_ko: "부산광역시 강서구 낙동북로73번가길 200-5 (강동동)",
            latitude: "35.22365536",
            location_id: 1,
            longitude: "128.94041200"
          },
          {
            address_ko: "부산광역시 강서구 거가대로 2571 (천성동)",
            latitude: "35.02301425",
            location_id: 2,
            longitude: "128.80958840"
          },
          {
            address_ko: "부산광역시 해운대구 센텀중앙로 92 (우동)",
            latitude: "35.17469312",
            location_id: 3,
            longitude: "129.12848456"
          },
          {
            address_ko: "부산광역시 동래구 명륜로 36 (명륜동)",
            latitude: "35.23254261",
            location_id: 4,
            longitude: "129.07848452"
          },
          {
            address_ko: "부산광역시 부산진구 부전로 18 (부전동)",
            latitude: "35.15803907",
            location_id: 5,
            longitude: "129.05867288"
          },
          {
            address_ko: "부산광역시 남구 대연로 70 (대연동)",
            latitude: "35.13327401",
            location_id: 6,
            longitude: "129.10343523"
          },
          {
            address_ko: "부산광역시 수영구 민락로 29 (민락동)",
            latitude: "35.15482722",
            location_id: 7,
            longitude: "129.11678967"
          },
          {
            address_ko: "부산광역시 북구 화명동 1412-1",
            latitude: "35.25348399",
            location_id: 8,
            longitude: "128.99768325"
          },
          {
            address_ko: "부산광역시 기장군 기장읍 기장해안로 224",
            latitude: "35.23614581",
            location_id: 9,
            longitude: "129.21540468"
          },
          {
            address_ko: "부산광역시 영도구 동삼동 33-2",
            latitude: "35.07891852",
            location_id: 10,
            longitude: "129.07143514"
          },
          {
            address_ko: "부산광역시 사상구 괘법로 11 (괘법동)",
            latitude: "35.14562821",
            location_id: 11,
            longitude: "128.98267549"
          },
          {
            address_ko: "부산광역시 서구 충무대로 45 (충무동)",
            latitude: "35.09840523",
            location_id: 12,
            longitude: "129.02048471"
          },
          {
            address_ko: "부산광역시 동구 자갈치로 52 (초량동)",
            latitude: "35.10274374",
            location_id: 13,
            longitude: "129.03446256"
          },
          {
            address_ko: "부산광역시 강서구 유통단지로 105",
            latitude: "35.22249151",
            location_id: 14,
            longitude: "128.95124636"
          },
          {
            address_ko: "부산광역시 금정구 장전로 29 (장전동)",
            latitude: "35.23621192",
            location_id: 15,
            longitude: "129.10084519"
          },
          {
            address_ko: "부산광역시 해운대구 해운대해변로 32 (우동)",
            latitude: "35.16340188",
            location_id: 16,
            longitude: "129.16005009"
          },
          {
            address_ko: "부산광역시 사하구 하단로 220 (하단동)",
            latitude: "35.09821242",
            location_id: 17,
            longitude: "128.98687233"
          },
          {
            address_ko: "부산광역시 연제구 거제천로 11 (거제동)",
            latitude: "35.16848537",
            location_id: 18,
            longitude: "129.10638741"
          },
          {
            address_ko: "부산광역시 부산진구 중앙대로 788 (초읍동)",
            latitude: "35.15637522",
            location_id: 19,
            longitude: "129.05531704"
          },
          {
            address_ko: "부산광역시 남구 수영로 266 (수영동)",
            latitude: "35.14967222",
            location_id: 20,
            longitude: "129.12003458"
          }
        ], // DB에서 위치 데이터를 저장할 배열 - 임시 데이터 넣어둠
      isMapVisible: false, // 지도 표시 여부
      selectedLocation: null, // 선택된 낚시터 데이터
      isDetailsVisible: false, // 상세 정보 슬라이드 표시 여부
      dynamicMaxHeight: window.innerHeight,
      bodyScrollEnabled: true,
    };
  },
  mounted() {
    // 컴포넌트가 마운트된 후에 DB에서 위치 정보 가져오기
    // this.fetchLocations();
    // 페이지 드래그 방지 및 스크롤 숨김 설정
    this.updateMaxHeight(); // 초기 설정
    this.toggleBodyScroll(false);
    window.addEventListener("resize", this.updateMaxHeight); // 화면 크기 변화 감지
  },
  beforeUnmount() {
    // 컴포넌트 제거 시 스크롤 복원
    this.toggleBodyScroll(true);
    window.removeEventListener("resize", this.updateMaxHeight); // 이벤트 제거
  },
  methods: {
    updateMaxHeight() {
      const headerHeight = 240;
      const footerHeight = 100;
      const availableHeight = window.innerHeight - headerHeight - footerHeight;
      this.dynamicMaxHeight = Math.max(availableHeight, 300);
    },
    toggleBodyScroll(enable) {
      this.bodyScrollEnabled = enable;
      document.body.style.overflow = enable ? "auto" : "hidden";
    },
    showDetails(location) {
      this.selectedLocation = location;
      this.isDetailsVisible = true;
    },
    hideDetails() {
      this.selectedLocation = null;
      this.isDetailsVisible = false;
    },
    toggleMapComponent() {
      this.isMapVisible = !this.isMapVisible;
    },
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
.parent-container {
  position: relative; /* 부모 컨테이너 기준점 */
  overflow: hidden; /* 부모 밖으로 나가는 요소 숨김 */
}

#top-map {
  display: right;
  /* flex-direction: column; 요소들을 세로로 배치 */
  gap: 5px; /* 요소 간격 설정 */
  margin-bottom: 0; /* 아래 여백 제거 */
}

#searchbar {
  margin-top: 100px;
}

/* 버튼 스타일 */
.show-map-btn {
  margin: 0;
  padding: 8px 16px;
  background-color: #45a049;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 12px;
}

.show-map-btn:hover {
  background-color: #3d8e41;
}

/* 지도 컨테이너 */
.map-container {
  position: absolute;
  top: 75px;
  left: 0;
  width: 100%;
  height: 75%;
  background-color: white;
  z-index: 10;
  /* box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); */
  /* border-bottom: 1px solid #ddd; */
}

/* 리스트 스타일 */
.location-item {
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

/* 슬라이드 패널 */
.slide-up-panel {
  position: absolute; /* 부모 컨테이너 기준으로 배치 */
  bottom: 0;
  left: 0;
  width: 100%;
  height: 85%;
  background: white;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transform: translateY(100%);
  transition: transform 0.3s ease-in-out;
  z-index: 10;
}

.slide-up-panel.visible {
  transform: translateY(0);
}

.details-content {
  padding: 20px;
  overflow-y: auto;
  max-height: 100%;
}

.close-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #ff5a5a;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.close-btn:hover {
  background-color: #e04e4e;
}

/* 검색바 */
#searchbar {
  display: flex;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.search-btn {
  padding: 5px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.search-btn:hover {
  background-color: #0056b3;
}
</style>