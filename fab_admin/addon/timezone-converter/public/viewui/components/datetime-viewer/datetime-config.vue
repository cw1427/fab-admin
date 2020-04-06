<template>
  <Modal
          v-model="computeVisible"
          title="Config source timezone"
          :draggable="false"
          @onCancel="emitDone">
    <Form  :label-width="80">
        <FormItem label="Locale">
                <Select v-model="selectedTimezoneGroup" size="large" style="width:150px" filterable>
                  <Option v-for="item in groupOptions" :value="item.value" :key="item.value">{{ item.text }}</Option>
                </Select>
                 <Select v-model="selectedTimezone" size="large" style="width:150px" filterable>
                  <Option v-for="item in timezoneOptions" :value="item.value" :key="item.value">{{ item.text }}</Option>
                </Select>
        </FormItem>

        <FormItem label="Datetime">
          <DatePicker v-model="selectedTimestamp" size="large" type="datetime" placeholder="Select datetime"></DatePicker>
        </FormItem>
    </Form>
          <div slot="footer">
              <Button type="primary" @click="emitResult">OK</Button>
          </div>

  </Modal>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import * as Timezone from './Timezone'
import moment from 'moment-timezone'

export class Result {
  public timezone: string = ''
  public timestamp: number = Number.MIN_VALUE
  public title: string=''
}

interface ISelectItem {
  value: string
  text: string
}

@Component
export default class DTConfiger extends Vue {
  @Prop()
  private visible!: boolean

  @Prop()
  private timezone!: string

  @Prop()
  private timestamp!: number

  selectedTimezoneGroup: string = (Timezone.getByID(this.timezone) as Timezone.Timezone).group

  selectedTimezone: string = this.timezone

  selectedTimestamp: Date = new Date()

  selectedDate: string = ''

  selectedTime: string = ''

  get NO_GROUP_TEXT (): string {
    return '- others -' as string
  }

  get groupOptions (): ISelectItem[] {
    const result : ISelectItem[] = []
    let hasOthers: boolean = false
    Timezone.getGroups().forEach((group: string): void => {
      if (group === '') {
        hasOthers = true
      } else {
        result.push({ value: group, text: group })
      }
    })
    if (hasOthers) {
      result.push({ value: 'other', text: this.NO_GROUP_TEXT })
    }
    return result
  }

  get timezoneOptions (): ISelectItem[] {
    const result: ISelectItem[] = []
    const grouped = Timezone.getGroupedTimezones()
    if (grouped.hasOwnProperty(this.selectedTimezoneGroup)) {
      grouped[this.selectedTimezoneGroup].forEach((timezone: Timezone.Timezone) => {
        result.push({ value: timezone.id, text: timezone.locality })
      })
    }
    return result
  }


  get computeVisible (): boolean {
    return this.visible
  }

  set computeVisible (value) {
    this.emitDone()
  }

  mounted () {
    this.onTimezoneChanged(this.timezone)
    this.onTimestampChanged(this.timestamp)
  }


  @Watch('timezone')
  onTimezoneChanged (value: string) {
    this.selectedTimezone = value
    const timezone = Timezone.getByID(value)
    if (timezone === null) {
      this.selectedTimezoneGroup = ''
    } else {
      this.selectedTimezoneGroup = timezone.group
    }
  }

  @Watch('timestamp')
  onTimestampChanged (value: number) {
    const datetime = moment.tz(value * 1000, this.timezone)
    this.selectedTimestamp = moment(datetime.format('YYYY-MM-DD HH:mm:ss')).toDate()
  }

  dateStringFormat(d: Date): string{
     return d.getFullYear().toString()+"-"+((d.getMonth()+1).toString().length==2?(d.getMonth()+1).toString():"0"+(d.getMonth()+1).toString())+"-"+(d.getDate().toString().length==2?d.getDate().toString():"0"+d.getDate().toString())+" "+(d.getHours().toString().length==2?d.getHours().toString():"0"+d.getHours().toString())+":"+(d.getMinutes().toString().length==2?d.getMinutes().toString():"0"+d.getMinutes().toString())+":"+(d.getSeconds().toString().length==2?d.getSeconds().toString():"0"+d.getSeconds().toString());
  }


  emitResult (): void {
    const result = new Result()
    result.timezone = this.selectedTimezone
    result.timestamp = moment.tz(this.dateStringFormat(this.selectedTimestamp), this.selectedTimezone ).unix()
    this.$emit('configured', result)
  }

  emitDone (): void {
    this.$emit('configurationCompleted')
  }
}
</script>
