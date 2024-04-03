// import React from "react";
import { ThemeProvider } from "@emotion/react";
import Home from "./pages/Home";
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom";
import createMuiTheme from "./theme/theme";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={ <Home />} />
    </Route>
  )
);

const App = () => {
  const theme = createMuiTheme();
  return (
    <ThemeProvider theme={ theme } >
      <RouterProvider router={router} />
    </ThemeProvider>
  ); 
};

// or with typescript
// React.FC specifies the type
// const App: React.FC = () => {
//   return <RouterProvider router={router} />;
// };

export default App;
