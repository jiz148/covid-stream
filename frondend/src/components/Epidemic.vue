<template>
  <div>
    <h1 class="title">
      {{ mainTitle }}
    </h1>
    <a-divider orientation="center"/>
    <a-row :align="center" type="flex" class="content">

      <!-- part1 -->
      <a-col class="leftCol">
<!--        <a-col :flex="4">-->
        <!-- pie chart -->
        <a-card style="color: #939191" :title="pieTitle" >
          <div id="pieChart" style="width: 100%; min-width: 200px; height: 300px"></div>
        </a-card>
        <!-- line chart -->
        <a-card :title="lineTitle" >
          <div id="lineChart" style="width: 100%; min-width: 200px; height: 300px"></div>
        </a-card>
      </a-col>

      <!-- part2 -->
      <a-col class="midCol">
        <!-- thermodynamic -->
        <a-card :title="thermodynamicTitle" >
          <div id="thermodynamicChart" style="width: 100%; min-width: 300px; height: 400%"></div>
        </a-card>
      </a-col>

      <!-- part3 -->
      <a-col class="rightCol">
        <!-- vertical chart -->
        <a-card :title="verticalTitle" >
          <div id="verticalChart" style="width: 100%; min-width: 200px; height: 300px"></div>
        </a-card>
        <!-- crosswise chart -->
        <a-card :title="crosswiseTitle" >
          <div id="crosswiseChart" style="width: 100%; min-width: 200px; height: 300px"></div>
        </a-card>
      </a-col>

    </a-row>


  </div>
</template>

<script>
import service from "../utils/request";
import postAction from "../utils/request";
import "./main.css";


// chart part
import * as echarts from 'echarts/core';



import axios from "axios";

import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  GridComponent,
  DataZoomComponent,
  VisualMapComponent,
  GeoComponent
} from 'echarts/components';

import { PieChart } from 'echarts/charts';
import { LabelLayout } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { BarChart } from 'echarts/charts';
import { MapChart } from 'echarts/charts';

echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  PieChart,
  CanvasRenderer,
  LabelLayout,
  LineChart,
  UniversalTransition,
  ToolboxComponent,
  GridComponent,
  DataZoomComponent,
  BarChart,
  VisualMapComponent,
  GeoComponent,
  MapChart
]);


export default {
  name: 'Epidemic',
  data () {
    return {
      // Title
      mainTitle: 'CS543 Project 1: Covid-19 Data Visualization',
      // pie
      pieTitle: "Male - Female Pie Chart",
      // lie
      lineTitle: "Cases by Time",
      // map
      thermodynamicTitle: "Thermodynamic Map",
      // vertical
      verticalTitle: "Age Groups",
      // crosswise
      crosswiseTitle: "Medical Process",
      // Timer
      refreshTime: 5,

      // chart options
      pieOptions: {},
      lineOptions: {},
      thermodynamicOptions: {},
      verticalOptions: {},
      crosswiseOptions: {},

      center: 'center',


      // word map json
      dataMapNew: {},
      dataMapNewData: []


    }
  },
  methods: {
    getChartInfo(){
      let url = "/getChartInfo"
      let data = {}
      postAction(url, data).then((res) => {
        // load chart

        console.log('rrr',res)

        res = res.data

        let pie = res.pie
        let line = res.line
        let thermodynamic = res.thermodynamic
        let vertical = res.vertical
        let crosswise = res.crosswise

        // load chart
        this.pieChart(pie)
        this.lineChart(line)
        this.thermodynamicChart(thermodynamic)
        this.verticalChart(vertical)
        this.crosswiseChart(crosswise)

      })
    },
    pieChart(data){
      let chartDom = document.getElementById('pieChart');
      let myChart = echarts.init(chartDom);
      let option;
      // set option
      option = {
        // title: {
        //   text: 'Referer of a Website',
        // subtext: 'Fake Data',
        //   left: 'center'
        // },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: data,
            // data: [
            //   { value: 100, name: 'male' },
            //   { value: 200, name: 'female' }
            // ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      myChart.setOption(option);
    },
    lineChart(data){
      let chartDom = document.getElementById('lineChart');
      let myChart = echarts.init(chartDom);
      let option;
      // set option
      option = {
        tooltip: {
          trigger: 'axis',
          position: function (pt) {
            return [pt[0], '50%'];
          }
        },
        // title: {
        //   left: 'center',
        //   text: this.lineTitle
        // },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'time',
          boundaryGap: false
        },
        yAxis: {
          type: 'value',
          boundaryGap: [0, '100%']
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100
          },
          {
            start: 0,
            end: 20
          }
        ],
        series: [
          {
            name: this.lineTitle,
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {},
            data: data
            // data: [
            //   ['2020-01', 100],
            //   ['2020-02', 343],
            //   ['2020-03', 52],
            //   ['2020-04', 300],
            //   ['2020-05', 400],
            //   ['2020-06', 244],
            //   ['2020-07', 32]
            // ]
          }
        ]
      }
      myChart.setOption(option);
    },
    thermodynamicChart(data){
      let chartDom = document.getElementById('thermodynamicChart');
      let myChart = echarts.init(chartDom);
      myChart.showLoading();
      myChart.hideLoading();
      let option;
      let usaJson;
      usaJson = this.dataMapNew
      console.log('uuu', usaJson)
      // register map
      echarts.registerMap('USA', usaJson, {
        Alaska: {
          left: -131,
          top: 25,
          width: 15
        },
        Hawaii: {
          left: -110,
          top: 28,
          width: 5
        },
        'Puerto Rico': {
          left: -76,
          top: 26,
          width: 2
        }
      });

      // set option
      option = {
        // title: {
        //   text: 'USA Population Estimates (2012)',
        //   subtext: 'Data from www.census.gov',
        //   sublink: 'http://www.census.gov/popest/data/datasets.html',
        //   left: 'right'
        // },
        tooltip: {
          trigger: 'item',
          showDelay: 0,
          transitionDuration: 0.2,
          formatter: function (params) {
            console.log("params.", params)
            const value = (params.value + '').split('.');
            const valueStr = value[0].replace(
              /(\d{1,3})(?=(?:\d{3})+(?!\d))/g,
              '$1,'
            );
            return params.seriesName + '<br/>' + params.name + ': ' + valueStr;
          }
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 5000000,
          inRange: {
            color: [
              '#313695',
              '#4575b4',
              '#74add1',
              '#abd9e9',
              '#e0f3f8',
              '#ffffbf',
              '#fee090',
              '#fdae61',
              '#f46d43',
              '#d73027',
              '#a50026'
            ]
          },
          text: ['High', 'Low'],
          calculable: true
        },
        toolbox: {
          show: true,
          //orient: 'vertical',
          left: 'left',
          top: 'top',
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        series: [
          {
            name: 'result',
            type: 'map',
            roam: true,
            map: 'USA',
            emphasis: {
              label: {
                show: true
              }
            },
            data: data
          }
        ]
      };

      myChart.setOption(option);
    },
    verticalChart(data){
      // console.log("data vertical.", data)
      let xData = data.xData
      let yData = data.yData
      // let xData = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      // let yData = [120, 200, 150, 80, 70, 110, 130]
      let chartDom = document.getElementById('verticalChart');
      let myChart = echarts.init(chartDom);
      let option;
      // set option
      option = {
        legend: {
          show: true
        },
        xAxis: {
          type: 'category',
          data: yData,
          axisLabel: { interval: 0, rotate: 30 }
        },
        yAxis: {
          type: 'value'
        },
        grid: {
          left: '5%',
          containLabel: true
        },
        series: [
          {
            data: xData,
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ]
      }
      myChart.setOption(option);
    },
    crosswiseChart(data){
      let xData = data.xData
      let yData = data.yData
      // let xData = [1, 2, 3, 4, 5]
      // let yData = ['A', 'B', 'C', 'D', 'E']
      let chartDom = document.getElementById('crosswiseChart');
      let myChart = echarts.init(chartDom);
      let option;
      // set option
      option = {
        grid: {
          top: '2%',
          bottom: '2%',
          left: '5%',
          containLabel: true
        },
        yAxis: {
          max: 'dataMax'
        },
        xAxis: {
          type: 'category',
          data: yData,
          inverse: true,
          animationDuration: 300,
          animationDurationUpdate: 300,
          axisLabel: { interval: 0, rotate: 45 }
          // max: 1 // only the largest 3 bars will be displayed
        },
        series: [
          {
            realtimeSort: true,
            name: 'The Number of Cases',
            type: 'bar',
            data: xData
            // label: {
            //   show: true,
            //   position: 'right',
            //   valueAnimation: true
            // }
          }
        ]
        // legend: {
        //   show: true
        // }
      }
      myChart.setOption(option);
    },
    getWordMap(){
      let that = this
      axios.get('/static/USA.json').then(function (res) {
        // console.log('aaaaaaa', res)
        that.dataMapNew = res.data
      })
    },
    getWordMockData(){
      let that = this
      axios.get('/static/mockMap.json').then(function (res) {
        console.log('aaaa', res.data.result)
        that.dataMapNewData = res.data.result
      })
    },
  },
  mounted() {
    // load word map
    this.getWordMap()

    this.getChartInfo()

    // timer
    let timer = setInterval(this.getChartInfo, this.refreshTime * 1000)
  },
  // mounted() {
    // this.timer = setInterval(this.getChartInfo, 1000)
  // }
}
</script>



<style scoped>



</style>
