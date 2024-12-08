<template>
  <!-- 하단 네비게이션 바 -->
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2">
    <div class="flex justify-between items-center">
      <!-- 홈 버튼 -->
      <button class="flex flex-col items-center p-2">
        <HomeIcon class="w-6 h-6" />
        <span class="text-xs mt-1">메인 화면</span>
      </button>
      <!-- 촬영 버튼 -->
      <button class="flex flex-col items-center p-2">
        <CameraIcon class="w-6 h-6" />
        <span class="text-xs mt-1">사진 찍기</span>
      </button>
      <!-- 프로필 버튼 -->
      <button class="flex flex-col items-center p-2">
        <UserIcon class="w-6 h-6" />
        <span class="text-xs mt-1">프로필</span>
      </button>
    </div>
  </nav>
</template>

<script>
import { HomeIcon, CameraIcon, UserIcon } from 'lucide-vue-next'

export default {
  name: 'BottomNavigation',
  components: {
    HomeIcon,
    CameraIcon,
    UserIcon
  }
}
</script>
