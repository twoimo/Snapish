import { createStore } from "vuex";
import axios from "@/axios"; // Ensure the correct path to axios.js
import { getCurrentLocation } from "../services/locationService";
import { fetchMulddae } from "../services/mulddaeService";

export default createStore({
  state: {
    // Existing state
    currentlocation: null,
    loading: false,
    error: null,
    mulddae: null, // 물때 정보 추가
    mulddaeDate: null,

    // Authentication state
    isAuthenticated: !!localStorage.getItem("token"),
    user: JSON.parse(localStorage.getItem("user")) || null,
    token: localStorage.getItem("token") || null,
  },
  mutations: {
    // Existing mutations
    setCurrentLocation(state, currentlocation) {
      state.currentlocation = currentlocation;
    },
    setLoading(state, isLoading) {
      state.loading = isLoading;
    },
    setError(state, error) {
      state.error = error;
    },
    setMulddae(state, mulddae) {
      state.mulddae = mulddae; // 물때 정보 업데이트
    },

    // Authentication mutations
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
    // Existing actions
    async fetchMulddae({ commit }) {
      console.log("vuex : fetchMulddae action triggered.");
      commit("setLoading", true);

      try {
        // localStorage에서 데이터 확인
        const cachedMulddae = localStorage.getItem("mulddae");
        console.log(`cachedmulddae : ${cachedMulddae}`);
        const cachedDate = localStorage.getItem("mulddaeDate"); // 이전에 저장된 날짜
        const today = new Date().toISOString().split("T")[0]; // 오늘 날짜 (yyyy-mm-dd 형식)

        if (cachedMulddae && cachedDate === today) {
          // 저장된 데이터와 오늘 날짜가 같다면, 캐시된 데이터를 사용
          console.log("success : Loaded mulddae from localStorage.");
          commit("setMulddae", JSON.parse(cachedMulddae));
        } else {
          // 날짜가 다르거나 데이터가 없는 경우
          if (!cachedDate) {
            console.log(
              "info : mulddaeDate is not found in localStorage, fetching new data."
            );
          } else if (cachedDate !== today) {
            console.log(
              "info : Cached date is different from today, fetching new data."
            );
          }

          const location = await getCurrentLocation();
          const mulddaeData = await fetchMulddae(
            location.latitude,
            location.longitude
          );
          commit("setMulddae", mulddaeData);

          // 캐시에 저장
          localStorage.setItem("mulddae", JSON.stringify(mulddaeData));
          localStorage.setItem("mulddaeDate", today);
        }
      } catch (error) {
        console.error("Error fetching mulddae:", error);
        commit("setError", error);
      } finally {
        commit("setLoading", false);
      }
    },

    // Authentication actions
    async login({ commit }, { username, password }) {
      try {
        const response = await axios.post("/login", { username, password });
        const { token, user } = response.data;

        // 저장소와 로컬 스토리지 업데이트
        localStorage.setItem("token", token);
        localStorage.setItem("user", JSON.stringify(user));

        commit("setAuth", {
          isAuthenticated: true,
          user: user,
          token: token,
        });
      } catch (error) {
        console.error("Login error:", error);
        throw error;
      }
    },
    async signup(_, { username, email, password }) {
      try {
        await axios.post("/signup", { username, email, password });
        // 회원가입 성공 후 추가 로직
      } catch (error) {
        console.error("Signup error:", error);
        throw error;
      }
    },
    logout({ commit }) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      commit("clearAuth");
    },
    async fetchUserProfile({ commit }) {
      try {
        const response = await axios.get("/profile");
        const userData = response.data;
        commit("setAuth", {
          isAuthenticated: true,
          user: userData,
          token: localStorage.getItem("token"),
        });
      } catch (error) {
        console.error("Fetch user profile error:", error);
        commit("clearAuth");
        throw error;
      }
    },
    async updateProfile({ commit, state }, payload) {
      try {
        const response = await axios.put("/profile", payload);
        const updatedUser = response.data;
        localStorage.setItem("user", JSON.stringify(updatedUser));
        commit("setAuth", {
          isAuthenticated: true,
          user: updatedUser,
          token: state.token,
        });
      } catch (error) {
        console.error("Update profile error:", error);
        throw error;
      }
    },
  },
  getters: {
    // Existing getters
    isAuthenticated(state) {
      return state.isAuthenticated;
    },
    user(state) {
      return state.user;
    },
  },
});
