
<script>
import { Line, mixins } from 'vue-chartjs';
import { Component,Vue,Mixins,Prop } from 'vue-property-decorator';
import ComputerService from '../services/ComputerService'
 
@Component({
    extends: Line, // this is important to add the functionality to your component
    mixins: [mixins.reactiveProp]
})
export default class DaysChart extends Mixins(mixins.reactiveProp, Line, Vue) {

  /**
   * @vuese
   * Used to render the chart, we override the renderchart method with our own options and data, retrieved from the database
   */
  mounted () {
    var data = []
    var labels = []
    var options = {
        responsive : true,
        maintainAspectRatio: false,
        legend: {
            display: false,
            title : false
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero : true,
                    callback: function(value, index, values) {
                        return  value + ' times';
                    }
                },
            }],
        }
    }
    ComputerService.getActiveData().then(
        (response) => {
            response.data.forEach((element) => {  
                data.push(element[1])
                labels.push(element[0])
          });
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: labels,
      datasets: [
        {
            label: "",
          backgroundColor:  'rgba(75, 100, 255, 0.8)',
          data: data,
        }
      ],
    },options)
        },
        (error) => {
          data = "No data yet registered"
          }
      )

  }
}
</script>