<template lang="pug">
.x-container
  .x-bar(v-bind:style='{ width: toWidth(percent), "background-color": toColor(percent) }')
    b.x-percent {{ Math.round(percent) }}%
</template>

<style scoped>
.x-container {
  padding: 0px;
  height: 15px;
  border: 0px;
  border-radius: 3px;
  background-color: rgb(236, 235, 235);
}
.x-bar {
  transition-property: width;
  transition-duration: 0.7s;
  transition-timing-function: cubic-bezier(0.25, 0.1, 0.25, 1);
  margin: 0px;
  padding: 0px 5px 0px 5px;
  border: 0px;
  left: 0px;
  height: 100%;
  line-height: 100%;
  text-align: center;
  border-radius: inherit;
  vertical-align: center;
}
.x-percent {
  margin: 0px;
  padding: 0px;
  font-size: 11px;
  word-wrap: normal;
  overflow-wrap: normal;
}
</style>

<script>
export default {
  props: {
    percent: Number,
    showPercentText: Boolean
  },
  methods: {
    toColor(percent) {
      if (percent < 0.5) return '#d8d7d7';
      if (percent < 10) return '#4ede72';
      if (percent < 30) return '#abe356';
      if (percent < 50) return '#d5e356';
      if (percent < 70) return '#e3af56';
      if (percent < 90) return '#e37756';
      return '#e35656';
    },
    toWidth(percent) {
      return Math.max(Math.round(percent), 5) + '%';
    }
  }
};
</script>