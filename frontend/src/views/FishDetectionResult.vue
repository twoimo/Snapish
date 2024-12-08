<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg">
      <!-- 헤더 -->
      <header class="sticky top-0 bg-white z-50 px-4 py-3 flex items-center justify-between border-b">
        <div class="flex items-center">
          <button class="mr-2">
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

      <!-- 메인 콘텐츠 -->
      <main class="pb-20 px-4">
        <!-- 물고기 이미지 -->
        <div class="mt-4 bg-gray-200 rounded-lg p-4 flex justify-center">
          <img src="@/../public/sample-img.jpg" alt="물고기 사진" class="w-full h-full object-cover" />
        </div>

        <!-- AI 판별 결과 -->
        <div class="mt-6 bg-blue-50 rounded-lg p-4">
          <h2 class="text-lg font-bold text-blue-700 mb-2">AI 판별 결과</h2>
          <p class="text-blue-600">
            이 물고기는 <strong>{{ mainResult }}</strong>입니다.
            <span class="text-sm text-blue-500">(신뢰도: {{ confidence }}%)</span>
          </p>
          <p class="text-sm text-blue-600 mt-2">
            다른 후보: <span class="text-blue-500">{{ alternativeFish.join(', ') }}</span>
          </p>
        </div>

        <!-- 물고기 상세 정보 -->
        <div class="mt-6 space-y-4">
          <div class="bg-gray-50 rounded-lg p-4">
            <h2 class="text-xl font-bold mb-2">{{ mainResult }}</h2>
            <p class="text-gray-600">일반적인 이름: {{ commonName }}</p>
            <p class="text-gray-600">학명: {{ scientificName }}</p>
            <p class="mt-2 text-gray-700">{{ fishDescription }}</p>
          </div>
        </div>

        <!-- 액션 버튼 -->
        <div class="mt-6 space-y-3">
          <button class="w-full bg-blue-500 text-white py-3 px-4 rounded-lg flex items-center justify-center">
            <PlusIcon class="w-5 h-5 mr-2" />
            <span>내 기록에 추가</span>
          </button>
          <button class="w-full bg-green-500 text-white py-3 px-4 rounded-lg flex items-center justify-center">
            <Share2Icon class="w-5 h-5 mr-2" />
            <span>공유하기</span>
          </button>
        </div>
      </main>

      <!-- 하단 네비게이션 -->
      <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2 max-w-md mx-auto">
        <div class="flex justify-between items-center">
          <button class="flex flex-col items-center p-2">
            <HomeIcon class="w-6 h-6" />
            <span class="text-xs mt-1">홈</span>
          </button>
          <button class="flex flex-col items-center p-2">
            <CameraIcon class="w-6 h-6" />
            <span class="text-xs mt-1">촬영</span>
          </button>
          <button class="flex flex-col items-center p-2">
            <UserIcon class="w-6 h-6" />
            <span class="text-xs mt-1">프로필</span>
          </button>
        </div>
      </nav>
    </div>
  </div>
</template>

<script setup>
import {
  BellIcon,
  Settings2Icon,
  ChevronLeftIcon,
  PlusIcon,
  Share2Icon,
  HomeIcon,
  CameraIcon,
  UserIcon
} from 'lucide-vue-next'
import { ref } from 'vue'

// 예시 데이터 (실제로는 props나 API로 받아올 수 있습니다)
const mainResult = ref('광어') // AI 판별 결과
const confidence = ref(95) // 신뢰도
const alternativeFish = ref(['참돔', '농어']) // 다른 후보 물고기
const commonName = ref('넙치') // 일반적인 이름
const scientificName = ref('Paralichthys olivaceus') // 학명
const fishDescription = ref('광어는 한국의 대표적인 양식 어종으로, 맛있는 횟감으로 널리 알려져 있습니다. 평평한 몸체와 양쪽 눈이 한쪽에 몰려있는 특징을 가지고 있습니다.') // 물고기 설명
</script>
