import { Box, CssBaseline } from "@mui/material";
import PrimaryAppBar from "./templates/PrimaryAppBar";
import PrimaryDraw from "./templates/PrimaryDraw";
import SecondaryDraw from "./templates/SecondaryDraw";
import Main from "./templates/Main";
import PopularChannels from "../components/PrimaryDraw/PopularChannels";
import ExplorerCategories from "../components/SecondaryDraw/ExplorerCategories";
import ExploreServers from "../components/Main/ExploreServers";

const Home = () => {
    return (
     <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <PrimaryAppBar />
        <PrimaryDraw>
            <PopularChannels open={false}/>
        </PrimaryDraw>
        <SecondaryDraw>
            <ExplorerCategories />
        </SecondaryDraw>
        <Main>
            <ExploreServers />
        </Main>
     </Box>
    );
};

export default Home;