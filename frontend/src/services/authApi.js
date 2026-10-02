import { http } from "@/services/http";
export const authApi = {
    async signup(payload) {
        const { data } = await http.post("/auth/signup", payload);
        return data.data;
    },
    async login(payload) {
        const { data } = await http.post("/auth/login", payload);
        return data.data;
    },
    async logout() {
        await http.post("/auth/logout");
    },
    async me() {
        const { data } = await http.get("/auth/me");
        return data.data;
    },
    async forgotPassword(email) {
        await http.post("/auth/forgot-password", { email });
    },
    async resetPassword(token, newPassword) {
        await http.post("/auth/reset-password", { token, new_password: newPassword });
    },
};
