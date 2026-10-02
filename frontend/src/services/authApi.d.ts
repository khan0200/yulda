import type { TokenPair, User, UserRole } from "@/types/user";
export interface SignupPayload {
    email: string;
    password: string;
    name: string;
    phone?: string;
    roles?: UserRole[];
}
export interface LoginPayload {
    email: string;
    password: string;
}
export declare const authApi: {
    signup(payload: SignupPayload): Promise<TokenPair>;
    login(payload: LoginPayload): Promise<TokenPair>;
    logout(): Promise<void>;
    me(): Promise<User>;
    forgotPassword(email: string): Promise<void>;
    resetPassword(token: string, newPassword: string): Promise<void>;
};
