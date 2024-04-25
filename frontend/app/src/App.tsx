// import React from "react";
import Home from "./pages/Home";
import Explore from "./pages/Home";
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom";
import ToggleColorMode from "./components/ToggleColorMode";
import Server from "./pages/Server";

// channelId? -> making the uri parameter optional
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={ <Home />} />
      <Route path="/server/:serverId/:channelId?" element={ <Server />} />
      <Route path="/explore/:categoryName" element={ <Explore />} />
    </Route>
  )
);

const App = () => {
  return (
    <ToggleColorMode >
      <RouterProvider router={router} />
    </ToggleColorMode>
  ); 
};

// or with typescript
// React.FC specifies the type
// const App: React.FC = () => {
//   return <RouterProvider router={router} />;
// };

export default App;
