import axios from "@/axios"; // Axios 인스턴스 임포트

const apiBaseUrl = process.env.VUE_APP_MULDDAE_URL;

export async function fetchMulddae(date) {
  console.log(`Call_fetchMulddae : ${date}`);
  try {
    const response = await axios.post(
      apiBaseUrl,
      new URLSearchParams({ nowdate: date }).toString(),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching mulddae data:", error);
    return { error: error.message };
  }
}
