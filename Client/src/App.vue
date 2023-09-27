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
      currentTemp: -1, //Stores current temperature on webapp
      message: 'Switch to \u{2109}', //Stores button text
      isCel: true, //If true, the temperature should be displayed in C
      componentKey: 0, //Refresh global variable for the graph
      fetchData: null, //Reference to temperature data received from HTTP request
      modalEnable: false, //Global boolean that brings open the settings menu when set to true
      carrier: "att", //Carrier the user selected
      upperTemp: 50, //Upper temperature of graph key
      lowerTemp: 10, //Lower temperature of graph key
      phoneNumber: '3193335747', //Phone number the user selects
      dataGrabbed: true, //One time boolean value that ensures we grab settings data
      errorBool: true, //Global boolean that ensures temperatuere is converted properly
      //Data for graph
      data: {
        labels: [], //Graph labels
        datasets: [
          {
            //Graph settings
            lineTension: 0.5,
            borderColor: "#ea5545",
            backgroundColor: '#ea5545',
            label: 'Temperature Data',
            data: [],
          }
        ]
      },
      //Grpah options
      options: {
        maintainAspectRatio: true,
        type: 'linear',
        bezierCurve: true,
        elements: {
          point: {
            radius: 0,
          },
        },
        //x and y axis settings
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
              text: 'Seconds Ago from the Current Time'
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
        const controller = new AbortController()
        //Grabs settings data on first run
        if (this.dataGrabbed) {
          fetch('http://172.23.49.73:5000/settings')
            .then(res => res.json())
            .then(data => {
              this.carrier = data['carrier']
              this.upperTemp = data['max_temp']
              this.lowerTemp = data['min_temp']
              this.phoneNumber = data['phone_number']
              this.dataGrabbed = false
            }).catch((error) => {
              console.log(error)
            });
        }
        // 1 second timeout incase request fails
        // Fetch temperature data and store accordingly
        const timeoutId = setTimeout(() => controller.abort(), 1000)
        fetch('http://172.23.49.73:5000/temp', { signal: controller.signal })
          .then(res => res.json())
          .then(data => {
            // this.fetchData = data.split(',')
            this.fetchData = data;
            this.errorBool = true;
          })
          .then(() => {
            if (this.fetchData[299] == null || this.fetchData[299] == 'null') {
              this.currentTemp = 'unplugged sensor'
            }
            else {
              this.currentTemp = this.fetchData[299]
            }
          }).catch((error) => {
            //this function is used for if the chart fetch fails
            //Scrolls everything left
            if (this.fetchData != null) {
              for (var i = 0; i < 300; i++) {
                if (i < 299) {
                  this.fetchData[i] = this.fetchData[i + 1]
                }
                else {
                  this.fetchData[i] = "null"
                }
                this.errorBool = false;
                this.currentTemp = 'no data available'
              }
              this.$refs.myChart.chart.update('none')
            }
            else {
              this.currentTemp = 'no data available'
            }
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
      //Checks if data is populated
      //If so, convert to F or C and push to graph
      if (this.fetchData != null) {
        var list = this.fetchData
        if (!this.isCel && this.errorBool) {
          for (var i = 0; i < 300; i++) {
            list[i] = (list[i] * 9 / 5) + 32
          }
        }
        try {
          this.$refs.myChart.chart.data.datasets[0].data = list
          this.$refs.myChart.chart.update('none')
        }
        catch (error) {
          console.log(error)
        }
      }
    },
    /**
     * Converts the current temperture to a string to display to the user
     */
    tempToString() {
      if (this.currentTemp == 'no data available' || this.currentTemp == 'unplugged sensor' || typeof this.currentTemp !== 'number' || this.currentTemp == null) {
        if (this.currentTemp == null) {
          return "no data available"
        }
        return this.currentTemp
      }
      if (this.isCel) {
        return this.currentTemp.toFixed(2) + " \u{2103}"
      }
      else {
        return ((this.currentTemp * 9 / 5) + 32).toFixed(2) + " \u{2109}"
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
        if (this.fetchData != null) {
          console.log('hit')
          var list = this.fetchData
          if (!this.isCel) {
            for (var i = 0; i < 300; i++) {
              list[i] = (list[i] * 9 / 5) + 32
            }
          }
          try {
            this.$refs.myChart.chart.data.datasets[0].data = list
            this.$refs.myChart.chart.update('none')
          }
          catch (error) {
            console.log(error)
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
        if (this.fetchData != null) {
          var list = this.fetchData
          if (this.isCel) {
            for (var i = 0; i < 300; i++) {
              //(32°F − 32) × 5/9
              list[i] = (list[i] - 32) / (9 / 5)
            }
          }
          try {
            this.$refs.myChart.chart.data.datasets[0].data = list
            this.$refs.myChart.chart.update('none')
          }
          catch (error) {
            console.log(error)
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
      if ((!isNaN(lowTem) && typeof lowTem === 'number') && ((!isNaN(highTem) && typeof highTem === 'number'))) {
        if (lowTem < highTem) {
          this.lowerTemp = lowTem
          this.upperTemp = highTem
          var myHeaders = new Headers();
          myHeaders.append("Content-Type", "text/plain");
          var raw = JSON.stringify({
            "phone_number": this.phoneNumber,
            "carrier": this.carrier,
            "max_temp": this.upperTemp,
            "min_temp": this.lowerTemp
          });
          var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
          };
          fetch("http://172.23.49.73:5000/settings", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));
        }
        else if (lowTem == highTem) {
          alert("Lower tempature and upper temperature cannot be equal");
          return
        }
        else {
          alert("Lower tempature cannot be a larger value than the upper temperature");
          return
        }
      }
      else {
        alert("Please enter a valid temperature");
        return
      }
      this.modalEnable = false;
    },
    toggleBoxButton(boolVal) {
      if (boolVal) {
        var raw = "";

        var requestOptions = {
          method: 'POST',
          body: raw,
          redirect: 'follow'
        };

        fetch("http://172.23.49.73:5000/button/True", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .catch(error => console.log('error', error));
      }
      else {
        var raw = "";

        var requestOptions = {
          method: 'POST',
          body: raw,
          redirect: 'follow'
        };

        fetch("http://172.23.49.73:5000/button/False", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .catch(error => console.log('error', error));
      }
    }

  },
};
</script>
<template>
  <div style="min-width: 100vw; min-height: 100vh; background-color: white; position: relative; left:0; top:0;">
    <div style="min-width: 95vw; min-height: 80vh; align-items: center; padding-top: 20vh;">
      <h1 size="+2" style="margin-left: 2.5vw; margin-bottom: 1vh;">Current Temperature: {{ tempToString() }}</h1>
      <v-btn style="margin-left: 2.5vw;" @mousedown="toggleBoxButton(true)" @mouseup="toggleBoxButton(false)">Turn on box
        display</v-btn>
      <v-btn style="margin-left: 2.5vw;" v-on:click="swapTemp()">{{ this.message }}</v-btn>
      <v-btn style="margin-left: 2.5vw;" variant="outlined" @click="modalEnable = !modalEnable">
        <b>Settings</b>
      </v-btn>
      <Line ref="myChart" :key="componentKey" :data="this.data" :options="this.options"
        style="position: absolute; height:40vh; width:80vw;" />
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
<style scoped>
/* add css if needed */
</style>
