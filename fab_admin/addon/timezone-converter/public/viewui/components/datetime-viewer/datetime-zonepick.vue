<template>
  <Modal
          v-model="computeVisible"
          title="Add other time zone"
          :draggable="false"
          @onCancel="emitDone">
    <Form  :label-width="80">
        <FormItem label="Title">
                <Input v-model="title" placeholder="Other time zone" style="width:300px;"></Input>
        </FormItem>
        <FormItem label="Locale">
                <Select v-model="selectedTimezoneGroup" size="large" style="width:150px;" filterable>
                  <Option v-for="item in groupOptions" :value="item.value" :key="item.value">{{ item.text }}</Option>
                </Select>
                 <Select v-model="selectedTimezone" size="large" style="width:150px" filterable>
                  <Option v-for="item in timezoneOptions" :value="item.value" :key="item.value">{{ item.text }}</Option>
                </Select>
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
import { Result } from './datetime-config.vue'

interface ISelectItem {
  value: string
  text: string
}

@Component
export default class DTZonepick extends Vue {
  @Prop()
  private visible!: boolean

  @Prop()
  private timezone!: string


  selectedTimezoneGroup: string = (Timezone.getByID(Timezone.MY_TIMEZONE) as Timezone.Timezone).group

  selectedTimezone: string = Timezone.MY_TIMEZONE

  title: string = "Other time zone"


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
      result.push({ value: '', text: this.NO_GROUP_TEXT })
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
    this.title = 'Other time zone'
    return this.visible
  }

  set computeVisible (value) {
    this.emitDone()
  }

  mounted () {
    this.onTimezoneChanged(this.timezone)
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

  emitResult (): void {
    const result = new Result()
    result.timezone = this.selectedTimezone
    result.title = this.title
    this.$emit('timezonePicked', result)
  }

  emitDone (): void {
    this.$emit('timezonePickCompleted')
  }

}
</script>