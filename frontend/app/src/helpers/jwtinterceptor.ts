// intercepting request or responses before they get handled by the app
import axios, { AxiosInstance } from "axios";
import { useNavigate } from "react-router-dom";
import { BACKEND_BASE_URL } from "../config";

const API_BACKEND_BASE_URL = BACKEND_BASE_URL;


const useAxiosWithInterceptor = (): AxiosInstance => {
    const jwtAxios = axios.create({ baseURL: API_BACKEND_BASE_URL});
    const navigate = useNavigate();

    jwtAxios.interceptors.response.use(
        (resp) => {
            return resp;
        },
    async (err) => {
        const originalRequest = err.config;
        // so lets say when we try to make a request and we are not authenticated
        // potentaily then we want to make another reqeust with the refresh token to get
        // a new access token, at least we will try
        // if refresh token will also expiere we will have to redirect the user and
        // make the user to log in again
        // we get 401 - forbiden or 403 unauthorized if we are not autheticated
        if (err.response?.status === 401 || 403) {
            // first using a refresh  token to get a new access token
            const refreshToken = localStorage.getItem("refresh_token");
            const refresTokenURL = "/token/refresh/";
            if (refreshToken) {
                // only if a refresh token exists
                try {
                    const refreshResponse = await axios.post(
                        `${API_BACKEND_BASE_URL}${refresTokenURL}`,
                        {
                            refresh: `${refreshToken}`,
                        },
                    );
                    const newAccessToken = refreshResponse.data.access;
                    localStorage.setItem("access_token", newAccessToken);
                    // refreing to the original request
                    // changing the access token that was applied to the original
                    // request, and then we are just going to change it with 
                    // the new access token
                    originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                    // and now we simply retry the original request
                    return jwtAxios(originalRequest);
                } catch (refreshError) { 
                    // if we get an error with getting a new access token we will redirect to login page
                    // for example we cant access the refres token, or it expired
                    navigate('/login');
                    throw refreshError;
                }
            } else {
                // so if we dont have a refresh token we simply navigate the user to login page
                navigate('/login');
            };
        }
        throw err;
    }
    )
    return jwtAxios;
};

export default useAxiosWithInterceptor;