import { Box, useMediaQuery, Typography, styled } from "@mui/material";
import { useEffect, useState } from "react";
import { useTheme } from "@mui/material/styles";
import DrawerToggle from "../../components/PrimaryDraw/DrawToggle";
import MuiDrawer from "@mui/material/Drawer";

const PrimaryDraw = () => {
    const theme = useTheme();
    const bellow600 = useMediaQuery("(max-width:599px)");
    const [open, setOpen] = useState(!bellow600);

    const openedMixin = () => ({
        transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
        overflowX: "hidden",
    });

    const closedMixin = () => ({
        transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
        overflowX: "hidden",
        width: theme.primaryDraw.closed,
    });

    const Drawer = styled(MuiDrawer, {})(({theme, open}) => ({
        width: theme.primaryDraw.width,
        whiteSpace: "nowrap",
        boxSizing: "border-box",
        ...(open && {
            ...openedMixin(),
            "& .MuiDrawer-paper": openedMixin(),
        }),
        ...(!open && {
            ...closedMixin(),
            "& .MuiDrawer-paper": closedMixin(),
        }),
    }));

    useEffect(() => {
        setOpen(!bellow600);
    }, [bellow600]);

    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };   

    return (
        <Drawer open={open} variant={ bellow600 ? "temporary" : "permanent" }
         PaperProps={{
            sx:{ 
                mt: `${theme.primaryAppBar.height}px`,
                height: `calc(100vh - ${theme.primaryAppBar.height}px )`,
                width: theme.primaryDraw.width,
            },
         }}
        >
            <Box>
                <Box sx={{ 
                        position: "absolute", 
                        top: 0, 
                        right: 0, 
                        p: 0, 
                        width: open ? "auto" : "100%",
                      }}
                >
                    <DrawerToggle 
                        open={open} 
                        handleDrawerClose={handleDrawerClose}
                        handleDrawerOpen={handleDrawerOpen}
                    />
                {[...Array(50)].map((_, i)=> (
                    <Typography key={i} paragraph>
                      {i+1}
                    </Typography>
                  ))}
                </Box>
            </Box>
        </Drawer>
    );
};
export default PrimaryDraw;