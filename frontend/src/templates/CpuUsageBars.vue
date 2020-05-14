<template lang="pug">
  .x-container
    .x-bar(v-for='percent in percentList' v-bind:style='{ "background-color": toColor(percent), height: toWidth(percent) }')
</template>

<style scoped>
.x-container {
  padding: 0px;
  height: 30px;
  border: 0px;
  border-radius: 3px;
  background-color: rgb(236, 235, 235);

  display: flex;
  flex: 0 0 1px;
  align-items:flex-end;
}

.x-bar {
  flex-direction: column;
  flex-basis: 0;
  flex-grow: 1;
  flex-flow: column;
  
  transition-property: height;
  transition-duration: 0.5s;
  transition-timing-function: linear;

  margin: 0px;
  padding: 0px;
  border: 0px;


  border-radius: inherit;
}
</style>

<script>
export default {
  props: {
    percentList: Array,
  },
  methods: {
    toColor(percent) {
      if (percent < 5) return '#d8d7d7';
      if (percent < 10) return '#4ede72';
      if (percent < 30) return '#abe356';
      if (percent < 50) return '#d5e356';
      if (percent < 70) return '#e3af56';
      if (percent < 90) return '#e37756';
      return '#e35656';
    },
    toWidth(percent) {
      return Math.max(Math.round(percent), 15) + '%';
    }
  }
};
</script>
