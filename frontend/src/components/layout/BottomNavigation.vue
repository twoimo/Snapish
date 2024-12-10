<template>
  <!-- 하단 네비게이션 바 -->
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2 max-w-md mx-auto">
    <div class="flex justify-between items-center">
      <!-- 카메라 액션 시트 -->
      <CameraActionSheet :is-open="showCameraActions" @close="showCameraActions = false" @select="handleCameraAction"
        class="z-50" />
      <!-- 메인 화면 링크 -->
      <router-link to="/" class="flex flex-col items-center p-2" active-class="active-link">
        <HomeIcon class="w-6 h-6" />
        <span class="text-xs mt-1">메인 화면</span>
      </router-link>
      <!-- 사진 찍기 버튼 -->
      <button @click="showCameraActions = true" class="flex flex-col items-center p-2">
        <CameraIcon class="w-6 h-6" />
        <span class="text-xs mt-1">사진 찍기</span>
      </button>
      <!-- 프로필 링크 -->
      <router-link to="/profile" class="flex flex-col items-center p-2" active-class="active-link">
        <UserIcon class="w-6 h-6" />
        <span class="text-xs mt-1">프로필</span>
      </router-link>
    </div>
  </nav>
</template>

<script>
import { ref } from 'vue'
import { HomeIcon, CameraIcon, UserIcon } from 'lucide-vue-next'
import CameraActionSheet from '../CameraActionSheet.vue'

export default {
  name: 'BottomNavigation',
  components: {
    HomeIcon,
    CameraIcon,
    UserIcon,
    CameraActionSheet
  },
  setup() {
    // 카메라 액션 시트 표시 여부를 관리하는 상태
    const showCameraActions = ref(false)

    // 카메라 액션을 처리하는 함수
    const handleCameraAction = (action) => {
      // 다양한 카메라 액션을 처리
      console.log('Selected action:', action)
    }

    return {
      showCameraActions,
      handleCameraAction
    }
  }
}
</script>
