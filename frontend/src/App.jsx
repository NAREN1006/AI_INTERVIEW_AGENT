import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Interview from "./pages/Interview";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <BrowserRouter>
      
      <div style={{ background: "red", color: "white", padding: "20px" }}>
        NAVBAR TEST
      </div>

      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>

    </BrowserRouter>
  );
}

export default App;