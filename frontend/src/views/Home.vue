<template>
    <!-- 전체 페이지 컨테이너 - 최소 화면 높이 설정 및 중앙 정렬 -->
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <!-- 메인 콘텐츠 영역 - 최대 너비 제한 및 그림자 효과 적용 -->
        <div class="w-full max-w-md bg-white shadow-lg">
            <!-- 상단 헤더 섹션 - 고정 위치 설정 -->
            <header class="sticky top-0 bg-white z-50 px-4 py-3 flex justify-between items-center border-b">
                <h1 class="text-xl font-bold">SNAPish</h1>
                <!-- 알림 및 설정 버튼 그룹 -->
                <div class="flex items-center gap-4">
                    <button class="p-2">
                        <BellIcon class="w-6 h-6" />
                    </button>
                    <button class="p-2">
                        <Settings2Icon class="w-6 h-6" />
                    </button>
                </div>
            </header>

            <!-- 메인 콘텐츠 영역 - 하단 네비게이션바 공간 확보를 위한 패딩 설정 -->
            <main class="pb-20 px-4">
                <!-- 날씨 섹션 -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium">오늘의 날씨</h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <!-- 날씨 표시 카드 -->
                    <div class="bg-gray-50 rounded-lg p-6 shadow-sm">
                        <div class="flex items-center justify-center h-32 bg-gray-200 rounded">
                            <CloudIcon class="w-12 h-12 text-gray-400" />
                        </div>
                    </div>
                </section>

                <!-- 물고기 캐치 기록 섹션 -->
                <section class="mb-6">
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium">내가 잡은 물고기</h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <!-- 물고기 그리드 레이아웃 - 3열 구성 -->
                    <div class="grid grid-cols-3 gap-3">
                        <div v-for="i in 3" :key="i" class="bg-gray-50 rounded-lg p-3 shadow-sm">
                            <div class="flex items-center justify-center h-24 bg-gray-200 rounded mb-2">
                                <FishIcon class="w-8 h-8 text-gray-400" />
                            </div>
                            <p class="text-sm text-gray-600">물고기</p>
                            <p class="text-sm">종류</p>
                        </div>
                    </div>
                </section>

                <!-- 커뮤니티 게시물 섹션 -->
                <section>
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium">
                            <router-link to="/community" class="flex flex-col items-center p-2">
                                커뮤니티
                            </router-link>
                        </h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <!-- 게시물 목록 -->
                    <div class="space-y-3">
                        <!-- 각 게시물 카드 -->
                        <article v-for="i in 4" :key="i" class="bg-gray-50 rounded-lg p-4 shadow-sm">
                            <div class="flex gap-3">
                                <!-- 게시물 썸네일 이미지 -->
                                <div
                                    class="w-16 h-16 bg-gray-200 rounded flex items-center justify-center flex-shrink-0">
                                    <ImageIcon class="w-8 h-8 text-gray-400" />
                                </div>
                                <!-- 게시물 내용 -->
                                <div class="flex-1">
                                    <h3 class="font-medium mb-1">게시물 제목</h3>
                                    <p class="text-sm text-gray-600 mb-2">게시물 내용 미리보기입니다. 여기에 간단한 설명이 들어갑니다.</p>
                                    <!-- 게시 시간 정보 -->
                                    <div class="flex items-center text-sm text-gray-500">
                                        <ClockIcon class="w-4 h-4 mr-1" />
                                        <span>오늘 • 23분 전</span>
                                    </div>
                                </div>
                                <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                            </div>
                        </article>
                    </div>
                </section>
            </main>

            <!-- 하단 네비게이션 바 - 고정 위치 설정 -->
            <nav class="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-2 max-w-md mx-auto">
                <div class="flex justify-between items-center">
                    <!-- 홈/커뮤니티 버튼 -->
                    <button class="flex flex-col items-center p-2">
                        <HomeIcon class="w-6 h-6" />
                        <span class="text-xs mt-1">커뮤니티</span>
                    </button>
                    <!-- 사진 촬영 버튼 -->
                    <button class="flex flex-col items-center p-2">
                        <PlusCircleIcon class="w-6 h-6" />
                        <span class="text-xs mt-1">사진 찍기</span>
                    </button>
                    <!-- 프로필 버튼 -->
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
// Lucide 아이콘 컴포넌트 임포트
import {
    BellIcon,        // 알림 아이콘
    Settings2Icon,   // 설정 아이콘
    ChevronRightIcon,// 오른쪽 화살표 아이콘
    CloudIcon,       // 구름 아이콘
    FishIcon,        // 물고기 아이콘
    ImageIcon,       // 이미지 아이콘
    ClockIcon,       // 시계 아이콘
    HomeIcon,        // 홈 아이콘
    PlusCircleIcon,  // 플러스 아이콘
    UserIcon         // 사용자 아이콘
} from 'lucide-vue-next'
</script>