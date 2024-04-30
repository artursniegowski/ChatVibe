export interface AuthServiceProps {
    login: (email: string, password: string) => any;
    isLoggedIn: boolean;
    logout: () => void;
}
