<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-4xl bg-white shadow-lg">
            <main class="p-4">
                <div v-if="catches.length > 0" class="grid grid-cols-2 gap-4">
                    <div v-for="(catchItem, index) in displayedCatches.slice().reverse()" :key="index"
                        class="bg-gray-50 p-4 rounded-lg shadow-sm">
                        <img :src="catchItem.imageUrl" alt="Catch Image"
                            class="w-full h-32 object-cover rounded-lg mb-2" />
                        <p class="text-gray-800 text-sm">{{ catchItem.detections }}</p>
                    </div>
                    <div ref="loadMoreTrigger" class="col-span-2 h-1"></div>
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
const displayedCatches = ref([]);
const loading = ref(false);
const itemsPerPage = 10;
let currentPage = 1;

const loadMoreItems = () => {
    if (loading.value) return;
    loading.value = true;
    setTimeout(() => {
        const start = (currentPage - 1) * itemsPerPage;
        const end = currentPage * itemsPerPage;
        displayedCatches.value.push(...catches.value.slice(start, end));
        currentPage++;
        loading.value = false;
    }, 1000); // Simulate network delay
};

const loadMoreTrigger = ref(null);

const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        loadMoreItems();
    }
}, {
    root: null,
    rootMargin: '0px',
    threshold: 1.0
});

onMounted(() => {
    loadMoreItems();
    if (loadMoreTrigger.value) {
        observer.observe(loadMoreTrigger.value);
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
