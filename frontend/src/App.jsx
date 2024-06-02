import React from "react";

import { Routes, Route } from "react-router-dom";
import Page1 from "./page1";
import Page2 from "./page2";
import Page3 from "./page3";
import "./App.css";

const App = () => {
  return (
    <Routes>
      <Route index element={<Page1 />} />
      <Route path="/lens" element={<Page2 />} />
      <Route path="/result" element={<Page3 />} />
    </Routes>
  );
};

export default App;
