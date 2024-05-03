import { useState } from "react";
import { useAuthServiceContext } from "../../context/AuthContext";
import { BACKEND_BASE_URL } from "../../config";
import useAxiosWithInterceptor from "../../helpers/jwtinterceptor";

const TestLogin = () => {
    const { isLoggedIn, logout } = useAuthServiceContext();
    const [ email, setEmail ] = useState("");
    const jwtAxios = useAxiosWithInterceptor();

    const getUserDetails = async () => {
        try { 
            // getting the userId from the local storage
            const userId = localStorage.getItem("userId");
            // const userId = localStorage.getItem("userId");
            // const access_token = localStorage.getItem("access_token");
            const getUserDetailUrl = `/user?by_userId=${userId}`;
            const url = `${BACKEND_BASE_URL}${getUserDetailUrl}`;
            // this view requires the user to be authenticated
            const res = await jwtAxios.get(
                url,
                {   
                    withCredentials: true  // bc now we pass the cookies as http only tokens with the request, 
                                            // and backedn will automatically check for the cookies if thye containe access token
                    // headers: {
                    //     Authorization: `Bearer ${access_token}`
                    // },
                }
            );
            const userDetails = res.data;
            setEmail(userDetails.email);
        } catch (error: any) {
            return error;
        }
    };

    return (
        <>
            <div>
                { isLoggedIn.toString() }
            </div>
            <div>
                <button onClick={logout}>Logout</button>
                <button onClick={getUserDetails}>Get user details</button>
            </div>
            <div>
                email: {email}
            </div>
        </>

    );
};
export default TestLogin;