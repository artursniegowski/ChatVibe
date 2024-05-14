import React, { createContext, useContext } from "react";
import { IuseServer } from "../@types/membership-service";
import useMembership from "../services/MembershipService";


const MembershipContext = createContext<IuseServer | null>(null);

export function MembershipProvider(props: React.PropsWithChildren<{}>) {
    const membership = useMembership();
    return (
        <MembershipContext.Provider value={membership}>
            {props.children}
        </MembershipContext.Provider>
    );
};

// this is going to allow components to consume the membership context
// and access the membership services
export function useMembershipContext(): IuseServer {
    // instead of directly accessing in the component, we are using this use of 
    // service context function. This is going to provide additional safety and better
    // error handling.
    // so by using the memebrshipcontext we are going to ensure that the component
    // using this hook must be wrapped within the membership provider component
    // which is responsible for providing the necessary context value
    const context = useContext(MembershipContext);

    // handlign scenario where the context value is null
    // this can occur for example if the membership service context hook is used outside
    // of the scope of the membership service provider, where the context value is expected
    // to be provided
    if (context === null) {
        throw new Error("Error - You have to use the MembershipProvider.");
    };

    return context
};

export default MembershipProvider;