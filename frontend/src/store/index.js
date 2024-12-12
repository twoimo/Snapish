import { createStore } from "vuex";
import { getCurrentLocation } from "../services/locationService";
import { fetchMulddae } from "../services/mulddaeService";

export default createStore({
  state: {
    currentlocation: null,
    loading: false,
    error: null,
    mulddae: null, // 물때 정보 추가
  },
  mutations: {
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
  },
  actions: {
    async fetchLocation({ commit }) {
      console.log("vuex : fetchLocation action triggered.");
      commit("setLoading", true);
      commit("setError", null);

      try {
        const { latitude, longitude } = await getCurrentLocation();

        if (latitude && longitude) {
          const currentloc = [latitude, longitude];
          console.log(`success : Fetch Location action ${currentloc}`);
          commit("setCurrentLocation", currentloc);
        } else {
          commit("setError", "No Location data found.");
        }
      } catch (error) {
        commit("setError", error);
      } finally {
        commit("setLoading", false);
      }
    },
    async fetchMulddae({ commit }, nowdate) {
      console.log("vuex : fetchMulddae action triggered.");
      commit("setLoading", true);

      try {
        // localStorage에서 데이터 확인
        const cachedMulddae = localStorage.getItem("mulddae");
        if (cachedMulddae) {
          console.log("success : Loaded mulddae from localStorage.");
          commit("setMulddae", JSON.parse(cachedMulddae));
        } else {
          // 백엔드에서 데이터 가져오기
          console.log("failed : Can't loaded mulddae from localStorage.");
          const mulddaeData = await fetchMulddae(nowdate);
          if (mulddaeData.error) {
            throw new Error(mulddaeData.error);
          } 
          // localStorage에 저장
          localStorage.setItem("mulddae", JSON.stringify(mulddaeData));
          commit("setMulddae", mulddaeData);
        }
      } catch (error) {
        console.error("error : Failed to fetch mulddae.", error);
        commit("setError", error.message || "Failed to fetch mulddae.");
      } finally {
        commit("setLoading", false);
      }
    },
  },
});
