<template>
<div>
  <Row type="flex">
    <Col span="24">
      <Card >
        <p slot="title">
            <Icon type="ios-bug"></Icon>
            <Span>Sample benchmark list</Span>
        </p>
        <BootstrapTable
            :columns="tableColumns"
            :options="options"
            @onPostBody="vueFormatterPostBody"
        >

        </BootstrapTable>
      </Card>
    </Col>
  </Row>
</div>
</template>

<script>
import { Message,Spin,LoadingBar } from 'iview'
import Vue from 'vue'
import baseURL from '_conf/url'
import mixin from '_c/common/btMixin.js'
export default {
  name: 'SampleBenchmark',
  mixins: [mixin],
  components: {
      
  },
  data () {
    return {
      search: {},
      loading:false,
      tableColumns: [
          {
            title: 'id',
            field: 'id',
            visible: false
          },
          {
            title: 'Server',
            field: 'server',
            width: 200,
            minWidth: 100
          },
          {
            title: 'Benchmark server',
            field: 'ben_server',
            width: 150,
            minWidth: 50
          },
          {
            title: 'Site',
            field: 'site',
            width: 80,
          },
          {
            title: 'Operation',
            field: 'operation',
            width: 80,
          },
          {
            title: 'Start',
            field: 'start',
            sortable: true,
          },
          {
            title: 'End',
            field: 'end',
            sortable: true,
          }
        ],
      options: {
          showColumns: true,
          showRefresh: true,
          search: true,
          url: baseURL + 'sample/api/list',
          ajaxOptions: {
            xhrFields: {
                withCredentials: true
            }
          },
          sidePagination: "server",
          pagination: true,
          pageSize: 10,
          pageNumber: 1,
          pageList:[10,20,50,100],
          smartDisplay: false
      },
    }
  },//end of data()
  methods: {
 
  }

}
</script>

<style>

</style>
