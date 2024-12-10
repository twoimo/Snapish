<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg relative">
      <router-view></router-view>

      <!-- 상단 헤더 -->
      <Header />

      <!-- 하단 네비게이션 -->
      <BottomNavigation @toggleCameraActions="showCameraActions = true" />
    </div>
  </div>
</template>

<script setup>
import BottomNavigation from './components/layout/BottomNavigation.vue';
import Header from './components/layout/Header.vue';

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
