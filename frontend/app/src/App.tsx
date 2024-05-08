// import React from "react";
import Home from "./pages/Home";
import Explore from "./pages/Home";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ToggleColorMode from "./components/ToggleColorMode";
import Server from "./pages/Server";
import Login from "./pages/Login";
import { AuthServiceProvider } from "./context/AuthContext";
import TestLogin from "./pages/templates/TestLogin";
import ProtectedRoute from "./services/ProtectedRoute";



const App = () => {
  return (
    <BrowserRouter>
    <AuthServiceProvider>
      <ToggleColorMode >
        <Routes>
          <Route path="/" element={ <Home />} />
          <Route 
            path="/server/:serverId/:channelId?" 
            element=
              { 
                <ProtectedRoute>
                  <Server />
                </ProtectedRoute>
              } 
          />
          <Route path="/explore/:categoryName" element={ <Explore />} />
          <Route path="/login" element={ <Login />} />
          <Route 
            path="/testlogin" 
            element={
              <ProtectedRoute>
                <TestLogin />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </ToggleColorMode>
    </AuthServiceProvider>
    </BrowserRouter>
  ); 
};

export default App;
