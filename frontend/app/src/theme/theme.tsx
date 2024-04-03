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
export const createMuiTheme = () => {
    let theme = createTheme({

        // using the ibm font system weight
        typography: {
            fontFamily: ["IBM Plex Sans", "sans-serif"].join(","),
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
        // overiding components - for the whole site
        components:{
            MuiAppBar: {
                defaultProps: {
                    color: "default",
                    elevation: 0,
                }
            }
        }
    });
    theme = responsiveFontSizes(theme);
    return theme;
};

export default createMuiTheme;