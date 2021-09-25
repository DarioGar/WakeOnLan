
<script>
import { Bar, mixins } from 'vue-chartjs';
import { Component,Vue,Mixins,Prop } from 'vue-property-decorator';
import ComputerService from '../services/ComputerService'
 
@Component({
    extends: Bar, // this is important to add the functionality to your component
    mixins: [mixins.reactiveProp]
})
export default class DaysChart extends Mixins(mixins.reactiveProp, Bar, Vue) {

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
                    // Use this function to change the units from minutes to whatever u want
                    callback: function(value, index, values) {
                        return  value + ' min';
                    }
                },
                
            }]
        }
    }
    ComputerService.getOnline().then(
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
          backgroundColor:  [
                'rgba(153, 23, 23, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(23, 146, 22, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(75, 100, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(255, 99, 132, 0.8)'
            ],
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