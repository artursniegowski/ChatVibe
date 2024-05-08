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
            const getUserDetailUrl = `/user?by_userId=${userId}`;
            const url = `${BACKEND_BASE_URL}${getUserDetailUrl}`;
            // this view requires the user to be authenticated
            const res = await axios.get(
                url,
                { withCredentials: true }
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


    const login = async (email: string, password: string) => {
        try {
            const getTokenUrl = "/token/";
            const url = `${BACKEND_BASE_URL}${getTokenUrl}`;
            const res = await axios.post(
                url,
                {
                    email,
                    password,
                // The browser will include any relevant credentials associated with the current origin
                // so basicaly the browser will send the tokens for authentication automaticaly 
                }, { withCredentials: true },  
            );

            // console.log(res.data)
            const user_id = res.data.user_id
            localStorage.setItem("isLoggedIn", "true");
            localStorage.setItem("userId", user_id);
            // we assume the user is logged in
            setIsLoggedIn(true);
            getUserDetails();
            
        } catch (error: any) {
            return error;
        }
    };

    const refreshAccessToken = async () => {
        try {
            const refreshTokenUrl = "/token/refresh/";
            const url = `${BACKEND_BASE_URL}${refreshTokenUrl}`;
            // try and connect to the refresh endpoint to retrive a new access token
            // which should be set access token by the browser as a new http only cookie
            await axios.post(
                url, {}, {withCredentials: true}
            ) 
        } catch (refreshError) {
            return Promise.reject(refreshError);
        };
    };

    const logout = () => {
        // removing data storage points
        localStorage.setItem("isLoggedIn","false");
        localStorage.removeItem("userEmail");
        localStorage.removeItem("userId");
        setIsLoggedIn(false);
    };

    return {login, isLoggedIn, logout, refreshAccessToken}
};