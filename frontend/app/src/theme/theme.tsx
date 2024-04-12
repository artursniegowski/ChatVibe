// creating our own them for MUI - overriding css
import { createTheme, responsiveFontSizes } from "@mui/material";

// creating our own styling
declare module "@mui/material/styles" {
    interface Theme {
        primaryAppBar: {
            height: number;
        };
        primaryDraw: {
            width: number;
            closed: number;
        };
        secondaryDraw: {
            width: number;
        };    
    }
    interface ThemeOptions {
        primaryAppBar: {
            height: number;
        };
        primaryDraw: {
            width: number;
            closed: number;
        };  
        secondaryDraw: {
            width: number;
        }; 
    }
}

// basically copying existing theme and extending it
export const createMuiTheme = (mode: "light" | "dark") => {
    let theme = createTheme({
        // using the ibm font system weight
        typography: {
            fontFamily: ["IBM Plex Sans", "sans-serif"].join(","),
            body1:{
                fontWeight: 500,
                letterSpacing: "-0.5px",
            },
            body2:{
                fontWeight: 500,
                fontSize: "15px",
                letterSpacing: "-0.5px",
            },
        },
        primaryAppBar: {
            height: 50,
        },
        primaryDraw: {
            width: 240,
            // closed width
            closed: 70,
        },
        secondaryDraw: {
            width: 240,
        },
        palette: {
            mode,
        },
        // overiding components - for the whole site
        components:{
            MuiAppBar: {
                defaultProps: {
                    color: "default",
                    elevation: 0,
                },
            },
        },
    });
    theme = responsiveFontSizes(theme);
    return theme;
};

export default createMuiTheme;