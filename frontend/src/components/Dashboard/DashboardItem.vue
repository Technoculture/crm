<template>
  <div class="h-full w-full">
    <div
      v-if="item.type == 'number_chart'"
      class="flex h-full w-full rounded shadow overflow-hidden cursor-pointer relative"
    >
      <div
        v-if="numberFilterOptions.length"
        class="absolute right-2 top-2 z-10"
      >
        <Dropdown
          size="sm"
          variant="ghost"
          v-model="selectedFilter"
          :options="numberFilterOptions"
        />
      </div>
      <Tooltip :text="__(item.data.tooltip)">
        <NumberChart
          class="!items-start"
          v-if="numberConfig"
          :key="index + String(selectedFilter)"
          :config="numberConfig"
        />
      </Tooltip>
    </div>
    <div
      v-else-if="item.type == 'spacer'"
      class="rounded bg-surface-white h-full overflow-hidden text-ink-gray-5 flex items-center justify-center"
      :class="editing ? 'border border-dashed border-outline-gray-2' : ''"
    >
      {{ editing ? __('Spacer') : '' }}
    </div>
    <div
      v-else-if="item.type == 'axis_chart'"
      class="h-full w-full rounded-md bg-surface-white shadow"
    >
      <AxisChart v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'donut_chart'"
      class="h-full w-full rounded-md bg-surface-white shadow overflow-hidden"
    >
      <DonutChart v-if="item.data" :config="item.data" />
    </div>
  </div>
</template>
<script setup>
import { AxisChart, DonutChart, NumberChart, Tooltip, Dropdown } from 'frappe-ui'
import { computed, ref, watch } from 'vue'

const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
  editing: {
    type: Boolean,
    default: false,
  },
})

const selectedFilter = ref(null)

const numberFilterOptions = computed(() => {
  if (props.item.type !== 'number_chart') return []
  return props.item.data?.filters?.map((f) => ({
    label: __(f.label || f.value),
    value: f.value,
  })) || []
})

const numberConfig = computed(() => {
  if (props.item.type !== 'number_chart') return null
  if (!props.item.data) return null

  const config = { ...props.item.data }

  if (config.filters?.length && config.values) {
    const active =
      selectedFilter.value ||
      (config.filters.find((f) => f.default)?.value ?? config.filters[0]?.value)
    const activeKey =
      config.filters.find((f) => f.value === active)?.key || config.filters[0]?.key

    if (activeKey && Object.prototype.hasOwnProperty.call(config.values, activeKey)) {
      config.value = config.values[activeKey] ?? config.value
    }
  }

  return config
})

watch(
  () => props.item?.data,
  (data) => {
    if (data?.filters?.length) {
      selectedFilter.value = data.filters.find((f) => f.default)?.value || data.filters[0].value
    } else {
      selectedFilter.value = null
    }
  },
  { immediate: true },
)
</script>
