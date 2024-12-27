<template>
    <div class="min-h-screen bg-white flex flex-col">
        <!-- 헤더 -->
        <header class="fixed top-0 left-0 right-0 bg-white px-4 py-3 flex items-center justify-between border-b z-10 max-w-md mx-auto">
            <div class="flex items-center">
                <button class="mr-2" @click="goBack">
                    <ChevronLeftIcon class="w-6 h-6" />
                </button>
                <h1 class="text-xl font-bold">오류 발생</h1>
            </div>
        </header>

        <!-- 메인 콘텐츠 -->
        <main class="flex-1 pb-20 px-4 overflow-auto max-w-md mx-auto">
            <!-- 에러 메시지 -->
            <div class="h-full flex items-center justify-center">
                <div class="text-center p-4">
                    <!-- Webpack이 처리하도록 하는 이미지 -->
                    <img :src="errorImage" alt="Error" class="w-60 h-60 mx-auto mb-4">
                    <h2 class="text-xl font-bold text-gray-800 mb-2">{{ errorMessage }}</h2>
                    <p class="text-gray-600 mb-8">{{ errorDescription }}</p>
                    
                    <!-- 버튼 그룹 -->
                    <div class="space-y-4">
                        <!-- 이전으로 버튼 -->
                        <button 
                            class="w-full bg-gray-500 text-white py-3 px-4 rounded-lg flex items-center justify-center"
                            @click="goHome">
                            <ChevronLeftIcon class="w-5 h-5 mr-2" />
                            <span>홈으로 돌아가기</span>
                        </button>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ChevronLeftIcon } from 'lucide-vue-next';

// 이미지 불러오기
import errorImagePath from '@/assets/images/Error_Page.png';

const route = useRoute();
const router = useRouter();

const errorTypes = {
    no_detection: {
        message: '물고기를 감지할 수 없습니다.',
        description: '물고기가 포함된 사진을 다시 업로드 해주세요.'
    },
    low_confidence: {
        message: '물고기를 정확하게 인식할 수 없습니다.',
        description: '더 선명한 사진으로 다시 시도해주세요.'
    }, 
    invalid_file_name: {
        message: '파일명 형식 오류',
        description: 'PNG, JPG, JPEG 형식의 이미지만 업로드 가능합니다.'
    },
    invalid_file_type: {
        message: '지원하지 않는 파일 형식입니다.',
        description: 'PNG, JPG, JPEG 형식의 이미지만 업로드 가능합니다.'
    },
    invalid_file_open: {
        message: '업로드 이미지를 열지 못했습니다.',
        description: '파일을 열 수 없습니다.'
    },
    invalid_image_formatting_error: {
        message: '지원하지 않는 파일 형식입니다.',
        description: '파일이 변환 중 오류가 발생했습니다.'
    },
    analyze_failed: {
        message: '분석 작업 중 오류가 발생하였습니다.',
        description: '분석 작업 중 오류가 발생하였습니다.'
    }
};

const errorType = computed(() => route.query.errorType || 'analyze_failed');
const errorMessage = computed(() => route.query.message || errorTypes[errorType.value].message);
const errorDescription = computed(() => errorTypes[errorType.value].description);
const errorImage = errorImagePath; // 불러온 이미지 경로를 바인딩

const goHome = () => {
    router.push('/');
};
</script>

<style scoped>
.min-h-screen {
    min-height: 100vh;
}

/* 페이드 인 애니메이션 */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.text-center {
    animation: fadeIn 0.5s ease-out forwards;
}
</style>
