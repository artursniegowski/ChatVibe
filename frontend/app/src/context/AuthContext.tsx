import React, { createContext, useContext } from "react";
import { AuthServiceProps } from "../@types/auth-service";
import { useAuthService } from "../services/AuthServices";


const AuthServiceContext = createContext<AuthServiceProps | null>(null);

export function AuthServiceProvider(props: React.PropsWithChildren<{}>) {
    const authServices = useAuthService();
    return (
        <AuthServiceContext.Provider value={authServices}>
            {props.children}
        </AuthServiceContext.Provider>
    );
};

// this is going to allow components to consume the auth service context
// and access the authentication services
export function useAuthServiceContext(): AuthServiceProps {
    // instead of directly accessing in the component, we are using this use of 
    // service context function. This is going to provide additional safety and better
    // error handling.
    // so by using the authservicecontext weare going to ensure that the component
    // using this hook must be wrapped within the auth services provider component
    // which is responsible for providing the necessary context value
    const context = useContext(AuthServiceContext);

    // handlign scenario where the context value is null
    // this can occur for example if the auth service context hook is used outside
    // of the scope of the auth service provider, where teh context value is expected
    // to be provided
    if (context === null) {
        throw new Error("Error - You have to use the AuthServiceProvider.");
    };

    return context
};

export default AuthServiceProvider;