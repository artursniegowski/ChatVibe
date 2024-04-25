import { Box, styled } from "@mui/material";
import React, { useCallback, useEffect, useRef } from "react";

interface ScrollProps {
    children: React.ReactNode;
};

const ScrollContainer = styled(Box)(() => ({
    // -100 px for the top bar and for the input , each is 50px, 90px for the message
    height: `calc(100vh - 190px)`,
    overflowY: "scroll",
    "&::-webkit-scrollbar": {
        width: "8px",
        height: "8px",
    },
    "&::-webkit-scrollbar-thumb": {
        backgroundColor: "#888",
        borderRadius: "4px",
    },
    "&::-webkit-scrollbar-thumb:hover": {
        backgroundColor: "#555",
    },
    "&::-webkit-scrollbar-track": {
        // backgroundColor: "#f0f0f0",
    },
    "&::-webkit-scrollbar-corner": {
        backgroundColor: "transparent",
    },
}));

const Scroll = ({children}: ScrollProps) => {
    // creating a mutable reference to an element or value
    // returns a mutable reference object that persists across rerenders of the component
    const scrolRef = useRef<HTMLDivElement>(null);

    // returns a memoraized version of a callback funciton
    // for optimizations and it is going to prevent any unnecessary recreations
    // or callback functions in functional compoenents
    const scrollToBottom = useCallback(() => {
        // making sure teh scroll eleemnt exists before accessing and modyfing the property
        if (scrolRef.current) {
            // moving basicaly the scrol to max height, which means the scroll will go to the bottom
            scrolRef.current.scrollTop = scrolRef.current.scrollHeight;
        };
    }, []);

    useEffect(() => {
        scrollToBottom();
        // scrolling to bottom wheneve childrean or scroltobottom change
    }, [scrollToBottom, children]);

    return(
        // by passing the scrolRef to the ref prop to the ScrollContainer 
        // the component is going to assign the reference to that div element
        <ScrollContainer ref={scrolRef}>
            {children}
        </ScrollContainer>
    );
};
export default Scroll;