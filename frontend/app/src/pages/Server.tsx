import { Box, CssBaseline } from "@mui/material";
import PrimaryAppBar from "./templates/PrimaryAppBar";
import PrimaryDraw from "./templates/PrimaryDraw";
import SecondaryDraw from "./templates/SecondaryDraw";
import Main from "./templates/Main";
import MessageInterface from "../components/Main/MessageInterface";
import ServerChannels from "../components/SecondaryDraw/ServerChannels";
import UserServers from "../components/PrimaryDraw/UserServers";
import { useNavigate, useParams } from "react-router-dom";
import useCrud from "../hooks/useCrud";
import { ServerData } from "../@types/server";
import { useEffect } from "react";


const Server = () => {
    // navigate users away if they are not logged in
    const navigate = useNavigate();
    const { serverId, channelId } = useParams();

    const  { dataCRUD, error, isLoading, fetchData } = useCrud<ServerData>(
        [],
        `/servers?by_serverId=${serverId}`
    )

    // sending user back to home if error 
    if (error !== null && error.message === "400") {
        navigate("/");
        return null;
    };

    useEffect(() => {
        fetchData();
    }, []);

    // check if the channelId is valid by searching for it in the data fetched from the API
    const isChannel = (): Boolean => {
        if (!channelId) {
            return true;
        }
        return dataCRUD.some((server) => 
            server.channel_server.some((channel) => channel.id === channelId)
        );
    };

    // monitoring everytime the user makes a change to the channel ID
    useEffect(() => {
        // returns false if channel does not exists!
        if (!isChannel()) {
            // reroute the user to the current specific server
            navigate(`/server/${serverId}`);
        }
    }, [isChannel, channelId]);

    return (
     <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <PrimaryAppBar />
        <PrimaryDraw>
            <UserServers open={false} data={dataCRUD}/>
        </PrimaryDraw>
        <SecondaryDraw>
            <ServerChannels data={dataCRUD}/>
        </SecondaryDraw>
        <Main>
            <MessageInterface data={dataCRUD}/>
        </Main>
     </Box>
    );
};

export default Server;