import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "@/App.vue";
import { getInitialLocale, i18n } from "@/i18n";
import router from "@/router";

import "@/assets/main.css";
import "@/services/http";

document.documentElement.setAttribute("lang", getInitialLocale());

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(i18n);

app.mount("#app");
