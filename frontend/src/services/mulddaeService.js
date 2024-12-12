const apiBaseUrl = process.env.VUE_APP_MULDDAE_URL;

export async function fetchMulddae(date) {
  try {
    const response = await fetch(apiBaseUrl, {
      method: 'POST', // POST 요청 방식 설정
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // URL 인코딩된 데이터 전송
      },
      body: `nowdate=${encodeURIComponent(date)}`, // 문자열 형태로 데이터 전송
    });

    if (!response.ok) throw new Error(`Error: ${response.status}`);

    const data = await response.json();
    console.log("mulddaeService : Getmulddae");
    return data;
  } catch (error) {
    console.error("Error fetching mulddae data:", error);
    return { error: error.message };
  }
}
