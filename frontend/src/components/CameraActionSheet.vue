<template>
    <!-- isOpen이 true일 때만 표시되는 배경 레이어 -->
    <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end justify-center"
        @click="$emit('close')">
        <!-- 클릭 이벤트 전파를 막기 위해 @click.stop 사용 -->
        <div class="bg-white w-full max-w-sm rounded-t-xl" @click.stop>
            <div class="p-4">
                <!-- 제목 -->
                <h2 class="text-lg font-semibold text-center mb-4">사진 업로드</h2>
                <div class="space-y-2">
                    <!-- 옵션 버튼들 -->
                    <button v-for="(option, index) in options" :key="index"
                        class="w-full py-3 px-4 text-center text-blue-500 bg-white hover:bg-gray-50 border-b last:border-b-0"
                        @click="handleOption(option.action)">
                        {{ option.text }}
                    </button>
                </div>
                <!-- 취소 버튼 -->
                <button class="w-full py-3 px-4 text-center text-red-500 font-medium mt-2" @click="$emit('close')">
                    취소
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'

// 컴포넌트 속성 정의
defineProps({
    isOpen: Boolean
})

// 이벤트 정의
const emit = defineEmits(['close', 'select'])
const router = useRouter()

// 옵션 목록
const options = [
    { text: '사진 촬영', action: 'camera' },
    { text: '갤러리에서 선택', action: 'gallery' },
    { text: '파일 선택', action: 'file' }
]

// 옵션 클릭 시 실행되는 함수
const handleOption = (action) => {
    if (action === 'gallery') {
        // 갤러리 선택 시 경로 이동 및 창 닫기
        router.push('/fish-warning')
        emit('close')
    } else if (action === 'camera') {
        // 카메라 선택 시 경로 이동 및 창 닫기
        router.push('/fish-detection-result')
        emit('close')
    } else {
        // 기타 파일 선택 시 select 이벤트 발생 및 창 닫기
        emit('select', action)
        emit('close')
    }
}
</script>