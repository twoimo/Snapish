<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg relative">
      <router-view></router-view>

      <!-- 하단 네비게이션 -->
      <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2 max-w-md mx-auto">
        <div class="flex justify-between items-center">
          <!-- 메인 화면 링크 -->
          <router-link to="/" class="flex flex-col items-center p-2" active-class="active-link">
            <HomeIcon class="w-6 h-6" />
            <span class="text-xs mt-1">메인 화면</span>
          </router-link>
          <!-- 사진 찍기 버튼 -->
          <button @click="showCameraActions = true" class="flex flex-col items-center p-2">
            <PlusCircleIcon class="w-6 h-6" />
            <span class="text-xs mt-1">사진 찍기</span>
          </button>
          <!-- 프로필 링크 -->
          <router-link to="/profile" class="flex flex-col items-center p-2" active-class="active-link">
            <UserIcon class="w-6 h-6" />
            <span class="text-xs mt-1">프로필</span>
          </router-link>
        </div>
      </nav>

      <!-- 카메라 액션 시트 -->
      <CameraActionSheet :is-open="showCameraActions" @close="showCameraActions = false" @select="handleCameraAction" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { HomeIcon, PlusCircleIcon, UserIcon } from 'lucide-vue-next'
import CameraActionSheet from './components/CameraActionSheet.vue'

// 카메라 액션 시트 표시 여부를 관리하는 상태
const showCameraActions = ref(false)

// 카메라 액션을 처리하는 함수
const handleCameraAction = (action) => {
  // 다양한 카메라 액션을 처리
  console.log('Selected action:', action)
}
</script>

<style>
body {
  @apply antialiased text-gray-900 bg-gray-100;
}

.active-link {
  color: #1d4ed8;
  /* 선호하는 활성화 색상으로 변경 */
}
</style>
