import { reactive, ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { AxiosError } from "axios";
import BaseButton from "@/components/common/BaseButton.vue";
import BaseInput from "@/components/common/BaseInput.vue";
import { useAuthStore } from "@/stores/authStore";
const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const form = reactive({ email: "", password: "" });
const errorMessage = ref("");
const isSubmitting = ref(false);
async function handleSubmit() {
    errorMessage.value = "";
    isSubmitting.value = true;
    try {
        await auth.login(form);
        const redirect = typeof route.query.redirect === "string" ? route.query.redirect : "/";
        router.push(redirect);
    }
    catch (error) {
        if (error instanceof AxiosError) {
            const data = error.response?.data;
            errorMessage.value = data?.message ?? "Unable to log in. Please try again.";
        }
        else {
            errorMessage.value = "Unable to log in. Please try again.";
        }
    }
    finally {
        isSubmitting.value = false;
    }
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({
    ...{ class: "text-2xl font-bold text-yulda-black" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "mt-2 text-sm text-yulda-gray-500" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
    ...{ onSubmit: (__VLS_ctx.handleSubmit) },
    ...{ class: "mt-8 flex flex-col gap-4" },
});
/** @type {[typeof BaseInput, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(BaseInput, new BaseInput({
    modelValue: (__VLS_ctx.form.email),
    type: "email",
    label: "Email",
    placeholder: "you@example.com",
    autocomplete: "email",
    required: true,
}));
const __VLS_1 = __VLS_0({
    modelValue: (__VLS_ctx.form.email),
    type: "email",
    label: "Email",
    placeholder: "you@example.com",
    autocomplete: "email",
    required: true,
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
/** @type {[typeof BaseInput, ]} */ ;
// @ts-ignore
const __VLS_3 = __VLS_asFunctionalComponent(BaseInput, new BaseInput({
    modelValue: (__VLS_ctx.form.password),
    type: "password",
    label: "Password",
    placeholder: "••••••••",
    autocomplete: "current-password",
    required: true,
}));
const __VLS_4 = __VLS_3({
    modelValue: (__VLS_ctx.form.password),
    type: "password",
    label: "Password",
    placeholder: "••••••••",
    autocomplete: "current-password",
    required: true,
}, ...__VLS_functionalComponentArgsRest(__VLS_3));
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "flex justify-end" },
});
const __VLS_6 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
// @ts-ignore
const __VLS_7 = __VLS_asFunctionalComponent(__VLS_6, new __VLS_6({
    to: "/forgot-password",
    ...{ class: "text-sm font-medium text-yulda-gray-600 hover:text-yulda-black" },
}));
const __VLS_8 = __VLS_7({
    to: "/forgot-password",
    ...{ class: "text-sm font-medium text-yulda-gray-600 hover:text-yulda-black" },
}, ...__VLS_functionalComponentArgsRest(__VLS_7));
__VLS_9.slots.default;
var __VLS_9;
if (__VLS_ctx.errorMessage) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600" },
    });
    (__VLS_ctx.errorMessage);
}
/** @type {[typeof BaseButton, typeof BaseButton, ]} */ ;
// @ts-ignore
const __VLS_10 = __VLS_asFunctionalComponent(BaseButton, new BaseButton({
    type: "submit",
    fullWidth: true,
    loading: (__VLS_ctx.isSubmitting),
}));
const __VLS_11 = __VLS_10({
    type: "submit",
    fullWidth: true,
    loading: (__VLS_ctx.isSubmitting),
}, ...__VLS_functionalComponentArgsRest(__VLS_10));
__VLS_12.slots.default;
var __VLS_12;
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "mt-8 text-sm text-yulda-gray-500" },
});
const __VLS_13 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
// @ts-ignore
const __VLS_14 = __VLS_asFunctionalComponent(__VLS_13, new __VLS_13({
    to: "/signup",
    ...{ class: "font-semibold text-yulda-black" },
}));
const __VLS_15 = __VLS_14({
    to: "/signup",
    ...{ class: "font-semibold text-yulda-black" },
}, ...__VLS_functionalComponentArgsRest(__VLS_14));
__VLS_16.slots.default;
var __VLS_16;
/** @type {__VLS_StyleScopedClasses['text-2xl']} */ ;
/** @type {__VLS_StyleScopedClasses['font-bold']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-black']} */ ;
/** @type {__VLS_StyleScopedClasses['mt-2']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-gray-500']} */ ;
/** @type {__VLS_StyleScopedClasses['mt-8']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-4']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['justify-end']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-gray-600']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:text-yulda-black']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-red-50']} */ ;
/** @type {__VLS_StyleScopedClasses['px-4']} */ ;
/** @type {__VLS_StyleScopedClasses['py-3']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['text-red-600']} */ ;
/** @type {__VLS_StyleScopedClasses['mt-8']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-gray-500']} */ ;
/** @type {__VLS_StyleScopedClasses['font-semibold']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-black']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            RouterLink: RouterLink,
            BaseButton: BaseButton,
            BaseInput: BaseInput,
            form: form,
            errorMessage: errorMessage,
            isSubmitting: isSubmitting,
            handleSubmit: handleSubmit,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
