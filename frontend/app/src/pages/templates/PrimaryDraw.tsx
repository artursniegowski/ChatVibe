import { Box, useMediaQuery, styled } from "@mui/material";
import React, { ReactNode, useEffect, useState } from "react";
import { useTheme } from "@mui/material/styles";
import DrawerToggle from "../../components/PrimaryDraw/DrawToggle";
import MuiDrawer from "@mui/material/Drawer";

type Props = {
    children: ReactNode;
};

type ChildProps = {
    open: boolean;
};

type ChildElement = React.ReactElement<ChildProps>;

export const PrimaryDraw: React.FC<Props> = ({ children }) => {
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

    const Drawer = styled(MuiDrawer, {})(({ theme, open }) => ({
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
        <Drawer open={open} variant={bellow600 ? "temporary" : "permanent"}
            PaperProps={{
                sx: {
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
                </Box>
                {React.Children.map( children, (child) => {
                    return React.isValidElement(child) 
                    ? React.cloneElement(child as ChildElement, {open})
                    : child;
                })}
            </Box>
        </Drawer>
    );
};

export default PrimaryDraw;