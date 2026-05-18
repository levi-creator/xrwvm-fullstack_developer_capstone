import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import DealerDetails from "./components/DealerDetails";
import Dealers from './components/Dealers/Dealers';
import Register from "./components/Register/Register";
import Home from "./components/Home/Home";




function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/dealer/:id" element={<DealerDetails />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/dealers" element={<Dealers />} />

    </Routes>
  );
}
export default App;
