<template>
    <div class="min-h-screen bg-gray-100 flex justify-center p-4">
        <div class="w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">
            <main class="pb-20 px-4">
                <section class="mb-6 pt-4">
                    <div v-if="displayedCatches.length > 0" class="grid grid-cols-2 gap-4">
                        <div v-for="(catchItem, index) in displayedCatches" :key="index"
                            class="bg-gray-50 p-4 rounded-lg shadow-sm">
                            <img :src="catchItem.imageUrl" alt="Catch Image"
                                class="w-full h-32 object-cover rounded-lg mb-2" />
                            <p class="text-gray-800 text-sm">{{ catchItem.detections }}</p>
                        </div>
                    </div>
                    <div v-else class="text-gray-500 flex flex-col items-center p-2">아직 잡은 물고기가 없습니다.</div>
                    <div ref="loadMoreTrigger" class="h-1"></div>
                </section>
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

.scroll-smooth {
    scroll-behavior: smooth;
}

.hover\:bg-gray-50:hover {
    background-color: #f9fafb;
}

.transition {
    transition: background-color 0.3s ease;
}
</style>
