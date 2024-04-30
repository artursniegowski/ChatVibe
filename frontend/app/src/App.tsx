// import React from "react";
import Home from "./pages/Home";
import Explore from "./pages/Home";
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom";
import ToggleColorMode from "./components/ToggleColorMode";
import Server from "./pages/Server";
import Login from "./pages/Login";
import { AuthServiceProvider } from "./context/AuthContext";
import TestLogin from "./pages/templates/TestLogin";
import ProtectedRoute from "./services/ProtectedRoute";

// channelId? -> making the uri parameter optional
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={ <Home />} />
      <Route path="/server/:serverId/:channelId?" element={ <Server />} />
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
    </Route>
  )
);

const App = () => {
  return (
    <AuthServiceProvider>
      <ToggleColorMode >
        <RouterProvider router={router} />
      </ToggleColorMode>
    </AuthServiceProvider>
  ); 
};

// or with typescript
// React.FC specifies the type
// const App: React.FC = () => {
//   return <RouterProvider router={router} />;
// };

export default App;
