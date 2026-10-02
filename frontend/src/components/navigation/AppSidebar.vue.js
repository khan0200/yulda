import { RouterLink } from "vue-router";
import { Car, Heart, Home, MessageSquare, Package, Settings, ShoppingBag, User, Wallet, Wrench, } from "lucide-vue-next";
const mainLinks = [
    { to: "/", label: "Home", icon: Home },
    { to: "/taxi", label: "Taxi", icon: Car },
    { to: "/delivery", label: "Delivery", icon: Package },
    { to: "/jobs", label: "Jobs", icon: ShoppingBag },
    { to: "/services", label: "Services", icon: Wrench },
];
const secondaryLinks = [
    { to: "/orders", label: "Orders", icon: ShoppingBag },
    { to: "/messages", label: "Messages", icon: MessageSquare },
    { to: "/favorites", label: "Favorites", icon: Heart },
];
const accountLinks = [
    { to: "/payments", label: "Payments", icon: Wallet },
    { to: "/profile", label: "Settings", icon: Settings },
];
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.aside, __VLS_intrinsicElements.aside)({
    ...{ class: "flex h-full w-64 flex-col border-r border-yulda-gray-100 bg-white px-4 py-6" },
});
const __VLS_0 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    to: "/",
    ...{ class: "mb-8 px-2 text-xl font-extrabold tracking-tight" },
}));
const __VLS_2 = __VLS_1({
    to: "/",
    ...{ class: "mb-8 px-2 text-xl font-extrabold tracking-tight" },
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
__VLS_3.slots.default;
var __VLS_3;
__VLS_asFunctionalElement(__VLS_intrinsicElements.nav, __VLS_intrinsicElements.nav)({
    ...{ class: "flex flex-1 flex-col gap-6" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "flex flex-col gap-1" },
});
for (const [link] of __VLS_getVForSourceType((__VLS_ctx.mainLinks))) {
    const __VLS_4 = {}.RouterLink;
    /** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
    // @ts-ignore
    const __VLS_5 = __VLS_asFunctionalComponent(__VLS_4, new __VLS_4({
        key: (link.to),
        to: (link.to),
        ...{ class: "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black" },
        activeClass: "bg-yulda-yellow/15 text-yulda-black font-semibold",
    }));
    const __VLS_6 = __VLS_5({
        key: (link.to),
        to: (link.to),
        ...{ class: "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black" },
        activeClass: "bg-yulda-yellow/15 text-yulda-black font-semibold",
    }, ...__VLS_functionalComponentArgsRest(__VLS_5));
    __VLS_7.slots.default;
    const __VLS_8 = ((link.icon));
    // @ts-ignore
    const __VLS_9 = __VLS_asFunctionalComponent(__VLS_8, new __VLS_8({
        ...{ class: "h-[18px] w-[18px]" },
    }));
    const __VLS_10 = __VLS_9({
        ...{ class: "h-[18px] w-[18px]" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_9));
    (link.label);
    var __VLS_7;
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "flex flex-col gap-1 border-t border-yulda-gray-100 pt-4" },
});
for (const [link] of __VLS_getVForSourceType((__VLS_ctx.secondaryLinks))) {
    const __VLS_12 = {}.RouterLink;
    /** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
    // @ts-ignore
    const __VLS_13 = __VLS_asFunctionalComponent(__VLS_12, new __VLS_12({
        key: (link.to),
        to: (link.to),
        ...{ class: "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black" },
        activeClass: "bg-yulda-yellow/15 text-yulda-black font-semibold",
    }));
    const __VLS_14 = __VLS_13({
        key: (link.to),
        to: (link.to),
        ...{ class: "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black" },
        activeClass: "bg-yulda-yellow/15 text-yulda-black font-semibold",
    }, ...__VLS_functionalComponentArgsRest(__VLS_13));
    __VLS_15.slots.default;
    const __VLS_16 = ((link.icon));
    // @ts-ignore
    const __VLS_17 = __VLS_asFunctionalComponent(__VLS_16, new __VLS_16({
        ...{ class: "h-[18px] w-[18px]" },
    }));
    const __VLS_18 = __VLS_17({
        ...{ class: "h-[18px] w-[18px]" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_17));
    (link.label);
    var __VLS_15;
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "flex flex-col gap-1 border-t border-yulda-gray-100 pt-4" },
});
for (const [link] of __VLS_getVForSourceType((__VLS_ctx.accountLinks))) {
    const __VLS_20 = {}.RouterLink;
    /** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
    // @ts-ignore
    const __VLS_21 = __VLS_asFunctionalComponent(__VLS_20, new __VLS_20({
        key: (link.to),
        to: (link.to),
        ...{ class: "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black" },
        activeClass: "bg-yulda-yellow/15 text-yulda-black font-semibold",
    }));
    const __VLS_22 = __VLS_21({
        key: (link.to),
        to: (link.to),
        ...{ class: "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-yulda-gray-700 hover:bg-yulda-gray-100 hover:text-yulda-black" },
        activeClass: "bg-yulda-yellow/15 text-yulda-black font-semibold",
    }, ...__VLS_functionalComponentArgsRest(__VLS_21));
    __VLS_23.slots.default;
    const __VLS_24 = ((link.icon));
    // @ts-ignore
    const __VLS_25 = __VLS_asFunctionalComponent(__VLS_24, new __VLS_24({
        ...{ class: "h-[18px] w-[18px]" },
    }));
    const __VLS_26 = __VLS_25({
        ...{ class: "h-[18px] w-[18px]" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_25));
    (link.label);
    var __VLS_23;
}
const __VLS_28 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.RouterLink, ]} */ ;
// @ts-ignore
const __VLS_29 = __VLS_asFunctionalComponent(__VLS_28, new __VLS_28({
    to: "/profile",
    ...{ class: "mt-4 flex items-center gap-3 rounded-xl border border-yulda-gray-100 px-3 py-2.5 hover:bg-yulda-gray-50" },
}));
const __VLS_30 = __VLS_29({
    to: "/profile",
    ...{ class: "mt-4 flex items-center gap-3 rounded-xl border border-yulda-gray-100 px-3 py-2.5 hover:bg-yulda-gray-50" },
}, ...__VLS_functionalComponentArgsRest(__VLS_29));
__VLS_31.slots.default;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "flex h-8 w-8 items-center justify-center rounded-full bg-yulda-black text-white" },
});
const __VLS_32 = {}.User;
/** @type {[typeof __VLS_components.User, ]} */ ;
// @ts-ignore
const __VLS_33 = __VLS_asFunctionalComponent(__VLS_32, new __VLS_32({
    ...{ class: "h-4 w-4" },
}));
const __VLS_34 = __VLS_33({
    ...{ class: "h-4 w-4" },
}, ...__VLS_functionalComponentArgsRest(__VLS_33));
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
    ...{ class: "truncate text-sm font-medium" },
});
var __VLS_31;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['h-full']} */ ;
/** @type {__VLS_StyleScopedClasses['w-64']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['border-r']} */ ;
/** @type {__VLS_StyleScopedClasses['border-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-white']} */ ;
/** @type {__VLS_StyleScopedClasses['px-4']} */ ;
/** @type {__VLS_StyleScopedClasses['py-6']} */ ;
/** @type {__VLS_StyleScopedClasses['mb-8']} */ ;
/** @type {__VLS_StyleScopedClasses['px-2']} */ ;
/** @type {__VLS_StyleScopedClasses['text-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['font-extrabold']} */ ;
/** @type {__VLS_StyleScopedClasses['tracking-tight']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-1']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-6']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-1']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['px-3']} */ ;
/** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-gray-700']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:bg-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:text-yulda-black']} */ ;
/** @type {__VLS_StyleScopedClasses['h-[18px]']} */ ;
/** @type {__VLS_StyleScopedClasses['w-[18px]']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-1']} */ ;
/** @type {__VLS_StyleScopedClasses['border-t']} */ ;
/** @type {__VLS_StyleScopedClasses['border-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['pt-4']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['px-3']} */ ;
/** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-gray-700']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:bg-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:text-yulda-black']} */ ;
/** @type {__VLS_StyleScopedClasses['h-[18px]']} */ ;
/** @type {__VLS_StyleScopedClasses['w-[18px]']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['flex-col']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-1']} */ ;
/** @type {__VLS_StyleScopedClasses['border-t']} */ ;
/** @type {__VLS_StyleScopedClasses['border-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['pt-4']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['px-3']} */ ;
/** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
/** @type {__VLS_StyleScopedClasses['text-yulda-gray-700']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:bg-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:text-yulda-black']} */ ;
/** @type {__VLS_StyleScopedClasses['h-[18px]']} */ ;
/** @type {__VLS_StyleScopedClasses['w-[18px]']} */ ;
/** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['gap-3']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-xl']} */ ;
/** @type {__VLS_StyleScopedClasses['border']} */ ;
/** @type {__VLS_StyleScopedClasses['border-yulda-gray-100']} */ ;
/** @type {__VLS_StyleScopedClasses['px-3']} */ ;
/** @type {__VLS_StyleScopedClasses['py-2.5']} */ ;
/** @type {__VLS_StyleScopedClasses['hover:bg-yulda-gray-50']} */ ;
/** @type {__VLS_StyleScopedClasses['flex']} */ ;
/** @type {__VLS_StyleScopedClasses['h-8']} */ ;
/** @type {__VLS_StyleScopedClasses['w-8']} */ ;
/** @type {__VLS_StyleScopedClasses['items-center']} */ ;
/** @type {__VLS_StyleScopedClasses['justify-center']} */ ;
/** @type {__VLS_StyleScopedClasses['rounded-full']} */ ;
/** @type {__VLS_StyleScopedClasses['bg-yulda-black']} */ ;
/** @type {__VLS_StyleScopedClasses['text-white']} */ ;
/** @type {__VLS_StyleScopedClasses['h-4']} */ ;
/** @type {__VLS_StyleScopedClasses['w-4']} */ ;
/** @type {__VLS_StyleScopedClasses['truncate']} */ ;
/** @type {__VLS_StyleScopedClasses['text-sm']} */ ;
/** @type {__VLS_StyleScopedClasses['font-medium']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            RouterLink: RouterLink,
            User: User,
            mainLinks: mainLinks,
            secondaryLinks: secondaryLinks,
            accountLinks: accountLinks,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
