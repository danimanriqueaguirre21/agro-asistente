import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import HomePage from "./pages/HomePage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import ContextPage from "./pages/ContextPage.jsx";
import QueryPage from "./pages/QueryPage.jsx";
import KnowledgePage from "./pages/KnowledgePage.jsx";
import RiskPage from "./pages/RiskPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/context" element={<ContextPage />} />
        <Route path="/query" element={<QueryPage />} />
        <Route path="/knowledge" element={<KnowledgePage />} />
        <Route path="/riesgo" element={<RiskPage />} />
      </Route>
    </Routes>
  );
}
