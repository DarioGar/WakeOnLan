
<script>
import { Doughnut, mixins } from 'vue-chartjs';
import { Component,Vue,Mixins,Prop } from 'vue-property-decorator';
import ComputerService from '../services/ComputerService'
 
@Component({
    extends: Doughnut, // this is important to add the functionality to your component
    mixins: [mixins.reactiveProp]
})
export default class DaysChart extends Mixins(mixins.reactiveProp, Doughnut, Vue) {

  mounted () {
    var data = []
    ComputerService.getDaysData().then(
        (response) => {
          data = response.data
              // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday'],
      datasets: [
        {
          label: 'Computers powered on each day',
          backgroundColor:  [
                'rgba(153, 23, 23, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(23, 146, 22, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(75, 100, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(255, 99, 132, 0.8)'
            ],
          data: data
        }
      ],
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Computers powered on each day'
          }
        }
      },
    })
        },
        (error) => {
          data = "No groups yet assigned"
          }
      )

  }
}
</script>