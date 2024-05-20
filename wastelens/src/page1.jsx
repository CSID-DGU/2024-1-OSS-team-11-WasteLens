import React from "react";
import { useNavigate } from "react-router-dom";
import "./page1.css";
import bigLogo from "./logo.png";
import lens from "./lens.png";
function MainPage() {
  const navigate = useNavigate();

  // 버튼 클릭 시 라우팅 함수
  const handleButtonClick = () => {
    navigate("/lens");
  };
  return (
    <div className="main">
      <div className="contents">
        <h2>당신의 쓰레기를 보여주세요.</h2>
        <img src={bigLogo} className="bigLogo" alt="logo" />
        <div className="intro">
          <span className="text_b">'WASTELENS'</span>는 <br />
          간단한 사진 촬영을 통해
          <br />
          음식물쓰레기를 구분해드립니다.
        </div>
        <div className="buttonArea">
          <button class="my-button" onClick={handleButtonClick}>
            <img src={lens} className="lensLogo" alt="lensLogo" />
            <span>쓰레기 스캔</span>
          </button>
        </div>
      </div>
    </div>
  );
}
function Page1() {
  return <MainPage />;
}

export default Page1;
