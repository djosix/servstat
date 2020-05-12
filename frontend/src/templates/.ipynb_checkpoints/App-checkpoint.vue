<template lang="pug">
  .ui.very.padded.basic.segment
    h1.ui.header Training Servers
    table.ui.celled.unstackable.table
      thead
        tr
          th.four.wide Host / CPU / Mem
          th.eight.wide GPUs
      tbody
        tr(v-for='stat, hostIndex in stats')
          td
            div(v-if='stat.data')
              h2 {{ stat.host }}
              span &nbsp;
              span &nbsp;
              span &nbsp;
              .label <br/> 
            div(v-if='stat.data')
              .ui.small.reversed.progress(:x-percent='stat.data.cpu.usage')
                .bar: .progress
                .label {{ stat.data.cpu.info.brand }} <br/> ({{ stat.data.cpu.count }} Cores)
              div
                span &nbsp;
              div
                span(v-for='percent, i in stat.data.cpu.percent')
                  .ui.basic.mini.red.label(v-if='percent >= 99.9') {{ 99.9 }}%
                  .ui.basic.mini.red.label(v-else-if='percent >= 70') {{ String(Number.parseFloat(percent).toFixed(1)).padStart(4, '0') }}%
                  .ui.basic.mini.orange.label(v-else-if='percent >= 40') {{ String(Number.parseFloat(percent).toFixed(1)).padStart(4, '0') }}%
                  .ui.basic.mini.yellow.label(v-else-if='percent >= 20') {{ String(Number.parseFloat(percent).toFixed(1)).padStart(4, '0') }}%
                  .ui.basic.mini.green.label(v-else) {{ String(Number.parseFloat(percent).toFixed(1)).padStart(4, '0') }}%
                  | &hairsp;
              hr.light
              .ui.small.reversed.progress(:x-percent='100 * stat.data.mem.used / stat.data.mem.total')
                .bar: .progress
                .label Memory Usage ({{ stat.data.mem.used | size }} / {{ stat.data.mem.total | size }})

            div(v-else)
              h2 {{ stat.host }}
          td
            div(v-if='stat.data')
              .ui.cards
                .card(v-for='gpu in stat.data.gpu')
                  .content
                    .header [{{ gpu.index }}] {{ gpu.name }}
                    br
                    .description
                      .ui.small.reversed.progress(:x-percent='gpu["utilization.gpu"]')
                        .bar: .progress
                        .label Util. {{ gpu['utilization.gpu'] }}% ({{ gpu['temperature.gpu'] }}&deg;C, fan: {{ gpu['fan.speed'] }})
                      .ui.small.reversed.progress(:x-percent='100 * gpu["memory.used"] / gpu["memory.total"]')
                        .bar: .progress
                        .label Mem. {{ (gpu['memory.used'] / gpu['memory.total']) * 100 | round }}% ({{ gpu['memory.used'] }}M / {{ gpu['memory.total'] }}M) 
                  .extra.content
                    pre(v-if='gpu.processes.length > 0' style="font-size: 0.9em; margin: 0px ")
                      span(v-for='p, i in gpu.processes')
                        br(v-if='i > 0')
                        | <b>{{ p.username }}</b> (<b>{{ p.command }}</b>:{{ p.pid }}, <b>{{ p.gpu_memory_usage }}M</b>)
                    
            div(v-else)
              i.power.off.icon
              i Server Offline
</template>


<script>
import axios from "axios";
import $ from "jquery";
import _ from "lodash";

let round = (n, f = 2) => {
  let x = 10 ** f;
  return Math.round(n * x) / x;
};

let formatSize = n => {
  const units = ["", "K", "M", "G", "T", "P", "E", "Z"];
  let p = 2 ** 10;
  for (let unit of units) {
    if (n < p) return `${round(n)}${unit}`;
    n /= p;
  }
  return `${n}Y`;
};

let updateProgress = _.debounce(() => {
  document.querySelectorAll(".ui.progress").forEach(el => {
    let $el = $(el);
    $el.progress({
      autoSuccess: false,
      percent: $el.attr("x-percent")
    });
  });
}, 256);

export default {
  created() {
    axios
      .get("config.json")
      .then(res => {
        for (let [i, [host,link]] of res.data.links.entries()) {
          let addr;
          try {
            const regex = /https?:\/\/(?<host>[a-zA-Z0-9\.]+)(?::(?<port>[0-9]+))?(?<path>\/.*)?/;
            addr = regex.exec(link).groups.host;
          } catch (e) {
            addr = "(unknown address)";
          }
          this.stats.push({ addr, link });
          this.$set(this.stats[i], "host", host);
          this.update(i, link, res.data.interval || 5000);
        }
      })
      .catch(err => {
        alert("Failed to load config.json");
      });
  },
  data() {
    return {
      stats: []
    };
  },
  methods: {
    update(index, link, interval) {
      axios
        .get(link)
        .then(res => {
          this.$set(this.stats[index], "data", res.data);
          this.$nextTick(updateProgress);
        })
        .finally(() => {
          setTimeout(() => {
            this.update(index, link, interval);
          }, interval);
        });
    }
  },
  filters: {
    size(n) {
      return formatSize(n);
    },
    round(n) {
      return Math.round(n);
    }
  }
};
</script>



<style lang="less" scoped>
hr.light {
  border-top: 1px solid rgba(34, 36, 38, 0.1);
  border-bottom: 0px;
  border-left: 0px;
  border-right: 0px;
}

.ui.reversed.progress[data-percent^="1"] .bar,
.ui.reversed.progress[data-percent^="2"] .bar {
  background-color: #66da81;
}

.ui.reversed.progress[data-percent^="3"] .bar {
  background-color: #b4d95c;
}

.ui.reversed.progress[data-percent^="4"] .bar,
.ui.reversed.progress[data-percent^="5"] .bar {
  background-color: #ddc928;
}

.ui.reversed.progress[data-percent^="6"] .bar {
  background-color: #e6bb48;
}

.ui.reversed.progress[data-percent^="7"] .bar,
.ui.reversed.progress[data-percent^="8"] .bar {
  background-color: #efbc72;
}

.ui.reversed.progress[data-percent^="9"] .bar,
.ui.reversed.progress[data-percent^="100"] .bar {
  background-color: #d95c5c;
}

/* Indicating Label */

.ui.reversed.progress[data-percent^="1"] .label,
.ui.reversed.progress[data-percent^="2"] .label {
  color: rgba(0, 0, 0, 0.87);
}

.ui.reversed.progress[data-percent^="3"] .label {
  color: rgba(0, 0, 0, 0.87);
}

.ui.reversed.progress[data-percent^="4"] .label,
.ui.reversed.progress[data-percent^="5"] .label {
  color: rgba(0, 0, 0, 0.87);
}

.ui.reversed.progress[data-percent^="6"] .label {
  color: rgba(0, 0, 0, 0.87);
}

.ui.reversed.progress[data-percent^="7"] .label,
.ui.reversed.progress[data-percent^="8"] .label {
  color: rgba(0, 0, 0, 0.87);
}

.ui.reversed.progress[data-percent^="9"] .label,
.ui.reversed.progress[data-percent^="100"] .label {
  color: rgba(0, 0, 0, 0.87);
}

/* Single Digits */

.ui.reversed.progress[data-percent="1"] .bar,
.ui.reversed.progress[data-percent="2"] .bar,
.ui.reversed.progress[data-percent="3"] .bar,
.ui.reversed.progress[data-percent="4"] .bar,
.ui.reversed.progress[data-percent="5"] .bar,
.ui.reversed.progress[data-percent="6"] .bar,
.ui.reversed.progress[data-percent="7"] .bar,
.ui.reversed.progress[data-percent="8"] .bar,
.ui.reversed.progress[data-percent="9"] .bar {
  background-color: #66da81;
}

.ui.reversed.progress[data-percent="1"] .label,
.ui.reversed.progress[data-percent="2"] .label,
.ui.reversed.progress[data-percent="3"] .label,
.ui.reversed.progress[data-percent="4"] .label,
.ui.reversed.progress[data-percent="5"] .label,
.ui.reversed.progress[data-percent="6"] .label,
.ui.reversed.progress[data-percent="7"] .label,
.ui.reversed.progress[data-percent="8"] .label,
.ui.reversed.progress[data-percent="9"] .label {
  color: rgba(0, 0, 0, 0.87);
}

/* Indicating Success */

.ui.reversed.progress.success .label {
  color: rgb(83, 26, 26);
}
</style>
