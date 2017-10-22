<style scoped>
  .content-head {
    margin: 0 0 15px 0;
    padding: 0 0 10px 0;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0,0,0,.1);
  }
</style>

<template>
  <div class="content" style="overflow: auto">
    <div class="content-head">
      <h1>test</h1>
    </div>
    <highcharts_component :options="options" :styles="styles" ref="simpleChart"></highcharts_component>
    <highcharts_component :options="cpu_options" :styles="styles" ref="simpleChart"></highcharts_component>

  </div>

</template>

<script>
  import highcharts_component from './chart_highcharts.vue'
  export default {
    data() {
      return {
        options: {
            chart: {
                type: 'bar'                         //指定图表的类型，默认是折线图（line）
            },
            title: {
                text: '我的第一个图表'                //指定图表标题
            },
            xAxis: {
                categories: ['苹果', '香蕉', '橙子'] //指定x轴分组
            },
            yAxis: {
                title: {
                    text: '吃水果个数'                //指定y轴的标题
                }
            },
            series: [{                              //指定数据列
                name: '小明',                       //数据列名
                data: [1, 0, 4]                     //数据
            }, {
                name: '小红',
                data: [5, 7, 3]
            }]
        },
        cpu_options: {
          title: {
            text: 'CPU usage'                //指定图表标题
          },
          xAxis: {
            title: {
              text: '时间'
            },
            type: 'datetime',
            //坐标间隔
            tickPixelInterval: 100
          },
          yAxis: {
            title: {
              text: 'cpu use'                //指定y轴的标题
            }
          },
          series: [{                              //指定数据列
            name: 'cpu使用率',                       //数据列名
            data: (function() {
              // 初始化数据
              var data = [], time = (new Date()).getTime(), i;
              for (i = -39; i <= 0; i++) {
                data.push({
                  x: time + i * 1000,
                  y: Math.random() * 100
                });
              }
              return data;
            })()
            }]
        },
        styles: {
          width: null
        }
      }
    },
    components: {
      highcharts_component
    }
  }
</script>
