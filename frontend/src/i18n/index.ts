import { createI18n } from "vue-i18n";

import en from "@/locales/en.json";
import ko from "@/locales/ko.json";
import ru from "@/locales/ru.json";
import uz from "@/locales/uz.json";

export type SupportedLocale = "ru" | "en" | "uz" | "ko";

export const SUPPORTED_LOCALES: { code: SupportedLocale; label: string; nativeLabel: string }[] = [
  { code: "ru", label: "Russian", nativeLabel: "Русский" },
  { code: "en", label: "English", nativeLabel: "English" },
  { code: "uz", label: "Uzbek", nativeLabel: "O'zbekcha" },
  { code: "ko", label: "Korean", nativeLabel: "한국어" },
];

const LOCALE_STORAGE_KEY = "yulda_locale";
const DEFAULT_LOCALE: SupportedLocale = "ru";

function isSupportedLocale(value: string | null): value is SupportedLocale {
  return SUPPORTED_LOCALES.some((locale) => locale.code === value);
}

export function getInitialLocale(): SupportedLocale {
  const stored = localStorage.getItem(LOCALE_STORAGE_KEY);
  if (isSupportedLocale(stored)) {
    return stored;
  }
  return DEFAULT_LOCALE;
}

export function persistLocale(locale: SupportedLocale): void {
  localStorage.setItem(LOCALE_STORAGE_KEY, locale);
}

export const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: DEFAULT_LOCALE,
  messages: { ru, en, uz, ko },
});

export function setLocale(locale: SupportedLocale): void {
  i18n.global.locale.value = locale;
  persistLocale(locale);
  document.documentElement.setAttribute("lang", locale);
}
