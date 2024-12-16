<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-md bg-white shadow-lg">
            <main class="p-4">
                <h1 class="text-lg font-medium mb-4">내가 잡은 물고기</h1>
                <div v-if="catches.length > 0" class="overflow-x-auto touch-pan-x scroll-smooth">
                    <div class="flex space-x-4">
                        <div v-for="(catchItem, index) in catches" :key="index"
                            class="bg-gray-50 p-4 rounded-lg shadow-sm flex-shrink-0 w-48">
                            <img :src="catchItem.imageUrl" alt="Catch Image"
                                class="w-full h-32 object-cover rounded-lg mb-2" />
                            <p class="text-gray-800 text-sm">{{ catchItem.detections }}</p>
                        </div>
                    </div>
                </div>
                <div v-else class="text-gray-500">아직 잡은 물고기가 없습니다.</div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const catches = computed(() => store.getters.catches);
</script>

<style scoped>
.touch-pan-x {
    -webkit-overflow-scrolling: touch;
    overflow-scrolling: touch;
}

.scroll-smooth {
    scroll-behavior: smooth;
}
</style>
