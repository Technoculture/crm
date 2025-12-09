<template>
  <Dialog v-model="show" :options="{ size: '3xl' }">
    <template #body>
      <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
        <div class="mb-5 flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ editMode ? __('Edit Person') : __('Add Person') }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button variant="ghost" class="w-7" @click="show = false" icon="x" />
          </div>
        </div>

        <div class="space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label class="mb-1 block text-sm font-medium text-ink-gray-7">
                {{ __('Salutation') }}
              </label>
              <FormControl
                type="select"
                v-model="_person.salutation"
                :options="salutationOptions"
                class="w-full"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium text-ink-gray-7">
                {{ __('Status') }}
              </label>
              <Link
                class="form-control w-full"
                :value="_person.status"
                doctype="CRM Person Status"
                @change="(v) => (_person.status = v)"
                :placeholder="__('Select Status')"
                :onCreate="createPersonStatus"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium text-ink-gray-7">
                {{ __('First Name') }} <span class="text-red-500">*</span>
              </label>
              <FormControl
                type="text"
                v-model="_person.first_name"
                :placeholder="__('First Name')"
                class="w-full"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium text-ink-gray-7">
                {{ __('Last Name') }}
              </label>
              <FormControl
                type="text"
                v-model="_person.last_name"
                :placeholder="__('Last Name')"
                class="w-full"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium text-ink-gray-7">
                {{ __('Job Title') }}
              </label>
              <FormControl
                type="text"
                v-model="_person.job_title"
                :placeholder="__('Job Title')"
                class="w-full"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium text-ink-gray-7">
                {{ __('Department') }}
              </label>
              <FormControl
                type="text"
                v-model="_person.department"
                :placeholder="__('Department')"
                class="w-full"
              />
            </div>
            <div class="flex items-center gap-2 sm:col-span-2">
              <FormControl
                type="checkbox"
                v-model="_person.is_primary"
              />
              <label class="text-sm font-medium text-ink-gray-7">
                {{ __('Is Primary Contact') }}
              </label>
            </div>
          </div>

          <!-- Emails Section -->
          <div>
            <div class="mb-2 flex items-center justify-between">
              <label class="text-sm font-medium text-ink-gray-7">
                {{ __('Email Addresses') }}
              </label>
              <Button
                variant="ghost"
                icon="plus"
                size="sm"
                @click="addEmail"
              />
            </div>
            <div class="space-y-2">
              <div
                v-for="(email, idx) in _person.emails"
                :key="idx"
                class="flex items-center gap-2"
              >
                <FormControl
                  type="text"
                  v-model="email.email"
                  :placeholder="__('Email')"
                  class="flex-1"
                />
                <FormControl
                  type="select"
                  v-model="email.email_type"
                  :options="emailTypeOptions"
                  class="w-28"
                />
                <FormControl
                  type="checkbox"
                  v-model="email.is_primary"
                  @change="setPrimaryEmail(idx)"
                />
                <Button
                  variant="ghost"
                  icon="trash-2"
                  size="sm"
                  @click="removeEmail(idx)"
                />
              </div>
              <div
                v-if="!_person.emails?.length"
                class="py-2 text-center text-sm text-ink-gray-5"
              >
                {{ __('No emails added') }}
              </div>
            </div>
          </div>

          <!-- Phones Section -->
          <div>
            <div class="mb-2 flex items-center justify-between">
              <label class="text-sm font-medium text-ink-gray-7">
                {{ __('Phone Numbers') }}
              </label>
              <Button
                variant="ghost"
                icon="plus"
                size="sm"
                @click="addPhone"
              />
            </div>
            <div class="space-y-2">
              <div
                v-for="(phone, idx) in _person.phones"
                :key="idx"
                class="flex items-center gap-2"
              >
                <FormControl
                  type="text"
                  v-model="phone.phone"
                  :placeholder="__('Phone')"
                  class="flex-1"
                />
                <FormControl
                  type="select"
                  v-model="phone.phone_type"
                  :options="phoneTypeOptions"
                  class="w-28"
                />
                <FormControl
                  type="checkbox"
                  v-model="phone.is_primary"
                  @change="setPrimaryPhone(idx)"
                />
                <Button
                  variant="ghost"
                  icon="trash-2"
                  size="sm"
                  @click="removePhone(idx)"
                />
              </div>
              <div
                v-if="!_person.phones?.length"
                class="py-2 text-center text-sm text-ink-gray-5"
              >
                {{ __('No phones added') }}
              </div>
            </div>
          </div>

          <!-- Degrees Section -->
          <div>
            <div class="mb-2 flex items-center justify-between">
              <label class="text-sm font-medium text-ink-gray-7">
                {{ __('Degrees / Education') }}
              </label>
              <Button
                variant="ghost"
                icon="plus"
                size="sm"
                @click="addDegree"
              />
            </div>
            <div class="space-y-2">
              <div
                v-for="(degree, idx) in _person.degrees"
                :key="idx"
                class="flex items-center gap-2"
              >
                <FormControl
                  type="text"
                  v-model="degree.degree"
                  :placeholder="__('Degree')"
                  class="flex-1"
                />
                <FormControl
                  type="text"
                  v-model="degree.institution"
                  :placeholder="__('Institution')"
                  class="flex-1"
                />
                <FormControl
                  type="text"
                  v-model="degree.year"
                  :placeholder="__('Year')"
                  class="w-20"
                />
                <Button
                  variant="ghost"
                  icon="trash-2"
                  size="sm"
                  @click="removeDegree(idx)"
                />
              </div>
              <div
                v-if="!_person.degrees?.length"
                class="py-2 text-center text-sm text-ink-gray-5"
              >
                {{ __('No degrees added') }}
              </div>
            </div>
          </div>

          <!-- Notes -->
          <div>
            <label class="mb-1 block text-sm font-medium text-ink-gray-7">
              {{ __('Notes') }}
            </label>
            <FormControl
              type="textarea"
              v-model="_person.notes"
              :placeholder="__('Notes about this person')"
              class="w-full"
              :rows="3"
            />
          </div>

          <ErrorMessage v-if="error" :message="__(error)" />
        </div>
      </div>
      <div class="px-4 pb-7 pt-4 sm:px-6">
        <div class="flex flex-row-reverse gap-2">
          <Button
            variant="solid"
            :label="editMode ? __('Update') : __('Add')"
            :loading="isSubmitting"
            @click="submitPerson"
          />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import Link from '@/components/Controls/Link.vue'
import { call } from 'frappe-ui'
import { ref, watch, computed } from 'vue'

const props = defineProps({
  person: {
    type: Object,
    default: () => ({}),
  },
  lead: {
    type: String,
    required: true,
  },
})

const show = defineModel()
const emit = defineEmits(['personAdded', 'personUpdated'])

const error = ref(null)
const isSubmitting = ref(false)
const _person = ref({
  salutation: '',
  first_name: '',
  last_name: '',
  status: 'Active',
  job_title: '',
  department: '',
  is_primary: false,
  emails: [],
  phones: [],
  degrees: [],
  notes: '',
})

const editMode = computed(() => !!props.person?.name)

const salutationOptions = [
  { label: '', value: '' },
  { label: 'Mr', value: 'Mr' },
  { label: 'Mrs', value: 'Mrs' },
  { label: 'Ms', value: 'Ms' },
  { label: 'Dr', value: 'Dr' },
  { label: 'Prof', value: 'Prof' },
]

const emailTypeOptions = [
  { label: 'Work', value: 'Work' },
  { label: 'Personal', value: 'Personal' },
  { label: 'Other', value: 'Other' },
]

const phoneTypeOptions = [
  { label: 'Mobile', value: 'Mobile' },
  { label: 'Work', value: 'Work' },
  { label: 'Home', value: 'Home' },
  { label: 'Other', value: 'Other' },
]

watch(
  () => props.person,
  (newPerson) => {
    if (newPerson?.name) {
      _person.value = {
        ...newPerson,
        emails: newPerson.emails || [],
        phones: newPerson.phones || [],
        degrees: newPerson.degrees || [],
      }
    } else {
      resetPerson()
    }
  },
  { immediate: true }
)

function resetPerson() {
  _person.value = {
    salutation: '',
    first_name: '',
    last_name: '',
    status: 'Active',
    job_title: '',
    department: '',
    is_primary: false,
    emails: [],
    phones: [],
    degrees: [],
    notes: '',
  }
}

function addEmail() {
  _person.value.emails.push({
    email: '',
    email_type: 'Work',
    is_primary: _person.value.emails.length === 0,
  })
}

function removeEmail(idx) {
  _person.value.emails.splice(idx, 1)
}

function setPrimaryEmail(idx) {
  _person.value.emails.forEach((e, i) => {
    e.is_primary = i === idx
  })
}

function addPhone() {
  _person.value.phones.push({
    phone: '',
    phone_type: 'Mobile',
    is_primary: _person.value.phones.length === 0,
  })
}

function removePhone(idx) {
  _person.value.phones.splice(idx, 1)
}

function setPrimaryPhone(idx) {
  _person.value.phones.forEach((p, i) => {
    p.is_primary = i === idx
  })
}

function addDegree() {
  _person.value.degrees.push({
    degree: '',
    institution: '',
    year: '',
  })
}

function removeDegree(idx) {
  _person.value.degrees.splice(idx, 1)
}

async function createPersonStatus(value, close) {
  await call('frappe.client.insert', {
    doc: {
      doctype: 'CRM Person Status',
      status_name: value,
      color: 'gray',
    },
  })
  _person.value.status = value
  close()
}

async function submitPerson() {
  error.value = null

  if (!_person.value.first_name) {
    error.value = __('First Name is required')
    return
  }

  isSubmitting.value = true

  try {
    if (editMode.value) {
      await call('crm.fcrm.doctype.crm_lead_person.crm_lead_person.update_person', {
        person_name: props.person.name,
        person_data: _person.value,
      })
      emit('personUpdated')
    } else {
      await call('crm.fcrm.doctype.crm_lead_person.crm_lead_person.add_person', {
        lead: props.lead,
        person_data: _person.value,
      })
      emit('personAdded')
    }
    show.value = false
  } catch (err) {
    error.value = err.messages?.[0] || err.message || __('An error occurred')
  } finally {
    isSubmitting.value = false
  }
}
</script>

