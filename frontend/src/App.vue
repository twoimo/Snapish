<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg relative">
      <router-view></router-view>

      <!-- Bottom Navigation -->
      <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2 max-w-md mx-auto">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex flex-col items-center p-2" active-class="active-link">
            <HomeIcon class="w-6 h-6" />
            <span class="text-xs mt-1">메인 화면</span>
          </router-link>
          <button @click="showCameraActions = true" class="flex flex-col items-center p-2">
            <PlusCircleIcon class="w-6 h-6" />
            <span class="text-xs mt-1">사진 찍기</span>
          </button>
          <router-link to="/profile" class="flex flex-col items-center p-2" active-class="active-link">
            <UserIcon class="w-6 h-6" />
            <span class="text-xs mt-1">프로필</span>
          </router-link>
        </div>
      </nav>

      <!-- Camera Action Sheet -->
      <CameraActionSheet :is-open="showCameraActions" @close="showCameraActions = false" @select="handleCameraAction" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { HomeIcon, PlusCircleIcon, UserIcon } from 'lucide-vue-next'
import CameraActionSheet from './components/CameraActionSheet.vue'

const showCameraActions = ref(false)

const handleCameraAction = (action) => {
  // Handle different camera actions
  console.log('Selected action:', action)
}
</script>

<style>
body {
  @apply antialiased text-gray-900 bg-gray-100;
}

.active-link {
  color: #1d4ed8;
  /* Change to your preferred active color */
}
</style>
