<template>
<Card style="width:300px;text-align: center">
    <p slot="title" style="text-align: left;">
        <i class="fa fa-clock-o"></i>
        {{ title }}
    </p>

    <slot name="action" slot="extra"/>

    <Tag color="primary"> {{ timezoneDisplay }} </Tag>
    <div class="time-display">
          {{ timeDisplay }}
    </div>
    <div class="date-display">
          {{ dateDisplay }}
    </div>
</Card>

</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import * as Timezone from './Timezone'
import moment from 'moment-timezone'

@Component
export default class DateTimeViewer extends Vue {
  @Prop()
  private title!: string
  @Prop()
  private timezone!: string
  @Prop()
  private timestamp!: number
  get timezoneDisplay () {
    const timezone = Timezone.getByID(this.timezone)
    return timezone === null ? '' : timezone.displayName
  }
  get moment () : moment.Moment {
    return moment.tz(this.timestamp * 1000, this.timezone)
  }
  get timeDisplay () : string {
    return this.moment.format('LT')
  }
  get dateDisplay () : string {
    return this.moment.format('LL')
  }
  get showFooter () : boolean {
    return !!this.$slots.action
  }
}
</script>

<style scoped type="text/scss">
.time-display {
  font-size: 100%;
  font-weight: bold;
}
</style>