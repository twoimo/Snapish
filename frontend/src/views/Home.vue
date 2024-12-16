<template>
    <!-- 전체 페이지 컨테이너 - 최소 화면 높이 설정 및 중앙 정렬 -->
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <!-- 메인 콘텐츠 영역 - 최대 너비 제한 및 그림자 효과 적용 -->
        <div class="w-full max-w-md bg-white shadow-lg">
            <!-- 메인 콘텐츠 영역 - 하단 네비게이션바 공간 확보를 위한 패딩 설정 -->
            <main class="pb-20 px-4">
                <!-- 물때/날씨 섹션 -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/map-location-service" class="flex justify-between items-center p-2 w-full">
                            <h2 class="text-lg font-medium mr-2">오늘의 물때</h2>
                            <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                        </router-link>
                    </div>
                    <!-- 물때 표시 카드 -->
                    <MulddaeWidget></MulddaeWidget>
                </section>

                <!-- 물고기 캐치 기록 섹션 -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/catches" class="flex flex-col items-center p-2">
                            <h2 class="text-lg font-medium mr-2">내가 잡은 물고기</h2>
                        </router-link>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div v-if="catches.length > 0" class="overflow-x-auto touch-pan-x">
                        <div class="flex space-x-4">
                            <div v-for="(catchItem, index) in catches" :key="index"
                                class="bg-gray-50 p-4 rounded-lg shadow-sm flex-shrink-0 w-48">
                                <img :src="catchItem.imageUrl" alt="Catch Image"
                                    class="w-full h-32 object-cover rounded-lg mb-2" />
                                <p class="text-gray-800 text-sm">{{ catchItem.detections }}</p>
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-gray-500 flex flex-col items-center p-2">아직 잡은 물고기가 없습니다.</div>
                </section>

                <!-- 커뮤니티 게시물 섹션 -->
                <section>
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/community" class="flex flex-col items-center p-2">
                            <h2 class="text-lg font-medium">커뮤니티</h2>
                        </router-link>
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
        </div>
    </div>
</template>

<script setup>
// Lucide 아이콘 컴포넌트 임포트
/* eslint-disable */
import {
    ChevronRightIcon,// 오른쪽 화살표 아이콘
    // CloudIcon,       // 구름 아이콘
    FishIcon,        // 물고기 아이콘
    ImageIcon,       // 이미지 아이콘
    ClockIcon,       // 시계 아이콘
} from 'lucide-vue-next'
import { onMounted, computed } from "vue";
import { useStore } from "vuex";
import MulddaeWidget from '../components/MulddaeWidget.vue';

const store = useStore();

onMounted(() => {
    store.dispatch("fetchMulddae");
    store.dispatch("fetchCatches"); // Fetch catches when the component is mounted
});

const catches = computed(() => store.getters.catches);
</script>

<style>
* {
    -ms-overflow-style: none;
    /* IE and Edge */
    scrollbar-width: none;
    /* Firefox */
}

*::-webkit-scrollbar {
    display: none;
    /* Chrome, Safari, Opera*/
}

.touch-pan-x {
    -webkit-overflow-scrolling: touch;
    overflow-scrolling: touch;
}
</style>