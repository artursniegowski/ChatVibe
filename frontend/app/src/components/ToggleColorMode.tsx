import { CssBaseline, ThemeProvider, useMediaQuery } from "@mui/material";
import React, { useEffect, useMemo, useState } from "react";
import createMuiTheme from "../theme/theme";
import { ColorModeContext } from "../context/DarkModeContext";
import Cookies from "js-cookie";

interface ToggleColorModeProps {
    children: React.ReactNode
}

const ToggleColorMode: React.FC<ToggleColorModeProps> = ({ children }) => {
    // // set user prefernce for the color mode // dark mode // light mode
    // Retrieve the stored color mode from localStorage - or null if not existing
    // const storedMode = localStorage.getItem("colorMode") as "light" | "dark";
    const storedMode = Cookies.get("colorMode") as "light" | "dark";
    // Check if the preferred color mode is dark based on media query
    const preferedDarkMode = useMediaQuery("([prefers-color-scheme: dark])");
    // Determine the default color mode based on stored value or preferred dark mode
    const defaultMode = storedMode || (preferedDarkMode ? "dark" : "light");
    // Initialize state with the default color mode
    const [mode, setMode] = useState<"light" | "dark">(defaultMode);

    // returns memoriazed version of callback function
    // [] -> making sure taht it is created only once and is not dependant on anything
    const toggleColorMode = React.useCallback(() => {
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"))
    }, []);

    useEffect(()=> {
        Cookies.set("colorMode", mode)
        // localStorage.setItem("colorMode", mode)
    }, [mode]);

    // useMemo storing the result of caluations and only updates it if neccesery
    // it is used for optimazation
    const colorMode = useMemo(() => ({ toggleColorMode }), [toggleColorMode]);

    const theme = React.useMemo( () => createMuiTheme(mode), [mode]);

    return (
        <ColorModeContext.Provider value={colorMode}>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                { children }
            </ThemeProvider>
        </ColorModeContext.Provider>
    )
};
export default ToggleColorMode;