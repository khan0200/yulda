import { computed } from "vue";
import { Loader2 } from "lucide-vue-next";
const props = withDefaults(defineProps(), {
    variant: "primary",
    type: "button",
    loading: false,
    disabled: false,
    fullWidth: false,
});
const classes = computed(() => [
    `btn-${props.variant}`,
    props.fullWidth ? "w-full" : "",
]);
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_withDefaultsArg = (function (t) { return t; })({
    variant: "primary",
    type: "button",
    loading: false,
    disabled: false,
    fullWidth: false,
});
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    type: (__VLS_ctx.type),
    ...{ class: (__VLS_ctx.classes) },
    disabled: (__VLS_ctx.disabled || __VLS_ctx.loading),
});
if (__VLS_ctx.loading) {
    const __VLS_0 = {}.Loader2;
    /** @type {[typeof __VLS_components.Loader2, ]} */ ;
    // @ts-ignore
    const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
        ...{ class: "h-4 w-4 animate-spin" },
    }));
    const __VLS_2 = __VLS_1({
        ...{ class: "h-4 w-4 animate-spin" },
    }, ...__VLS_functionalComponentArgsRest(__VLS_1));
}
var __VLS_4 = {};
/** @type {__VLS_StyleScopedClasses['h-4']} */ ;
/** @type {__VLS_StyleScopedClasses['w-4']} */ ;
/** @type {__VLS_StyleScopedClasses['animate-spin']} */ ;
// @ts-ignore
var __VLS_5 = __VLS_4;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            Loader2: Loader2,
            classes: classes,
        };
    },
    __typeProps: {},
    props: {},
});
const __VLS_component = (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeProps: {},
    props: {},
});
export default {};
; /* PartiallyEnd: #4569/main.vue */
