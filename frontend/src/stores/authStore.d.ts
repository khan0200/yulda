import { type LoginPayload, type SignupPayload } from "@/services/authApi";
import type { User } from "@/types/user";
export declare const useAuthStore: import("pinia").StoreDefinition<"auth", Pick<{
    user: import("vue").Ref<{
        id: string;
        email: string;
        phone: string | null;
        name: string;
        avatar: string | null;
        roles: import("@/types/user").UserRole[];
        verification_status: import("@/types/user").VerificationStatus;
        location: {
            type: "Point";
            coordinates: [number, number];
        } | null;
        created_at: string;
        updated_at: string;
    } | null, User | {
        id: string;
        email: string;
        phone: string | null;
        name: string;
        avatar: string | null;
        roles: import("@/types/user").UserRole[];
        verification_status: import("@/types/user").VerificationStatus;
        location: {
            type: "Point";
            coordinates: [number, number];
        } | null;
        created_at: string;
        updated_at: string;
    } | null>;
    isLoading: import("vue").Ref<boolean, boolean>;
    isInitialized: import("vue").Ref<boolean, boolean>;
    isAuthenticated: import("vue").ComputedRef<boolean>;
    roles: import("vue").ComputedRef<import("@/types/user").UserRole[]>;
    hasRole: (role: string) => boolean;
    fetchCurrentUser: () => Promise<void>;
    signup: (payload: SignupPayload) => Promise<void>;
    login: (payload: LoginPayload) => Promise<void>;
    logout: () => Promise<void>;
}, "user" | "isLoading" | "isInitialized">, Pick<{
    user: import("vue").Ref<{
        id: string;
        email: string;
        phone: string | null;
        name: string;
        avatar: string | null;
        roles: import("@/types/user").UserRole[];
        verification_status: import("@/types/user").VerificationStatus;
        location: {
            type: "Point";
            coordinates: [number, number];
        } | null;
        created_at: string;
        updated_at: string;
    } | null, User | {
        id: string;
        email: string;
        phone: string | null;
        name: string;
        avatar: string | null;
        roles: import("@/types/user").UserRole[];
        verification_status: import("@/types/user").VerificationStatus;
        location: {
            type: "Point";
            coordinates: [number, number];
        } | null;
        created_at: string;
        updated_at: string;
    } | null>;
    isLoading: import("vue").Ref<boolean, boolean>;
    isInitialized: import("vue").Ref<boolean, boolean>;
    isAuthenticated: import("vue").ComputedRef<boolean>;
    roles: import("vue").ComputedRef<import("@/types/user").UserRole[]>;
    hasRole: (role: string) => boolean;
    fetchCurrentUser: () => Promise<void>;
    signup: (payload: SignupPayload) => Promise<void>;
    login: (payload: LoginPayload) => Promise<void>;
    logout: () => Promise<void>;
}, "roles" | "isAuthenticated">, Pick<{
    user: import("vue").Ref<{
        id: string;
        email: string;
        phone: string | null;
        name: string;
        avatar: string | null;
        roles: import("@/types/user").UserRole[];
        verification_status: import("@/types/user").VerificationStatus;
        location: {
            type: "Point";
            coordinates: [number, number];
        } | null;
        created_at: string;
        updated_at: string;
    } | null, User | {
        id: string;
        email: string;
        phone: string | null;
        name: string;
        avatar: string | null;
        roles: import("@/types/user").UserRole[];
        verification_status: import("@/types/user").VerificationStatus;
        location: {
            type: "Point";
            coordinates: [number, number];
        } | null;
        created_at: string;
        updated_at: string;
    } | null>;
    isLoading: import("vue").Ref<boolean, boolean>;
    isInitialized: import("vue").Ref<boolean, boolean>;
    isAuthenticated: import("vue").ComputedRef<boolean>;
    roles: import("vue").ComputedRef<import("@/types/user").UserRole[]>;
    hasRole: (role: string) => boolean;
    fetchCurrentUser: () => Promise<void>;
    signup: (payload: SignupPayload) => Promise<void>;
    login: (payload: LoginPayload) => Promise<void>;
    logout: () => Promise<void>;
}, "hasRole" | "fetchCurrentUser" | "signup" | "login" | "logout">>;
