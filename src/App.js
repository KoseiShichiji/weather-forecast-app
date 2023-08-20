import React, { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = React.useState();
  const [city, setCity] = useState("");
  // const [city, setSelectedPrefecture] = useState("");
  const url = "http://127.0.0.1:8000";

  const prefectures = [
    { id: 1, name: "北海道", roman: "hokkaido" },
    { id: 2, name: "青森", roman: "aomori" },
    { id: 3, name: "岩手", roman: "iwate" },
    { id: 4, name: "宮城", roman: "miyagi" },
    { id: 5, name: "秋田", roman: "akita" },
    { id: 6, name: "山形", roman: "yamagata" },
    { id: 7, name: "福島", roman: "fukushima" },
    { id: 8, name: "茨城", roman: "ibaraki" },
    { id: 9, name: "栃木", roman: "tochigi" },
    { id: 10, name: "群馬", roman: "gunma" },
    { id: 11, name: "埼玉", roman: "saitama" },
    { id: 12, name: "千葉", roman: "chiba" },
    { id: 13, name: "東京", roman: "tokyo" },
    { id: 14, name: "神奈川", roman: "kanagawa" },
    { id: 15, name: "新潟", roman: "niigata" },
    { id: 16, name: "富山", roman: "toyama" },
    { id: 17, name: "石川", roman: "ishikawa" },
    { id: 18, name: "福井", roman: "fukui" },
    { id: 19, name: "山梨", roman: "yamanashi" },
    { id: 20, name: "長野", roman: "nagano" },
    { id: 21, name: "岐阜", roman: "gifu" },
    { id: 22, name: "静岡", roman: "shizuoka" },
    { id: 23, name: "愛知", roman: "aichi" },
    { id: 24, name: "三重", roman: "mie" },
    { id: 25, name: "滋賀", roman: "shiga" },
    { id: 26, name: "京都", roman: "kyoto" },
    { id: 27, name: "大阪", roman: "osaka" },
    { id: 28, name: "兵庫", roman: "hyogo" },
    { id: 29, name: "奈良", roman: "nara" },
    { id: 30, name: "和歌山", roman: "wakayama" },
    { id: 31, name: "鳥取", roman: "tottori" },
    { id: 32, name: "島根", roman: "shimane" },
    { id: 33, name: "岡山", roman: "okayama" },
    { id: 34, name: "広島", roman: "hiroshima" },
    { id: 35, name: "山口", roman: "yamaguchi" },
    { id: 36, name: "徳島", roman: "tokushima" },
    { id: 37, name: "香川", roman: "kagawa" },
    { id: 38, name: "愛媛", roman: "ehime" },
    { id: 39, name: "高知", roman: "kochi" },
    { id: 40, name: "福岡", roman: "fukuoka" },
    { id: 41, name: "佐賀", roman: "saga" },
    { id: 42, name: "長崎", roman: "nagasaki" },
    { id: 43, name: "熊本", roman: "kumamoto" },
    { id: 44, name: "大分", roman: "oita" },
    { id: 45, name: "宮崎", roman: "miyazaki" },
    { id: 46, name: "鹿児島", roman: "kagoshima" },
    { id: 47, name: "沖縄", roman: "okinawa" },
  ];

  const handleSelectChange = (e) => {
    setCity(e.target.value);
  };

  const GetData = async () => {
    try {
      const response = await axios.get(`${url}/weather?city=${city}`);
      // console.log("response", response.data.result_from_mysql);
      // console.log("response1", response.data.result_from_mysql[0]);
      setData(response.data.result_from_mysql);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // アイコンコードからアイコン画像取得
  const getIconUrl = (iconCode) => {
    return `http://openweathermap.org/img/w/${iconCode}.png`;
  };

  //APIからデータ取得
  // const GetApiData = async () => {
  //   try {
  //     const response = await axios.get(`${url}/weatherAPI?city=${city}`);
  //     console.log("response", response.data.result_from_api);
  //   } catch (error) {
  //     console.error("Error fetching data:", error);
  //   }
  // };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "50vh",
      }}
    >
      {/* <button onClick={GetApiData}>データインサート</button> */}
      <div>天気予報</div>
      <select value={city} onChange={handleSelectChange}>
        <option>都道府県を選択してください</option>
        {prefectures.map((prefecture) => (
          <option key={prefecture.id} value={prefecture.roman}>
            {prefecture.name}
          </option>
        ))}
      </select>
      <button onClick={GetData}>検索</button>
      {data ? (
        <div>
          <p>天気: {data[0][0]}</p>{" "}
          {data[0][1] && (
            <img src={getIconUrl(data[0][1])} alt="Weather Icon" />
          )}
        </div>
      ) : null}
    </div>
  );
}

export default App;
