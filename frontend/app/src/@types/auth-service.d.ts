export interface AuthServiceProps {
    login: (email: string, password: string) => any;
    isLoggedIn: boolean;
    logout: () => void;
    // by using Promis<void> we indicating this function is asynchronous
    refreshAccessToken: () => Promise<void>;
}
