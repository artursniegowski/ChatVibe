import { AppBar, Toolbar, Typography, Link, Box, IconButton, Drawer, useMediaQuery } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import MenuIcon from "@mui/icons-material/Menu";
import React, { useEffect, useState } from "react";
import ExplorerCategories from "../../components/SecondaryDraw/ExplorerCategories";
import AccountButton from "../../components/PrimaryAppBar/AccountButton";

const PrimaryAppBar = () => {
    const [sideMenu, setSideMenu] = useState(false);
    const theme = useTheme();

    const isSmallScreen = useMediaQuery(theme.breakpoints.up("sm"));

    // so basicaly everytimme the isSmallScreen will change we will
    // run this user effect, so it is tracking the change of the state of the isSmallScreen
    useEffect( () => {
      if (isSmallScreen && sideMenu) {
        setSideMenu(false);
      }
    }, [isSmallScreen]);

    const toggleDrawer = 
      (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
        if (
          event.type === "keydown" &&
          // makign sure teh keys that normaly are used to navigate the website
          // will not cause the drawer to expand or collapse
          ((event as React.KeyboardEvent).key === "Tab" ||
           (event as React.KeyboardEvent).key === "Shift")
        ) {
          return;
        }
        setSideMenu(open);
    };

    const list = () => (
      <Box 
        sx={{ paddingTop: `${theme.primaryAppBar.height}px`, minWidth: 200 }}
        onClick={toggleDrawer(false)}
        onKeyDown={toggleDrawer(false)}
      >
        <ExplorerCategories />
      </Box>
    )

    return (
        <AppBar 
          sx={{
            // always on top // adjusting dynamically
            zIndex: (theme) => theme.zIndex.drawer + 2,
            backgroundColor: theme.palette.background.default,
            borderBottom: `1px solid ${theme.palette.divider}`,
          }}
        >
            <Toolbar 
              variant="dense" 
              sx={{ 
                height: theme.primaryAppBar.height,
                minHeight: theme.primaryAppBar.height,
              }}
            >
                <Box sx={{ display: {xs: "block", sm: "none"} }}>
                  <IconButton 
                    color="inherit" 
                    aria-label="open drawer" 
                    edge="start" 
                    sx={{ mr:1 }}
                    onClick={toggleDrawer(true)}
                  >
                    <MenuIcon />
                  </IconButton>
                </Box>
                <Drawer anchor="left" open={sideMenu} onClose={toggleDrawer(false)}>
                  {list()}
                </Drawer>
                <Link href="/" underline="none" color="inherit">
                    <Typography 
                        variant="h6" 
                        noWrap component="div"
                        sx={{ display: { fontWeight: 700, letterSpacing: "-0.5px" } }}
                    >
                        ChatVibe
                    </Typography>
                </Link>
                <Box sx={{ flexGrow: 1}}></Box>
                <AccountButton />
            </Toolbar>
        </AppBar>
    )
};
export default PrimaryAppBar;