<template>
    <div class="min-h-screen bg-gray-100 flex justify-center">
        <div class="w-full max-w-md bg-white shadow-lg">
            <!-- 헤더 섹션 -->
            <header class="sticky top-0 bg-white z-50 px-4 py-3 flex justify-between items-center border-b">
                <h1 class="text-xl font-bold">SNAPish</h1>
                <div class="flex items-center gap-4">
                    <!-- 알림 버튼 -->
                    <button class="p-2">
                        <BellIcon class="w-6 h-6" />
                    </button>
                    <!-- 설정 버튼 -->
                    <button class="p-2">
                        <Settings2Icon class="w-6 h-6" />
                    </button>
                </div>
            </header>

            <!-- 메인 콘텐츠 섹션 -->
            <main class="p-4">
                <div class="space-y-4">
                    <!-- 게시물 반복 렌더링 -->
                    <article v-for="(post, index) in posts" :key="index" class="bg-white rounded-lg shadow-sm">
                        <div class="p-4">
                            <div class="flex items-center mb-4">
                                <!-- 작성자 프로필 이미지 -->
                                <div class="w-10 h-10 rounded-full bg-gray-200"></div>
                                <div class="ml-3">
                                    <!-- 작성자 이름 -->
                                    <h3 class="font-bold">{{ post.author }}</h3>
                                    <!-- 작성 날짜 -->
                                    <p class="text-sm text-gray-500">{{ post.date }}</p>
                                </div>
                            </div>
                            <!-- 게시물 이미지 -->
                            <img :src="post.image" alt="" class="w-full h-64 object-cover rounded-lg mb-4" />
                            <!-- 게시물 내용 -->
                            <p class="text-gray-800">{{ post.content }}</p>
                            <div class="flex items-center mt-4 space-x-4 text-gray-500">
                                <!-- 좋아요 버튼 -->
                                <button class="flex items-center">
                                    <HeartIcon class="w-5 h-5 mr-1" />
                                    {{ post.likes }}
                                </button>
                                <!-- 댓글 버튼 -->
                                <button class="flex items-center">
                                    <MessageCircleIcon class="w-5 h-5 mr-1" />
                                    {{ post.comments }}
                                </button>
                            </div>
                        </div>
                    </article>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import {
    BellIcon,
    Settings2Icon,
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