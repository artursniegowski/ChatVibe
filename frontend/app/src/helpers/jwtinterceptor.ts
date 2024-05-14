// intercepting request or responses before they get handled by the app
import axios, { AxiosInstance } from "axios";
import { useNavigate } from "react-router-dom";
import { BACKEND_BASE_URL } from "../config";
import { useAuthService } from "../services/AuthServices";

const API_BACKEND_BASE_URL = BACKEND_BASE_URL;


const useAxiosWithInterceptor = (): AxiosInstance => {
    const jwtAxios = axios.create({ baseURL: API_BACKEND_BASE_URL});
    const navigate = useNavigate();
    const { logout } = useAuthService();

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
        if (err.response?.status === 401 || err.response?.status === 403) {
            axios.defaults.withCredentials = true;
            const refresTokenURL = "/token/refresh/";
            // only if a refresh token exists
            try {
                const resp = await axios.post(
                    `${API_BACKEND_BASE_URL}${refresTokenURL}`,
                );
                if (resp["status"] == 200) {
                    // and now we simply retry the original request
                    return jwtAxios(originalRequest);
                };
            } catch (refreshError) { 
                logout();
                // if we get an error with getting a new access token we will redirect to login page
                // for example we cant access the refres token, or it expired
                const goLogin = () => navigate('/login');
                goLogin();
                return Promise.reject(refreshError);
            }
        }
        // returning the error to he original component
        return Promise.reject(err);
    }
    );
    return jwtAxios;
};

export default useAxiosWithInterceptor;