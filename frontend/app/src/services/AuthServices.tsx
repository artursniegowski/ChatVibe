import axios from "axios";
import { AuthServiceProps } from "../@types/auth-service";
import { BACKEND_BASE_URL } from "../config";
import { useState } from "react";

export function useAuthService(): AuthServiceProps {

    const getInitialLoggedInValue = () => {
        const loggedIn = localStorage.getItem("isLoggedIn");
        return loggedIn !== null && loggedIn === "true";
      };

    // keeping track if user is logged in based on the fact
    // the token exists - access token
    // and that the access token has not expired yet
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>((getInitialLoggedInValue));

    // makign a request to backed for deatils on specific user with the
    // given userId
    const getUserDetails = async () => {
        try { 
            // getting the userId from the local storage
            const userId = localStorage.getItem("userId");
            const access_token = localStorage.getItem("access_token");
            const getUserDetailUrl = `/user?by_userId=${userId}`;
            const url = `${BACKEND_BASE_URL}${getUserDetailUrl}`;
            // this view requires the user to be authenticated
            const res = await axios.get(
                url,
                {
                    headers: {
                        Authorization: `Bearer ${access_token}`
                    },
                }
            );
            const userDetails = res.data;

            localStorage.setItem("userEmail", userDetails.email);
            // we assume the user is logged in
            setIsLoggedIn(true);
            // TODO: technicaly not safe as anyone can set them in the browser
            localStorage.setItem("isLoggedIn", "true");

        } catch (error: any) {
            // if we cant get user detail ther is potentialy a problem
            setIsLoggedIn(false);
            // TODO: technicaly not safe as anyone can set them in the browser
            localStorage.setItem("isLoggedIn", "false");
            return error;
        }
    };

    // retrives the user id from the token payload
    const getUserIdFromToken = (token: string) => {
        const tokenParts = token.split('.');
        const encodedPayLoad = tokenParts[1];
        // function to decod the base64 encoded string
        const decodedPayLoad = atob(encodedPayLoad);
        const payLoadData = JSON.parse(decodedPayLoad);
        const userId = payLoadData.user_id;

        return userId;
    };

    const login = async (email: string, password: string) => {
        try {
            const getTokenUrl = "/token/";
            const url = `${BACKEND_BASE_URL}${getTokenUrl}`;
            const res = await axios.post(
                url,
                {
                    email,
                    password,
                }
            );
            const {access, refresh} = res.data;
            // storing the data in the local storage
            // TODO: change to something more safer, 
            // localstorage is vulnerable to XSS
            localStorage.setItem("access_token", access);
            localStorage.setItem("refresh_token", refresh);
            localStorage.setItem("userId", getUserIdFromToken(access));
            // TODO: technicaly not safe as anyone can set them in the browser
            localStorage.setItem("isLoggedIn", "true");
            // we assume the user is logged in
            setIsLoggedIn(true);
            getUserDetails();
            
        } catch (error: any) {
            return error;
        }
    };

    const logout = () => {
        // removing data storage points
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("userId");
        localStorage.removeItem("userEmail");
        localStorage.setItem("isLoggedIn","false");
        setIsLoggedIn(false);
    };

    return {login, isLoggedIn, logout}
};