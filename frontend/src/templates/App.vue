<template lang="pug">
  .ui.container
    .ui.very.padded.segment
      h1.ui.header {{ name }}
      p p
</template>

<script>
const POLL_INTERVAL = 5000;

function extractHostFromLink(link) {
  let regex = /https?:\/\/([a-zA-Z0-9\.]+)(:[0-9]+)?(\/.*)?/;
  return regex.exec(link)[1];
}

import axios from 'axios';

export default {
  created() {
    axios.get('config.json').then(res => {
      res.data.urls.forEach(url => {
        this.update(url, res.data.interval || 5000);
      });
    });
  },
  data() {
    return {
      stats: {}
    };
  },
  methods: {
    update(link, interval) {
      let host = extractHostFromLink(link);

      axios.get(link).then(res => {
        // console.log(res.data);
        window.data = res.data;
        this.stats[host] = res.data;

        setTimeout(() => {
          this.update(link, interval);
        }, interval);
      });
    }
  },
  components: {
    // MainBlock,
    // ModBlock
  }
};
</script>
