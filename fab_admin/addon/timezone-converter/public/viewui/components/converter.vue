<template>
<div>
  <Row>
    <Col :span="span" >
          <DateTimeViewer
              title="Source time zone"
              :timezone="sourceTimezone"
              :timestamp="timestamp"
            >
              <template v-slot:action>
                <b-button
                  size="sm"
                  variant="success"
                  @click="configure()"
                >
                  <i class="fa fa-pencil-square-o" />
                  Edit
                </b-button>
              </template>
            </DateTimeViewer>
    </Col>

    <Col :span="span">
          <DateTimeViewer
              title="Your time zone"
              :timezone="localTimezone"
              :timestamp="timestamp"
            >
            </DateTimeViewer>
    </Col>

    <Col :span="span">
          <Card style="text-align: center; width:300px;height:152px"
              class="text-center add-timezone"
              border-variant="light"
            >
            <a style="font-size:6em;width:100%;height:100%" @click="pickTimezone"> <i class="fa fa-6 fa-plus"></i> </a>
            </Card>
    </Col>
  </Row>

  <DateTimeOtherViewer
      :otherTimezones="otherTimezones"
      :otherTimezoneTitles="otherTimezoneTitles"
      :timestamp="timestamp"
      :span="span"
      @otherTimezoneDelete="otherTimezoneDelete"
  >
  </DateTimeOtherViewer>

  <DTConfiger
      :timezone="computedSourceTimezone"
      :timestamp="timestamp"
      :visible="showConfig"
      @configured="configured"
      @configurationCompleted="showConfig=false"
  />

  <DTZonepick
      :timezone="computedSourceTimezone"
      :visible="showZonepick"
      @timezonePicked="timezonePicked"
      @timezonePickCompleted="showZonepick=false"
  />
</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import * as LocationHash from '#/timezone-converter/public/viewui/components/datetime-viewer/datetime-util.ts'
import moment from 'moment-timezone'
import DateTimeViewer from '#/timezone-converter/public/viewui/components/datetime-viewer'
import DateTimeOtherViewer from '#/timezone-converter/public/viewui/components/datetime-viewer/datetime-otherviewer.vue'
import DTConfiger from '#/timezone-converter/public/viewui/components/datetime-viewer/datetime-config.vue'
import { Result } from '#/timezone-converter/public/viewui/components/datetime-viewer/datetime-config.vue'
import DTZonepick from '#/timezone-converter/public/viewui/components/datetime-viewer/datetime-zonepick.vue'

@Component({
    components:{
        DateTimeViewer,
        DateTimeOtherViewer,
        DTConfiger,
        DTZonepick
    }
})
export default class Converter extends Vue {

  @Prop()
  private span!: number

  sourceTimezone:string ='America/Chicago'
  localTimezone:string =  moment.tz.guess()
  timestamp: number = Number.MIN_VALUE
  otherTimezones:string[] = []
  otherTimezoneTitles:string[] = []
  showConfig: boolean = false
  showZonepick: boolean = false

  created () {
    const hashData = new LocationHash.HashData()
    hashData.sourceTimezone = 'America/Chicago'
    this.sourceTimezone = hashData.sourceTimezone
    this.timestamp = hashData.timestamp
    this.otherTimezones = hashData.otherTimezones
  }

  configure() {
        this.showConfig=true
  }
  configured (data: Result) {
    this.showConfig = false
    this.sourceTimezone = data.timezone
    this.timestamp = data.timestamp
  }
  pickTimezone () {
       this.showZonepick=true
  }
  timezonePicked(data: Result){
      this.showZonepick = false
      this.otherTimezones.push(data.timezone)
      this.otherTimezoneTitles.push(data.title)
  }

  otherTimezoneDelete(index){
      this.otherTimezones.splice(index, 1)
      this.otherTimezoneTitles.splice(index, 1)
  }

   get  computedSourceTimezone():string  {
       return this.sourceTimezone
   }

}
</script>


<style scoped lang="scss">

.add-timezone {
  cursor: pointer;
  .card-body {
    font-size: 500%;
    opacity: 0.5;
    line-height: 200%;
    &:hover {
      opacity: 1;
    }
  }
}

</style>
