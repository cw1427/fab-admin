<template>
<div>
  <Row type="flex">
    <Col span="24">
      <Card >
        <p slot="title">
            <Icon type="ios-people"></Icon>
            SSE Hello
        </p>

        <label>{{resString}}</label>

      </Card>
    </Col>
  </Row>
</div>
</template>
<script>
import { NativeEventSource, EventSourcePolyfill,MessageEvent } from 'event-source-polyfill'
import ReconnectingEventSource from "reconnecting-eventsource";
import baseURL from '_conf/url'
global.EventSource =  NativeEventSource || EventSourcePolyfill

export default {
  name: 'Sse',

  data() {
    return {
      resString:''
    }
  },

  methods:{
     sseInit(){
       let source = new ReconnectingEventSource(baseURL + 'sse/api/subscribe',{withCredentials: true,max_retry_time: 3000})
       source.addEventListener('hello',this.handleHelloEvent)
       source.addEventListener('heartbeat',this.handleHeartBeatEvent)
     },

     handleHelloEvent(event){
         this.resString=event.data
     },

     handleHeartBeatEvent(event){
       console.log(event.type)
     }
  },
  created(){
    this.sseInit()
  }

}

</script>
<style>

</style>

