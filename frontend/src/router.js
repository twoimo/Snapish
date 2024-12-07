import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import FishWarning from "./views/FishWarning.vue";
import Profile from "./views/Profile.vue";
import Questions from "./views/Questions.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/fish-warning",
    name: "FishWarning",
    component: FishWarning,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/questions",
    name: "Questions",
    component: Questions,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
