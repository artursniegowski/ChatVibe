import useWebSocket from "react-use-websocket";
import { BACKEND_WEBSOCKET_BASE_URL } from "../../config";
import { useState } from "react";
import { useParams } from "react-router-dom";
import useCrud from "../../hooks/useCrud";
import { ServerData } from "../../@types/server";
import { Avatar, Box, List, ListItem, ListItemAvatar, ListItemText, Typography, useTheme, TextField } from "@mui/material";
import MessageInterfaceChannels from "./MessageInterfaceChannels";
import React from "react";
import Scroll from "./Scroll";
import { useAuthService } from "../../services/AuthServices";

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
    const [newMessage, setNewMessage] = useState<Message[]>([]);
    const [ message, setMessage] = useState("");
    const { serverId, channelId } = useParams();
    const { logout, refreshAccessToken } = useAuthService();
    const { fetchData } = useCrud<ServerData>(
        [],
        `/messages?by_channelId=${channelId}`
    );
    
    const socketPath = `/${serverId}/${channelId}/`;
    // making only a request if channelId exists
    const socketURL = channelId ? `${BACKEND_WEBSOCKET_BASE_URL}${socketPath}` : null;

    // state to capture the reconnection
    const [reconnectionAttempt, setReconnectionAttempt] = useState(0);
    const maxConnectionAttempts = 4;

    const { sendJsonMessage } = useWebSocket(socketURL, {
        onOpen: async () => {
            try {
                const data = await fetchData();
                setNewMessage([]);
                setNewMessage(Array.isArray(data) ? data : []);
                console.log("Connected");
            } catch (error) {
                console.log(error);
            };
        },
        onClose: (event: CloseEvent) => {
            // if we get autheticaaiton error we will try to refresh the token
            if (event.code == 4001){
                console.log("Authentication Error");
                refreshAccessToken().catch((error) => {
                    if (error.response && error.response.status === 401) {
                        // so refresh token was not valid then logout the user
                        logout();
                    }
                });
            };
            console.log("Closed");
            setReconnectionAttempt((prevAttempt) => prevAttempt + 1);
        },
        onError: () => {
            console.log("Error");
        },
        // message that is returned from the server
        onMessage: (msg) => {
            const data = JSON.parse(msg.data);
            // new_message comes from the consumer from backend
            setNewMessage( (prev_msg) => [...prev_msg, data.new_message]);
            setMessage("");
        },
        // what should happen if we, for example do have an error and we
        // do close the connection maybe prematurly, we can go ahead and try
        // and reconnect automatically

        // using the should reconnect, to try and reconnect shoudl there be a problem
        // should we retrive 4001 error, when we close and we are going to set this 
        // so it just reconnects four times
        shouldReconnect: (closeEvent) => {
            if (closeEvent.code === 4001 && reconnectionAttempt >= maxConnectionAttempts) {
                setReconnectionAttempt(0);
                // in this case we want to stop reconnecting
                return false;
            };
            // continue connection
            return true;
        },
        // settign the reconection interval to 2 seconds
        reconnectInterval: 2000,
    });

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



