type __VLS_Props = {
    modelValue: string;
    label?: string;
    type?: string;
    placeholder?: string;
    error?: string;
    required?: boolean;
    autocomplete?: string;
};
declare const _default: import("vue").DefineComponent<__VLS_Props, {}, {}, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {
    "update:modelValue": (value: string) => any;
}, string, import("vue").PublicProps, Readonly<__VLS_Props> & Readonly<{
    "onUpdate:modelValue"?: ((value: string) => any) | undefined;
}>, {
    label: string;
    type: string;
    placeholder: string;
    error: string;
    required: boolean;
    autocomplete: string;
}, {}, {}, {}, string, import("vue").ComponentProvideOptions, false, {}, any>;
export default _default;
