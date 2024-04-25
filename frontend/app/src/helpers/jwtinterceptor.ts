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
        if (err.response?.status === 403) {
            //TODO: if forbiden refirect back to home / later to sigin !
            const goRoot = () => navigate("/");
            goRoot();
        }
        throw err;
    }
    )
    return jwtAxios;
};

export default useAxiosWithInterceptor;