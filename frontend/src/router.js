import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import Community from "./views/Community.vue";
import Profile from "./views/Profile.vue";
import FishWarning from "./views/FishWarning.vue";
import FishDetectionResult from "./views/FishDetectionResult.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/community",
    name: "Community",
    component: Community,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/fish-detection-result",
    name: "FishDetectionResult",
    component: FishDetectionResult,
  },
  {
    path: "/fish-warning",
    name: "FishWarning",
    component: FishWarning,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
