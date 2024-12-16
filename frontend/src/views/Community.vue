<template>
    <div class="min-h-screen bg-gray-100 flex justify-center p-4">
        <div class="w-full max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
            <main class="pb-20 px-4">
                <section class="mb-6 pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-lg font-medium mr-2">커뮤니티</h2>
                        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
                    </div>
                    <div class="space-y-3">
                        <article v-for="(post, index) in posts" :key="index"
                            class="bg-gray-50 rounded-lg p-4 shadow-sm hover:bg-gray-100 transition">
                            <div class="flex gap-3">
                                <div
                                    class="w-16 h-16 bg-gray-200 rounded flex items-center justify-center flex-shrink-0">
                                    <ImageIcon class="w-8 h-8 text-gray-400" />
                                </div>
                                <div class="flex-1">
                                    <h3 class="font-medium mb-1">{{ post.author }}</h3>
                                    <p class="text-sm text-gray-600 mb-2">{{ post.content }}</p>
                                    <div class="flex items-center text-sm text-gray-500">
                                        <ClockIcon class="w-4 h-4 mr-1" />
                                        <span>{{ post.date }}</span>
                                    </div>
                                    <div class="flex items-center mt-4 space-x-4 text-gray-500">
                                        <button class="flex items-center">
                                            <HeartIcon class="w-5 h-5 mr-1" />
                                            {{ post.likes }}
                                        </button>
                                        <button class="flex items-center">
                                            <MessageCircleIcon class="w-5 h-5 mr-1" />
                                            {{ post.comments }}
                                        </button>
                                    </div>
                                </div>
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
    HeartIcon,
    MessageCircleIcon
} from 'lucide-vue-next'

const posts = [
    {
        author: '낚시왕', // 작성자 이름
        date: '1시간 전', // 작성 날짜
        content: '오늘의 조과입니다! 날씨가 정말 좋네요.', // 게시물 내용
        image: '/placeholder.svg?height=300&width=400', // 게시물 이미지
        likes: 24, // 좋아요 수
        comments: 8 // 댓글 수
    },
    {
        author: '바다사랑', // 작성자 이름
        date: '3시간 전', // 작성 날짜
        content: '초보자도 잡을 수 있는 포인트를 공유합니다.', // 게시물 내용
        image: '/placeholder.svg?height=300&width=400', // 게시물 이미지
        likes: 45, // 좋아요 수
        comments: 12 // 댓글 수
    }
]
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