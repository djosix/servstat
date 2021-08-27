
<template lang="pug">
.app
  .ui.very.padded.basic.segment
    h1.ui.header {{ title }}
    table.ui.celled.unstackable.table
      thead
        tr
          th.two.wide Host
          th.six.wide CPU / Mem. / Swap / Disks
          th.eight.wide GPUs
      tbody
        tr(v-for='server in orderedServers')
          template(v-if='server.data')
            td
              h3 {{ server.name || server.data.host }}
              div {{ server.addr }} &nbsp;
              div
                a(:data-tooltip='`Show API response from "${server.link}"`' :href='server.link' data-position="bottom left")
                  i.ui.external.alternate.icon
                template(v-if='server.pinned')
                  a(data-tooltip="Unpin this server" style="cursor: pointer" data-position="bottom left" v-on:click='toggleServerPinning(server)')
                    i.ui.bookmark.icon
                template(v-else)
                  a(data-tooltip="Pin this server to top" style="cursor: pointer" data-position="bottom left" v-on:click='toggleServerPinning(server)')
                    i.ui.bookmark.outline.icon
            td
              b {{ server.data.cpu.info.brand || server.data.cpu.info.brand_raw }} ({{ server.data.cpu.count }} Cores)
              CpuUsageBars.usage-bar(:percentList='server.data.cpu.percent')
              UsageBar.usage-bar(:percent='server.data.cpu.usage')
              .little-break
              b Memory Usage ({{ $filters.formatSize(server.data.mem.used) }} / {{ $filters.formatSize(server.data.mem.total) }}) 
              UsageBar.usage-bar(:percent='100 * server.data.mem.used / server.data.mem.total')
              .little-break
              b Swap Usage ({{ $filters.formatSize(server.data.swap.used) }} / {{ $filters.formatSize(server.data.swap.total) }}) 
              UsageBar.usage-bar(:percent='100 * server.data.swap.used / server.data.swap.total')
              table.ui.compact.table
                tbody
                  tr(v-for='disk in server.data.disk' :class="{ negative: disk.usage.total - disk.usage.used < 20 * 1073741824 }")
                    template(v-if='!disk.mountpoint.startsWith("/boot")')
                      td {{ disk.mountpoint }}
                      td {{ disk.device }} ({{ disk.fstype }})
                      td
                        | {{ $filters.formatSize(disk.usage.total, 'G', 'G', '', 2, true) }}
                        | (-{{ $filters.formatSize(disk.usage.used, 'G', 'G', '', 2, true) }},
                        | +{{ $filters.formatSize(disk.usage.total - disk.usage.used, 'G', 'G', '', 2, true) }})
            td
              div(v-if='server.data')
                .ui.cards
                  .card(v-for='gpu in server.data.gpu')
                    .content
                      .header [{{ gpu.index }}] {{ gpu.name }}
                      .little-break
                      .description
                        b Util.
                          | {{ gpu['utilization.gpu'] }}%
                          | ({{ gpu['temperature.gpu'] }}&deg;C, Fan: {{ gpu['fan.speed'] }}%)
                        UsageBar(:percent='gpu["utilization.gpu"]')
                        .little-break
                        b Mem.
                          | {{ Math.round((gpu['memory.used'] / gpu['memory.total']) * 100) }}%
                          | ({{ gpu['memory.used'] }}M / {{ gpu['memory.total'] }}M) 
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
    div
      a(style='cursor: pointer' v-on:click='toggleDarkMode') toggle dark mode (dev)
    div
      a(href="https://github.com/djosix/servstat") github repo
    link(rel="stylesheet" href="force_dark_mode.css" v-if='darkMode' style="display: none")

</template>


<script>
import UsageBar from './components/UsageBar.vue';
import CpuUsageBars from './components/CpuUsageBars.vue';


class LocalStorageManager {
  get(key, default_value) {
    try {
      let value = JSON.parse(window.localStorage[key]);
      // console.log(`GET ${key} = ${JSON.stringify(value)}`);
      return value;
    } catch (e) {
      // console.log(`GET ${key} default = ${JSON.stringify(default_value)}`);
      return default_value;
    }
  }
  set(key, value) {
    window.localStorage[key] = JSON.stringify(value);
    // console.log(`SET ${key} = ${JSON.stringify(value)}`);
  }
}

const DEFAULT_INTERVAL = 5000; // 5s
const DEFAULT_TITLE = 'Server Monitor'
const DEFAULT_ADDR = '[uknown address]'

export default {
  async created() {
    this.storage = new LocalStorageManager();
    this.darkMode = this.storage.get('dark', false);

    // Get config
    let json;
    try {
      json = await fetch("config.json").then(res => res.json());
    } catch (_) {
      alert('failed to fetch or decode config.json');
      return;
    }

    if (typeof json.title === "string") {
      // Update title from json
      this.title = document.title = json.title;
    }

    let pinnedServerLinks = this.storage.get('pinned', []);

    for (let [index, server] of json.servers.entries()) {
      let name, addr, link, interval;

      // Read server config
      if (typeof server === "string") {
        name = undefined; // obtained from API
        link = server;
        interval = json.interval || DEFAULT_INTERVAL;
      } else if (typeof server === "object") {
        name = server.name;
        link = server.link;
        interval = server.interval || json.interval || DEFAULT_INTERVAL;
      }
      if (link === undefined) {
        console.log(`Ignored invalid server entry: ${JSON.stringify(server)}`);
        continue;
      }

      try {
        // Extract server address from link
        const regex = /https?:\/\/(?<host>[a-zA-Z0-9\.]+)(?::(?<port>[0-9]+))?(?<path>\/.*)?/;
        addr = regex.exec(link).groups.host;
      } catch (_) {
        addr = DEFAULT_ADDR;
      }

      let isPinned = pinnedServerLinks.includes(link);

      this.servers.push({ name, addr, index, link, data: null, pinned: isPinned });
      this.update(index, link, interval);
    }
  },
  data() {
    return {
      title: DEFAULT_TITLE,
      servers: [],
      darkMode: false,
    };
  },
  methods: {
    update(index, link, interval) {
      fetch(link)
        .then(res => res.json())
        .then(data => {
          this.servers[index].data = data;
        })
        .finally(() => {
          setTimeout(() => {
            this.update(index, link, interval);
          }, interval);
        });
    },
    toggleServerPinning(server) {
      server.pinned = !server.pinned;
      this.storage.set('pinned', this.servers
        .filter(server => server.pinned)
        .map(server => server.link)
      );
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      this.storage.set('dark', this.darkMode);
    }
  },
  computed: {
    orderedServers() {
      let pinnedServers = [];
      let otherServers = [];

      this.servers.forEach(server => {
        if (server.pinned) {
          pinnedServers.push(server);
        } else {
          otherServers.push(server);
        }
      });
      
      return [...pinnedServers, ...otherServers];
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
