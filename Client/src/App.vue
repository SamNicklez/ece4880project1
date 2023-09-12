<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)
export default {
  components: {
    Line,
  },
  data() {
    return {
      currentTemp: -1,
      message: 'Switch to \u{2109}',
      isCel: true,
      componentKey: 0,
      data: {
        labels: [],
        datasets: [
          {
            lineTension: 0.5,
            borderColor: "#ea5545",
            backgroundColor: '#ea5545',
            label: 'Temperature Data',
            data: [],
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        type: 'linear',
        bezierCurve: true,
        elements: {
          point: {
            radius: 0,
          },
        },
          scales: {
            x: {
              ticks: {
                max: 300,
                min: 0,
                stepSize: 100,
                maxTicksLimit: 3,
              },
              title: {
                display: true,
                text: 'Seconds Ago'
              }
            },
            y: {
              max: 50, // Set the maximum value for the y-axis
              min: 10, // Set minimum value of the y-axis
              title: {
                display: true,
                text: 'Temp, \u{2103}'
              }
            },
          },
        }
      };
    },
      created() {
      this.graphSetup();
    },
    methods: {
      /**
       * Grabs the last 300 seconds of temperature data from the Pi
       */
      grabLast300() {
        fetch("FETCH STUFF", requestOptions)
          .then(response => response.json())
          .then(result => this.set300(result))
          .catch(error => console.log('error', error));
      },
      /**
       * Grabs the current temperature from the Pi
       */
      grabCurrentTemp() {
        fetch("FETCH STUFF", requestOptions)
          .then(response => response.json())
          .then(result => this.setCurrentTemp(result))
          .catch(error => console.log('error', error));
      },
      /**
       * Setter for currentTemp variable
       * @param {*} json 
       */
      setCurrentTemp(json) {
        this.currentTemp = json

        //append the current temp to the list after checking if it is currently in F or C
      },
      /**
       * Setter for last300 variable
       * @param {*} json 
       */
      set300(json) {
        this.data.datasets[0].data = json
      },
      graphSetup() {
        this.data.labels = []
        this.data.datasets[0].data = []
        for (var i = 0; i < 300; i++) {
          if (i == 0 || i == 99 || i == 199 || i == 299) {
            if (i == 0) {
              this.data.labels.push(300)
            }
            else if (i == 99) {
              this.data.labels.push(200)
            }
            else if (i == 199) {
              this.data.labels.push(100)
            }
            else {
              this.data.labels.push(0)
            }
          }
          else {
            this.data.labels.push(300 - i)
          }
          this.data.datasets[0].data.push(Math.floor(Math.random() * 40) + 10)
          //Eventually fetch real data
        }
      },
      toggleBoxButton(boolButton){
        if(boolButton){
          //turn on stuff
          console.log("ON")
        }
        else{
          //turn off stuff
          console.log("OFF")
        }
      },
      tempToString(){
        if(this.isCel){
          return this.currentTemp + " \u{2103}"
        }
        else{
          return ((this.currentTemp * 9 / 5) +32) + " \u{2109}"
        }
      },
      swapTemp(){
        if(this.isCel){
          this.isCel = false
          this.options.scales.y.max = 122
          this.options.scales.y.min = 50
          this.options.scales.y.title.text = 'Temp, \u{2109}'
          this.options.scales.y.title.display = true
          this.message = 'Switch to \u{2103}'
          for(var i = 0; i < this.data.datasets[0].data.length; i++){
            // (0°C × 9/5) + 32
            if(!isNaN(this.data.datasets[0].data[i])){
              this.data.datasets[0].data[i] = (this.data.datasets[0].data[i] * 9 / 5) + 32
            }
          }
          this.componentKey += 1;
        }
        else{
          this.isCel = true
          this.options.scales.y.max = 50
          this.options.scales.y.min = 10
          this.options.scales.y.title.text = 'Temp, \u{2103}'
          this.options.scales.y.title.display = true
          this.message = 'Switch to \u{2109}'
          for(var i = 0; i < this.data.datasets[0].data.length; i++){
            // (0°C × 9/5) + 32
            if(!isNaN(this.data.datasets[0].data[i])){
              //(°F - 32) ÷ 9/5
              this.data.datasets[0].data[i] = (this.data.datasets[0].data[i] - 32) / (9 / 5)
            }
          }
          this.componentKey += 1;
        }
      }

    },
  };
</script>

<template>
  <div style="min-width: 100vw; min-height: 100vh; background-color: white; position: relative; left:0; top:0;">
    <div style="min-width: 95vw; min-height: 80vh; align-items: center; padding-top: 20vh;">
      <h1 size="+2" style="margin-left: 2.5vw;">Current Temperature: {{ tempToString() }}</h1>
      <button class="btn btn-secondary" style="margin-left: 2.5vw;" @mousedown="toggleBoxButton(true)" @mouseup="toggleBoxButton(false)">Turn on box display</button>
      <button class="btn btn-secondary" style="margin-left: 2.5vw;" v-on:click="swapTemp()">{{ this.message }}</button>
      <Line :key="componentKey" :data="this.data" :options="this.options"
        style="position: absolute; height:40vh; width:80vw; padding-right: 10vw;" />
    </div>
  </div>
</template>

<style scoped>
/* You can add custom CSS styles here if needed */
</style>
