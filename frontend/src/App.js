import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import DealerDetails from "./components/DealerDetails";


function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/dealer/:id" element={<DealerDetails />} />
    </Routes>
  );
}
export default App;
