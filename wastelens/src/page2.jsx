import React from "react";
import { useNavigate } from "react-router-dom";
import "./page2.css";
import logo2 from "./logo3.png";
function LensPage() {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate("/result");
  };
  return (
    <div className="lens">
      <div className="contents">
        <div className="top">
          <img src={logo2} className="logo2" alt="logo" />
        </div>
        <div className="middle">
          <h2>쓰레기를 촬영해주세요.</h2>
          <div className="lensArea"></div>
          <h2>Tip.</h2>
          <p>
            '가축이 먹을 수 있는지'를
            <br />
            생각해보면, 쓰레기를 분류할 수 있습니다.
          </p>
        </div>
        <div className="bottom">
          <button class="my-button" onClick={handleButtonClick}>
            <span>결과 확인하기</span>
          </button>
        </div>
      </div>
    </div>
  );
}
function Page2() {
  return <LensPage />;
}

export default Page2;
