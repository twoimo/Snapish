<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg">
      <!-- 헤더 -->
      <header class="sticky top-0 bg-white px-4 py-3 flex items-center justify-between border-b">
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
        <!-- 업로드된 물고기 이미지 표시 -->
        <div class="mt-4 bg-gray-200 rounded-lg p-4 flex justify-center">
          <img :src="props.imageUrl" alt="물고기 사진" class="w-full h-full object-cover" />
        </div>

        <!-- AI 판별 결과 -->
        <div class="mt-6 bg-blue-50 rounded-lg p-4">
          <h2 class="text-lg font-bold text-blue-700 mb-2">AI 판별 결과</h2>
          <p class="text-blue-600">
            이 물고기는 <strong>{{ props.labels[0] }}</strong>입니다.
          </p>
          <p class="text-sm text-blue-600 mt-2" v-if="props.labels.length > 1">
            다른 후보: <span class="text-blue-500">{{ props.labels.slice(1).join(', ') }}</span>
          </p>
        </div>

        <!-- 공유하기 버튼 -->
        <div class="mt-6">
          <button class="w-full bg-green-500 text-white py-3 px-4 rounded-lg flex items-center justify-center">
            <Share2Icon class="w-5 h-5 mr-2" />
            <span>공유하기</span>
          </button>
        </div>
      </main>

      <!-- 하단 네비게이션 -->
      <BottomNavigation />
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import BottomNavigation from '../components/layout/BottomNavigation.vue';
import {
  BellIcon,
  Settings2Icon,
  ChevronLeftIcon,
  Share2Icon,
} from 'lucide-vue-next';

// props 정의
const props = defineProps({
  labels: {
    type: Array,
    required: true,
  },
  imageUrl: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.uploaded-image img {
  max-width: 100%;
  height: auto;
  object-fit: cover;
}
</style>