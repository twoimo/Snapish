<template>
    <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end justify-center">
        <div class="bg-white w-full max-w-md rounded-t-xl">
            <div class="p-4">
                <h2 class="text-lg font-semibold text-center mb-4">사진 업로드</h2>
                <div class="space-y-2">
                    <button v-for="(option, index) in options" :key="index"
                        class="w-full py-3 px-4 text-center text-blue-500 bg-white hover:bg-gray-50 border-b last:border-b-0"
                        @click="handleOption(option.action)">
                        {{ option.text }}
                    </button>
                </div>
                <button class="w-full py-3 px-4 text-center text-red-500 font-medium mt-2" @click="$emit('close')">
                    취소
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

defineProps({
    isOpen: Boolean
})

const emit = defineEmits(['close', 'select'])

const options = [
    { text: '사진 촬영', action: 'camera' },
    { text: '갤러리에서 선택', action: 'gallery' },
    { text: '파일 선택', action: 'file' }
]

const handleOption = (action) => {
    emit('select', action)
    emit('close')
}
</script>