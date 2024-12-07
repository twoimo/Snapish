<template>
  <div class="min-h-screen bg-gray-100 flex justify-center">
    <div class="w-full max-w-md bg-white shadow-lg">
      <!-- Header -->
      <header class="sticky top-0 bg-white z-50 px-4 py-3 flex items-center border-b">
        <button class="mr-2">
          <ChevronLeftIcon class="w-6 h-6" />
        </button>
        <h1 class="text-xl font-bold">물고기 판별 결과</h1>
      </header>

      <!-- Main Content -->
      <main class="pb-20 px-4">
        <!-- Fish Image -->
        <div class="mt-4 bg-gray-200 rounded-lg p-4 flex justify-center">
          <img src="/placeholder.svg?height=200&width=300" alt="물고기 사진" class="w-full h-48 object-contain" />
        </div>

        <!-- Warning Message -->
        <div class="mt-6 bg-red-50 rounded-lg p-4 border-2 border-red-500">
          <div class="flex items-center mb-2">
            <AlertTriangleIcon class="w-6 h-6 text-red-500 mr-2" />
            <h2 class="text-lg font-bold text-red-700">주의: 현재 포획 금지 어종</h2>
          </div>
          <p class="text-red-600">이 물고기는 <strong>참돔</strong>으로, 현재 포획이 금지되어 있습니다.</p>
        </div>

        <!-- Fish Details -->
        <div class="mt-6 bg-gray-50 rounded-lg p-4">
          <h2 class="text-xl font-bold mb-2">참돔</h2>
          <p class="text-gray-600">학명: Pagrus major</p>
          <p class="mt-2 text-gray-700">참돔은 한국 연안에서 흔히 볼 수 있는 어종이지만, 현재 자원 보호를 위해 포획이 제한되어 있습니다.</p>
        </div>

        <!-- Reason for Restriction -->
        <div class="mt-6 bg-yellow-50 rounded-lg p-4">
          <h3 class="font-bold text-yellow-700 mb-2">포획 제한 이유</h3>
          <ul class="list-disc list-inside text-yellow-800">
            <li>산란기 보호 (5월 1일 ~ 6월 30일)</li>
            <li>어족 자원 회복을 위한 조치</li>
            <li>생태계 균형 유지</li>
          </ul>
        </div>

        <!-- Recommended Actions -->
        <div class="mt-6 bg-green-50 rounded-lg p-4">
          <h3 class="font-bold text-green-700 mb-2">권장 행동</h3>
          <ul class="list-disc list-inside text-green-800">
            <li>즉시 물고기를 놓아주세요.</li>
            <li>가능한 한 물고기에 상처를 주지 않도록 주의하세요.</li>
            <li>다른 낚시꾼들에게 현재 상황을 알려주세요.</li>
          </ul>
        </div>

        <!-- Action Buttons -->
        <div class="mt-6 space-y-3">
          <button class="w-full bg-blue-500 text-white py-3 px-4 rounded-lg flex items-center justify-center">
            <InfoIcon class="w-5 h-5 mr-2" />
            <span>더 자세한 정보 보기</span>
          </button>
          <button class="w-full bg-green-500 text-white py-3 px-4 rounded-lg flex items-center justify-center">
            <Share2Icon class="w-5 h-5 mr-2" />
            <span>이 정보 공유하기</span>
          </button>
        </div>
      </main>

      <!-- Bottom Navigation -->
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
  ChevronLeftIcon,
  AlertTriangleIcon,
  InfoIcon,
  Share2Icon,
  HomeIcon,
  CameraIcon,
  UserIcon
} from 'lucide-vue-next'
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
