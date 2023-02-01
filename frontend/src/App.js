import Registration from "./components/Registration";
import { Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import MonitorBrand from "./components/MonitorBrand";
import Mentions from "./components/Mentions/Mentions";
import Comparison from "./components/Comparison/Comparison";
import Dashboard from "./components/Dashboard";
import PageNotFound from "./components/PageNotFound";
import Report from "./components/Reports/Report";
import ForgotPassword from "./components/ForgotPassword";
import AboutUs from "./components/AboutUs";
import ContactUs from "./components/ContactUs";
import Welcome from "./components/Welcome";
function App() {
  return (
    <>
      <div className="h-screen">
        <Routes>
          <Route path="/" element={<Registration />} />
          <Route path="login" element={<Login />} />
          <Route path="forgot-password" element={<ForgotPassword />} />
          <Route path="monitor" element={<MonitorBrand />} />
          <Route path="mentions" element={<Mentions />} />
          <Route path="comparison" element={<Comparison />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="report" element={<Report />} />
          <Route path="aboutus" element={<AboutUs />} />
          <Route path="contactus" element={<ContactUs />} />
          <Route path="welcome" element={<Welcome />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
