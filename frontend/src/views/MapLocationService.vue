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
            <input v-model="searchQuery" type="text" placeholder="원하는 낚시터 이름을 넣어주세요" key="search-input"
              class="form-control search-input" @input="filterLocations" />
          </div>
        </section>
        <br />

        <section class="mb-3">
          <div id="middle-list" :style="{
            maxHeight: `${dynamicMaxHeight}px`,
            overflowY: 'scroll',
            paddingRight: '10px'
          }">
            <div>
              <ul class="location-list">
                <li v-for="(location, index) in filteredLocations" :key="index" class="location-item"
                  @click="showDetails(location)">
                  <h3><strong>{{ location.name }}</strong></h3>
                  <p><strong>도로명 주소: </strong> {{ location.adrees_road }}</p>
                  <p><strong>지번 주소: </strong> {{ location.address_land }}</p>
                  <p><strong>낚시터 타입:</strong> {{ location.type }}</p>
                </li>
              </ul>
            </div>
          </div>

          <div class="slide-up-panel" :class="{ visible: isDetailsVisible }" @click.self="hideDetails">
            <MapLocationDetail v-if="isDetailsVisible" :location="selectedLocation" @close="hideDetails" />
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";
import MapComponent from '@/components/MapComponent.vue'
import MapLocationDetail from '@/components/MapLocationDetail.vue'

export default {
  components: {
    MapComponent,
    MapLocationDetail,
  },
  data() {
    return {
      searchQuery: "", // 검색 입력값
      filteredLocations: [],
      locations: [
  {
    fishing_place_id: 1,
    name: "착한붕어 낚시카페",
    type: "기타",
    adrees_road: "서울특별시 종로구 대학로8가길 52, 지하1층 (동숭동)",
    address_land: "서울특별시 종로구 동숭동 1-48 지하1층",
    Latitude: 37.582964,
    Longitude: 127.002648,
    phone_number: "02-741-1733",
    main_fish_species: "붕어",
    usage_fee: "1시간(성인:10천원, 초,중,고 학생:9천원)",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  },
  {
    fishing_place_id: 2,
    name: "붕어의 신",
    type: "기타",
    adrees_road: "서울특별시 양천구 신월로 321",
    address_land: "서울특별시 양천구 신정동 977-16",
    Latitude: 37.5217038,
    Longitude: 126.8565155,
    phone_number: "02-2603-2266",
    main_fish_species: "붕어",
    usage_fee: "1시간(남 10천, 여9천, 커플18천, 청소년 7천, 아동 5천)  1시간 추가시 요금 발생",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  },
  {
    fishing_place_id: 3,
    name: "가자실내낚시터",
    type: "기타",
    adrees_road: "서울특별시 양천구 지양로 34",
    address_land: "서울특별시 양천구 신월동 991-12",
    Latitude: 37.519435,
    Longitude: 126.8363231,
    phone_number: "02-2691-2733",
    main_fish_species: "붕어",
    usage_fee: "1시간(남 10천, 여10천, 아동 8천)",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  },
  {
    fishing_place_id: 4,
    name: "입큰붕어낚시카페",
    type: "기타",
    adrees_road: "서울특별시 은평구 은평로 101, 지하1층 (응암동)",
    address_land: "서울특별시 은평구 응암동 90-14",
    Latitude: "",
    Longitude: "",
    phone_number: "",
    main_fish_species: "-",
    usage_fee: "10,000원/시간",
    safety_facilities: "-",
    convenience_facilities: "-"
  },
  {
    fishing_place_id: 5,
    name: "잉어킹낚시카페",
    type: "기타",
    adrees_road: "서울특별시 은평구 연서로26길 8, 지하1층 (대조동)",
    address_land: "서울특별시 은평구 대조동 200-2",
    Latitude: "",
    Longitude: "",
    phone_number: "",
    main_fish_species: "민물고기",
    usage_fee: "10,000원/시간",
    safety_facilities: "구급함 구비",
    convenience_facilities: "음료 자판대"
  },
  {
    fishing_place_id: 6,
    name: "용곡낚시터",
    type: "저수지",
    adrees_road: "충청북도 청주시 상당구 미원면 미원초정로 685-26",
    address_land: "충청북도 청주시 상당구 미원면 종암리 449",
    Latitude: 36.683613,
    Longitude: 127.636857,
    phone_number: "",
    main_fish_species: "붕어+잉어+향어",
    usage_fee: "20000원",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  },
  {
    fishing_place_id: 7,
    name: "황청낚시터",
    type: "저수지",
    adrees_road: "충청북도 청주시 상당구 남일면 황청리길 119",
    address_land: "충청북도 청주시 상당구 남일면 황청리 163",
    Latitude: 36.594752,
    Longitude: 127.555039,
    phone_number: "",
    main_fish_species: "붕어+잉어+향어",
    usage_fee: "25000원",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  },
  {
    fishing_place_id: 8,
    name: "한계리낚시터",
    type: "저수지",
    adrees_road: "충청북도 청주시 상당구 가덕면 한계1길 170",
    address_land: "충청북도 청주시 상당구 가덕면 한계리 294-1",
    Latitude: 36.606594,
    Longitude: 127.562466,
    phone_number: "",
    main_fish_species: "붕어+잉어+향어",
    usage_fee: "30000원",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  },
  {
    fishing_place_id: 9,
    name: "중리낚시터",
    type: "저수지",
    adrees_road: "충청북도 청주시 상당구 미원면 쌍이운교로 262",
    address_land: "충청북도 청주시 상당구 미원면 중리 316-1",
    Latitude: 36.669118,
    Longitude: 127.665454,
    phone_number: "",
    main_fish_species: "붕어+잉어+향어",
    usage_fee: "25000원",
    safety_facilities: "구명부환+소화기+구급약품+전기설비",
    convenience_facilities: "화장실+쓰레기통"
  }], // DB에서 위치 데이터를 저장할 배열 - 임시 데이터 넣어둠
      isMapVisible: false, // 지도 표시 여부
      selectedLocation: null, // 선택된 낚시터 데이터
      isDetailsVisible: false, // 상세 정보 슬라이드 표시 여부
      dynamicMaxHeight: window.innerHeight,
      bodyScrollEnabled: true,
    };
  },
  mounted() {
    // this.fetchLocations();     // 컴포넌트가 마운트된 후에 DB에서 위치 정보 가져오기
    this.filteredLocations = this.locations; // 초기에는 모든 locations를 표시
    this.updateMaxHeight();     // 페이지 드래그 방지 및 스크롤 숨김 설정
    this.toggleBodyScroll(false);     // 페이지 드래그 방지 및 스크롤 숨김 설정
    window.addEventListener("resize", this.updateMaxHeight); // 화면 크기 변화 감지
  },
  beforeUnmount() {
    // 컴포넌트 제거 시 스크롤 복원
    this.toggleBodyScroll(true);
    window.removeEventListener("resize", this.updateMaxHeight); // 이벤트 제거
  },
  methods: {
    filterLocations() {
      const query = this.searchQuery.trim();
      if (query === "") {
        this.filteredLocations = [...this.locations]; // 모든 데이터 표시
      } else {
        this.filteredLocations = this.locations.filter((location) =>
          String(location.name || "").includes(query)
        );
      }
    },
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
          const locationDict = response.data.location; // 딕셔너리
          this.locations = Object.values(locationDict); // 딕셔너리 값을 배열로 변환
          this.filteredLocations = [...this.locations]; // 초기 필터링 배열 설정
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
  position: relative;
  /* 부모 컨테이너 기준점 */
  overflow: hidden;
  /* 부모 밖으로 나가는 요소 숨김 */
}

#top-map {
  display: right;
  /* flex-direction: column; 요소들을 세로로 배치 */
  gap: 5px;
  /* 요소 간격 설정 */
  margin-bottom: 0;
  /* 아래 여백 제거 */
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
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 90%;
  background: white;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transform: translateY(100%);
  /* 기본 상태 */
  transition: transform 0.3s ease-in-out;
  /* 애니메이션 추가 */
  z-index: 10;
}

.slide-up-panel.visible {
  transform: translateY(0);
  /* 보이는 상태 */
}

.details-content {
  padding: 20px;
  overflow-y: auto;
  max-height: 100%;
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