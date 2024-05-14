import { useMembershipContext } from "../../context/MemberContext";
import { useParams } from "react-router-dom";

const JoinRemoveServerButton = () => {
    const { serverId } = useParams();
    const { joinServer, leaveServer, isLoading, error, isUserMember } = useMembershipContext();

    const handleJoinServer = async () => {
        try {
            // await joinServer(serverId ?? '');
            await joinServer(String(serverId));
            console.log("User has joined server.");
        } catch (error) {
            console.log("Error joining", error);
        }
    };

    const handleLeaveServer = async () => {
        try {
            await leaveServer(String(serverId));
            console.log("User has left server.");
        } catch (error) {
            console.log("Error leaving the server:", error);
        }
    };

    if (isLoading) {
        return <div>Loading...</div>;
    };

    // just commented out bc we dont want this to be included in the
    // page, but depends on the requirements we might add it or not.
    // if (error) {
    //     return <div>Error: {error.message}</div>;
    // };

    return (
        <>
            ismember: {isUserMember.toString()}
            {isUserMember ? (
                <button onClick={handleLeaveServer}>Leave Server</button>  
            ) : (
                <button onClick={handleJoinServer}>Join Server</button>  
            )
            }
        </>
    );
};

export default JoinRemoveServerButton;