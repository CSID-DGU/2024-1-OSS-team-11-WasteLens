import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./page3.css";
import logo2 from "./logo3.png";

function ResultPage() {
  const location = useLocation();
  const detectionResults = location.state?.detectionResults || [];
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate("/");
  };

  const labelMapping = {
    "chicken": "치킨 뼈",
    "watermelon": "수박",
    "apple": "사과",
    "pineapple": "파인애플",
    "onion": "양파",
    "seashell": "조개 껍질",
    "corn": "옥수수"
  };

  const getResultType = (label) => {
    const foodWasteLabels = ["수박", "사과"];
    const generalWasteLabels = ["치킨 뼈", "파인애플", "양파", "조개 껍질", "옥수수"];

    if (foodWasteLabels.includes(label)) {
      return "음식물 쓰레기";
    } else if (generalWasteLabels.includes(label)) {
      return "일반 쓰레기";
    } else {
      return "알 수 없음";
    }
  };

  const getResultColor = (resultType) => {
    return resultType === "일반 쓰레기" ? "generalW" : "foodW";
  };

  return (
    <div className="lens">
      <div className="contents">
        <div className="top">
          <img src={logo2} className="logo2" alt="logo" />
        </div>
        <div className="middle3">
          <div className="resultArea">
            <div>당신의 쓰레기</div>
            {detectionResults.length > 0 ? (
              detectionResults.map((result, index) => {
                const mappedLabel = labelMapping[result.label] || result.label;
                const resultType = getResultType(mappedLabel);
                const resultColor = getResultColor(resultType);
                return (
                  <div key={index} className="resultItem">
                    <div><span className="typeText">{mappedLabel}</span>(은)는</div>
                    <div><span className={`resultText ${resultColor}`}>{resultType}</span>입니다.</div>
                  </div>
                );
              })
            ) : (
              <>
                <div>이미지에서 쓰레기가</div>
                <div>검출되지 않았습니다.</div>
              </>
            )}
          </div>
          <h2>Tip.</h2>
          <p>
            음식물 - 수박, 귤, 사과
            <br />
            일반 - 치킨뼈, 조개, 파인애플, 옥수수, 양파
          </p>
        </div>
        <div className="bottom">
          <button className="my-button" onClick={handleButtonClick}>
            <span>다시 물어보기</span>
          </button>
        </div>
      </div>
    </div>
  );
}

function Page3() {
  return <ResultPage />;
}

export default Page3;