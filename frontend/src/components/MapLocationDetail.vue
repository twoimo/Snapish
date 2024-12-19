<template>
  <div class="fixed inset-0 z-50 flex justify-center max-w-md mx-auto">
    <!-- 배경 오버레이 -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')"></div>
    
    <!-- 상세 정보 컨테이너 -->
    <div class="relative w-full bg-white h-full overflow-y-auto">
      <!-- 헤더 영역 -->
      <header class="sticky top-0 bg-white z-10 px-4 py-3 border-b">
        <div class="flex justify-between items-center">
          <h1 class="text-xl font-bold">{{ location.name }}</h1>
          <button class="close-btn" @click="$emit('close')">
            <XIcon class="w-6 h-6" />
          </button>
        </div>
      </header>

      <!-- 기본 정보 영역 -->
      <section class="info-section p-4">
        <div class="facilities-container space-y-6">
          <!-- 주소 섹션 -->
          <div class="facility-section">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <MapPinIcon class="w-5 h-5" /> 
              위치
            </h3>
            <div class="facility-content mt-2">
              {{ location.address_road || location.address_land }}
            </div>
          </div>

          <!-- 이용료 섹션 -->
          <div class="facility-section" v-if="location.usage_fee">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <WalletIcon class="w-5 h-5" />
              이용료
            </h3>
            <div class="facility-content mt-2">
              {{ location.usage_fee }}
            </div>
          </div>

          <!-- 주요어종 섹션 -->
          <div class="facility-section" v-if="location.main_fish_species">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <FishIcon class="w-5 h-5" />
              주요 어종
            </h3>
            <div class="facility-tags mt-2">
              <span v-for="species in location.main_fish_species.split(/[+,]/).filter(Boolean)"
                    :key="species"
                    class="inline-block px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm mr-2 mb-2">
                {{ species.trim() }}
              </span>
            </div>
          </div>

          <!-- 안전시설 섹션 -->
          <div class="facility-section" v-if="location.safety_facilities">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <ShieldCheckIcon class="w-5 h-5" />
              안전 시설
            </h3>
            <div class="facility-tags mt-2">
              <span v-for="facility in location.safety_facilities.split(/[+*]/).filter(Boolean)"
                    :key="facility"
                    class="inline-block px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm mr-2 mb-2">
                {{ facility.trim() }}
              </span>
            </div>
          </div>

          <!-- 편의시설 섹션 -->
          <div class="facility-section" v-if="location.convenience_facilities">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <Coffee class="w-5 h-5" />
              편의시설
            </h3>
            <div class="facility-tags mt-2">
              <span v-for="facility in location.convenience_facilities.split(/[+*]/).filter(Boolean)"
                    :key="facility"
                    class="inline-block px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm mr-2 mb-2">
                {{ facility.trim() }}
              </span>
            </div>
          </div>

          <!-- 화장실 섹션 -->
          <div class="facility-section" v-if="location.toilet_facilities">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <Bath class="w-5 h-5" />
              화장실
            </h3>
            <div class="facility-tags mt-2">
              <span v-for="facility in location.toilet_facilities.split(/[+*]/).filter(Boolean)"
                    :key="facility"
                    class="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 rounded-full text-sm mr-2 mb-2">
                {{ facility.trim() }}
              </span>
            </div>
          </div>

          <!-- 날씨 정보 영역 -->
          <section class="weather-section facility-section">
            <h3 class="flex items-center gap-2 text-lg font-semibold">
              <CloudIcon class="w-5 h-5" />
              날씨 정보
            </h3>
            <div class="mt-2">
              <div v-if="location.type === '바다'">
                <MapLocationWeatherSea :spotlocation="[location.latitude, location.longitude]" />
              </div>
              <div v-if="location.type === '저수지'">
                <MapLocationWeatherLand :spotlocation="[location.latitude, location.longitude]" />
              </div>
            </div>
          </section>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { 
  XIcon, 
  MapPinIcon, 
  WalletIcon, 
  FishIcon, 
  ShieldCheckIcon,
  Coffee,
  Bath,
  CloudIcon
} from 'lucide-vue-next';
import MapLocationWeatherSea from './MapLocationWeatherSea.vue';
import MapLocationWeatherLand from './MapLocationWeatherLand.vue';

defineProps({
  location: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
/* 이전 스타일 유지 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E0 transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #CBD5E0;
  border-radius: 3px;
}

.facility-tags span {
  transition: all 0.2s ease;
}

.facility-tags span:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.facility-section:not(:last-child) {
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 1.5rem;
}
</style>