<template>
  <div class="theme-button">
    <Dropdown transfer @on-click="handleClick" style="margin-top:5px;">
         <a href="javascript:void(0)">
            <Icon :size="23" v-if="theme=='light'" type="ios-cog-outline"></Icon>
            <Icon :size="23" v-else type="ios-cog"></Icon>
         </a>
        <DropdownMenu slot="list">
          <DropdownItem name="light" v-on:click.self.prevent><Checkbox v-on:click.self.prevent v-on:change.self.prevent :value="theme=='light'" :style="{width: '100%'}">light</Checkbox></DropdownItem>
          <DropdownItem name="dark"><Checkbox :value="theme=='dark'" :style="{width: '100%'}">dark</Checkbox></DropdownItem>
        </DropdownMenu>
    </Dropdown>
  </div>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'

export default {
  name: 'Theme',
  data () {
    return {
      theme:this.$store.getters.themeGetter
    }
  },

  methods: {
    ...mapMutations([
      'setTheme'
    ]),
    handleClick (name) {
        this.theme = name
        this.setTheme(name)
    }
  },

}
</script>

<style>

</style>
>
