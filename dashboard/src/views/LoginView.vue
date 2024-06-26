<script setup>
import { reactive }      from 'vue'
import { useRouter }     from 'vue-router'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox           from '@/components/CardBox.vue'
import FormCheckRadio    from '@/components/FormCheckRadio.vue'
import FormField         from '@/components/FormField.vue'
import FormControl       from '@/components/FormControl.vue'
import BaseButton        from '@/components/BaseButton.vue'
import BaseButtons       from '@/components/BaseButtons.vue'
import LayoutGuest       from '@/layouts/LayoutGuest.vue'

import {
    mdiAccount
  , mdiAsterisk
} from '@mdi/js'

const form = reactive({
  login: 'vitor.watanabe',
  pass: 'senha-super-segura',
  remember: true
})

const router = useRouter()

const submit = () => {
  router.push('/')
}
</script>

<template>
  <LayoutGuest>
    <SectionFullScreen v-slot="{ cardClass }" bg="purplePink">
      <CardBox :class="cardClass" is-form @submit.prevent="submit">
        <FormField label="Login" help="Insira seu login">
          <FormControl
            v-model="form.login"
            :icon="mdiAccount"
            name="login"
            autocomplete="usuario"
          />
        </FormField>

        <FormField label="Password" help="Insira sua senha">
          <FormControl
            v-model="form.pass"
            :icon="mdiAsterisk"
            type="senha"
            name="senha"
            autocomplete="senha-atual"
          />
        </FormField>

        <FormCheckRadio
          v-model="form.remember"
          name="lembrar"
          label="lembrar"
          :input-value="true"
        />

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Login" />
            <BaseButton to="/" color="info" outline label="Voltar" />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>
