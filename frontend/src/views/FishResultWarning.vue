<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg">
      <header class="fixed top-0 left-0 right-0 bg-white px-4 py-3 flex items-center justify-between border-b z-15 max-w-md mx-auto">
        <div class="flex items-center">
          <button class="mr-2" @click="goBack">
            <ChevronLeftIcon class="w-6 h-6" />
          </button>
          <h1 class="text-xl font-bold">물고기 판별 결과</h1>
        </div>
        <div class="flex items-center gap-4">
          <button class="p-2">
            <BellIcon class="w-6 h-6" />
          </button>
          <button class="p-2">
            <Settings2Icon class="w-6 h-6" />
          </button>
        </div>
      </header>

      <main class="pb-20 px-4">
        <!-- 로딩 상태 -->
        <div v-if="isLoading" class="flex justify-center items-center h-64">
          <span class="text-gray-500">로딩 중...</span>
        </div>

        <!-- 에러 메시지 -->
        <div v-if="errorMessage" class="p-4 bg-red-100 text-red-600 rounded-lg">
          {{ errorMessage }}
        </div>

        <!-- 업로드된 물고기 이미지 표시 -->
        <div v-if="!isLoading && !errorMessage" class="mt-4 bg-gray-200 rounded-lg p-4 flex justify-center">
          <img :src="imageSource" alt="물고기 사진" class="max-w-full max-h-96 object-contain cursor-pointer" @click="openImagePopup(imageSource)" />
        </div>
        
        <div v-if="fishName" class="mt-6 bg-red-50 rounded-lg p-4 border-2 border-red-500">
          <div class="flex items-center mb-2">
            <AlertTriangleIcon class="w-6 h-6 text-red-500 mr-2" />
            <h2 class="text-lg font-bold text-red-700">주의: 현재 포획 금지 어종</h2>
          </div>
          <p class="text-red-600 mt-2">이 물고기는 <strong>{{ fishName }}</strong>입니다.
                <span class="text-sm text-red-500">(신뢰도: {{ (confidence * 100).toFixed(2) }}%)</span>
          </p>
          <p class="text-red-600 mt-2">금어기 기간: {{ prohibitedDates }}</p>
        </div>

        <div class="mt-6 bg-gray-50 rounded-lg p-4">
          <h2 class="text-xl font-bold mb-2">{{ fishName }}</h2>
          <p class="text-gray-600">학명: {{ scientificName }}</p>
          <p class="mt-2 text-gray-700">{{ fishDescription }}</p>
        </div>

        <div class="mt-6 bg-yellow-50 rounded-lg p-4">
          <h3 class="font-bold text-yellow-700 mb-2">포획 제한 이유</h3>
          <ul class="list-disc list-inside text-yellow-800">
            <li>ChatGPT로 생성된 포획 제한 이유</li>
          </ul>
        </div>

        <div class="mt-6 space-y-3">
          <button class="w-full bg-blue-500 text-white py-3 px-4 rounded-lg flex items-center justify-center">
            <InfoIcon class="w-5 h-5 mr-2" />
            <span>더 자세한 정보 보기</span>
          </button>
          <button class="w-full bg-green-500 text-white py-3 px-4 rounded-lg flex items-center justify-center" @click="shareResult">
            <Share2Icon class="w-5 h-5 mr-2" />
            <span>이 정보 공유하기</span>
          </button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ChevronLeftIcon, AlertTriangleIcon, BellIcon, Settings2Icon, InfoIcon, Share2Icon } from 'lucide-vue-next';
import store from '../store';

const route = useRoute();
const detections = JSON.parse(decodeURIComponent(route.query.detections || '[]')); // detections 결과 가져오기

const confidence = detections.length > 0 ? detections[0].confidence : 0; // 첫 번째 감지 결과의 신뢰도
const fishName = detections.length > 0 ? detections[0].label : '알 수 없는 물고기'; // 첫 번째 감지 결과의 라벨
const prohibitedDates = route.query.prohibitedDates || '알 수 없음'; // 금어기 기간
const scientificName = ref('ChatGPT로 생성된 학명'); // 필요에 따라 학명 정보를 추가하세요.
const fishDescription = ref('ChatGPT로 생성된 물고기 설명'); // 필요에 따라 물고기 설명을 추가하세요.

const imageUrl = ref('');
const imageBase64 = ref('');

// Define backend base URL
const BACKEND_BASE_URL = 'http://localhost:5000';

const goBack = () => {
  window.history.back();
};

const shareResult = () => {
  // 공유 기능 구현
  alert('결과를 공유합니다.');
};

// onMounted 훅을 사용하여 DOM 요소가 마운트된 후에 접근
onMounted(() => {
  console.log('컴포넌트가 마운트되었습니다.');
  
  // 이미지 URL과 Base64 데이터를 라우트 쿼리에서 가져오기
  imageUrl.value = route.query.imageUrl || '';
  imageBase64.value = route.query.imageBase64 || '';
});

const imageSource = computed(() => {
  if (imageUrl.value && store.state.isAuthenticated) {
    return `${BACKEND_BASE_URL}/uploads/${imageUrl.value}`; // Updated to backend URL
  } else if (imageBase64.value) {
    return `data:image/jpeg;base64,${imageBase64.value}`;
  }
  return '/placeholder.svg';
});
</script>

<style scoped>
.uploaded-image img {
  max-width: 100%;
  height: auto;
  object-fit: cover;
}

.fixed {
  position: fixed;
}

.absolute {
  position: absolute;
}

/* Ensure pop-up images are displayed correctly */
.object-contain {
  object-fit: contain;
}

header {
  position: fixed;
  top: 0;
  z-index: 10; /* 헤더가 다른 요소 위에 오도록 설정 */
}
</style>
