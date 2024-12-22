<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8">
    <!-- Main content -->
    <main class="max-w-5xl mx-auto px-4">
      <!-- Post list -->
      <div class="grid gap-8">
        <article 
          v-for="post in posts" 
          :key="post.post_id" 
          class="bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100/50"
        >
          <!-- Post header -->
          <div class="p-6">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center space-x-4">
                <div class="relative">
                  <img 
                    :src="getImageUrl(post.avatar)" 
                    alt="User avatar" 
                    class="w-12 h-12 rounded-full object-cover border-2 border-white shadow-md"
                  >
                  <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-2 border-white shadow-sm"></div>
                </div>
                <div>
                  <div class="font-bold text-gray-900">{{ post.username }}</div>
                  <div class="text-sm text-gray-500 flex items-center">
                    <Clock class="w-4 h-4 mr-1 text-gray-400" />
                    {{ formatDate(post.created_at) }}
                  </div>
                </div>
              </div>
              <div v-if="post.user_id === currentUserId" class="relative" v-click-outside="() => post.showOptions = false">
                <button 
                  @click="post.showOptions = !post.showOptions"
                  class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100/80 transition-all duration-200"
                >
                  <MoreVertical class="w-5 h-5" />
                </button>
                <div 
                  v-if="post.showOptions"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100/50 py-1 z-10"
                >
                  <router-link 
                    :to="`/community/edit/${post.post_id}`"
                    class="flex items-center px-4 py-2.5 text-gray-700 hover:bg-gray-50 transition-colors duration-200"
                  >
                    <Edit2 class="w-4 h-4 mr-2 text-blue-500" />
                    <span>수정하기</span>
                  </router-link>
                  <button 
                    @click="confirmDelete(post)"
                    class="flex items-center w-full px-4 py-2.5 text-red-500 hover:bg-red-50 transition-colors duration-200"
                  >
                    <Trash2 class="w-4 h-4 mr-2" />
                    <span>삭제하기</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Post content -->
            <div class="space-y-4">
              <h2 class="text-2xl font-bold text-gray-900 leading-tight">{{ post.title }}</h2>
              <p class="text-gray-600 leading-relaxed">{{ post.content }}</p>
              
              <!-- Image gallery -->
              <div v-if="post.images?.length" class="space-y-4">
                <div 
                  class="relative rounded-2xl overflow-hidden"
                  :data-post-id="post.post_id"
                  @touchstart="handleTouchStart($event, post)"
                  @touchmove="handleTouchMove($event, post)"
                  @touchend="handleTouchEnd($event, post)"
                >
                  <!-- Image container -->
                  <div class="relative w-full overflow-hidden" ref="imageContainer">
                    <div 
                      class="flex w-full transition-transform duration-300"
                      :style="{
                        transform: `translateX(${post.translateX || 0}px)`,
                        width: `${post.images.length * 100}%`
                      }"
                    >
                      <div 
                        v-for="(image, index) in post.images"
                        :key="index"
                        class="w-full flex-shrink-0"
                        :style="{ width: `${100 / post.images.length}%` }"
                      >
                        <img 
                          :src="image" 
                          alt="Post image"
                          class="w-full h-full object-cover"
                          style="max-height: 32rem;"
                          loading="lazy"
                          @load="onImageLoad"
                        >
                      </div>
                    </div>
                  </div>
                  
                  <!-- Dot indicators -->
                  <div 
                    v-if="post.images.length > 1"
                    class="absolute bottom-4 left-0 right-0 flex justify-center space-x-2 z-10"
                  >
                    <button
                      v-for="(_, index) in post.images"
                      :key="index"
                      @click="setImageIndex(post, index)"
                      class="w-2 h-2 rounded-full transition-all duration-200"
                      :class="index === post.currentImageIndex ? 'bg-white scale-110' : 'bg-white/50'"
                    ></button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Post actions -->
            <div class="flex items-center justify-between pt-6 mt-6 border-t border-gray-100">
              <div class="flex items-center divide-x divide-gray-200">
                <button 
                  @click="toggleLike(post)"
                  class="group flex items-center pr-6"
                >
                  <div class="w-10 h-10 flex items-center justify-center rounded-full group-hover:bg-red-50 transition-colors duration-200">
                    <Heart
                      class="w-5 h-5 transition-all duration-200"
                      :class="post.is_liked ? 'fill-red-500 stroke-red-500 transform scale-110' : 'stroke-gray-400 group-hover:stroke-red-500'"
                    />
                  </div>
                  <div class="ml-2">
                    <span class="text-base font-semibold" :class="post.is_liked ? 'text-red-500' : 'text-gray-900'">
                      {{ post.likes_count.toLocaleString() }}
                    </span>
                  </div>
                </button>

                <button 
                  @click="showComments(post)"
                  class="group flex items-center px-6"
                >
                  <div class="w-10 h-10 flex items-center justify-center rounded-full group-hover:bg-blue-50 transition-colors duration-200">
                    <MessageCircle
                      class="w-5 h-5 transition-all duration-200"
                      :class="post.showComments ? 'stroke-blue-500 transform scale-110' : 'stroke-gray-400 group-hover:stroke-blue-500'"
                    />
                  </div>
                  <div class="ml-2">
                    <span class="text-base font-semibold" :class="post.showComments ? 'text-blue-500' : 'text-gray-900'">
                      {{ post.comments_count.toLocaleString() }}
                    </span>
                  </div>
                </button>

                <button 
                  @click="sharePost(post)"
                  class="group flex items-center pl-6"
                >
                  <div class="w-10 h-10 flex items-center justify-center rounded-full group-hover:bg-gray-50 transition-colors duration-200">
                    <Share2
                      class="w-5 h-5 transition-all duration-200"
                      :class="'stroke-gray-400 group-hover:stroke-gray-500'"
                    />
                  </div>
                </button>
              </div>

              <div class="flex items-center space-x-1 text-sm text-gray-500">
                <Eye class="w-4 h-4" />
                <span>{{ (post.views_count || 0).toLocaleString() }}</span>
              </div>
            </div>
          </div>

          <!-- Comments section -->
          <div 
            v-if="post.showComments"
            class="bg-gray-50/50 backdrop-blur-sm border-t border-gray-100"
          >
            <div class="p-6 space-y-6">
              <!-- Comments list -->
              <div class="space-y-4">
                <div 
                  v-for="comment in post.comments" 
                  :key="comment.comment_id" 
                  class="flex items-start space-x-3 group"
                >
                  <img 
                    :src="getImageUrl(comment.avatar)" 
                    alt="User avatar" 
                    class="w-10 h-10 rounded-full object-cover border-2 border-white shadow-sm"
                  >
                  <div class="flex-1 bg-white rounded-2xl p-4 shadow-sm group-hover:shadow-md transition-shadow duration-200">
                    <div class="flex items-center justify-between mb-2">
                      <span class="font-bold text-gray-900">{{ comment.username }}</span>
                      <span class="text-xs text-gray-400 flex items-center">
                        <Clock class="w-3 h-3 mr-1" />
                        {{ formatDate(comment.created_at) }}
                      </span>
                    </div>
                    <p class="text-gray-600">{{ comment.content }}</p>
                  </div>
                </div>
              </div>

              <!-- New comment form -->
              <div class="relative">
                <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                  <MessageSquarePlus class="w-5 h-5" />
                </div>
                <input 
                  v-model="newComments[post.post_id]"
                  type="text"
                  placeholder="댓글을 입력하세요..."
                  class="w-full pl-12 pr-12 py-4 bg-white rounded-full border-2 border-gray-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
                  @keyup.enter="addComment(post)"
                >
                <button 
                  @click="addComment(post)"
                  class="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center hover:from-blue-700 hover:to-purple-700 transform hover:scale-110 transition-all duration-200"
                >
                  <Send class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </article>
      </div>
    </main>

    <!-- Floating action button -->
    <router-link 
      to="/community/new"
      class="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg flex items-center justify-center hover:from-blue-700 hover:to-purple-700 transform hover:scale-110 hover:rotate-180 transition-all duration-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
    >
      <PenLine class="w-6 h-6" />
    </router-link>
  </div>
</template>

<script>
import axios from '@/axios'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { 
  Clock, 
  MoreVertical, 
  Edit2, 
  Trash2, 
  Heart, 
  MessageCircle,
  MessageSquarePlus,
  Send,
  PenLine,
  Share2,
  Eye
} from 'lucide-vue-next'

const DEFAULT_AVATAR = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGNpcmNsZSBjeD0iMTAwIiBjeT0iMTAwIiByPSIxMDAiIGZpbGw9IiNFMkU4RjAiLz4KICA8Y2lyY2xlIGN4PSIxMDAiIGN5PSI4NSIgcj0iMzUiIGZpbGw9IiM5NEEzQjgiLz4KICA8cGF0aCBkPSJNMTY1IDE2NS41QzE2NSAxNjUuNSAxNjUgMTM1IDE2NSAxMzVDMTY1IDExMC4xNDcgMTM1LjIyOCA5MCAxMDAgOTBDNjQuNzcxNSA5MCAzNSAxMTAuMTQ3IDM1IDEzNUMzNSAxMzUgMzUgMTY1LjUgMzUgMTY1LjVIMTY1WiIgZmlsbD0iIzk0QTNCOCIvPgo8L3N2Zz4='

export default {
  name: 'Community',
  components: {
    Clock,
    MoreVertical,
    Edit2,
    Trash2,
    Heart,
    MessageCircle,
    MessageSquarePlus,
    Send,
    PenLine,
    Share2,
    Eye
  },
  directives: {
    'click-outside': {
      mounted(el, binding) {
        el.clickOutsideEvent = function(event) {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value(event)
          }
        }
        document.addEventListener('click', el.clickOutsideEvent)
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
      }
    }
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const posts = ref([])
    const newComments = ref({})
    const currentPage = ref(1)
    const totalPages = ref(1)
    const currentUserId = ref(store.state.user?.user_id)

    const imageContainer = ref(null)
    const touchStart = ref({ x: 0, y: 0 })
    const touchEnd = ref({ x: 0, y: 0 })
    const minSwipeDistance = 50

    const fetchPosts = async () => {
      try {
        const response = await axios.get('/api/posts', {
          params: {
            page: currentPage.value,
            per_page: 10
          },
          headers: {
            'Authorization': `Bearer ${store.state.token}`
          }
        })
        posts.value = response.data.posts.map(post => ({
          ...post,
          showComments: false,
          showOptions: false,
          comments: [],
          currentImageIndex: 0,
          translateX: 0,
          isDragging: false,
          containerWidth: 0
        }))
        totalPages.value = response.data.pages
      } catch (error) {
        console.error('Error fetching posts:', error)
        if (error.response?.status === 401) {
          store.dispatch('logout')
          router.push('/login')
        }
      }
    }

    const confirmDelete = async (post) => {
      if (confirm('정말로 이 게시물을 삭제하시겠습니까?')) {
        try {
          await axios.delete(`/api/posts/${post.post_id}`, {
            headers: {
              'Authorization': `Bearer ${store.state.token}`
            }
          })
          posts.value = posts.value.filter(p => p.post_id !== post.post_id)
        } catch (error) {
          console.error('Error deleting post:', error)
          alert('게시물 삭제 중 오류가 발생했습니다.')
        }
      }
    }

    const toggleLike = async (post) => {
      try {
        await axios.post(`/api/posts/${post.post_id}/like`, {}, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`
          }
        })
        post.is_liked = !post.is_liked
        post.likes_count += post.is_liked ? 1 : -1
      } catch (error) {
        console.error('Error toggling like:', error)
        alert('좋아요 처리 중 오류가 발생했습니다.')
      }
    }

    const showComments = async (post) => {
      try {
        const response = await axios.get(`/api/posts/${post.post_id}/comments`, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`
          }
        })
        post.comments = response.data.comments
        post.showComments = !post.showComments
      } catch (error) {
        console.error('Error fetching comments:', error)
        alert('댓글을 불러오는 중 오류가 발생했습니다.')
      }
    }

    const addComment = async (post) => {
      const content = newComments.value[post.post_id]
      if (!content?.trim()) return

      try {
        await axios.post(`/api/posts/${post.post_id}/comments`, 
          { content },
          {
            headers: {
              'Authorization': `Bearer ${store.state.token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        const response = await axios.get(`/api/posts/${post.post_id}/comments`, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`
          }
        })
        post.comments = response.data.comments
        post.comments_count += 1
        newComments.value[post.post_id] = ''
      } catch (error) {
        console.error('Error adding comment:', error)
        alert('댓글 작성 중 오류가 발생했습니다.')
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }

    const sharePost = async (post) => {
      try {
        const shareData = {
          title: post.title,
          text: post.content,
          url: `${window.location.origin}/community/${post.post_id}`
        }

        if (navigator.share && navigator.canShare(shareData)) {
          await navigator.share(shareData)
        } else {
          await navigator.clipboard.writeText(shareData.url)
          alert('링크가 클립보드에 복사되었습니다.')
        }
      } catch (error) {
        console.error('Error sharing:', error)
        if (error.name !== 'AbortError') {
          alert('공유하기에 실패했습니다.')
        }
      }
    }

    const getImageUrl = (url) => {
      if (!url) return DEFAULT_AVATAR
      if (url.startsWith('data:')) return url
      return url
    }

    const onImageLoad = (event) => {
      event.target.classList.add('loaded')
    }

    const setImageIndex = (post, index) => {
      if (!post.images || post.images.length <= 1) return
      post.currentImageIndex = index
      const container = document.querySelector(`[data-post-id="${post.post_id}"] .overflow-hidden`)
      post.containerWidth = container ? container.offsetWidth : window.innerWidth
      post.translateX = -index * post.containerWidth
    }

    const handleTouchStart = (event, post) => {
      if (!post.images || post.images.length <= 1) return
      
      const touch = event.touches[0]
      touchStart.value = { x: touch.clientX, y: touch.clientY }
      touchEnd.value = { x: touch.clientX, y: touch.clientY }
      
      const container = event.currentTarget.querySelector('.overflow-hidden')
      post.containerWidth = container ? container.offsetWidth : window.innerWidth
      post.isDragging = true
      post.startTranslateX = post.translateX || 0
    }

    const handleTouchMove = (event, post) => {
      if (!post.isDragging || !post.images || post.images.length <= 1) return
      
      event.preventDefault()
      const touch = event.touches[0]
      touchEnd.value = { x: touch.clientX, y: touch.clientY }
      
      const deltaX = touchEnd.value.x - touchStart.value.x
      const deltaY = touchEnd.value.y - touchStart.value.y
      
      if (Math.abs(deltaY) > Math.abs(deltaX)) {
        post.isDragging = false
        return
      }
      
      const newTranslateX = post.startTranslateX + deltaX
      const maxTranslateX = 0
      const minTranslateX = -(post.images.length - 1) * post.containerWidth
      
      if (newTranslateX > maxTranslateX) {
        post.translateX = newTranslateX * 0.3
      } else if (newTranslateX < minTranslateX) {
        post.translateX = minTranslateX + (newTranslateX - minTranslateX) * 0.3
      } else {
        post.translateX = newTranslateX
      }
    }

    const handleTouchEnd = (event, post) => {
      if (!post.isDragging || !post.images || post.images.length <= 1) return
      
      post.isDragging = false
      const deltaX = touchEnd.value.x - touchStart.value.x
      
      if (Math.abs(deltaX) > minSwipeDistance) {
        if (deltaX < 0 && post.currentImageIndex < post.images.length - 1) {
          post.currentImageIndex++
        } else if (deltaX > 0 && post.currentImageIndex > 0) {
          post.currentImageIndex--
        }
      }
      
      post.translateX = -post.currentImageIndex * post.containerWidth
    }

    onMounted(() => {
      fetchPosts()
    })

    return {
      posts,
      newComments,
      currentUserId,
      toggleLike,
      showComments,
      addComment,
      formatDate,
      confirmDelete,
      sharePost,
      getImageUrl,
      onImageLoad,
      setImageIndex,
      handleTouchStart,
      handleTouchMove,
      handleTouchEnd,
      imageContainer
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #3B82F6, #7C3AED);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #2563EB, #6D28D9);
}

/* Smooth image loading */
img {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

img[loading] {
  opacity: 0;
  transform: scale(0.95);
}

img.loaded {
  opacity: 1;
  transform: scale(1);
}

/* Add fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Add custom scrollbar for thumbnails */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E0 transparent;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: #CBD5E0;
  border-radius: 3px;
}

/* Add slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-out;
}

.slide-enter-from {
  transform: translateX(100%);
}

.slide-leave-to {
  transform: translateX(-100%);
}

/* Prevent text selection during swipe */
.touch-pan-y {
  touch-action: pan-x;
  user-select: none;
  -webkit-user-select: none;
}

/* Remove slide transition styles as we're using transform now */
.slide-enter-active,
.slide-leave-active,
.slide-enter-from,
.slide-leave-to {
  display: none;
}

/* Add smooth transition for dot indicators */
.dot-indicator {
  transition: all 0.2s ease-out;
}

/* Add smooth transition for image sliding */
.image-slider {
  transition: transform 0.3s ease-out;
}

/* Update touch action for proper swipe handling */
.overflow-hidden {
  touch-action: none;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
}

/* Remove conflicting styles */
.touch-pan-y {
  touch-action: none;
}

/* Optimize for mobile */
@media (hover: none) and (pointer: coarse) {
  .overflow-hidden {
    overscroll-behavior: none;
  }
}
</style>