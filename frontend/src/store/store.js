import { createStore } from "vuex";
import axios from "./axios"; // Axios 인스턴스 임포트

export default createStore({
  state: {
    isAuthenticated: !!localStorage.getItem("token"),
    user: JSON.parse(localStorage.getItem("user")) || null,
    token: localStorage.getItem("token") || null,
  },
  mutations: {
    setAuth(state, payload) {
      state.isAuthenticated = payload.isAuthenticated;
      state.user = payload.user;
      state.token = payload.token;
    },
    clearAuth(state) {
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
    },
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const response = await axios.post("/api/login", { username, password });
        const { token, user } = response.data;

        // 토큰 및 사용자 정보 저장
        localStorage.setItem("token", token);
        localStorage.setItem("user", JSON.stringify(user));

        commit("setAuth", {
          isAuthenticated: true,
          user: user,
          token: token,
        });
      } catch (error) {
        throw error;
      }
    },
    logout({ commit }) {
      // 토큰 및 사용자 정보 삭제
      localStorage.removeItem("token");
      localStorage.removeItem("user");

      commit("clearAuth");
    },
    async fetchUserProfile({ commit }) {
      try {
        const response = await axios.get("/api/profile");
        const userData = response.data;

        commit("setAuth", {
          isAuthenticated: true,
          user: userData,
          token: state.token, // 기존 토큰 유지
        });
      } catch (error) {
        console.error("프로필 정보를 가져오는데 실패했습니다:", error);
        commit("clearAuth");
      }
    },
  },
  getters: {
    isAuthenticated(state) {
      return state.isAuthenticated;
    },
    user(state) {
      return state.user;
    },
  },
});
