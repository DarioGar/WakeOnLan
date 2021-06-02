<template>
<v-container fluid>
    <v-select
      v-model="computer.selectedPrograms"
      :items="programs"
      @input="emitPrograms"
      label="Programs(optional)"
      multiple
    >
    </v-select>
  </v-container>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from "vue-property-decorator";
import { namespace } from "vuex-class";

const Auth = namespace("Auth");

@Component
  export default class ProgramPicker extends Vue{
  programs = [
        'Apples',
        'Apricots',
        'Avocado',
        'Bananas',
        'Blueberries',
        'Blackberries',
        'Boysenberries',
        'Bread fruit',
        'Cantaloupes (cantalope)',
        'Cherries',
        'Cranberries',
        'Cucumbers',
        'Currants',
        'Dates',
        'Eggplant',
        'Figs',
        'Grapes',
        'Grapefruit',
        'Guava',
        'Honeydew melons',
        'Huckleberries',
        'Kiwis',
        'Kumquat',
        'Lemons',
        'Limes',
        'Mangos',
        'Mulberries',
        'Muskmelon',
        'Nectarines',
        'Olives',
        'Oranges',
        'Papaya',
        'Peaches',
        'Pears',
        'Persimmon',
        'Pineapple',
        'Plums',
        'Pomegranate',
        'Raspberries',
        'Rose Apple',
        'Starfruit',
        'Strawberries',
        'Tangerines',
        'Tomatoes',
        'Watermelons',
        'Zucchini',
      ]
    
  created(){
    this.getPrograms()
  }

  getPrograms() {
    throw new Error("Method not implemented.");
  }

  @Prop() computer: any


  @Emit()
    emitPrograms(programs : any) {
      programs = this.programs
  }


}
</script>
