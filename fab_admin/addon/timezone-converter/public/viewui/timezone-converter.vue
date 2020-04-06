<template>
<Row  style="padding: 7em 0">
  <Col span="24" offset="1">
    <Converter :span="8"/>
  </Col>
</Row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Converter from '#/timezone-converter/public/viewui/components/converter.vue'

@Component({
  components:{
    Converter
  }
})
export default class TimezoneConverter extends Vue {

}
</script>

<style>

</style>
