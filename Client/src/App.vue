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
      fetchData: null,
      compatConfig: { MODE: 3 },
      loaded: false,
      modalEnable: false,
      carrier: "att",
      carrier2: null,
      upperTemp: 50,
      lowerTemp: 10,
      phoneNumber: '3193335747',
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
            position: 'right',
            title: {
              display: true,
              text: 'Temp, \u{2103}'
            }
          },
        },
      }
    };
  },
  /**
   * runs on the creation of the webpage
   */
  created() {
    this.updateData()
    this.grabLast300()
    setInterval(() => {
      this.updateData()
    }, 1000);
  },
  methods: {
    /**
     * Grabs the last 300 seconds of data from the server
     */
    async grabLast300() {
      while (true) {
        const startTime = performance.now(); // Get the start time
        fetch('http://172.23.49.73:5000/data')
          .then(res => res.json())
          .then(data => {
            this.fetchData = data;
          })
          .then(() => {
            this.currentTemp = this.fetchData[299]
          }).catch((error) => {
            console.log(error)
          });
        const endTime = performance.now(); // Get the end time
        const executionTime = endTime - startTime; // Calculate the execution time in milliseconds

        // Calculate the sleep duration based on the execution time
        const sleepDuration = Math.max(0, 1000 - executionTime); // Ensure a minimum sleep of 0 milliseconds

        await new Promise(resolve => setTimeout(resolve, sleepDuration)); // Sleep for the calculated duration
      }
    },
    /**
     * updates the graph with the most current data available
     */
    updateData() {
      //this.loaded = false
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
      }
      if (this.fetchData != null) {
        //this.loaded = true;
        var list = this.fetchData
        //console.log(this.$refs.myChart.chart.data.datasets[0].data)
        if (this.isCel) {
          for (var i = 0; i < 300; i++) {
            list[i] = (list[i] * 9 / 5) + 32
          }
        }
        this.$refs.myChart.chart.data.datasets[0].data = list
        this.$refs.myChart.chart.update('none')
      }
    },
    /**
     * Handles errors if server is down
     * @param {*} error 
     */
    fetchError(error) {
      console.log(error)
      //this function is used for if the chart fetch fails
      for (var i = 0; i < 300; i++) {
        if (i < 299) {
          this.data.datasets[0].data[i] = this.data.datasets[0].data[i + 1]
        }
        else {
          this.data.datasets[0].data[i] = "null"
        }
        this.currentTemp = 'no data available'
      }
    },
    /**
     * Converts the current temperture to a string to display to the user
     */
    tempToString() {
      if (this.isCel) {
        return this.currentTemp + " \u{2103}"
      }
      else {
        return ((this.currentTemp * 9 / 5) + 32) + " \u{2109}"
      }
    },
    /**
     * Changes the scale of the table, converts from C to F and vis versa
     */
    swapTemp() {
      if (this.isCel) {
        this.isCel = false
        this.options.scales.y.max = 122
        this.options.scales.y.min = 50
        this.options.scales.y.title.text = 'Temp, \u{2109}'
        this.options.scales.y.title.display = true
        this.message = 'Switch to \u{2103}'
        for (var i = 0; i < this.data.datasets[0].data.length; i++) {
          // (0°C × 9/5) + 32
          if (!isNaN(this.data.datasets[0].data[i])) {
            this.data.datasets[0].data[i] = (this.data.datasets[0].data[i] * 9 / 5) + 32
          }
        }
        this.componentKey += 1;
      }
      else {
        this.isCel = true
        this.options.scales.y.max = 50
        this.options.scales.y.min = 10
        this.options.scales.y.title.text = 'Temp, \u{2103}'
        this.options.scales.y.title.display = true
        this.message = 'Switch to \u{2109}'
        for (var i = 0; i < this.data.datasets[0].data.length; i++) {
          // (0°C × 9/5) + 32
          if (!isNaN(this.data.datasets[0].data[i])) {
            //(°F - 32) ÷ 9/5
            this.data.datasets[0].data[i] = (this.data.datasets[0].data[i] - 32) / (9 / 5)
          }
        }
        this.componentKey += 1;
      }
    },
    /**
     * Sets user defined parameters and sends it to the server
     */
    setPhone() {
      const phonePattern = /^(?:\+1)?\s*\(?(\d{3})\)?[-.\s]*?(\d{3})[-.\s]*?(\d{4})$/;
      const lowTem = parseFloat(this.lowerTemp)
      const highTem = parseFloat(this.upperTemp)
      if (phonePattern.test(this.phoneNumber)) {
        // If it's valid, remove any non-digit characters and format it
        const formattedNumber = this.phoneNumber.replace(/\D/g, "");
        this.phoneNumber = formattedNumber
      } 
      else {
        // If it's not valid, return null or any other appropriate value
        alert("Please enter a valid phone number");
        this.phoneNumber = ""
        return
      }
      if((!isNaN(lowTem) && typeof lowTem === 'number') && ((!isNaN(highTem) && typeof highTem === 'number'))){
        if(lowTem < highTem){
          this.lowerTemp = lowTem
          this.upperTemp = highTem
          //DO API CALL HERE







        }
        else if(lowTem == highTem){
          alert("Lower tempature and upper temperature cannot be equal");
          return
        }
        else{
          alert("Lower tempature cannot be a larger value than the upper temperature");
          return
        }
      }
      else{
        alert("Please enter a valid temperature");
        return
      }
      this.modalEnable = false;
    }

  },
};
</script>
<template>
  <div style="min-width: 100vw; min-height: 100vh; background-color: white; position: relative; left:0; top:0;">
    <div style="min-width: 95vw; min-height: 80vh; align-items: center; padding-top: 20vh;">
      <h1 size="+2" style="margin-left: 2.5vw;">Current Temperature: {{ tempToString() }}</h1>
      <v-btn style="margin-left: 2.5vw;" @mousedown="toggleBoxButton(true)" @mouseup="toggleBoxButton(false)">Turn on box
        display</v-btn>
      <v-btn style="margin-left: 2.5vw;" v-on:click="swapTemp()">{{ this.message }}</v-btn>
      <v-btn style="margin-left: 2.5vw;" variant="outlined" @click="modalEnable = !modalEnable">
        <b>Settings</b>
      </v-btn>
      <Line ref="myChart" :key="componentKey" :data="this.data" :options="this.options"
        style="position: absolute; height:40vh; width:80vw; padding-right: 10vw;" />
    </div>
  </div>
  <v-dialog v-model="modalEnable" persistent max-width="40vw">
    <v-card>
      <v-card-title class="headline">Text Message Settings</v-card-title>
      <v-select style="margin-left: 2.5vw; margin-right: 2.5vw; margin-top: 1vh;" v-model="carrier"
        :items="['att', 'tmobile', 'verizon', 'sprint', 'uscellular']"></v-select>
      <v-text-field style="margin-left: 2.5vw; margin-right: 2.5vw;" v-model="phoneNumber" label="Phone Number"
        variant="outlined"></v-text-field>
      <v-text-field style="margin-left: 2.5vw; margin-right: 2.5vw;" v-model="lowerTemp" label="Min Temp (Celcius)"
        variant="outlined"></v-text-field>
      <v-text-field style="margin-left: 2.5vw; margin-right: 2.5vw;" v-model="upperTemp" label="Max Temp (Celcius)"
        variant="outlined"></v-text-field>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="setPhone()">Return</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<style scoped>/* add css if needed */</style>
