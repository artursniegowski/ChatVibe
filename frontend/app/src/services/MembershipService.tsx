import { useState } from "react";
import { IuseServer } from "../@types/membership-service";
import { BACKEND_BASE_URL } from "../config";
import useAxiosWithInterceptor from "../helpers/jwtinterceptor";


const useMembership = (): IuseServer => {
    const jwtAxios = useAxiosWithInterceptor();
    const [ error, setError ] = useState<Error | null>(null);
    const [ isLoading, setIsLoading ] = useState(false);
    const [ isUserMember, setIsUserMember ] = useState(false);

    const joinServer = async (serverId: string): Promise<void> => {
        setIsLoading(true);
        try {
            const membershipURL = `/servers/membership/${serverId}/membership`;
            const url = `${BACKEND_BASE_URL}${membershipURL}`;
            await jwtAxios.post(
                url, {}, {withCredentials:true}
            );
            // if successful
            setIsLoading(false);
            setIsUserMember(true);
        } catch (error: any) {
           setError(error);
           setIsLoading(false);
           throw error;
        };
    };

    const leaveServer = async (serverId: string): Promise<void> => {
        setIsLoading(true);
        try {
            const removeMembershipURL = `/servers/membership/${serverId}/membership/remove_member`;
            const url = `${BACKEND_BASE_URL}${removeMembershipURL}`;
            await jwtAxios.delete(
                url, {withCredentials:true}
            );
            // if successful
            setIsLoading(false);
            setIsUserMember(false);
        } catch (error: any) {
           setError(error);
           setIsLoading(false);
           throw error;
        };
    };

    const isMember = async (serverId: string): Promise<void> => {
        setIsLoading(true);
        try {
            const isMembershipURL = `/servers/membership/${serverId}/membership/is_member`;
            const url = `${BACKEND_BASE_URL}${isMembershipURL}`;
            const res = await jwtAxios.get(
                url, {withCredentials:true}
            );
            // if successful
            setIsLoading(false);
            setIsUserMember(res.data.is_member);
        } catch (error: any) {
           setError(error);
           setIsLoading(false);
           throw error;
        };
    };

    return {joinServer, leaveServer, error, isLoading, isMember, isUserMember};
};

export default useMembership;