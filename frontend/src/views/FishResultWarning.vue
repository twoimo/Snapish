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
          <span class="text-gray-500">Loading...</span>
        </div>

        <!-- 에러 메시지 -->
        <div v-if="errorMessage" class="p-4 bg-red-100 text-red-600 rounded-lg">
          {{ errorMessage }}
        </div>

        <!-- 업로드된 물고기 이미지 표시 -->
        <div v-if="!isLoading && !errorMessage" class="mt-4 bg-gray-200 rounded-lg p-4 flex justify-center">
          <img :src="imageSource" alt="물고기 사진" class="max-w-full max-h-96 object-contain cursor-pointer" @click="openImagePopup(imageSource)" />
        </div>
        
        <!-- AI 판별 결과 -->
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

        <!-- 공유하기 버튼 -->
        <div v-if="!isLoading && !errorMessage" class="mt-6">
          <button class="w-full bg-green-500 text-white py-3 px-4 rounded-lg flex items-center justify-center"
            @click="shareResult">
            <Share2Icon class="w-5 h-5 mr-2" />
            <span>공유하기</span>
          </button>
        </div>

        <!-- 내가 잡은 물고기 페이지로 이동 버튼 -->
        <div v-if="!isLoading && !errorMessage" class="mt-4">
          <button class="w-full bg-blue-500 text-white py-3 px-4 rounded-lg flex items-center justify-center"
            @click="navigateToCatches">
            <InfoIcon class="w-5 h-5 mr-2" />
            <span>내가 잡은 물고기 리스트 보기</span>
          </button>
        </div>
      </main>

      <!-- 이미지 팝업 모달 -->
      <div v-if="isImagePopupVisible" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div class="bg-white p-4 rounded-lg relative">
          <button class="absolute top-2 right-2" @click="isImagePopupVisible = false">
            &times;
          </button>
          <img :src="popupImageUrl" alt="확대된 이미지" class="max-w-full max-h-full" />
        </div>
      </div>

      <!-- 공유 모달 -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div class="bg-white p-6 rounded-lg relative">
          <button class="absolute top-2 right-2" @click="showModal = false">
            &times;
          </button>
          <h2 class="text-xl font-bold mb-4">공유하기</h2>
          <!-- 공유 옵션들 -->
          <button class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg mb-2">Facebook으로 공유</button>
          <button class="w-full bg-blue-700 text-white py-2 px-4 rounded-lg mb-2">Twitter로 공유</button>
          <button class="w-full bg-green-500 text-white py-2 px-4 rounded-lg">링크 복사</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ChevronLeftIcon, AlertTriangleIcon, BellIcon, Settings2Icon, InfoIcon, Share2Icon } from 'lucide-vue-next';
import { useStore } from 'vuex'; // Updated to use useStore for reactivity

const store = useStore(); // Use the Vuex store with reactivity

const route = useRoute();
const router = useRouter();

const detections = JSON.parse(decodeURIComponent(route.query.detections || '[]')); // detections 결과 가져오기

const confidence = detections.length > 0 ? detections[0].confidence : 0; // 첫 번째 감지 결과의 신뢰도
const fishName = detections.length > 0 ? detections[0].label : '알 수 없는 물고기'; // 첫 번째 감지 결과의 라벨
const prohibitedDates = route.query.prohibitedDates || '알 수 없음'; // 금어기 기간
const scientificName = ref('ChatGPT로 생성된 학명'); // 필요에 따라 학명 정보를 추가하세요.
const fishDescription = ref('ChatGPT로 생성된 물고기 설명'); // 필요에 따라 물고기 설명을 추가하세요.
const isLoading = ref(true);
const errorMessage = ref('');
const imageUrl = ref('');
const imageBase64 = ref('');
const showModal = ref(false);

// Define backend base URL
const BACKEND_BASE_URL = 'http://localhost:5000';

const goBack = () => {
  window.history.back();
};

// 공유하기 기능 구현
const shareResult = () => {
  showModal.value = true;
};

// onMounted 훅을 사용하여 DOM 요소가 마운트된 후에 접근
onMounted(() => {
  console.log('컴포넌트가 마운트되었습니다.');
  
  // 이미지 URL과 Base64 데이터를 라우트 쿼리에서 가져오기
  imageUrl.value = route.query.imageUrl || '';
  imageBase64.value = route.query.imageBase64 ? decodeURIComponent(route.query.imageBase64) : '';

  // Simulate loading
  setTimeout(() => {
    isLoading.value = false;
    if (!imageSource.value) {
      errorMessage.value = '이미지를 불러오는 데 실패했습니다.';
    }
  }, 1000);
});

const imageSource = computed(() => {
  if (imageBase64.value) {
    return `data:image/jpeg;base64,${imageBase64.value}`;
  } else if (imageUrl.value && store.state.isAuthenticated) {
    return `${BACKEND_BASE_URL}/uploads/${imageUrl.value}`;
  }
  return '/placeholder.svg';
});

// 이미지 팝업 열기
function openImagePopup(imageSrc) {
  popupImageUrl.value = imageSrc.startsWith('data:image/')
    ? imageSrc
    : `${BACKEND_BASE_URL}/uploads/${imageSrc}`;
  isImagePopupVisible.value = true;
}

// Define additional refs for popup
const popupImageUrl = ref('');
const isImagePopupVisible = ref(false);

// 내가 잡은 물고기 페���지로 이동
function navigateToCatches() {
  router.push('/catches');
}
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

.fixed {
  position: fixed;
}

.bg-opacity-50 {
  background-opacity: 0.5;
}

.modal {
  /* 추가적인 모달 스타일이 필요하다면 여기에 작성 */
}
</style>
