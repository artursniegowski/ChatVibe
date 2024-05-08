import { useParams } from "react-router-dom";
import { ServerData } from "../../@types/server";
import { Avatar, Box, List, ListItem, ListItemAvatar, ListItemText, Typography, useTheme, TextField } from "@mui/material";
import MessageInterfaceChannels from "./MessageInterfaceChannels";
import React from "react";
import Scroll from "./Scroll";
import useChatWebSocket from "../../services/chatService";

interface SendMessageData {
    type: string;
    message: string;
    [key: string]: any;
};

interface ServerChannelProps {
    data: ServerData[];
};

interface Message {
    id: string;
    sender: string;
    content: string;
    created: string;
};

const MessageInterface = (props: ServerChannelProps) => {
    const {data} = props;
    const theme = useTheme();
    // using optional chain operator to check if data exists and if it does
    // we use it as serverName otherwise we set a default
    const serverName = data?.[0]?.name ?? "Server";
    
    const { serverId, channelId } = useParams();
    const { newMessage, message, setMessage, sendJsonMessage } = useChatWebSocket(
        channelId || "", 
        serverId || "",
    );
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key == "Enter") { //if enter presed we want to send the text
            e.preventDefault();
            sendJsonMessage({
                type: "message", 
                message,
            } as SendMessageData);
        };
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        sendJsonMessage({
            type: "message", 
            message,
        } as SendMessageData);
    };

    function formatTimeStamp(timeStamp: string): string {
        // converting teh date string into timestamp value
        const date = new Date(Date.parse(timeStamp));
        const formattedDate = `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()}`;
        // const formattedTime = `${date.getSeconds()}:${date.getMinutes()}:${date.getHours()}`;
        const formattedTime = date.toLocaleTimeString([], {
            hour: "2-digit", 
            minute: "2-digit", 
            hour12: true
        });
        return `${formattedDate} at ${formattedTime}`;
    };

    return (
        <>
            <MessageInterfaceChannels data={data}/>
            {channelId == undefined ? (
                <Box sx={{
                        overflow: "hidden", 
                        p: {xs: 0}, 
                        height: `calc(80vh)`,
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                      }}
                >
                    <Box sx={{ textAlign: "center"}}>
                        <Typography variant="h4" fontWeight={700} letterSpacing={"-0.5px"} sx={{ px:5, maxWidth: "600px"}}>
                            Welcome to {serverName}
                        </Typography>
                        <Typography>
                            {data?.[0]?.description ?? "This is our home"}
                        </Typography>
                    </Box>
                </Box>
            ) : (
            <>
                <Box 
                    // -100 px for the top bar and the input, eahc is of height 50px
                    sx={{ overflow: "hidden", p:0, height: `calc(100vh - 100px)`,}}
                >
                    <Scroll>
                        <List sx={{ width: "100%", bgcolor: "background.paper" }}>
                            {newMessage.map((msg: Message, index: number) => {
                                return (
                                    <ListItem key={index} alignItems="flex-start">
                                        <ListItemAvatar>
                                            <Avatar alt="user image" />
                                        </ListItemAvatar>
                                        <ListItemText 
                                            primaryTypographyProps={{ 
                                                fontSize: "12px", 
                                                variant: "body2" }}
                                            primary={
                                                <>
                                                    <Typography 
                                                        component="span" 
                                                        variant="body1"
                                                        color="text.primary"
                                                        sx={{ display: "inline", fontWeight: 600 }}
                                                    >
                                                        {msg.sender}
                                                    </Typography>
                                                    <Typography component="span" variant="caption" color="textSecondary">
                                                        {" at "}{formatTimeStamp(msg.created)}
                                                    </Typography>
                                                </>
                                            }
                                            secondary={
                                                <React.Fragment>
                                                    <Typography
                                                        variant="body1"
                                                        style={{ overflow: "visible", whiteSpace: "normal", textOverflow: "clip",}}
                                                        sx={{ display: "inline", lineHeight:1.2, fontWeight:400, letterSpacing: "-0.2px",}}
                                                        component="span"
                                                        color="text.primary"
                                                    >
                                                        {msg.content}
                                                    </Typography>
                                                </React.Fragment>
                                            }
                                        />
                                    </ListItem>
                                )
                            })}
                        </List>
                    </Scroll>
                </Box>
                <Box sx={{ position: "sticky", bottom: 0, width:"100%"}}>
                        <form 
                            onSubmit={handleSubmit} 
                            style={{
                                bottom:0, 
                                right:0, 
                                padding: "1rem", 
                                backgroundColor: theme.palette.background.default, 
                                zIndex:1, 
                            }}
                        >
                            <Box sx={{ display: "flex"}}>
                                <TextField 
                                    fullWidth 
                                    multiline 
                                    minRows={1} 
                                    maxRows={4}
                                    sx={{flexGrow: 1}}
                                    value={message}
                                    onChange={(e) => setMessage(e.target.value)}
                                    onKeyDown={handleKeyDown}
                                />
                            </Box>
                        </form>
                </Box>
            </>
            )}
        </>
    );
};
export default MessageInterface;



