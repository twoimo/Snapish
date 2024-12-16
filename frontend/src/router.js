import { createRouter, createWebHistory } from "vue-router";
import store from "./store"; // 스토어 임포트

// 컴포넌트 임포트
import Home from "./views/Home.vue";
import Community from "./views/Community.vue";
import MapLocationService from "./views/MapLocationService.vue";
import Profile from "./views/Profile.vue";
import FishResultNormal from "./views/FishResultNormal.vue";
import FishResultWarning from "./views/FishResultWarning.vue";
import Login from "./views/Login.vue";
import EditProfile from "./views/EditProfile.vue"; // 프로필 수정 컴포넌트 임포트
import Signup from "./views/Signup.vue"; // Signup 컴포넌트 임포트
import Catches from "./views/Catches.vue"; // Catches 컴포넌트 임포트

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
    path: "/map-location-service",
    name: "MapLocationService",
    component: MapLocationService, // 날씨 상세 정보 컴포넌트
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile, // 프로필 컴포넌트
    meta: { requiresAuth: true }, // 인증이 필요한 라우트로 설정
  },
  {
    path: "/fish-result-normal",
    name: "FishResultNormal",
    component: FishResultNormal,
    props: (route) => {
      try {
        const detections = decodeURIComponent(route.query.detections);
        console.log("Decoded detections in router:", detections); // 추가된 로그
        return {
          detections,
          imageUrl: route.query.imageUrl,
        };
      } catch (error) {
        console.error("Error decoding detections:", error);
        return {
          detections: "[]",
          imageUrl: route.query.imageUrl,
        };
      }
    },
  },
  {
    path: "/fish-result-warning",
    name: "FishResultWarning",
    component: FishResultWarning, // 물고기 경고 컴포넌트
  },
  {
    path: "/login",
    name: "Login",
    component: Login, // 로그인 컴포넌트 추가
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup, // 회원가입 컴포넌트 추가
  },
  {
    path: "/edit-profile",
    name: "EditProfile",
    component: EditProfile, // 프로필 수정 컴포넌트 추가
    meta: { requiresAuth: true },
  },
  {
    path: "/catches",
    name: "Catches",
    component: Catches, // Catches 컴포넌트 추가
  },
];

// 라우터 생성
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 네비게이션 가드 설정 (인증 여부 확인)
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthenticated = store.getters.isAuthenticated;

  if (requiresAuth && !isAuthenticated) {
    // 토큰이 있을 경우 스토어에 사용자 정보 로드 시도
    if (localStorage.getItem("token")) {
      try {
        await store.dispatch("fetchUserProfile");
        next();
      } catch (error) {
        console.error("Error fetching user profile:", error);
        next("/login");
      }
    } else {
      next("/login");
    }
  } else {
    next();
  }
});

// 전역 에러 핸들러 추가
router.onError((error) => {
  console.error("Router error:", error);
});

// 추가된 비동기 응답 처리
router.afterEach((to, from) => {
  console.log(`Navigation to ${to.fullPath} from ${from.fullPath} completed.`);
});

// 추가된 비동기 응답 처리
router.afterEach((to, from) => {
  setTimeout(() => {
    console.log(
      `Navigation to ${to.fullPath} from ${from.fullPath} completed.`
    );
  }, 0);
});

export default router;
