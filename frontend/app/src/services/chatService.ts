import useWebSocket from "react-use-websocket";
import { BACKEND_WEBSOCKET_BASE_URL } from "../config";
import { useState } from "react";
import { useAuthService } from "./AuthServices";
import useCrud from "../hooks/useCrud";
import { ServerData } from "../@types/server";

interface Message {
    id: string;
    sender: string;
    content: string;
    created: string;
};

const useChatWebSocket = (channelId: string, serverId: string) => {

    const [newMessage, setNewMessage] = useState<Message[]>([]);
    const [ message, setMessage] = useState("");
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

    return {
        newMessage,
        message,
        setMessage, 
        sendJsonMessage, 
    }
};

export default useChatWebSocket;