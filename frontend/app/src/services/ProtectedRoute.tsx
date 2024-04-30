import { Navigate } from "react-router-dom";
import { useAuthServiceContext } from "../context/AuthContext";
import React from "react";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const { isLoggedIn } = useAuthServiceContext();
    // so if the user is not logged in we send the user back to login page
    if (!isLoggedIn) {
        return <Navigate to="/login" replace={true} />;
    };
    return <>{children}</>;
};
export default ProtectedRoute;