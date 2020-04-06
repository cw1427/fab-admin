<template>
<div>
<template v-for="(tz,index) in watchOtherTimezones">
   <template v-if="index % 3==0">
      <Row  style="padding: 2em 0" :gutter="10" :key="`row_${index}`">
          <template v-if="index < watchOtherTimezones.length">
            <Col :span="span" >
                  <DateTimeViewer
                      :title="otherTimezoneTitles[index]"
                      :timezone="tz"
                      :timestamp="timestamp"
                    >
                    <template v-slot:action>
                      <Button type="error" icon="ios-trash" size="small" @click="emitDelete(index)">Delete</Button>
                    </template>
                    </DateTimeViewer>
            </Col>
          </template>
          <template v-if="index+1 < watchOtherTimezones.length">
            <Col :span="span" >
                  <DateTimeViewer
                      :title="otherTimezoneTitles[index+1]"
                      :timezone="watchOtherTimezones[index+1]"
                      :timestamp="timestamp"
                    >
                    <template v-slot:action>
                      <Button type="error" icon="ios-trash" size="small" @click="emitDelete(index+1)">Delete</Button>
                    </template>
                    </DateTimeViewer>
            </Col>
          </template>
          <template v-if="index+2 < watchOtherTimezones.length">
            <Col  :span="span" >
                  <DateTimeViewer
                      :title="otherTimezoneTitles[index+2]"
                      :timezone="watchOtherTimezones[index+2]"
                      :timestamp="timestamp"
                    >
                    <template v-slot:action>
                      <Button type="error" icon="ios-trash" size="small" @click="emitDelete(index+2)">Delete</Button>
                    </template>
                    </DateTimeViewer>
            </Col>
          </template>
      </Row>
   </template>
</template>
</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import DateTimeViewer from './datetime-viewer'

@Component({
  components: {
    DateTimeViewer
  }
})
export default class DateTimeOtherViewer extends Vue {
  @Prop()
  private otherTimezones!: string[]

  @Prop()
  private otherTimezoneTitles!: string[]

  @Prop()
  private timestamp!: number

  @Prop()
  private span!: number

  get watchOtherTimezones () : string[] {
    return this.otherTimezones
  }

  emitDelete (index): void {
    this.$emit('otherTimezoneDelete', index)
  }



}
</script>

<style>

</style>