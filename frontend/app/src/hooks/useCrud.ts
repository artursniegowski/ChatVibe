// custom hook for the backedn API
import useAxiosWithInterceptor from "../helpers/jwtinterceptor";
import { BACKEND_BASE_URL } from "../config";
import { useState } from "react";

interface IuseCrud<T> {
    dataCRUD: T[];
    fetchData: () => Promise<void>;
    error: Error | null;
    isLoading: boolean;
};

const useCrud = <T>(initialData: T[], apiURL: string): IuseCrud<T> => {
    const jwtAxions = useAxiosWithInterceptor();
    const [dataCRUD, setDataCRUD] = useState<T[]>(initialData);
    const [error, setError] = useState<Error | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const res = await jwtAxions.get(`${BACKEND_BASE_URL}${apiURL}`, {});
            const data = res.data;
            setDataCRUD(data);
            setError(null);
            setIsLoading(false)
            return data;
        } catch (error: any) {
            if (error.response && error.response.status === 400 ) {
                setError(new Error("400"));
            }
            setIsLoading(false);
            throw error;
        }
    };

    return {fetchData, dataCRUD, error, isLoading };
};
export default useCrud;