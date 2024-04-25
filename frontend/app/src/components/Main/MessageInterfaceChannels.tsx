import { AppBar, Toolbar, Box, ListItemAvatar, Avatar, Typography, IconButton, Drawer, useTheme, useMediaQuery } from "@mui/material";
import { BACKEND_MEDIA_URL } from "../../config";
import { ServerData } from "../../@types/server";
import { useParams } from "react-router-dom";
import ServerChannels from "../SecondaryDraw/ServerChannels";
import { useState, useEffect } from "react";
import MoreVertIcon from "@mui/icons-material/MoreVert";

interface ServerChannelProps {
    data: ServerData[];
};

const MessageInterfaceChannels = (props: ServerChannelProps) => {
    const {data} = props;
    const theme = useTheme();
    const { serverId, channelId } = useParams();
    const channelName = data
        ?.find((server) => server.id === serverId)
        ?.channel_server?.find((channel) => channel.id === channelId)
        ?.name || "home";
    
    const [sideMenu, setSideMenu] = useState(false);
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
            <ServerChannels data={data}/>
        </Box>
        )

    return (
        <>
            <AppBar 
                sx={{ 
                    backgroundColor: theme.palette.background.default,
                    borderBottom: `1px solid ${theme.palette.divider}`,
                }}
                color="default"
                position="sticky"
                elevation={0}
            >
                <Toolbar 
                    variant="dense" 
                    sx={{ 
                        minHeight: theme.primaryAppBar.height, 
                        height: theme.primaryAppBar.height,
                        display: "flex",
                        alignItems: "center",
                    }}
                >   
                    <Box sx={{ display: {xs: "block", sm:"none"}}}>
                        <ListItemAvatar sx={{minWidth: "40px"}}>
                            <Avatar 
                                alt="Server Icon" 
                                src={data?.[0]?.icon ? `${BACKEND_MEDIA_URL}${data?.[0]?.icon}` : ""}
                                sx={{width:30, height:30}}
                            />
                        </ListItemAvatar>
                    </Box>
                    <Typography noWrap component="div">
                        {channelName}
                    </Typography>
                    <Box sx={{ flexGrow: 1}}></Box>
                    <Box sx={{ display: {xs: "block", sm:"none"}}}>
                        <IconButton color="inherit" onClick={toggleDrawer(true)} edge="end">
                            <MoreVertIcon />
                        </IconButton>
                    </Box>
                    <Drawer
                        anchor="left"
                        open={sideMenu}
                        onClose={toggleDrawer(false)}
                    >
                        {list()}
                    </Drawer>
                </Toolbar>
            </AppBar>
        </>
    );
};
export default MessageInterfaceChannels;