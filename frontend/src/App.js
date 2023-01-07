import Registration from "./components/Registration";
import { Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import MonitorBrand from "./components/MonitorBrand";
import Mentions from "./components/Mentions/Mentions";
import Comparison from "./components/Comparison/Comparison";
import Dashboard from "./components/Dashboard";
import PageNotFound from "./components/PageNotFound";
import Report from "./components/Reports/Report";
import SentimentGraph from "./components/Mentions/SentimentGraph";

function App() {
  return (
    <>
      <div className="h-screen">
        <Routes>
          <Route path="/" element={<Registration />} />
          <Route path="login" element={<Login />} />
          <Route path="monitor" element={<MonitorBrand />} />
          <Route path="mentions" element={<Mentions />} />
          <Route path="comparison" element={<Comparison />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="report" element={<Report />} />
          <Route path="*" element={<PageNotFound />} />
          <Route path="line" element={<SentimentGraph/>}/>
        </Routes>
      </div>
    </>
  );
}

export default App;
