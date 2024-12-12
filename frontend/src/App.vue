<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg relative">
      <!-- 상단 헤더 -->
      <Header v-if="!hideHeader" />
      <router-view></router-view>
      <!-- 하단 네비게이션 -->
      <BottomNavigation @toggleCameraActions="showCameraActions = true" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import BottomNavigation from './components/layout/BottomNavigation.vue';
import Header from './components/layout/Header.vue';

// 현재 라우트 확인
const route = useRoute();

// 특정 경로에서만 헤더 숨기기
const hideHeader = computed(() => /^\/(fish-result)/.test(route.path));


</script>

<style>
body {
  /* eslint-disable-next-line */
  @apply antialiased text-gray-900 bg-gray-100;
}

.active-link {
  color: #1d4ed8;
  /* 선호하는 활성화 색상으로 변경 */
}
</style>
