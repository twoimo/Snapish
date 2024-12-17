<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-4xl bg-white shadow-lg">
            <main class="p-4">
                <h1 class="text-xl font-semibold mb-4">내가 잡은 물고기</h1>
                <div v-if="catches.length > 0" class="grid grid-cols-2 gap-4">
                    <div v-for="(catchItem, index) in catches.slice().reverse()" :key="index"
                        class="bg-gray-50 p-4 rounded-lg shadow-sm">
                        <img :src="catchItem.imageUrl" alt="Catch Image"
                            class="w-full h-32 object-cover rounded-lg mb-2" />
                        <p class="text-gray-800 text-sm">{{ catchItem.detections[0].label }}</p>
                        <p class="text-gray-600 text-xs">{{ catchItem.catch_date }}</p>
                    </div>
                </div>
                <div v-else class="text-gray-500">아직 잡은 물고기가 없습니다.</div>
                <div v-if="loading" class="text-center text-gray-500 mt-4">Loading...</div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const catches = computed(() => store.getters.catches);
const loading = ref(false);

onMounted(() => {
    if (store.getters.isAuthenticated) {
        store.dispatch('fetchCatches');
    }
});
</script>

<style scoped>
.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}
</style>
