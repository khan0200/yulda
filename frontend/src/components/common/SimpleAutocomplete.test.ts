import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import SimpleAutocomplete from "./SimpleAutocomplete.vue";

const OPTIONS = ["Hyundai", "Kia", "Genesis", "BMW", "Mercedes-Benz"];

describe("SimpleAutocomplete", () => {
  it("renders the current modelValue in the input", () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "Hyundai", options: OPTIONS },
    });
    expect((wrapper.find("input").element as HTMLInputElement).value).toBe("Hyundai");
  });

  it("shows all options (capped at 20) when focused with an empty value", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "", options: OPTIONS },
    });
    await wrapper.find("input").trigger("focus");
    expect(wrapper.findAll("li")).toHaveLength(OPTIONS.length);
  });

  it("filters options case-insensitively based on modelValue", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "ge", options: OPTIONS },
    });
    await wrapper.find("input").trigger("focus");

    const items = wrapper.findAll("li").map((li) => li.text());
    expect(items).toEqual(["Genesis"]);
  });

  it("emits update:modelValue on every keystroke", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "", options: OPTIONS },
    });
    await wrapper.find("input").setValue("Ki");
    expect(wrapper.emitted("update:modelValue")?.at(-1)).toEqual(["Ki"]);
  });

  it("selects an option on mousedown and closes the dropdown", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "", options: OPTIONS },
    });
    await wrapper.find("input").trigger("focus");
    await wrapper.findAll("li")[1].trigger("mousedown");

    expect(wrapper.emitted("update:modelValue")?.at(-1)).toEqual(["Kia"]);
    expect(wrapper.find("ul").exists()).toBe(false);
  });

  it("selects the first filtered option on Enter", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "ben", options: OPTIONS },
    });
    await wrapper.find("input").trigger("keydown.enter");

    expect(wrapper.emitted("update:modelValue")?.at(-1)).toEqual(["Mercedes-Benz"]);
  });

  it("closes the dropdown on Escape", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "", options: OPTIONS },
    });
    await wrapper.find("input").trigger("focus");
    expect(wrapper.find("ul").exists()).toBe(true);

    await wrapper.find("input").trigger("keydown.escape");
    expect(wrapper.find("ul").exists()).toBe(false);
  });

  it("does not open the dropdown when disabled", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "", options: OPTIONS, disabled: true },
    });
    await wrapper.find("input").trigger("focus");
    expect(wrapper.find("ul").exists()).toBe(false);
  });

  it("shows no matches when nothing filters", async () => {
    const wrapper = mount(SimpleAutocomplete, {
      props: { modelValue: "zzz-no-match", options: OPTIONS },
    });
    await wrapper.find("input").trigger("focus");

    expect(wrapper.find("ul").exists()).toBe(false);
  });
});
