<template>
  <div class="min-h-screen bg-white">
    <main class="h-screen flex flex-col">
      <!-- Top action bar -->
      <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <button 
          @click="$router.go(-1)"
          class="p-2 -ml-2 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100/80 transition-all duration-200"
        >
          <X class="w-6 h-6" />
        </button>
        <div class="flex items-center space-x-3">
          <button
            v-if="$route.params.id"
            @click="confirmDelete"
            class="p-2 text-red-500 hover:text-red-600 rounded-full hover:bg-red-50 transition-all duration-200"
          >
            <Trash2 class="w-5 h-5" />
          </button>
          <button
            type="button"
            @click="submitEdit"
            :disabled="isSubmitting"
            class="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
          >
            <Save class="w-4 h-4" />
            <span>{{ isSubmitting ? '저장 중...' : (post ? '수정' : '작성') }}</span>
          </button>
        </div>
      </div>

      <!-- Content area -->
      <div class="flex-1 overflow-y-auto">
        <form @submit.prevent="submitEdit" class="h-full">
          <div class="p-4 space-y-6">
            <!-- Title input -->
            <div>
              <input
                type="text"
                v-model="title"
                required
                class="w-full text-2xl font-bold bg-transparent border-0 focus:ring-0 p-0 placeholder-gray-400"
                placeholder="제목을 입력하세요"
              >
            </div>

            <!-- Content input -->
            <div>
              <textarea
                v-model="content"
                required
                rows="8"
                class="w-full text-lg bg-transparent border-0 focus:ring-0 p-0 placeholder-gray-400 resize-none"
                placeholder="내용을 입력하세요"
              ></textarea>
            </div>

            <!-- Image upload -->
            <div>
              <div 
                class="relative group cursor-pointer"
                :class="{'border-2 border-dashed border-gray-200 rounded-2xl hover:border-blue-400 transition-colors duration-200': !imagePreview && !post?.image_url}"
              >
                <!-- Empty state -->
                <div 
                  v-if="!imagePreview && !post?.image_url" 
                  class="flex flex-col items-center justify-center py-12"
                  @click="$refs.fileInput.click()"
                >
                  <div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                    <ImagePlus class="w-8 h-8 text-blue-500" />
                  </div>
                  <div class="text-center">
                    <p class="text-sm font-medium text-gray-900 mb-1">이미지를 업로드하세요</p>
                    <p class="text-xs text-gray-500">PNG, JPG, GIF (최대 10MB)</p>
                  </div>
                </div>

                <!-- Preview state -->
                <div v-else class="relative rounded-2xl overflow-hidden group">
                  <img
                    :src="imagePreview || post?.image_url"
                    alt="Preview"
                    class="w-full object-cover rounded-2xl transform group-hover:scale-105 transition-transform duration-500"
                    style="max-height: 32rem;"
                  >
                  <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
                    <button
                      type="button"
                      @click="removeImage"
                      class="bg-white/10 backdrop-blur-sm text-white rounded-full p-3 hover:bg-white/20 transform hover:scale-110 transition-all duration-200"
                    >
                      <Trash2 class="w-6 h-6" />
                    </button>
                  </div>
                </div>

                <input
                  ref="fileInput"
                  type="file"
                  class="hidden"
                  accept="image/*"
                  @change="handleImageUpload"
                >
              </div>
            </div>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script>
import axios from '@/axios'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { X, Save, Trash2, ImagePlus } from 'lucide-vue-next'

export default {
  name: 'EditPost',
  components: {
    X,
    Save,
    Trash2,
    ImagePlus
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const post = ref(null)
    const title = ref('')
    const content = ref('')
    const imageFile = ref(null)
    const imagePreview = ref(null)
    const isSubmitting = ref(false)
    const shouldRemoveImage = ref(false)

    const fetchPost = async () => {
      if (!route.params.id) return

      try {
        const response = await axios.get(`/api/posts/${route.params.id}`)
        post.value = response.data
        title.value = post.value.title
        content.value = post.value.content
        if (post.value.image_url) {
          imagePreview.value = post.value.image_url
        }
      } catch (error) {
        console.error('Error fetching post:', error)
        router.push('/community')
      }
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 10 * 1024 * 1024) {
        alert('이미지 크기는 10MB를 초과할 수 없습니다.')
        return
      }

      imageFile.value = file
      shouldRemoveImage.value = false
      const reader = new FileReader()
      reader.onload = (e) => {
        imagePreview.value = e.target.result
      }
      reader.readAsDataURL(file)
    }

    const removeImage = () => {
      imageFile.value = null
      imagePreview.value = null
      shouldRemoveImage.value = true
      if (post.value) {
        post.value.image_url = null
      }
    }

    const submitEdit = async () => {
      if (isSubmitting.value) return
      isSubmitting.value = true

      try {
        const formData = new FormData()
        formData.append('title', title.value)
        formData.append('content', content.value)
        if (imageFile.value) {
          formData.append('image', imageFile.value)
        }
        if (shouldRemoveImage.value) {
          formData.append('remove_image', 'true')
        }

        if (route.params.id) {
          await axios.post(`/api/posts/${route.params.id}/edit`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        } else {
          await axios.post('/api/posts', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        }

        router.push('/community')
      } catch (error) {
        console.error('Error saving post:', error)
        alert(route.params.id ? '게시물 수정 중 오류가 발생했습니다.' : '게시물 작성 중 오류가 발생했습니다.')
      } finally {
        isSubmitting.value = false
      }
    }

    const confirmDelete = async () => {
      if (confirm('정말로 이 게시물을 삭제하시겠습니까?')) {
        try {
          await axios.post(`/api/posts/${route.params.id}/delete`)
          router.push('/community')
        } catch (error) {
          console.error('Error deleting post:', error)
          alert('게시물 삭제 중 오류가 발생했습니다.')
        }
      }
    }

    onMounted(() => {
      fetchPost()
    })

    return {
      post,
      title,
      content,
      imagePreview,
      isSubmitting,
      handleImageUpload,
      removeImage,
      submitEdit,
      confirmDelete
    }
  }
}
</script>

<style scoped>
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

/* Custom scrollbar */
textarea {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E0 #EDF2F7;
}

textarea::-webkit-scrollbar {
  width: 4px;
}

textarea::-webkit-scrollbar-track {
  background: transparent;
}

textarea::-webkit-scrollbar-thumb {
  background: #CBD5E0;
  border-radius: 2px;
}

/* Remove autofill background */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
textarea:-webkit-autofill,
textarea:-webkit-autofill:hover,
textarea:-webkit-autofill:focus {
  -webkit-box-shadow: 0 0 0px 1000px white inset;
  transition: background-color 5000s ease-in-out 0s;
}
</style> 