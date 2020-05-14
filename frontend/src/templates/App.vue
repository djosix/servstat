<template lang="pug">
  .ui.very.padded.basic.segment
    h1.ui.header {{ title }}
    table.ui.celled.unstackable.table
      thead
        tr
          th.two.wide Host
          th.six.wide CPU / Mem. / Swap
          th.eight.wide GPUs
      tbody
        tr(v-for='server in servers')
          template(v-if='server.data')
            td
              h3 {{ server.data.host }}
              span {{ server.addr }} &nbsp;
              a(:data-tooltip='"[API] " + server.link' :href='server.link')
                i.ui.external.alternate.icon
            td
              b {{ server.data.cpu.info.brand }} ({{ server.data.cpu.count }} Cores)
              CpuUsageBars.usage-bar(:percentList='server.data.cpu.percent')
              UsageBar.usage-bar(:percent='server.data.cpu.usage')
              .little-break
              b Memory Usage ({{ server.data.mem.used | size }} / {{ server.data.mem.total | size }}) 
              UsageBar.usage-bar(:percent='100 * server.data.mem.used / server.data.mem.total')
              .little-break
              b Swap Usage ({{ server.data.swap.used | size }} / {{ server.data.swap.total | size }}) 
              UsageBar.usage-bar(:percent='100 * server.data.swap.used / server.data.swap.total')
            td
              div(v-if='server.data')
                .ui.cards
                  .card(v-for='gpu in server.data.gpu')
                    .content
                      .header [{{ gpu.index }}] {{ gpu.name }}
                      .little-break
                      .description
                        b Util. {{ gpu['utilization.gpu'] }}% ({{ gpu['temperature.gpu'] }}&deg;C, Fan: {{ gpu['fan.speed'] }}%)
                        UsageBar(:percent='gpu["utilization.gpu"]')
                        .little-break
                        b Mem. {{ (gpu['memory.used'] / gpu['memory.total']) * 100 | round }}% ({{ gpu['memory.used'] }}M / {{ gpu['memory.total'] }}M) 
                        UsageBar(:percent='100 * gpu["memory.used"] / gpu["memory.total"]')
                    .extra.content
                      pre(style="font-size: 0.9em; margin: 0px")
                        template(v-if='gpu.processes.length > 0')
                          span(v-for='p, i in gpu.processes')
                            br(v-if='i > 0')
                            | <b>{{ p.username }}</b> (<b>{{ p.command }}</b>:{{ p.pid }}, <b>{{ p.gpu_memory_usage }}M</b>)
                        template(v-else)
                          i (no process)
          template(v-else)
            td
              i {{ server.link }}
            td
              i.spinner.loading.icon
              i Loading...
            td
              i.spinner.loading.icon
              i Loading...
</template>


<script>
import axios from "axios";
import $ from "jquery";
import _ from "lodash";

import UsageBar from './UsageBar';
import CpuUsageBars from './CpuUsageBars';

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
  document.querySelectorAll(".ui.progressX").forEach(el => {
    let $el = $(el);
    $el.progressX({
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
        // Set title
        if (typeof res.data.title === "string") {
          this.title = document.title = res.data.title;
        }

        for (let [i, server] of res.data.servers.entries()) {
          let name, addr, link, interval;

          if (typeof server === "string") {
            link = server;
          } else if (typeof server === "object") {
            name = server.name;
            link = server.link;
            interval = server.interval;
          }

          if (link === undefined) {
            continue;
          }

          try {
            // Extract server address from link
            const regex = /https?:\/\/(?<host>[a-zA-Z0-9\.]+)(?::(?<port>[0-9]+))?(?<path>\/.*)?/;
            addr = regex.exec(link).groups.host;
          } catch (e) {
            addr = "(unknown address)";
          }

          this.servers.push({ name, addr, link });
          this.update(i, link, interval || res.data.interval || 5000);
        }
      })
      .catch(err => {
        alert("Failed to load config.json");
      });
  },
  data() {
    return {
      title: "Server Status",
      servers: []
    };
  },
  methods: {
    update(index, link, interval) {
      axios
        .get(link)
        .then(res => {
          this.$set(this.servers[index], "data", res.data);
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
  },
  components: {
    UsageBar,
    CpuUsageBars
  }
};
</script>



<style lang="less" scoped>
.little-break {
  height: 7px;
}

hr.light {
  border-top: 1px solid rgba(34, 36, 38, 0.1);
  border-bottom: 0px;
  border-left: 0px;
  border-right: 0px;
}

.usage-bar {
  margin-top: 3px;
  margin-bottom: 3px;
}
</style>
