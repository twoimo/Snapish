import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import Community from "./views/Community.vue";
import Profile from "./views/Profile.vue";
import FishWarning from "./views/FishWarning.vue";
import FishDetectionResult from "./views/FishDetectionResult.vue";

// 라우트 설정
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home, // 홈 컴포넌트
  },
  {
    path: "/community",
    name: "Community",
    component: Community, // 커뮤니티 컴포넌트
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile, // 프로필 컴포넌트
  },
  {
    path: "/fish-detection-result",
    name: "FishDetectionResult",
    component: FishDetectionResult, // 물고기 감지 결과 컴포넌트
  },
  {
    path: "/fish-warning",
    name: "FishWarning",
    component: FishWarning, // 물고기 경고 컴포넌트
  },
];

// 라우터 생성
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // 웹 히스토리 모드 사용
  routes, // 설정한 라우트들
});

export default router; // 라우터 내보내기
