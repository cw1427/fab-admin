<template>
<div>
  <Row type="flex">
    <Col span="24">
      <Card >
        <p slot="title">
            <i class="fa fa-anchor"></i>
            Echart Typescript Sample
        </p>
        <div ref="dom" style="width:100%;height:400px"></div>
      </Card>
    </Col>
  </Row>
</div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import echarts from "echarts";

@Component
export default class EchartSample extends Vue {
  name = "echartSample";

  //data
  dom: echarts.ECharts | null = null;

  resize() {
    this.dom && this.dom!.resize();
  }
  created() {
    const option = {
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "cross",
          label: {
            backgroundColor: "#6a7985"
          }
        }
      },
      grid: {
        top: "3%",
        left: "1.2%",
        right: "1%",
        bottom: "3%",
        containLabel: true
      },
      xAxis: [
        {
          type: "category",
          boundaryGap: false,
          data: ["Mon", "Tue", "Wen", "Thi", "Fri", "Sat", "Sun"]
        }
      ],
      yAxis: [
        {
          type: "value"
        }
      ],
      series: [
        {
          name: "Supplier",
          type: "line",
          stack: "Total",
          areaStyle: {
            normal: {
              color: "#2d8cf0"
            }
          },
          data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
          name: "Bank",
          type: "line",
          stack: "Total",
          areaStyle: {
            normal: {
              color: "#10A6FF"
            }
          },
          data: [257, 358, 278, 234, 290, 330, 310]
        },
        {
          name: "Game",
          type: "line",
          stack: "Total",
          areaStyle: {
            normal: {
              color: "#0C17A6"
            }
          },
          data: [379, 268, 354, 269, 310, 478, 358]
        },
        {
          name: "Food",
          type: "line",
          stack: "Total",
          areaStyle: {
            normal: {
              color: "#4608A6"
            }
          },
          data: [320, 332, 301, 334, 390, 330, 320]
        },
        {
          name: "Express",
          type: "line",
          stack: "Total",
          label: {
            normal: {
              show: true,
              position: "top"
            }
          },
          areaStyle: {
            normal: {
              color: "#398DBF"
            }
          },
          data: [820, 645, 546, 745, 872, 624, 258]
        }
      ]
    };

    this.$nextTick(() => {
      this.dom = echarts.init(this.$refs.dom as HTMLDivElement);
      this.dom.setOption(option as echarts.EChartOption);
    });

  }
  beforeDestroy() {
  }
}
</script>

<style>

</style>
