import { 
    List, 
    ListItem,  
    ListItemAvatar, 
    ListItemText, 
    Box, 
    ListItemIcon, 
    Typography,
    Grid,
    Card,
    CardMedia,
    CardContent,
    Container,
    Avatar
} from "@mui/material";
import useCrud from "../../hooks/useCrud";
import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { BACKEND_MEDIA_URL } from "../../config";

interface Server {
    id: string;
    name: string;
    category: string;
    icon: string;
    banner: string;
};


const ExploreServers = () => {
    // capturing the parameter in the url
    const { categoryName } = useParams();
    const url = categoryName ? `/servers?category=${categoryName}` : "/servers"
    const { dataCRUD, fetchData } = useCrud<Server>([], url);

    useEffect(() => {
        fetchData();
    }, [categoryName]);


    return (
        <>
           <Container maxWidth="lg">
                <Box sx={{ pt: 6}}>
                    <Typography 
                        variant="h3" 
                        noWrap 
                        component="h1" 
                        sx={{ 
                                display: {sm: "block", fontWeight: 700, letterSpacing: "-2px", textTransform: "capitalize" },
                                textAlign: {xs: "center", sm: "left"} 
                        }}
                    >
                        {categoryName ? categoryName : "Popular Channels"}
                    </Typography>
                </Box>
                <Box>
                    <Typography 
                        variant="h6" 
                        noWrap 
                        component="h2" 
                        color="textSecondary"
                        sx={{ 
                                display: {sm: "block", fontWeight: 700, letterSpacing: "-1px"},
                                textAlign: {xs: "center", sm: "left"} 
                        }}
                    >
                        {categoryName ? `Channels talking about ${categoryName}` : "Check out some of our popular channels"}
                    </Typography>
                </Box>
                <Typography 
                    variant="h6"
                    sx={{ pt: 6, pb: 1, fontWeight: 700, letterSpacing: "-1px" }}
                >
                    Recommended Channels
                </Typography>
                <Grid container spacing={{xs: 0, sm: 2}}>
                        {dataCRUD.map((item) => (
                            <Grid item key={item.id} xs={12} sm={6} md={6} lg={3}>
                                <Card sx={{
                                        height: "100",
                                        display: "flex",
                                        flexDirection: "column",
                                        boxShadow: "none",
                                        backgroundImage: "none",
                                        borderRadius: 0,
                                    }}
                                >
                                    <Link to={`/server/${item.id}`}
                                        style={{ textDecoration: "none", color: "inherit" }}
                                    >
                                        <CardMedia component="img"
                                            image={item.banner ? `${BACKEND_MEDIA_URL}${item.banner}` : "need_default_picture" }
                                            alt="random"
                                            sx={{ display: {xs:"none", sm: "block"}}}
                                        >
                                        </CardMedia>
                                        <CardContent
                                            sx={{flexGrow: 1, p: 0, "&:last-child": {paddingBottom: 0}, }}
                                        >
                                            <List>
                                                <ListItem disablePadding>
                                                    <ListItemIcon sx={{ minWidth: 0 }}>
                                                        <ListItemAvatar sx={{minWidth: "50px"}}>
                                                            <Avatar alt="server icon" src={`${BACKEND_MEDIA_URL}${item.icon}`} />
                                                        </ListItemAvatar>
                                                    </ListItemIcon>
                                                    <ListItemText
                                                        primary={
                                                            <Typography 
                                                                variant="body2"
                                                                textAlign="start" 
                                                                sx={{ fontWeight: 700, textOverflow: "ellipsis", overflow:"hidden", whiteSpace:"nowrap"}}
                                                            >
                                                                {item.name}
                                                            </Typography>
                                                        }
                                                        secondary={
                                                            <Typography variant="body2">
                                                                {item.category}
                                                            </Typography>
                                                        }
                                                    />
                                                </ListItem>
                                            </List>
                                        </CardContent>
                                    </Link>
                                </Card>
                            </Grid>
                        ))}
                </Grid>
           </Container>
        </>
    );
};
export default ExploreServers;