import { createStore } from "vuex";
import { getCurrentLocation } from "../services/locationService";
// import { fetchWeatherByCoordinates } from "../services/weatherService";

export default createStore({
  state: {
    // weather: JSON.parse(localStorage.getItem("weather")) || null,
    currentlocation: null,
    loading: false,
    error: null,
    // lastupdated: (() => {
    //   const weatherData = JSON.parse(localStorage.getItem("weather"));
    //   return weatherData?.current?.last_updated || null; // 안전하게 last_updated 추출
    // })(),
  },
  mutations: {
    // setWeather(state, weather) {
    //   state.weather = weather;
    //   localStorage.setItem("weather", JSON.stringify(weather));
    // },
    setCurrentLocation(state, currentlocation) {
      state.currentlocation = currentlocation;
    },
    setLoading(state, isLoading) {
      state.loading = isLoading;
    },
    setError(state, error) {
      state.error = error;
    },
    // setLastUpdated(state, lastUpdated) {
    //   state.lastupdated = lastUpdated;
    //   localStorage.setItem("lastupdated", lastUpdated);
    // },
  },
  actions: {
    async fetchLocation({ commit }) {
      console.log("vuex : fetchLocation action triggered."); // 액션 호출 확인
      commit("setLoading", true);
      commit("setError", null);

      try {
        const { latitude, longitude } = await getCurrentLocation();

        if (latitude && longitude) {
          const currentloc = [latitude, longitude]
          commit("setCurrentLocation", currentloc)
        }else {
          commit("setError", "No Location data found.");
        }
        } catch (error) {
          commit("setError", error);
        } finally {
          commit("setLoading", false);
        }
      },
    },
    //     const weatherData = await fetchWeatherByCoordinates(latitude, longitude);

    //     if (weatherData) {
    //       const lastUpdated = weatherData.current.last_updated;
    //       console.log(`check: ${ lastUpdated } `)
    //       commit("setWeather", weatherData);
    //       commit("setLastUpdated", lastUpdated);
    //     } else {
    //       commit("setError", "No weather data found.");
    //     }
    //   } catch (error) {
    //     const defaultLat = 37.5665; // 위치 권한을 받아올 수 없는 경우
    //     const defaultLon = 126.9780;
    //     try {
    //       const weatherData = await fetchWeatherByCoordinates(defaultLat, defaultLon);
    //       if (weatherData) {
    //         commit("setWeather", weatherData); // 서울 데이터 저장
    //         commit("setLastUpdated", weatherData.last_updated); // 현재 시간을 last_updated에 저장
    //       } else {
    //         commit("setError", "No fallback weather data found.");
    //       }
    //     } catch (fallbackError) {
    //       commit("setError", "Failed to fetch weather data.");
    //     }
    //   } finally {
    //     commit("setLoading", false);
    //   }
    // }
  }
)