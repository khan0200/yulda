import type { TokenPair } from "@/types/user";
export declare const http: import("axios").AxiosInstance;
export declare function getAccessToken(): string | null;
export declare function getRefreshToken(): string | null;
export declare function setTokens(tokens: TokenPair): void;
export declare function clearTokens(): void;
