<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-4xl bg-white shadow-lg overflow-hidden">
            <main class="pb-20 px-4">
                <!-- 오늘의 물때 섹션 -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/map-location-service"
                            class="flex justify-between items-center p-2 w-full hover:bg-gray-50 rounded-lg transition">
                            <h2 class="text-lg font-medium mr-2">오늘의 물때</h2>
                            <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                        </router-link>
                    </div>
                    <MulddaeWidget></MulddaeWidget>
                </section>

                <!-- 내가 잡은 물고기 섹션 -->
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/catches"
                            class="flex flex-col items-center p-2 hover:bg-gray-50 rounded-lg transition">
                            <h2 class="text-lg font-medium mr-2">내가 잡은 물고기</h2>
                        </router-link>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div v-if="catches.length > 0" class="overflow-x-auto touch-pan-x">
                        <div class="flex space-x-4">
                            <div v-for="(catchItem, index) in [...catches].reverse()" :key="index"
                                class="bg-gray-50 p-4 rounded-lg shadow-sm flex-shrink-0 w-48 h-48">
                                <img :src="catchItem.imageUrl" alt="Catch Image"
                                    class="w-full h-32 object-cover rounded-lg mb-2" />
                                <p class="text-gray-800 text-sm">{{ catchItem.detections }}</p>
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-gray-500 flex flex-col items-center p-2">아직 잡은 물고기가 없습니다.</div>
                </section>

                <!-- 커뮤니티 섹션 -->
                <section>
                    <div class="flex justify-between items-center mb-3">
                        <router-link to="/community"
                            class="flex flex-col items-center p-2 hover:bg-gray-50 rounded-lg transition">
                            <h2 class="text-lg font-medium">커뮤니티</h2>
                        </router-link>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div class="space-y-3">
                        <article v-for="i in 4" :key="i"
                            class="bg-gray-50 rounded-lg p-4 shadow-sm hover:bg-gray-100 transition">
                            <div class="flex gap-3">
                                <div
                                    class="w-16 h-16 bg-gray-200 rounded flex items-center justify-center flex-shrink-0">
                                    <ImageIcon class="w-8 h-8 text-gray-400" />
                                </div>
                                <div class="flex-1">
                                    <h3 class="font-medium mb-1">게시물 제목</h3>
                                    <p class="text-sm text-gray-600 mb-2">게시물 내용 미리보기입니다. 여기에 간단한 설명이 들어갑니다.</p>
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
import {
    ChevronRightIcon,
    ImageIcon,
    ClockIcon,
} from 'lucide-vue-next'
import { onMounted, computed } from "vue";
import { useStore } from "vuex";
import MulddaeWidget from '../components/MulddaeWidget.vue';

// Vuex 스토어 사용
const store = useStore();

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
    if (!store.state.mulddae) {
        store.dispatch("fetchMulddae");
    }
    store.dispatch("fetchCatches");
    
});

// Vuex 스토어에서 잡은 물고기 데이터 가져오기
const catches = computed(() => store.getters.catches);
</script>

<style  lang="css">
* {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

*::-webkit-scrollbar {
    display: none;
}

.touch-pan-x {
    -webkit-overflow-scrolling: touch;
    overflow-scrolling: touch;
}

.scroll-smooth {
    scroll-behavior: smooth;
}

.hover\:bg-gray-50:hover {
    background-color: #f9fafb;
}

.hover\:bg-gray-100:hover {
    background-color: #f3f4f6;
}

.transition {
    transition: background-color 0.3s ease;
}
</style>
